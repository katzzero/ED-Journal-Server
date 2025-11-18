#!/usr/bin/env python3
"""
Elite Dangerous Data Storage
Stores current game state with thread-safe updates
"""

import threading
from datetime import datetime


class EDData:
    """Stores current Elite Dangerous game state"""
    
    def __init__(self):
        self.data = {
            'commander': 'Unknown',
            'ship': 'Unknown',
            'system': 'Unknown',
            'station': None,
            'credits': 0,
            'location': {},
            'fuel': {},
            'cargo': [],
            'last_update': None,
            'status': 'Aguardando arquivos do Elite Dangerous...',
            'journal_file': None,
            'waiting_for_files': True,
            'planetary_coordinates': {
                'latitude': None,
                'longitude': None,
                'altitude': None,
                'heading': None,
                'body_name': None,
                'on_surface': False
            },
            'vehicle_state': {
                'docked': False,
                'landed': False,
                'in_srv': False,
                'in_fighter': False,
                'supercruise': False,
                'landing_gear_down': False,
                'shields_up': True,
                'in_flight': True
            },
            'system_bodies': [],
            'system_stations': [],
            'modules': []  # Garantido para o dashboard
        }
        self.lock = threading.Lock()
    
    def update(self, key, value):
        """Thread-safe update of a data key"""
        with self.lock:
            self.data[key] = value
            self.data['last_update'] = datetime.now().isoformat()
    
    def get_all(self):
        """Thread-safe retrieval of all data"""
        with self.lock:
            return self.data.copy()
