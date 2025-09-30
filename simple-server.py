#!/usr/bin/env python3
"""
Simple Server - Unified entry point for HTTP and UDP servers
"""

import sys
import os
import subprocess

def show_help():
    """Show help information"""
    print("Simple Server - Unified server launcher")
    print()
    print("Usage: python simple-server.py <server_type> [options]")
    print()
    print("Server Types:")
    print("  http              Start HTTP server")
    print("  udp               Start UDP server")
    print()
    print("Options:")
    print("  port              Port number (default: 8000 for HTTP, 9000 for UDP)")
    print("  --no-json         Disable JSON validation for HTTP POST requests")
    print("  -h, --help        Show this help message")
    print()
    print("Examples:")
    print("  python simple-server.py http                    # Start HTTP server on port 8000")
    print("  python simple-server.py http 8080               # Start HTTP server on port 8080")
    print("  python simple-server.py http 8080 --no-json     # Start HTTP server without JSON validation")
    print("  python simple-server.py udp                     # Start UDP server on port 9000")
    print("  python simple-server.py udp 9999                # Start UDP server on port 9999")
    print()
    print("Direct server access:")
    print("  python http/http_server.py [port] [--no-json]")
    print("  python udp/udp_server.py [port]")

def start_http_server(args):
    """Start HTTP server with given arguments"""
    script_path = os.path.join(os.path.dirname(__file__), 'http', 'http_server.py')
    cmd = [sys.executable, script_path] + args
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"HTTP server failed to start: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nHTTP server stopped by user")
        sys.exit(0)

def start_udp_server(args):
    """Start UDP server with given arguments"""
    script_path = os.path.join(os.path.dirname(__file__), 'udp', 'udp_server.py')
    cmd = [sys.executable, script_path] + args
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"UDP server failed to start: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nUDP server stopped by user")
        sys.exit(0)

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Error: Server type is required!")
        print("Use -h or --help for usage information")
        sys.exit(1)
    
    # Check for help flags
    if sys.argv[1] in ['-h', '--help']:
        show_help()
        sys.exit(0)
    
    server_type = sys.argv[1].lower()
    remaining_args = sys.argv[2:]
    
    if server_type == 'http':
        start_http_server(remaining_args)
    elif server_type == 'udp':
        start_udp_server(remaining_args)
    else:
        print(f"Error: Unknown server type '{server_type}'")
        print("Valid server types: http, udp")
        print("Use -h or --help for usage information")
        sys.exit(1)

if __name__ == '__main__':
    main()
