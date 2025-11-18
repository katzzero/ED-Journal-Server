#!/usr/bin/env python3
"""
Elite Dangerous Real-time Information Server
Monitors the game journal and serves data via HTTP with GUI
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import socket
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser

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
            'system_stations': []
        }
        self.lock = threading.Lock()
    
    def update(self, key, value):
        with self.lock:
            self.data[key] = value
            self.data['last_update'] = datetime.now().isoformat()
    
    def get_all(self):
        with self.lock:
            return self.data.copy()

class JournalMonitor:
    """Monitors Elite Dangerous journal files for updates"""
    def __init__(self, ed_data, journal_dir=None, allow_start_without_files=True):
        self.ed_data = ed_data
        if journal_dir:
            self.journal_dir = Path(journal_dir) if not isinstance(journal_dir, Path) else journal_dir
        else:
            self.journal_dir = self.find_journal_directory()
        
        self.running = True
        self.last_file = None
        self.last_position = 0
        self.status_callback = None
        self.allow_start_without_files = allow_start_without_files
        
        if not self.journal_dir:
            self.ed_data.update('status', 'Aguardando arquivos do Elite Dangerous...')
            self.ed_data.update('waiting_for_files', True)
        else:
            self.ed_data.update('waiting_for_files', False)
    
    def find_journal_directory(self):
        """Find the Elite Dangerous journal directory"""
        possible_paths = [
            # Windows
            Path.home() / 'Saved Games' / 'Frontier Developments' / 'Elite Dangerous',
            Path(os.getenv('USERPROFILE', '')) / 'Saved Games' / 'Frontier Developments' / 'Elite Dangerous',
            # Linux (Steam)
            Path.home() / '.local' / 'share' / 'Steam' / 'steamapps' / 'compatdata' / '359320' / 'pfx' / 'drive_c' / 'users' / 'steamuser' / 'Saved Games' / 'Frontier Developments' / 'Elite Dangerous',
            # Linux (Proton)
            Path.home() / '.steam' / 'steam' / 'steamapps' / 'compatdata' / '359320' / 'pfx' / 'drive_c' / 'users' / 'steamuser' / 'Saved Games' / 'Frontier Developments' / 'Elite Dangerous',
            # macOS
            Path.home() / 'Library' / 'Application Support' / 'Frontier Developments' / 'Elite Dangerous',
        ]
        
        for path in possible_paths:
            if path.exists() and list(path.glob('Journal.*.log')):
                return path
        
        return None
    
    def set_journal_directory(self, path):
        """Manually set the journal directory"""
        if path:
            self.journal_dir = Path(path) if not isinstance(path, Path) else path
        else:
            self.journal_dir = None
        
        self.last_file = None
        self.last_position = 0
        
        if self.journal_dir and self.journal_dir.exists():
            self.ed_data.update('waiting_for_files', False)
            self.ed_data.update('status', f'Diretório configurado: {self.journal_dir}')
        else:
            self.ed_data.update('waiting_for_files', True)
            self.ed_data.update('status', 'Aguardando arquivos do Elite Dangerous...')
    
    def get_latest_journal(self):
        """Get the most recent journal file"""
        if not self.journal_dir or not self.journal_dir.exists():
            return None
        
        journals = list(self.journal_dir.glob('Journal.*.log'))
        if not journals:
            return None
        
        return max(journals, key=lambda p: p.stat().st_mtime)
    
    def process_event(self, event):
        """Process a journal event and update game state"""
        event_type = event.get('event')
        
        if event_type == 'LoadGame':
            self.ed_data.update('commander', event.get('Commander', 'Unknown'))
            self.ed_data.update('ship', event.get('Ship', 'Unknown'))
            self.ed_data.update('credits', event.get('Credits', 0))
        
        elif event_type == 'Location' or event_type == 'FSDJump':
            self.ed_data.update('system', event.get('StarSystem', 'Unknown'))
            location = {
                'system': event.get('StarSystem'),
                'coords': event.get('StarPos', []),
                'body': event.get('Body')
            }
            self.ed_data.update('location', location)
            
            # Limpa listas ao mudar de sistema
            self.ed_data.update('system_bodies', [])
            self.ed_data.update('system_stations', [])
            
            # Captura estações do sistema no evento FSDJump
            if 'Stations' in event:
                stations = []
                for station in event.get('Stations', []):
                    stations.append({
                        'name': station.get('Name'),
                        'type': station.get('StationType'),
                        'services': station.get('StationServices', []),
                        'distance': station.get('DistFromStarLS')
                    })
                self.ed_data.update('system_stations', stations)
            
            # Captura coordenadas planetárias se disponíveis
            if 'Latitude' in event and 'Longitude' in event:
                coords = {
                    'latitude': event.get('Latitude'),
                    'longitude': event.get('Longitude'),
                    'altitude': event.get('Altitude'),
                    'heading': event.get('Heading'),
                    'body_name': event.get('Body'),
                    'on_surface': True
                }
                self.ed_data.update('planetary_coordinates', coords)
        
        # Evento Scan - captura informações de corpos celestes
        elif event_type == 'Scan':
            body_info = {
                'name': event.get('BodyName'),
                'type': event.get('PlanetClass') or event.get('StarType') or 'Desconhecido',
                'is_landable': event.get('Landable', False),
                'distance': event.get('DistanceFromArrivalLS'),
                'terraform_state': event.get('TerraformState'),
                'atmosphere': event.get('Atmosphere'),
                'volcanism': event.get('Volcanism'),
                'mass': event.get('MassEM'),
                'radius': event.get('Radius'),
                'gravity': event.get('SurfaceGravity'),
                'surface_temp': event.get('SurfaceTemperature'),
                'rings': event.get('Rings', [])
            }
            
            # Cria nova lista ao invés de modificar cópia
            current_bodies = self.ed_data.get_all().get('system_bodies', [])
            body_names = [b['name'] for b in current_bodies if b.get('name')]
            
            if body_info['name'] and body_info['name'] not in body_names:
                updated_bodies = current_bodies + [body_info]
                self.ed_data.update('system_bodies', updated_bodies)
        
        elif event_type == 'FSSDiscoveryScan':
            bodies_count = event.get('BodyCount', 0)
            print(f"Sistema tem {bodies_count} corpos celestes")
        
        elif event_type == 'Docked':
            self.ed_data.update('station', event.get('StationName'))
            
            self.ed_data.update('vehicle_state', {
                'docked': True,
                'landed': False,
                'in_srv': False,
                'in_fighter': False,
                'supercruise': False,
                'landing_gear_down': False,
                'shields_up': True,
                'in_flight': False
            })
            
            self.ed_data.update('planetary_coordinates', {
                'latitude': None,
                'longitude': None,
                'altitude': None,
                'heading': None,
                'body_name': None,
                'on_surface': False
            })
        
        elif event_type == 'Undocked':
            self.ed_data.update('station', None)
            
            self.ed_data.update('vehicle_state', {
                'docked': False,
                'landed': False,
                'in_srv': False,
                'in_fighter': False,
                'supercruise': False,
                'landing_gear_down': False,
                'shields_up': True,
                'in_flight': True
            })
        
        elif event_type == 'Touchdown':
            coords = {
                'latitude': event.get('Latitude'),
                'longitude': event.get('Longitude'),
                'body_name': event.get('Body'),
                'on_surface': True,
                'nearest_destination': event.get('NearestDestination')
            }
            self.ed_data.update('planetary_coordinates', coords)
            
            current_state = self.ed_data.get_all().get('vehicle_state', {})
            new_state = current_state.copy()
            new_state.update({
                'landed': True,
                'in_flight': False
            })
            self.ed_data.update('vehicle_state', new_state)
        
        elif event_type == 'Liftoff':
            coords = {
                'latitude': event.get('Latitude'),
                'longitude': event.get('Longitude'),
                'body_name': event.get('Body'),
                'on_surface': False
            }
            self.ed_data.update('planetary_coordinates', coords)
            
            current_state = self.ed_data.get_all().get('vehicle_state', {})
            new_state = current_state.copy()
            new_state.update({
                'landed': False,
                'in_flight': True
            })
            self.ed_data.update('vehicle_state', new_state)
        
        elif event_type == 'ApproachSettlement':
            coords = {
                'latitude': event.get('Latitude'),
                'longitude': event.get('Longitude'),
                'body_name': event.get('BodyName'),
                'settlement': event.get('Name'),
                'on_surface': True
            }
            self.ed_data.update('planetary_coordinates', coords)
        
        elif event_type == 'LaunchSRV':
            current_state = self.ed_data.get_all().get('vehicle_state', {})
            new_state = current_state.copy()
            new_state.update({
                'in_srv': True,
                'landed': False
            })
            self.ed_data.update('vehicle_state', new_state)
        
        elif event_type == 'DockSRV':
            current_state = self.ed_data.get_all().get('vehicle_state', {})
            new_state = current_state.copy()
            new_state['in_srv'] = False
            self.ed_data.update('vehicle_state', new_state)
        
        elif event_type == 'LaunchFighter':
            current_state = self.ed_data.get_all().get('vehicle_state', {})
            new_state = current_state.copy()
            new_state['in_fighter'] = True
            self.ed_data.update('vehicle_state', new_state)
        
        elif event_type == 'DockFighter':
            current_state = self.ed_data.get_all().get('vehicle_state', {})
            new_state = current_state.copy()
            new_state['in_fighter'] = False
            self.ed_data.update('vehicle_state', new_state)
        
        elif event_type == 'SupercruiseEntry':
            current_state = self.ed_data.get_all().get('vehicle_state', {})
            new_state = current_state.copy()
            new_state.update({
                'supercruise': True,
                'landed': False,
                'in_flight': True
            })
            self.ed_data.update('vehicle_state', new_state)
        
        elif event_type == 'SupercruiseExit':
            current_state = self.ed_data.get_all().get('vehicle_state', {})
            new_state = current_state.copy()
            new_state['supercruise'] = False
            self.ed_data.update('vehicle_state', new_state)
        
        elif event_type == 'FuelScoop':
            fuel = event.get('Total', 0)
            self.ed_data.update('fuel', {'current': fuel})
        
        elif event_type == 'Cargo':
            inventory = event.get('Inventory', [])
            self.ed_data.update('cargo', inventory)
    
    def monitor(self):
        """Main monitoring loop"""
        print("Starting journal monitor...")
        retry_count = 0
        
        while self.running:
            try:
                if not self.journal_dir:
                    self.journal_dir = self.find_journal_directory()
                    if self.journal_dir:
                        print(f"Journal directory found: {self.journal_dir}")
                        self.ed_data.update('waiting_for_files', False)
                        self.ed_data.update('status', f'Monitorando: {self.journal_dir}')
                    else:
                        if retry_count % 10 == 0:
                            print("Aguardando arquivos do Elite Dangerous...")
                        self.ed_data.update('status', 'Aguardando arquivos do Elite Dangerous...')
                        self.ed_data.update('waiting_for_files', True)
                        retry_count += 1
                        time.sleep(5)
                        continue
                
                current_journal = self.get_latest_journal()
                
                if not current_journal:
                    self.ed_data.update('status', 'Diretório encontrado, aguardando journal files...')
                    self.ed_data.update('journal_file', None)
                    self.ed_data.update('waiting_for_files', True)
                    time.sleep(5)
                    continue
                
                if self.ed_data.get_all().get('waiting_for_files', True):
                    self.ed_data.update('waiting_for_files', False)
                    print(f"Journal file found: {current_journal.name}")
                
                if current_journal != self.last_file:
                    self.last_file = current_journal
                    self.last_position = 0
                    self.ed_data.update('status', f'Monitorando: {current_journal.name}')
                    self.ed_data.update('journal_file', current_journal.name)
                    print(f"Reading journal: {current_journal.name}")
                
                with open(current_journal, 'r', encoding='utf-8') as f:
                    f.seek(self.last_position)
                    lines = f.readlines()
                    self.last_position = f.tell()
                    
                    for line in lines:
                        try:
                            event = json.loads(line)
                            self.process_event(event)
                        except json.JSONDecodeError:
                            pass
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Error monitoring journal: {e}")
                self.ed_data.update('status', f'Erro: {str(e)}')
                time.sleep(5)

class EDRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the Elite Dangerous server"""
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_html_page().encode())
        
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            data = self.server.ed_data.get_all()
            self.wfile.write(json.dumps(data, indent=2).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_html_page(self):
        """Generate the HTML dashboard"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Elite Dangerous Dashboard</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #00ff00;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            color: #ff6600;
            text-shadow: 0 0 10px #ff6600;
        }
        h2 {
            color: #00ddff;
            margin-top: 0;
        }
        .status-box {
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid #ff6600;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 0 20px rgba(255, 102, 0, 0.3);
        }
        .waiting-status {
            border-color: #ffaa00;
            animation: pulse 2s infinite;
        }
        .coordinates-box {
            background: rgba(0, 100, 150, 0.3);
            border: 2px solid #00aaff;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 0 20px rgba(0, 170, 255, 0.3);
        }
        .vehicle-status-box {
            background: rgba(100, 0, 100, 0.3);
            border: 2px solid #ff00ff;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);
        }
        .bodies-box, .stations-box {
            background: rgba(50, 50, 0, 0.3);
            border: 2px solid #ffdd00;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 0 20px rgba(255, 221, 0, 0.2);
        }
        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 20px rgba(255, 170, 0, 0.3); }
            50% { box-shadow: 0 0 30px rgba(255, 170, 0, 0.6); }
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .info-item {
            background: rgba(0, 50, 0, 0.3);
            padding: 15px;
            border-radius: 5px;
            border-left: 3px solid #00ff00;
        }
        .coord-item {
            background: rgba(0, 50, 100, 0.3);
            padding: 15px;
            border-radius: 5px;
            border-left: 3px solid #00aaff;
        }
        .vehicle-item {
            background: rgba(50, 0, 50, 0.3);
            padding: 15px;
            border-radius: 5px;
            border-left: 3px solid #ff00ff;
        }
        .info-label {
            color: #888;
            font-size: 0.9em;
            text-transform: uppercase;
        }
        .info-value {
            color: #00ff00;
            font-size: 1.2em;
            font-weight: bold;
            margin-top: 5px;
        }
        .coord-value {
            color: #00ddff;
            font-size: 1.2em;
            font-weight: bold;
            margin-top: 5px;
            font-family: 'Courier New', monospace;
        }
        .vehicle-value {
            color: #ff00ff;
            font-size: 1.2em;
            font-weight: bold;
            margin-top: 5px;
        }
        .warning {
            color: #ffaa00;
            text-align: center;
            font-size: 1.2em;
            padding: 20px;
            background: rgba(255, 170, 0, 0.1);
            border-radius: 5px;
            margin: 20px 0;
        }
        .last-update {
            text-align: center;
            color: #666;
            margin-top: 20px;
            font-size: 0.9em;
        }
        .planet-icon, .station-icon, .vehicle-icon {
            font-size: 1.5em;
            margin-right: 10px;
        }
        .body-list, .station-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        .body-card, .station-card {
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #ffdd00;
            border-radius: 5px;
            padding: 12px;
        }
        .body-name, .station-name {
            color: #ffdd00;
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 8px;
        }
        .body-detail, .station-detail {
            color: #aaa;
            font-size: 0.9em;
            margin: 3px 0;
        }
        .landable {
            color: #00ff00;
            font-weight: bold;
        }
        .status-active {
            color: #00ff00;
            font-weight: bold;
        }
        .status-inactive {
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Elite Dangerous Dashboard</h1>
        <div id="content"></div>
    </div>
    
    <script>
        function formatCoordinate(value, type) {
            if (value === null || value === undefined) return 'N/A';
            const direction = type === 'lat' 
                ? (value >= 0 ? 'N' : 'S')
                : (value >= 0 ? 'E' : 'W');
            return `${Math.abs(value).toFixed(4)}° ${direction}`;
        }
        
        function getVehicleStatus(vehicleState) {
            if (vehicleState.in_srv) return '🚙 No SRV';
            if (vehicleState.in_fighter) return '✈️ No Fighter';
            if (vehicleState.docked) return '🔒 Acoplado na Estação';
            if (vehicleState.landed) return '🛬 Pousado';
            if (vehicleState.supercruise) return '⚡ Em Supercruise';
            if (vehicleState.in_flight) return '🚀 Em Voo';
            return '❓ Desconhecido';
        }
        
        function updateDashboard() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    let html = '';
                    
                    const statusClass = data.waiting_for_files ? 'status-box waiting-status' : 'status-box';
                    html += `<div class="${statusClass}">`;
                    html += `<div class="info-label">Status do Sistema</div>`;
                    html += `<div class="info-value">${data.status}</div>`;
                    html += `</div>`;
                    
                    if (data.waiting_for_files) {
                        html += `<div class="warning">`;
                        html += `⏳ Aguardando arquivos do Elite Dangerous...<br>`;
                        html += `<small>O servidor está ativo. Inicie o jogo para começar o monitoramento.</small>`;
                        html += `</div>`;
                    } else {
                        const vehicleState = data.vehicle_state || {};
                        html += `<div class="vehicle-status-box">`;
                        html += `<h2><span class="vehicle-icon">🎮</span>Estado do Veículo</h2>`;
                        html += `<div class="info-grid">`;
                        
                        html += `<div class="vehicle-item">`;
                        html += `<div class="info-label">Situação Atual</div>`;
                        html += `<div class="vehicle-value">${getVehicleStatus(vehicleState)}</div>`;
                        html += `</div>`;
                        
                        html += `<div class="vehicle-item">`;
                        html += `<div class="info-label">Acoplado</div>`;
                        html += `<div class="vehicle-value ${vehicleState.docked ? 'status-active' : 'status-inactive'}">`;
                        html += vehicleState.docked ? '✅ Sim' : '❌ Não';
                        html += `</div></div>`;
                        
                        html += `<div class="vehicle-item">`;
                        html += `<div class="info-label">Pousado</div>`;
                        html += `<div class="vehicle-value ${vehicleState.landed ? 'status-active' : 'status-inactive'}">`;
                        html += vehicleState.landed ? '✅ Sim' : '❌ Não';
                        html += `</div></div>`;
                        
                        html += `<div class="vehicle-item">`;
                        html += `<div class="info-label">Em Voo</div>`;
                        html += `<div class="vehicle-value ${vehicleState.in_flight ? 'status-active' : 'status-inactive'}">`;
                        html += vehicleState.in_flight ? '✅ Sim' : '❌ Não';
                        html += `</div></div>`;
                        
                        html += `</div></div>`;
                        
                        const coords = data.planetary_coordinates || {};
                        if (coords.on_surface && coords.latitude !== null) {
                            html += `<div class="coordinates-box">`;
                            html += `<h2><span class="planet-icon">🌍</span>Coordenadas Planetárias</h2>`;
                            html += `<div class="info-grid">`;
                            
                            if (coords.body_name) {
                                html += `<div class="coord-item">`;
                                html += `<div class="info-label">Corpo Celeste</div>`;
                                html += `<div class="coord-value">${coords.body_name}</div>`;
                                html += `</div>`;
                            }
                            
                            html += `<div class="coord-item">`;
                            html += `<div class="info-label">Latitude</div>`;
                            html += `<div class="coord-value">${formatCoordinate(coords.latitude, 'lat')}</div>`;
                            html += `</div>`;
                            
                            html += `<div class="coord-item">`;
                            html += `<div class="info-label">Longitude</div>`;
                            html += `<div class="coord-value">${formatCoordinate(coords.longitude, 'lon')}</div>`;
                            html += `</div>`;
                            
                            if (coords.altitude !== null && coords.altitude !== undefined) {
                                html += `<div class="coord-item">`;
                                html += `<div class="info-label">Altitude</div>`;
                                html += `<div class="coord-value">${coords.altitude.toFixed(0)} m</div>`;
                                html += `</div>`;
                            }
                            
                            html += `</div></div>`;
                        }
                        
                        html += `<div class="info-grid">`;
                        html += `<div class="info-item">`;
                        html += `<div class="info-label">Comandante</div>`;
                        html += `<div class="info-value">${data.commander}</div>`;
                        html += `</div>`;
                        
                        html += `<div class="info-item">`;
                        html += `<div class="info-label">Nave</div>`;
                        html += `<div class="info-value">${data.ship}</div>`;
                        html += `</div>`;
                        
                        html += `<div class="info-item">`;
                        html += `<div class="info-label">Sistema</div>`;
                        html += `<div class="info-value">${data.system}</div>`;
                        html += `</div>`;
                        
                        html += `<div class="info-item">`;
                        html += `<div class="info-label">Estação</div>`;
                        html += `<div class="info-value">${data.station || 'No espaço'}</div>`;
                        html += `</div>`;
                        
                        html += `<div class="info-item">`;
                        html += `<div class="info-label">Créditos</div>`;
                        html += `<div class="info-value">${data.credits.toLocaleString()} CR</div>`;
                        html += `</div>`;
                        html += `</div>`;
                        
                        const stations = data.system_stations || [];
                        if (stations.length > 0) {
                            html += `<div class="stations-box">`;
                            html += `<h2><span class="station-icon">🏢</span>Estações do Sistema (${stations.length})</h2>`;
                            html += `<div class="station-list">`;
                            
                            stations.forEach(station => {
                                html += `<div class="station-card">`;
                                html += `<div class="station-name">${station.name}</div>`;
                                html += `<div class="station-detail">Tipo: ${station.type || 'Desconhecido'}</div>`;
                                if (station.distance) {
                                    html += `<div class="station-detail">Distância: ${station.distance.toLocaleString()} LS</div>`;
                                }
                                html += `</div>`;
                            });
                            
                            html += `</div></div>`;
                        }
                        
                        const bodies = data.system_bodies || [];
                        if (bodies.length > 0) {
                            html += `<div class="bodies-box">`;
                            html += `<h2><span class="planet-icon">🪐</span>Corpos Celestes Escaneados (${bodies.length})</h2>`;
                            html += `<div class="body-list">`;
                            
                            bodies.forEach(body => {
                                html += `<div class="body-card">`;
                                html += `<div class="body-name">${body.name}</div>`;
                                html += `<div class="body-detail">Tipo: ${body.type || 'Desconhecido'}</div>`;
                                
                                if (body.is_landable) {
                                    html += `<div class="body-detail landable">✅ Aterrissável</div>`;
                                }
                                
                                if (body.distance) {
                                    html += `<div class="body-detail">Distância: ${body.distance.toLocaleString()} LS</div>`;
                                }
                                
                                if (body.atmosphere) {
                                    html += `<div class="body-detail">Atmosfera: ${body.atmosphere}</div>`;
                                }
                                
                                if (body.terraform_state) {
                                    html += `<div class="body-detail">🌱 ${body.terraform_state}</div>`;
                                }
                                
                                html += `</div>`;
                            });
                            
                            html += `</div></div>`;
                        }
                    }
                    
                    if (data.last_update) {
                        const updateTime = new Date(data.last_update).toLocaleString('pt-BR');
                        html += `<div class="last-update">Última atualização: ${updateTime}</div>`;
                    }
                    
                    document.getElementById('content').innerHTML = html;
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('content').innerHTML = 
                        '<div class="warning">Erro ao conectar com o servidor</div>';
                });
        }
        
        updateDashboard();
        setInterval(updateDashboard, 2000);
    </script>
</body>
</html>
        """

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread"""
    def __init__(self, *args, **kwargs):
        self.ed_data = kwargs.pop('ed_data', None)
        super().__init__(*args, **kwargs)

class EDGUI:
    """GUI for the Elite Dangerous server"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Elite Dangerous Server")
        self.root.geometry("600x500")
        
        self.ed_data = EDData()
        self.monitor = None
        self.server = None
        self.server_thread = None
        self.monitor_thread = None
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI components"""
        header = tk.Label(self.root, text="Elite Dangerous Local Server", 
                         font=("Arial", 16, "bold"))
        header.pack(pady=10)
        
        status_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label = tk.Label(status_frame, text="Servidor parado", 
                                     font=("Arial", 10))
        self.status_label.pack()
        
        journal_frame = ttk.LabelFrame(self.root, text="Diretório de Journals", padding=10)
        journal_frame.pack(fill="x", padx=10, pady=5)
        
        dir_input_frame = tk.Frame(journal_frame)
        dir_input_frame.pack(fill="x")
        
        self.dir_entry = tk.Entry(dir_input_frame)
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ttk.Button(dir_input_frame, text="Procurar", 
                  command=self.browse_directory).pack(side="left")
        
        ttk.Button(journal_frame, text="Auto-detectar", 
                  command=self.auto_detect).pack(pady=5)
        
        controls_frame = ttk.LabelFrame(self.root, text="Controles do Servidor", padding=10)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        port_frame = tk.Frame(controls_frame)
        port_frame.pack(pady=5)
        
        tk.Label(port_frame, text="Porta:").pack(side="left", padx=5)
        self.port_entry = tk.Entry(port_frame, width=10)
        self.port_entry.insert(0, "8080")
        self.port_entry.pack(side="left")
        
        button_frame = tk.Frame(controls_frame)
        button_frame.pack(pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Iniciar Servidor", 
                                       command=self.start_server)
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Parar Servidor", 
                                      command=self.stop_server, state="disabled")
        self.stop_button.pack(side="left", padx=5)
        
        info_frame = ttk.LabelFrame(self.root, text="Informações do Servidor", padding=10)
        info_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.info_text = tk.Text(info_frame, height=10, wrap="word")
        self.info_text.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.info_text)
        scrollbar.pack(side="right", fill="y")
        self.info_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.info_text.yview)
        
        self.browser_button = ttk.Button(self.root, text="Abrir Dashboard no Navegador", 
                                        command=self.open_browser, state="disabled")
        self.browser_button.pack(pady=10)
        
        self.auto_detect()
    
    def browse_directory(self):
        """Browse for journal directory"""
        directory = filedialog.askdirectory(title="Selecionar Diretório de Journals")
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
            if self.monitor:
                self.monitor.set_journal_directory(directory)
    
    def auto_detect(self):
        """Auto-detect journal directory"""
        temp_monitor = JournalMonitor(self.ed_data)
        if temp_monitor.journal_dir:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, str(temp_monitor.journal_dir))
            messagebox.showinfo("Sucesso", f"Diretório encontrado:\n{temp_monitor.journal_dir}")
        else:
            messagebox.showwarning("Aviso", 
                                  "Diretório não encontrado automaticamente.\n"
                                  "Você pode iniciar o servidor mesmo assim.\n"
                                  "O sistema aguardará os arquivos do jogo.")
    
    def start_server(self):
        """Start the HTTP server and journal monitor"""
        try:
            port = int(self.port_entry.get())
            journal_dir = self.dir_entry.get() if self.dir_entry.get() else None
            
            if journal_dir:
                journal_path = Path(journal_dir)
                if not journal_path.exists():
                    if not messagebox.askyesno("Confirmar", 
                        "O diretório especificado não existe.\n"
                        "Deseja iniciar mesmo assim e aguardar os arquivos?"):
                        return
                    journal_dir = None
            
            self.monitor = JournalMonitor(self.ed_data, journal_dir, allow_start_without_files=True)
            self.monitor_thread = threading.Thread(target=self.monitor.monitor, daemon=True)
            self.monitor_thread.start()
            
            self.server = ThreadedHTTPServer(('', port), EDRequestHandler, ed_data=self.ed_data)
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            
            ip = self.get_local_ip()
            url = f"http://{ip}:{port}"
            
            self.status_label.config(text=f"Servidor rodando em {url}")
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Servidor HTTP iniciado\n")
            self.info_text.insert(tk.END, f"URL Local: http://localhost:{port}\n")
            self.info_text.insert(tk.END, f"URL Rede: {url}\n")
            
            if not journal_dir:
                self.info_text.insert(tk.END, f"\n⏳ Aguardando arquivos do Elite Dangerous...\n")
                self.info_text.insert(tk.END, f"O servidor está ativo e pronto para monitorar.\n")
            else:
                self.info_text.insert(tk.END, f"\nMonitorando: {journal_dir}\n")
            
            self.info_text.insert(tk.END, f"\nAbra o dashboard no navegador para ver os dados em tempo real.\n")
            
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.browser_button.config(state="normal")
            
        except ValueError:
            messagebox.showerror("Erro", "Porta inválida")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar servidor:\n{str(e)}")
    
    def stop_server(self):
        """Stop the server and monitor"""
        if self.monitor:
            self.monitor.running = False
        
        if self.server:
            self.server.shutdown()
            self.server = None
        
        self.status_label.config(text="Servidor parado")
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "Servidor parado.\n")
        
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.browser_button.config(state="disabled")
    
    def open_browser(self):
        """Open dashboard in browser"""
        if self.server:
            port = int(self.port_entry.get())
            webbrowser.open(f"http://localhost:{port}")
    
    def get_local_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def run(self):
        """Run the GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle window closing"""
        if self.server:
            self.stop_server()
        self.root.destroy()

def main():
    app = EDGUI()
    app.run()

if __name__ == '__main__':
    main()
