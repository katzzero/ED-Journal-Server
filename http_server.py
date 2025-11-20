#!/usr/bin/env python3
"""
Elite Dangerous HTTP Server
Serves game data via HTTP with REST API and dashboard
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from dashboard_html import get_dashboard_html


class EDRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the Elite Dangerous server"""
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
                        self.send_header('Cache-Control', 'no-cache, must-revalidate')  # [PERFORMANCE FIX #5] Ensure latest dashboard is fetched
            self.end_headers()
            self.wfile.write(get_dashboard_html().encode())
            
        elif self.path.split('?')[0] == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')  # [PERFORMANCE FIX #5] Prevent caching of API data
            self.end_headers()
            data = self.server.ed_data.get_all()
            self.wfile.write(json.dumps(data, indent=2).encode())
        
        else:
            self.send_response(404)
            self.end_headers()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread"""
    def __init__(self, *args, **kwargs):
        self.ed_data = kwargs.pop('ed_data', None)
        super().__init__(*args, **kwargs)
