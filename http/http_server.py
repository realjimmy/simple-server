from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import time
import json
import threading
from datetime import datetime

# Multi-threaded processing class
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Allow each request to be handled by a separate thread"""
    daemon_threads = True  # Automatically close child threads when main thread exits
    allow_reuse_address = True  # Allow address reuse

class LongConnectionHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.validate_json = kwargs.pop('validate_json', True)
        self.delay_ms = kwargs.pop('delay_ms', 0)
        super().__init__(*args, **kwargs)
    
    def _send_response(self, content, content_type='text/plain', status_code=200):
        """Send HTTP response"""
        try:
            self.send_response(status_code)
            self.send_header('Content-Type', content_type)
            self.send_header('Connection', 'keep-alive')  # Support long connections
            self.send_header('Content-Length', str(len(content.encode('utf-8'))))
            self.send_header('Access-Control-Allow-Origin', '*')  # Support CORS
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError) as e:
            # Client disconnected before response was sent
            print(f"Client disconnected: {e}")
        except Exception as e:
            print(f"Error sending response: {e}")
    
    def _send_json_response(self, data, status_code=200):
        """Send JSON response"""
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        self._send_response(json_str, 'application/json', status_code)
    
    def do_GET(self):
        """Handle GET requests"""
        client_ip = self.client_address[0]
        client_port = self.client_address[1]
        thread_id = threading.current_thread().ident
        request_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"[{request_time}] GET request - Thread ID: {thread_id}, Client: {client_ip}:{client_port}, Path: {self.path}")
        
        try:
            # Add delay if specified
            if self.delay_ms > 0:
                time.sleep(self.delay_ms / 1000.0)
        
            # Return different content based on path
            if self.path == '/':
                response_data = {
                    "status": "success",
                    "message": "Welcome to the long connection server",
                    "client_ip": client_ip,
                    "client_port": client_port,
                    "time": time.ctime()
                }
                self._send_json_response(response_data)
            else:
                response_data = {
                    "status": "success",
                    "message": f"GET request processed successfully",
                    "path": self.path,
                    "client_ip": client_ip,
                    "client_port": client_port,
                    "time": time.ctime()
                }
                self._send_json_response(response_data)
        except (BrokenPipeError, ConnectionResetError):
            print(f"[{request_time}] Client {client_ip}:{client_port} disconnected during request processing")
        except Exception as e:
            print(f"[{request_time}] Error processing GET request: {e}")
    
    def do_POST(self):
        """Handle POST requests"""
        client_ip = self.client_address[0]
        client_port = self.client_address[1]
        thread_id = threading.current_thread().ident
        request_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"[{request_time}] POST request - Thread ID: {thread_id}, Client: {client_ip}:{client_port}, Path: {self.path}")
        
        # Add delay if specified
        if self.delay_ms > 0:
            time.sleep(self.delay_ms / 1000.0)
        
        try:
            # Get request content length
            content_length = int(self.headers.get('Content-Length', 0))
            
            if content_length == 0:
                self._send_json_response({
                    "status": "error",
                    "message": "Request body is empty"
                }, 400)
                return
            
            # Read request body
            post_data = self.rfile.read(content_length)
            
            if self.validate_json:
                # Parse JSON data
                try:
                    json_data = json.loads(post_data.decode('utf-8'))
                    print(f"[{request_time}] Received JSON data:")
                    print(f"{json.dumps(json_data, ensure_ascii=False, indent=2)}")
                    # Return success response
                    response_data = {
                        "status": "success",
                        "message": "POST request processed successfully",
                        "received_data": json_data,
                        "client_ip": client_ip,
                        "client_port": client_port,
                        "time": time.ctime()
                    }
                    self._send_json_response(response_data)
                    
                except json.JSONDecodeError as e:
                    raw_content = post_data.decode('utf-8', errors='ignore')
                    print(f"[{request_time}] Non-JSON data: {raw_content}")
                    self._send_json_response({
                        "status": "error",
                        "message": f"JSON parsing failed: {str(e)}"
                    }, 400)
            else:
                # No JSON validation, just return raw data
                raw_content = post_data.decode('utf-8', errors='ignore')
                print(f"[{request_time}] Received raw data: {raw_content}")
                response_data = {
                    "status": "success",
                    "message": "POST request processed successfully",
                    "received_data": raw_content,
                    "client_ip": client_ip,
                    "client_port": client_port,
                    "time": time.ctime()
                }
                self._send_json_response(response_data)
                
        except (BrokenPipeError, ConnectionResetError):
            print(f"[{request_time}] Client {client_ip}:{client_port} disconnected during request processing")
        except Exception as e:
            print(f"[{request_time}] Error processing POST request: {e}")
            try:
                self._send_json_response({
                    "status": "error",
                    "message": f"Internal server error: {str(e)}"
                }, 500)
            except (BrokenPipeError, ConnectionResetError):
                print(f"[{request_time}] Client {client_ip}:{client_port} disconnected before error response could be sent")
    
    def log_message(self, format, *args):
        """Override log method to avoid duplicate output"""
        # We already manually print logs in do_GET and do_POST
        pass

if __name__ == '__main__':
    import sys
    
    # Default settings
    port = 8000
    validate_json = True
    delay_ms = 0
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Check for help flags
        if sys.argv[1] in ['-h', '--help']:
            print("HTTP Server - Multi-threaded server with JSON support")
            print()
            print("Usage: python http_server.py [port] [--no-json] [--delay milliseconds]")
            print()
            print("Arguments:")
            print("  port              Port number (default: 8000)")
            print("  --no-json         Disable JSON validation for POST requests")
            print("  --delay ms        Response delay in milliseconds (default: 0)")
            print("  -h, --help        Show this help message")
            print()
            print("Examples:")
            print("  python http_server.py                    # Start on port 8000 with JSON validation")
            print("  python http_server.py 8080               # Start on port 8080 with JSON validation")
            print("  python http_server.py --no-json          # Start on port 8000 without JSON validation")
            print("  python http_server.py 8080 --no-json     # Start on port 8080 without JSON validation")
            print("  python http_server.py --delay 1000       # Start on port 8000 with 1 second delay")
            print("  python http_server.py 8080 --delay 500   # Start on port 8080 with 500ms delay")
            sys.exit(0)
        
        # Parse arguments
        args = sys.argv[1:]
        
        # Check for --no-json flag
        if '--no-json' in args:
            validate_json = False
            args = [arg for arg in args if arg != '--no-json']
        
        # Check for --delay parameter
        if '--delay' in args:
            delay_index = args.index('--delay')
            if delay_index + 1 < len(args):
                try:
                    delay_ms = int(args[delay_index + 1])
                    if delay_ms < 0:
                        print("Error: Delay must be non-negative!")
                        sys.exit(1)
                    # Remove delay arguments for port parsing
                    args = [arg for i, arg in enumerate(args) if i not in [delay_index, delay_index + 1]]
                except ValueError:
                    print("Error: Delay must be an integer!")
                    print("Use -h or --help for usage information")
                    sys.exit(1)
            else:
                print("Error: --delay requires a value!")
                print("Use -h or --help for usage information")
                sys.exit(1)
        
        # Parse port if provided
        if args:
            try:
                port = int(args[0])
                if port < 1 or port > 65535:
                    print("Error: Port number must be in range 1-65535")
                    sys.exit(1)
            except ValueError:
                print("Error: Port number must be a number")
                print("Use -h or --help for usage information")
                sys.exit(1)
    
    server_address = ('', port)
    
    # Create handler with JSON validation and delay settings
    def handler(*args, **kwargs):
        return LongConnectionHandler(*args, validate_json=validate_json, delay_ms=delay_ms, **kwargs)
    
    httpd = ThreadedHTTPServer(server_address, handler)
    
    print('=' * 60)
    print('Multi-threaded long connection server started successfully!')
    print(f'Listening address: http://localhost:{port}')
    print('Supported features:')
    print('  - GET requests: Return JSON formatted responses')
    if validate_json:
        print('  - POST requests: Receive and validate JSON data')
    else:
        print('  - POST requests: Receive raw data (no JSON validation)')
    print('  - Long connections: Support HTTP Keep-Alive')
    print('  - Parallel processing: Each request handled in independent thread')
    if delay_ms > 0:
        print(f'  - Response delay: {delay_ms}ms')
    print('=' * 60)
    print(f'Usage: python http_server.py [port] [--no-json] [--delay ms]')
    print(f'Current port: {port}')
    print(f'JSON validation: {"Enabled" if validate_json else "Disabled"}')
    print(f'Response delay: {delay_ms}ms')
    print('Press Ctrl+C to stop the server')
    print('=' * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nServer is shutting down...')
        httpd.server_close()
        print('Server has been closed')

