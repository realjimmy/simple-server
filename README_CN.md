# 简单服务器

python实现的一个轻量级的服务器，提供HTTP和UDP服务器功能，支持多线程处理和长连接功能，主要用于搭建测试环境做功能测试。

## 功能特性

### HTTP服务器 (`http/http_server.py`)
- **多线程处理**: 每个请求由独立线程处理
- **长连接支持**: 支持HTTP Keep-Alive
- **JSON API**: RESTful API，接收和返回JSON数据
- **请求日志**: 详细记录客户端IP、线程ID和请求信息
- **错误处理**: 全面的错误处理，返回适当的HTTP状态码

### UDP服务器 (`udp/udp_server.py`)
- **JSON响应服务器**: 接收UDP消息并发送JSON格式确认
- **客户端信息**: 返回客户端IP和端口信息
- **结构化响应**: 与HTTP服务器一致的JSON格式

## 系统要求

- Python 3.6+

## 使用方法

```bash
# 启动HTTP服务器（默认端口8000）
python simple-server.py http

# 启动HTTP服务器（自定义端口）
python simple-server.py http 8080

# 启动HTTP服务器（禁用JSON验证）
python simple-server.py http 8080 --no-json

# 启动UDP服务器（默认端口9000）
python simple-server.py udp

# 启动UDP服务器（自定义端口）
python simple-server.py udp 9999

# 显示帮助
python simple-server.py -h
```

显示帮助信息：
```bash
python http/http_server.py -h
python udp/udp_server.py --help
```

**请求示例:**

GET请求：
```bash
curl http://localhost:8000/
```

POST请求（带JSON数据）：
```bash
curl -X POST http://localhost:8000/api/test \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World", "data": [1, 2, 3]}'
```

### UDP服务器

使用默认端口9000启动UDP服务器：
```bash
python udp/udp_server.py
```

使用指定端口启动UDP服务器：
```bash
python udp/udp_server.py 9999
```

**UDP客户端示例:**
```bash
# 发送默认JSON消息
python udp/udp_client.py 127.0.0.1 9000

# 发送自定义消息
python udp/udp_client.py 127.0.0.1 9000 "Hello World"

# 发送JSON消息
python udp/udp_client.py 127.0.0.1 9000 '{"test": "data"}'

# 显示帮助
python udp/udp_client.py -h
```

## 项目结构

```
simple-server/
├── simple-server.py           # 统一入口点
├── http/
│   └── http_server.py          # 多线程HTTP服务器
├── udp/
│   ├── udp_server.py          # 简单UDP回显服务器
│   └── udp_client.py           # UDP测试客户端
└── README_CN.md               # 本文档
```

## API响应格式

HTTP和UDP服务器都返回一致的JSON响应，包含以下字段：
- `status`: 请求状态（"success" 或 "error"）
- `message`: 响应消息
- `client_ip`: 客户端IP地址
- `client_port`: 客户端端口号
- `time`: 人类可读的时间戳
- `received_data`: 从客户端接收的数据（HTTP POST和UDP）
- `path`: 请求路径（仅HTTP GET）

### HTTP服务器响应

**成功响应:**
```json
{
  "status": "success",
  "message": "Welcome to the long connection server",
  "client_ip": "127.0.0.1",
  "client_port": 54321,
  "time": "Mon Jan  1 12:00:00 2022"
}
```

**错误响应:**
```json
{
  "status": "error",
  "message": "Request body is empty"
}
```

### UDP服务器响应

UDP服务器返回JSON格式响应：
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

## 停止服务器

两个服务器都可以通过按`Ctrl+C`停止。它们会优雅地关闭并显示关闭消息。