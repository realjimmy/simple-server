import socket
import sys

def send_udp_request(message, host, port):
    # Create UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Set timeout to 5 seconds
        s.settimeout(5)
        
        try:
            # Send data to server
            s.sendto(message.encode('utf-8'), (host, port))
            print(f"Sent to {host}:{port}")
            
            # Wait for response
            data, addr = s.recvfrom(1024)
            response_text = data.decode('utf-8')
            
            # Try to format JSON response for better readability
            try:
                response_json = json.loads(response_text)
                print(f"Received response from {addr}:")
                print(json.dumps(response_json, ensure_ascii=False, indent=2))
            except json.JSONDecodeError:
                # If not JSON, display as plain text
                print(f"Received response from {addr}: {response_text}")
            
            return response_text
            
        except socket.timeout:
            print("Response timeout")
            return None
        except Exception as e:
            print(f"Error occurred: {e}")
            return None

if __name__ == "__main__":
    import json
    
    # Default JSON message
    default_message = json.dumps({
        "type": "test",
        "message": "Hello UDP Server",
        "timestamp": "2024-01-01T00:00:00Z",
        "data": {"key": "value", "number": 123}
    })
    
    # Check for help flags
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("UDP Client - Send messages to UDP server")
        print()
        print("Usage: python udp_client.py <host> <port> [message]")
        print()
        print("Arguments:")
        print("  host              Server IP address")
        print("  port              Server port number")
        print("  message           Message to send (optional, default: JSON)")
        print("  -h, --help        Show this help message")
        print()
        print("Examples:")
        print("  python udp_client.py 127.0.0.1 9000")
        print("  python udp_client.py 127.0.0.1 9000 'Hello World'")
        print("  python udp_client.py 127.0.0.1 9000 '{\"test\": \"data\"}'")
        sys.exit(0)
    
    # Check minimum required parameters
    if len(sys.argv) < 3:
        print("Error: Missing required parameters!")
        print("Use -h or --help for usage information")
        sys.exit(1)
    
    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
        # Check if port is within valid range
        if not (1 <= port <= 65535):
            print("Error: Port number must be between 1-65535!")
            sys.exit(1)
    except ValueError:
        print("Error: Port number must be an integer!")
        print("Use -h or --help for usage information")
        sys.exit(1)
    
    # Use provided message or default JSON message
    if len(sys.argv) > 3:
        message = ' '.join(sys.argv[3:])  # Support space-separated messages
    else:
        message = default_message
    
    send_udp_request(message, host, port)
    
