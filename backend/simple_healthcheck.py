#!/usr/bin/env python3
"""
A standalone health check server that runs alongside Gunicorn.
This will handle the Railway health check independently of Django.
"""

import http.server
import socketserver
import threading
import time
import logging
import os
import json
import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("health-check-server")

PORT = int(os.environ.get("HEALTH_PORT", "8001"))
HEALTH_PATH = "/api/health/"

class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == HEALTH_PATH:
            logger.info(f"Health check request received on path {self.path}")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "healthy",
                "time": datetime.datetime.now().isoformat(),
                "service": "RNA Lab Navigator",
                "version": "1.0.0",
            }
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            logger.info(f"Request for non-health path: {self.path}")
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        # Override to use our logger instead of printing to stderr
        logger.info(f"{self.address_string()} - {format % args}")

def run_health_server():
    try:
        with socketserver.TCPServer(("", PORT), HealthCheckHandler) as httpd:
            logger.info(f"Health check server started on port {PORT}")
            httpd.serve_forever()
    except Exception as e:
        logger.error(f"Health check server error: {e}")

if __name__ == "__main__":
    logger.info("Starting health check server...")
    health_thread = threading.Thread(target=run_health_server)
    health_thread.daemon = True
    health_thread.start()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Health check server shutting down")