#!/usr/bin/env python3
"""
Elite Dangerous Dashboard HTML Generator - Enhanced Version
Generates a beautiful, modern interactive web dashboard interface
"""


def get_dashboard_html():
    """Generate the enhanced HTML dashboard page"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Elite Dangerous Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0e17;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(255, 102, 0, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(0, 170, 255, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(255, 0, 255, 0.03) 0%, transparent 50%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1600px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            font-size: 3em;
            font-weight: 700;
            background: linear-gradient(135deg, #ff6600 0%, #ff9944 50%, #ffaa00 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            text-shadow: 0 0 40px rgba(255, 102, 0, 0.3);
            letter-spacing: 2px;
        }
        
        h2 {
            color: #00ddff;
            font-size: 1.5em;
            font-weight: 600;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #00ff00;
            box-shadow: 0 0 10px #00ff00;
            animation: pulse-status 2s infinite;
        }
        
        @keyframes pulse-status {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(0.9); }
        }
        
        .status-box {
            background: linear-gradient(135deg, rgba(20, 25, 35, 0.95) 0%, rgba(15, 20, 30, 0.95) 100%);
            border: 1px solid rgba(255, 102, 0, 0.3);
            border-radius: 16px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .status-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 102, 0, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .status-box:hover::before {
            left: 100%;
        }
        
        .status-box:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 12px 40px rgba(0, 0, 0, 0.4),
                0 0 0 1px rgba(255, 102, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        .waiting-status {
            border-color: rgba(255, 170, 0, 0.4);
            animation: pulse-box 2s infinite;
        }
        
        @keyframes pulse-box {
            0%, 100% { 
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 170, 0, 0.2);
            }
            50% { 
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 40px rgba(255, 170, 0, 0.4);
            }
        }
        
        .coordinates-box {
            background: linear-gradient(135deg, rgba(0, 50, 80, 0.4) 0%, rgba(0, 30, 60, 0.4) 100%);
            border: 1px solid rgba(0, 170, 255, 0.3);
            border-radius: 16px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                0 0 30px rgba(0, 170, 255, 0.15);
            transition: all 0.3s ease;
        }
        
        .coordinates-box:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 12px 40px rgba(0, 0, 0, 0.4),
                0 0 40px rgba(0, 170, 255, 0.25);
        }
        
        .vehicle-status-box {
            background: linear-gradient(135deg, rgba(80, 0, 80, 0.4) 0%, rgba(50, 0, 60, 0.4) 100%);
            border: 1px solid rgba(255, 0, 255, 0.3);
            border-radius: 16px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                0 0 30px rgba(255, 0, 255, 0.15);
            transition: all 0.3s ease;
        }
        
        .vehicle-status-box:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 12px 40px rgba(0, 0, 0, 0.4),
                0 0 40px rgba(255, 0, 255, 0.25);
        }
        
        .bodies-box, .stations-box {
            background: linear-gradient(135deg, rgba(80, 70, 0, 0.3) 0%, rgba(50, 40, 0, 0.3) 100%);
            border: 1px solid rgba(255, 221, 0, 0.3);
            border-radius: 16px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                0 0 30px rgba(255, 221, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .bodies-box:hover, .stations-box:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 12px 40px rgba(0, 0, 0, 0.4),
                0 0 40px rgba(255, 221, 0, 0.2);
        }
        
        .modules-box {
            background: linear-gradient(135deg, rgba(0, 80, 120, 0.3) 0%, rgba(0, 50, 80, 0.3) 100%);
            border: 1px solid rgba(0, 170, 255, 0.3);
            border-radius: 16px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                0 0 30px rgba(0, 170, 255, 0.15);
            transition: all 0.3s ease;
        }
        
        .modules-box:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 12px 40px rgba(0, 0, 0, 0.4),
                0 0 40px rgba(0, 170, 255, 0.25);
        }
        
        .module-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin-top: 15px;
        }
        
        .module-table th, .module-table td {
            padding: 10px 12px;
            text-align: left;
            font-size: 0.9em;
        }
        
        .module-table th {
            background: rgba(0, 100, 150, 0.3);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #00ddff;
            border-bottom: 2px solid rgba(0, 170, 255, 0.3);
            text-shadow: 0 0 8px rgba(0, 221, 255, 0.3);
        }
        
        .module-table th:first-child {
            border-top-left-radius: 8px;
        }
        
        .module-table th:last-child {
            border-top-right-radius: 8px;
        }
        
        .module-table tr {
            transition: all 0.2s ease;
        }
        
        .module-table tbody tr:hover {
            background: rgba(0, 170, 255, 0.15);
            transform: translateX(4px);
        }
        
        .module-table tbody tr {
            background: rgba(0, 0, 0, 0.2);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .module-table tbody tr:nth-child(even) {
            background: rgba(255, 255, 255, 0.02);
        }
        
        .module-table .hlth {
            color: #00ff00;
            font-weight: 600;
            text-align: center;
        }
        
        .module-table .prio {
            text-align: center;
            color: #ffaa00;
            font-weight: 600;
        }
        
        .module-slot {
            color: #00aaff;
            font-weight: 500;
        }
        
        .module-item {
            color: #cfcfcf;
        }
        
        .watermark {
            position: fixed;
            bottom: 10px;
            right: 15px;
            color: rgba(255, 255, 255, 0.2);
            font-size: 11px;
            opacity: 0.5;
            pointer-events: none;
            letter-spacing: 1px;
            font-style: italic;
            z-index: 99999;
            font-weight: 300;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .info-item, .coord-item, .vehicle-item {
            background: rgba(255, 255, 255, 0.02);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .info-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 3px;
            background: linear-gradient(180deg, #00ff00, #00aa00);
            box-shadow: 0 0 10px #00ff00;
        }
        
        .coord-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 3px;
            background: linear-gradient(180deg, #00aaff, #0066cc);
            box-shadow: 0 0 10px #00aaff;
        }
        
        .vehicle-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 3px;
            background: linear-gradient(180deg, #ff00ff, #cc00cc);
            box-shadow: 0 0 10px #ff00ff;
        }
        
        .info-item:hover, .coord-item:hover, .vehicle-item:hover {
            transform: translateX(4px);
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(255, 255, 255, 0.1);
        }
        
        .info-label {
            color: #888;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .info-value {
            color: #00ff00;
            font-size: 1.3em;
            font-weight: 700;
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
        }
        
        .coord-value {
            color: #00ddff;
            font-size: 1.3em;
            font-weight: 700;
            font-family: 'Courier New', monospace;
            text-shadow: 0 0 10px rgba(0, 221, 255, 0.3);
        }
        
        .vehicle-value {
            color: #ff00ff;
            font-size: 1.3em;
            font-weight: 700;
            text-shadow: 0 0 10px rgba(255, 0, 255, 0.3);
        }
        
        .warning {
            color: #ffaa00;
            text-align: center;
            font-size: 1.2em;
            padding: 30px;
            background: linear-gradient(135deg, rgba(255, 170, 0, 0.1), rgba(255, 136, 0, 0.05));
            border-radius: 12px;
            margin: 20px 0;
            border: 1px solid rgba(255, 170, 0, 0.3);
            box-shadow: 0 4px 20px rgba(255, 170, 0, 0.1);
        }
        
        .warning small {
            display: block;
            margin-top: 10px;
            opacity: 0.8;
            font-size: 0.85em;
        }
        
        .last-update {
            text-align: center;
            color: #666;
            margin-top: 30px;
            font-size: 0.9em;
            padding: 15px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .planet-icon, .station-icon, .vehicle-icon {
            font-size: 1.5em;
            filter: drop-shadow(0 0 5px currentColor);
        }
        
        .body-list, .station-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .body-card, .station-card {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 221, 0, 0.2);
            border-radius: 12px;
            padding: 18px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .body-card::after, .station-card::after {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, rgba(255, 221, 0, 0.05), transparent);
            border-radius: 50%;
            transform: translate(30%, -30%);
        }
        
        .body-card:hover, .station-card:hover {
            transform: translateY(-4px);
            background: rgba(0, 0, 0, 0.6);
            border-color: rgba(255, 221, 0, 0.4);
            box-shadow: 0 8px 24px rgba(255, 221, 0, 0.2);
        }
        
        .body-name, .station-name {
            color: #ffdd00;
            font-weight: 700;
            font-size: 1.15em;
            margin-bottom: 12px;
            text-shadow: 0 0 10px rgba(255, 221, 0, 0.3);
        }
        
        .body-detail, .station-detail {
            color: #aaa;
            font-size: 0.9em;
            margin: 6px 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .landable {
            color: #00ff00;
            font-weight: 700;
            text-shadow: 0 0 8px rgba(0, 255, 0, 0.4);
        }
        
        .status-active {
            color: #00ff00;
            font-weight: 700;
            text-shadow: 0 0 8px rgba(0, 255, 0, 0.4);
        }
        
        .status-inactive {
            color: #666;
        }
        
        .debug-info {
            position: fixed;
            bottom: 10px;
            left: 10px;
            background: rgba(0, 0, 0, 0.95);
            color: #0f0;
            padding: 12px 16px;
            border: 1px solid #0f0;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.8em;
            max-width: 350px;
            z-index: 99999;
            box-shadow: 0 4px 20px rgba(0, 255, 0, 0.3);
        }
        
        #content { 
            min-height: 80vh; 
            padding: 20px; 
            color: #cfcfcf;
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 102, 0, 0.5);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 102, 0, 0.7);
        }
        
        /* Loading animation */
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
        
        .loading {
            background: linear-gradient(90deg, rgba(255, 255, 255, 0.02) 25%, rgba(255, 255, 255, 0.05) 50%, rgba(255, 255, 255, 0.02) 75%);
            background-size: 1000px 100%;
            animation: shimmer 2s infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Elite Dangerous Dashboard</h1>
        <div id="content" class="loading"></div>
    </div>
    <div id="modules-box"></div>
    <div id="debug" class="debug-info" style="display: none;"></div>
    <div class="watermark">By Cmdr. Katzzero</div>
    
    <script>
        let updateCount = 0;
        let lastData = null;

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

        function updateDebug(message) {
            const debugDiv = document.getElementById('debug');
            const now = new Date().toLocaleTimeString('pt-BR');
            debugDiv.innerHTML = `${now}: ${message}`;
            console.log(`[${now}] ${message}`);
        }

        function renderModulesTable(modules) {
            const modulesContainer = document.getElementById('modules-box');
            
            if (!modules || modules.length === 0) {
                modulesContainer.innerHTML = '';
                return;
            }
            
            let html = '<div class="modules-box">';
            html += '<h2><span class="station-icon">⚙️</span>Módulos da Nave (' + modules.length + ')</h2>';
            html += '<table class="module-table"><thead><tr>';
            html += '<th>Slot</th><th>Módulo</th><th class="hlth">Integridade</th><th class="prio">Prioridade</th></tr></thead><tbody>';
            
            modules.forEach(m => {
                const health = m.health != null ? (m.health * 100).toFixed(0) : '--';
                const healthColor = health >= 80 ? '#00ff00' : health >= 50 ? '#ffaa00' : '#ff3333';
                
                html += `<tr>
                  <td class="module-slot">${m.slot ? m.slot.replace('Slot', '').replace(/([A-Z])/g, ' $1').trim() : '-'}</td>
                  <td class="module-item">${(m.item || '-').split('_').slice(-2).join(' ')}</td>
                  <td class="hlth" style="color: ${healthColor}">${health}%</td>
                  <td class="prio">${m.priority != null ? m.priority : '-'}</td>
                </tr>`;
            });
            
            html += '</tbody></table></div>';
            modulesContainer.innerHTML = html;
        }

        function updateDashboard() {
            updateCount++;
            const timestamp = new Date().getTime();
            fetch(`/api/data?_=${timestamp}`, {
                cache: 'no-cache',
                headers: {
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache'
                }
            })
                .then(response => {
                    if (!response.ok) {
                        if (response.status === 404) {
                            console.warn('API endpoint not found (404). Server might be initializing.');
                            return {};
                        }
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (Object.keys(data).length === 0) return;
                                        // [PERFORMANCE FIX #1] Compare data with lastData before rendering
                                                            if (lastData && JSON.stringify(lastData) === JSON.stringify(data)) {
                                                                                    console.log('[CACHE] Dados idênticos, ignorando atualização');
                                                                                                            return; // Skip rendering if no changes
                                                                                                                                }

                    lastData = data;
                    updateDebug(`Update #${updateCount} - CMDR: ${data.commander}, Ship: ${data.ship}, System: ${data.system}`);
                    let html = '';
                    const statusClass = data.waiting_for_files ? 'status-box waiting-status' : 'status-box';
                    html += `<div class="${statusClass}">`;
                    html += `<div class="info-label"><span class="status-indicator"></span> Status do Sistema</div>`;
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
                            
                html += '<div class="coord-item">';
                html += '<div class="info-label">Status</div>';
                html += '<div class="coord-value" style="color: #ffaa00;">🪐 Próximo a um Planeta</div>';
                html += '</div>';
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
                        html += `<div class="last-update">Última atualização: ${updateTime} | Refresh #${updateCount}</div>`;
                    }

                    document.getElementById('content').innerHTML = html;
                    document.getElementById('content').classList.remove('loading');
                    renderModulesTable(data.modules);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    updateDebug(`ERRO: ${error.message}`);
                    document.getElementById('content').innerHTML = 
                        `<div class="warning">Erro ao conectar com o servidor<br><small>${error.message}</small></div>`;
                    document.getElementById('content').classList.remove('loading');
                });
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'd' || e.key === 'D') {
                const debugDiv = document.getElementById('debug');
                debugDiv.style.display = debugDiv.style.display === 'none' ? 'block' : 'none';
            }
        });

        updateDashboard();
        setInterval(updateDashboard, 500);
    </script>
</body>
</html>
    """
