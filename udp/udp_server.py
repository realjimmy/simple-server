import socket
import sys
import json
import time

def run_server(port):
    # Create UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # Bind to specified port, allow access from all network interfaces
            s.bind(('0.0.0.0', port))
            print(f"UDP server started, listening on port {port}...")
            print("Press Ctrl+C to stop the server")
            
            while True:
                # Receive data
                data, addr = s.recvfrom(1024)
                message = data.decode('utf-8')
                client_ip = addr[0]
                client_port = addr[1]
                print(f"Received message from {addr}: {message}")
                
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
    # Default port
    port = 9000
    
    # Check if port parameter is provided
    if len(sys.argv) > 1:
        # Check for help flags
        if sys.argv[1] in ['-h', '--help']:
            print("UDP Server - Simple echo server")
            print()
            print("Usage: python udp_server.py [port]")
            print()
            print("Arguments:")
            print("  port              Port number (default: 9000)")
            print("  -h, --help        Show this help message")
            print()
            print("Examples:")
            print("  python udp_server.py           # Start on port 9000")
            print("  python udp_server.py 9999      # Start on port 9999")
            print()
            print("The server will echo back any message received from clients.")
            sys.exit(0)
        
        try:
            port = int(sys.argv[1])
            # Check if port is within valid range
            if not (1 <= port <= 65535):
                print("Error: Port number must be between 1-65535!")
                sys.exit(1)
        except ValueError:
            print("Error: Port number must be an integer!")
            print("Use -h or --help for usage information")
            sys.exit(1)
    
    run_server(port)
    
