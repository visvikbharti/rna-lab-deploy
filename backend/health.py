#!/usr/bin/env python3
"""
Extremely simple health check server with zero dependencies
"""
import socket
import json
import datetime
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "healthy",
            "time": datetime.datetime.now().isoformat(),
            "path": self.path
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        # Suppress logging
        pass

if __name__ == "__main__":
    port = int(os.environ.get("HEALTH_PORT", "8001"))
    httpd = HTTPServer(("", port), HealthHandler)
    print(f"Health check server running on port {port}")
    httpd.serve_forever()