import socket
import sys
import json
import time

def run_server(port, delay_ms=0):
    # Create UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # Bind to specified port, allow access from all network interfaces
            s.bind(('0.0.0.0', port))
            print(f"UDP server started, listening on port {port}...")
            if delay_ms > 0:
                print(f"Response delay: {delay_ms}ms")
            print("Press Ctrl+C to stop the server")
            
            while True:
                # Receive data
                data, addr = s.recvfrom(1024)
                message = data.decode('utf-8')
                client_ip = addr[0]
                client_port = addr[1]
                print(f"Received message from {addr}: {message}")
                
                # Add delay if specified
                if delay_ms > 0:
                    time.sleep(delay_ms / 1000.0)
                
                # Create JSON response (consistent with HTTP server format)
                response_data = {
                    "status": "success",
                    "message": "UDP request processed successfully",
                    "received_data": message,
                    "client_ip": client_ip,
                    "client_port": client_port,
                    "time": time.ctime()
                }
                
                # Send JSON response
                response = json.dumps(response_data, ensure_ascii=False)
                s.sendto(response.encode('utf-8'), addr)
                
        except KeyboardInterrupt:
            print("\nServer is shutting down...")
        except Exception as e:
            print(f"Server error: {e}")

if __name__ == "__main__":
    # Default settings
    port = 9000
    delay_ms = 0
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Check for help flags
        if sys.argv[1] in ['-h', '--help']:
            print("UDP Server - JSON response server with delay support")
            print()
            print("Usage: python udp_server.py [port] [--delay milliseconds]")
            print()
            print("Arguments:")
            print("  port              Port number (default: 9000)")
            print("  --delay ms        Response delay in milliseconds (default: 0)")
            print("  -h, --help        Show this help message")
            print()
            print("Examples:")
            print("  python udp_server.py                    # Start on port 9000, no delay")
            print("  python udp_server.py 9999               # Start on port 9999, no delay")
            print("  python udp_server.py --delay 1000       # Start on port 9000, 1 second delay")
            print("  python udp_server.py 9999 --delay 500   # Start on port 9999, 500ms delay")
            print()
            print("The server will send JSON responses back to clients with optional delay.")
            sys.exit(0)
        
        # Parse arguments
        args = sys.argv[1:]
        
        # Check for delay parameter
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
                # Check if port is within valid range
                if not (1 <= port <= 65535):
                    print("Error: Port number must be between 1-65535!")
                    sys.exit(1)
            except ValueError:
                print("Error: Port number must be an integer!")
                print("Use -h or --help for usage information")
                sys.exit(1)
    
    run_server(port, delay_ms)
    
