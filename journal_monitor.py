#!/usr/bin/env python3
"""
Elite Dangerous Journal Monitor
Monitors journal files for game events and updates game state
"""

import json
import time
from pathlib import Path
import os


class JournalMonitor:
    """Monitors Elite Dangerous journal files for updates"""
    
    def __init__(self, ed_data, journal_dir=None, allow_start_without_files=True):
        self.ed_data = ed_data
        
        # Garante que journal_dir seja Path ou None
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
        
        elif event_type == 'Scan':
            body_info = {
                'name': event.get('BodyName'),
                'type': event.get('PlanetClass') or event.get('StarType'),
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
            
            current_bodies = self.ed_data.get_all().get('system_bodies', [])
            body_names = [b['name'] for b in current_bodies]
            
            if body_info['name'] not in body_names:
                current_bodies.append(body_info)
                self.ed_data.update('system_bodies', current_bodies)
        
        elif event_type == 'FSSDiscoveryScan':
            bodies_count = event.get('BodyCount', 0)
            print(f"Sistema tem {bodies_count} corpos celestes")
        
        elif event_type == 'Docked':
            self.ed_data.update('station', event.get('StationName'))
            
            vehicle_state = self.ed_data.get_all().get('vehicle_state', {})
            vehicle_state.update({
                'docked': True,
                'landed': False,
                'in_flight': False,
                'supercruise': False
            })
            self.ed_data.update('vehicle_state', vehicle_state)
            
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
            
            vehicle_state = self.ed_data.get_all().get('vehicle_state', {})
            vehicle_state.update({
                'docked': False,
                'in_flight': True
            })
            self.ed_data.update('vehicle_state', vehicle_state)
        
        elif event_type == 'Touchdown':
            coords = {
                'latitude': event.get('Latitude'),
                'longitude': event.get('Longitude'),
                'body_name': event.get('Body'),
                'on_surface': True,
                'nearest_destination': event.get('NearestDestination')
            }
            self.ed_data.update('planetary_coordinates', coords)
            
            vehicle_state = self.ed_data.get_all().get('vehicle_state', {})
            vehicle_state.update({
                'landed': True,
                'in_flight': False
            })
            self.ed_data.update('vehicle_state', vehicle_state)
        
        elif event_type == 'Liftoff':
            coords = {
                'latitude': event.get('Latitude'),
                'longitude': event.get('Longitude'),
                'body_name': event.get('Body'),
                'on_surface': False
            }
            self.ed_data.update('planetary_coordinates', coords)
            
            vehicle_state = self.ed_data.get_all().get('vehicle_state', {})
            vehicle_state.update({
                'landed': False,
                'in_flight': True
            })
            self.ed_data.update('vehicle_state', vehicle_state)
        
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
            vehicle_state = self.ed_data.get_all().get('vehicle_state', {})
            vehicle_state.update({
                'in_srv': True,
                'landed': False
            })
            self.ed_data.update('vehicle_state', vehicle_state)
        
        elif event_type == 'DockSRV':
            vehicle_state = self.ed_data.get_all().get('vehicle_state', {})
            vehicle_state.update({
                'in_srv': False
            })
            self.ed_data.update('vehicle_state', vehicle_state)
        
        elif event_type == 'LaunchFighter':
            vehicle_state = self.ed_data.get_all().get('vehicle_state', {})
            vehicle_state['in_fighter'] = True
            self.ed_data.update('vehicle_state', vehicle_state)
        
        elif event_type == 'DockFighter':
            vehicle_state = self.ed_data.get_all().get('vehicle_state', {})
            vehicle_state['in_fighter'] = False
            self.ed_data.update('vehicle_state', vehicle_state)
        
        elif event_type == 'SupercruiseEntry':
            vehicle_state = self.ed_data.get_all().get('vehicle_state', {})
            vehicle_state.update({
                'supercruise': True,
                'landed': False,
                'in_flight': True
            })
            self.ed_data.update('vehicle_state', vehicle_state)
        
        elif event_type == 'SupercruiseExit':
            vehicle_state = self.ed_data.get_all().get('vehicle_state', {})
            vehicle_state['supercruise'] = False
            self.ed_data.update('vehicle_state', vehicle_state)
        
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
