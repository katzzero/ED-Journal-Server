#!/usr/bin/env python3
"""
Elite Dangerous Dashboard HTML Generator
Generates the interactive web dashboard interface
"""


def get_dashboard_html():
    """Generate the HTML dashboard page"""
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
        .module-table {
            position: fixed;
            top: 42px;
            right: 10px;
            background: rgba(5,5,5,0.92);
            border: 1px solid #444;
            border-radius: 8px;
            font-size: 14px;
max-width: 600px;            min-width: 400px;
            z-index: 9999;
            color: #cfcfcf;
        }
        .module-table th, .module-table td {
            padding: 8px 12px;
            text-align: left;
            font-size: 14px;
        }
        .module-table th {
            border-bottom: 1px solid #333;
            background: #363636;
        }
        .module-table tr:nth-child(even) {
            background: #222;
        }
        .module-table .hlth {
            width: 44px;
        }
        .module-table .prio {
            width: 30px;
            text-align: center;
        }
        .watermark {
            position: fixed;
            bottom: 7px;
            right: 12px;
            color: #666;
            font-size: 10px;
            opacity: 0.44;
            pointer-events: none;
            letter-spacing: 0.5px;
            font-style: italic;
            z-index: 99999;
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
        .debug-info {
            position: fixed;
            bottom: 10px;
            left: 10px;
            background: rgba(0, 0, 0, 0.91);
            color: #0f0;
            padding: 9px 12px;
            border: 1px solid #0f0;
            border-radius: 5px;
            font-family: monospace;
            font-size: 0.8em;
            max-width: 330px;
            z-index: 99999;
        }
        #content { min-height: 80vh; padding: 20px; color: #cfcfcf; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Elite Dangerous Dashboard</h1>
        <div id="content"></div>
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
            if (!modules || modules.length === 0) {
                document.getElementById('modules-box').innerHTML = '';
                return;
            }
            let html = '<div class="module-table"><table><thead><tr>';
            html += '<th>Slot</th><th>Módulo</th><th class="hlth">Vida</th><th class="prio">Prior.</th></tr></thead><tbody>';
            modules.forEach(m => {
                html += `<tr>
                  <td>${m.slot ? m.slot.replace('Slot', '').slice(0,10) : '-'}</td>
                  <td>${(m.item || '-').split('_').pop().slice(0,13)}</td>
                  <td class="hlth">${m.health != null ? (m.health * 100).toFixed(0) : '--'}%</td>
                  <td class="prio">${m.priority != null ? m.priority : '-'}</td>
                </tr>`;
            });
            html += '</tbody></table></div>';
            document.getElementById('modules-box').innerHTML = html;
        }

        function updateDashboard() {
            updateCount++;
            const timestamp = new Date().getTime();
            fetch(`/api/data?_=${timestamp}`, {                cache: 'no-cache',
                headers: {
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache'
                }
            })
                .then(response => {
                    if (!response.ok) {
                        // Se o status for 404, o servidor pode estar em um estado de inicialização.
                        // Retorna um objeto vazio para evitar o erro, mas não processa dados.
                        if (response.status === 404) {
                            console.warn('API endpoint not found (404). Server might be initializing.');
                            return {};
                        }
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    // Se o objeto de dados estiver vazio, interrompe o processamento do dashboard
                    if (Object.keys(data).length === 0) return;

                    lastData = data;
                    updateDebug(`Update #${updateCount} - CMDR: ${data.commander}, Ship: ${data.ship}, System: ${data.system}`);
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
                        html += `<div class="last-update">Última atualização: ${updateTime} | Refresh #${updateCount}</div>`;
                    }

                    document.getElementById('content').innerHTML = html;
                    // Renderiza tabela de módulos
                    renderModulesTable(data.modules);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    updateDebug(`ERRO: ${error.message}`);
                    document.getElementById('content').innerHTML = 
                        `<div class="warning">Erro ao conectar com o servidor<br><small>${error.message}</small></div>`;
                });
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'd' || e.key === 'D') {
                const debugDiv = document.getElementById('debug');
                debugDiv.style.display = debugDiv.style.display === 'none' ? 'block' : 'none';
            }
        });

        updateDashboard();
        setInterval(updateDashboard, 2000);
    </script>
</body>
</html>
    """
