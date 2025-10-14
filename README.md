# Simple Server

A lightweight Python server implementation that provides both HTTP and UDP server functionality with multi-threading support and long connection capabilities, mainly used for setting up test environments for functional testing.

[中文文档](README_CN.md) | [English Documentation](README.md)

## Features

### HTTP Server (`http/http_server.py`)
- **Multi-threaded Processing**: Each request is handled by a separate thread
- **Long Connection Support**: HTTP Keep-Alive support
- **JSON API**: RESTful API that accepts and returns JSON data
- **Request Logging**: Detailed logging of client IP, thread ID, and request information
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **Response Delay**: Configurable delay in milliseconds for testing timeouts

### UDP Server (`udp/udp_server.py`)
- **JSON Response Server**: Receives UDP messages and sends back JSON confirmation
- **Client Information**: Returns client IP and port information
- **Structured Response**: Consistent JSON format with HTTP server
- **Response Delay**: Configurable delay in milliseconds for testing timeouts

## Requirements

- Python 3.6+

## Usage

### Unified Entry Point

Start servers using the unified entry point:
```bash
# Start HTTP server (default port 8000)
python simple-server.py http

# Start HTTP server on custom port
python simple-server.py http 8080

# Start HTTP server without JSON validation
python simple-server.py http 8080 --no-json

# Start HTTP server with response delay
python simple-server.py http --delay 1000
python simple-server.py http 8080 --delay 500

# Start UDP server (default port 9000)
python simple-server.py udp

# Start UDP server on custom port
python simple-server.py udp 9999

# Start UDP server with response delay
python simple-server.py udp --delay 1000
python simple-server.py udp 9999 --delay 500

# Show help
python simple-server.py -h
```

### Direct Server Access

### HTTP Server

Start the HTTP server with default port 8000:
```bash
python http/http_server.py
```

Or specify a custom port:
```bash
python http/http_server.py 8080
```

Disable JSON validation for POST requests:
```bash
python http/http_server.py --no-json
python http/http_server.py 8080 --no-json
```

Show help information:
```bash
python http/http_server.py -h
python udp/udp_server.py --help
```

**Request Examples:**

GET request:
```bash
curl http://localhost:8000/
```

POST request with JSON data:
```bash
curl -X POST http://localhost:8000/api/test \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World", "data": [1, 2, 3]}'
```

### UDP Server

Start the UDP server with default port 9000:
```bash
python udp/udp_server.py
```

Or specify a custom port:
```bash
python udp/udp_server.py 9999
```

**UDP Client Example:**
```bash
# Send default JSON message
python udp/udp_client.py 127.0.0.1 9000

# Send custom message
python udp/udp_client.py 127.0.0.1 9000 "Hello World"

# Send JSON message
python udp/udp_client.py 127.0.0.1 9000 '{"test": "data"}'

# Show help
python udp/udp_client.py -h
```

## Project Structure

```
simple-server/
├── simple-server.py           # Unified entry point
├── http/
│   └── http_server.py          # Multi-threaded HTTP server
├── udp/
│   ├── udp_server.py          # Simple UDP echo server
│   └── udp_client.py          # UDP client for testing
└── README.md                  # This file
```

## API Response Format

Both HTTP and UDP servers return consistent JSON responses with the following fields:
- `status`: Request status ("success" or "error")
- `message`: Response message
- `client_ip`: Client IP address
- `client_port`: Client port number
- `time`: Human-readable timestamp
- `received_data`: Data received from client (HTTP POST and UDP)
- `path`: Request path (HTTP GET only)

### HTTP Server Responses

**Success Response:**
```json
{
  "status": "success",
  "message": "Welcome to the long connection server",
  "client_ip": "127.0.0.1",
  "client_port": 54321,
  "time": "Mon Jan  1 12:00:00 2022"
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Request body is empty"
}
```

### UDP Server Responses

The UDP server sends back a JSON response:
```json
{
  "status": "success",
  "message": "UDP request processed successfully",
  "received_data": "{\"test\": \"data\"}",
  "client_ip": "127.0.0.1",
  "client_port": 60322,
  "time": "Tue Sep 30 18:07:22 2025"
}
```

## Stopping the Servers

Both servers can be stopped by pressing `Ctrl+C`. They will gracefully shut down and display a shutdown message.
