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
        super().__init__(*args, **kwargs)
    
    def _send_response(self, content, content_type='text/plain', status_code=200):
        """Send HTTP response"""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Connection', 'keep-alive')  # Support long connections
        self.send_header('Content-Length', str(len(content.encode('utf-8'))))
        self.send_header('Access-Control-Allow-Origin', '*')  # Support CORS
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
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
        
        # Fast processing, no delay
        
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
    
    def do_POST(self):
        """Handle POST requests"""
        client_ip = self.client_address[0]
        client_port = self.client_address[1]
        thread_id = threading.current_thread().ident
        request_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"[{request_time}] POST request - Thread ID: {thread_id}, Client: {client_ip}:{client_port}, Path: {self.path}")
        
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
                
        except Exception as e:
            print(f"[{request_time}] Error processing POST request: {e}")
            self._send_json_response({
                "status": "error",
                "message": f"Internal server error: {str(e)}"
            }, 500)
    
    def log_message(self, format, *args):
        """Override log method to avoid duplicate output"""
        # We already manually print logs in do_GET and do_POST
        pass

if __name__ == '__main__':
    import sys
    
    # Default settings
    port = 8000
    validate_json = True
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Check for help flags
        if sys.argv[1] in ['-h', '--help']:
            print("HTTP Server - Multi-threaded server with JSON support")
            print()
            print("Usage: python http_server.py [port] [--no-json]")
            print()
            print("Arguments:")
            print("  port              Port number (default: 8000)")
            print("  --no-json         Disable JSON validation for POST requests")
            print("  -h, --help        Show this help message")
            print()
            print("Examples:")
            print("  python http_server.py                    # Start on port 8000 with JSON validation")
            print("  python http_server.py 8080               # Start on port 8080 with JSON validation")
            print("  python http_server.py --no-json          # Start on port 8000 without JSON validation")
            print("  python http_server.py 8080 --no-json     # Start on port 8080 without JSON validation")
            sys.exit(0)
        
        # Check for --no-json flag in any position
        if '--no-json' in sys.argv:
            validate_json = False
            # Remove --no-json from arguments for port parsing
            args = [arg for arg in sys.argv[1:] if arg != '--no-json']
        else:
            args = sys.argv[1:]
        
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
    
    # Create handler with JSON validation setting
    def handler(*args, **kwargs):
        return LongConnectionHandler(*args, validate_json=validate_json, **kwargs)
    
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
    print('=' * 60)
    print(f'Usage: python http_server.py [port] [--no-json]')
    print(f'Current port: {port}')
    print(f'JSON validation: {"Enabled" if validate_json else "Disabled"}')
    print('Press Ctrl+C to stop the server')
    print('=' * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nServer is shutting down...')
        httpd.server_close()
        print('Server has been closed')

