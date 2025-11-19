#!/usr/bin/env python3
"""
Elite Dangerous Dashboard HTML Generator with Responsive Design
Improved styling with ED colors and modules toggle button
"""
def get_dashboard_html():
    """Generate the HTML dashboard page"""
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Elite Dangerous Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --ed-primary: #1a1a1a;
            --ed-dark: #0f0f0f;
            --ed-accent: #1da552;
            --ed-orange: #ff6600;
            --ed-cyan: #00ccff;
            --ed-red: #ff3333;
            --ed-yellow: #ffdd00;
            --ed-purple: #dd33ff;
            --ed-text: #cfcfcf;
            --ed-subtle: #888888;
            --ed-grid: rgba(0, 204, 255, 0.05);
            
            --font-size-xs: clamp(0.75rem, 1.5vw, 1rem);
            --font-size-sm: clamp(0.875rem, 2vw, 1.1rem);
            --font-size-base: clamp(1rem, 2.5vw, 1.25rem);
            --font-size-lg: clamp(1.25rem, 3vw, 1.5rem);
            --font-size-xl: clamp(1.5rem, 4vw, 2rem);
            --font-size-2xl: clamp(2rem, 5vw, 2.5rem);
            
            --spacing-xs: clamp(0.25rem, 0.5vw, 0.5rem);
            --spacing-sm: clamp(0.5rem, 1vw, 1rem);
            --spacing-md: clamp(1rem, 2vw, 1.5rem);
            --spacing-lg: clamp(1.5rem, 3vw, 2.5rem);
            --spacing-xl: clamp(2rem, 4vw, 3rem);
            
            --border-width: clamp(0.5px, 0.1vw, 1px);
            --border-radius: clamp(2px, 0.5vw, 8px);
        }
        
        html, body {
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, var(--ed-dark) 0%, #1a1a2e 100%);
            color: var(--ed-text);
            font-family: 'Segoe UI', 'Courier New', Tahoma, Geneva, Verdana, sans-serif;
            font-size: var(--font-size-base);
            line-height: 1.4;
            overflow-x: hidden;
        }
        
        body {
            padding: var(--spacing-md) var(--spacing-sm);
            background-image: 
                linear-gradient(90deg, transparent 0%, var(--ed-grid) 50%, transparent 100%),
                linear-gradient(0deg, transparent 0%, var(--ed-grid) 50%, transparent 100%);
            background-size: 50px 50px;
        }
        
        .container {
            max-width: 90vw;
            margin: 0 auto;
            background: rgba(15, 15, 15, 0.7);
            border: var(--border-width) solid var(--ed-cyan);
            border-radius: var(--border-radius);
            padding: var(--spacing-lg);
            box-shadow: 
                0 0 var(--spacing-md) rgba(0, 204, 255, 0.3),
                inset 0 0 var(--spacing-md) rgba(0, 204, 255, 0.05);
        }
        
        h1 {
            font-size: var(--font-size-2xl);
            color: var(--ed-orange);
            text-shadow: 0 0 var(--spacing-md) var(--ed-orange);
            text-align: center;
            margin-bottom: var(--spacing-lg);
            letter-spacing: clamp(1px, 0.2vw, 3px);
        }
        
        h2 {
            font-size: var(--font-size-xl);
            color: var(--ed-cyan);
            margin: var(--spacing-lg) 0 var(--spacing-md) 0;
            border-bottom: var(--border-width) solid var(--ed-cyan);
            padding-bottom: var(--spacing-sm);
            text-shadow: 0 0 var(--spacing-sm) rgba(0, 204, 255, 0.5);
        }
        
        .controls {
            display: flex;
            justify-content: center;
            gap: var(--spacing-md);
            margin-bottom: var(--spacing-lg);
            flex-wrap: wrap;
        }
        
        .btn {
            background: linear-gradient(135deg, var(--ed-orange) 0%, #cc5500 100%);
            color: #000;
            border: none;
            padding: var(--spacing-sm) var(--spacing-md);
            border-radius: var(--border-radius);
            font-size: var(--font-size-sm);
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: clamp(0.5px, 0.1vw, 1px);
            box-shadow: 0 0 var(--spacing-sm) rgba(255, 102, 0, 0.5);
            transition: all 0.2s ease;
        }
        
        .btn:hover {
            background: linear-gradient(135deg, #ffaa00 0%, #ff6600 100%);
            box-shadow: 0 0 var(--spacing-md) rgba(255, 102, 0, 0.8);
            transform: translate(0, -2px);
        }
        
        .btn:active {
            transform: translate(0, 0);
        }
        
        .btn-modules {
            background: linear-gradient(135deg, var(--ed-purple) 0%, #bb00dd 100%);
            color: #fff;
            box-shadow: 0 0 var(--spacing-sm) rgba(221, 51, 255, 0.5);
        }
        
        .btn-modules:hover {
            background: linear-gradient(135deg, #ff66ff 0%, var(--ed-purple) 100%);
            box-shadow: 0 0 var(--spacing-md) rgba(221, 51, 255, 0.8);
        }
        
        .status-box {
            background: rgba(0, 0, 0, 0.5);
            border: var(--border-width) solid var(--ed-orange);
            border-radius: var(--border-radius);
            padding: var(--spacing-md);
            margin: var(--spacing-md) 0;
            box-shadow: 0 0 var(--spacing-md) rgba(255, 102, 0, 0.2);
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(clamp(150px, 25vw, 300px), 1fr));
            gap: var(--spacing-md);
            margin: var(--spacing-md) 0;
        }
        
        .info-item {
            background: rgba(0, 50, 0, 0.3);
            border-left: clamp(2px, 0.3vw, 4px) solid var(--ed-accent);
            padding: var(--spacing-md);
            border-radius: var(--border-radius);
        }
        
        .info-label {
            font-size: var(--font-size-xs);
            color: var(--ed-subtle);
            text-transform: uppercase;
            letter-spacing: clamp(0.5px, 0.1vw, 1px);
        }
        
        .info-value {
            font-size: var(--font-size-lg);
            color: var(--ed-accent);
            font-weight: bold;
            margin-top: var(--spacing-xs);
            word-break: break-word;
        }
        
        .module-table-container {
            position: fixed;
            bottom: var(--spacing-md);
            right: var(--spacing-md);
            background: rgba(15, 15, 15, 0.95);
            border: var(--border-width) solid var(--ed-purple);
            border-radius: var(--border-radius);
            box-shadow: 0 0 var(--spacing-lg) rgba(221, 51, 255, 0.3);
            max-width: clamp(300px, 30vw, 600px);
            max-height: clamp(200px, 60vh, 600px);
            overflow-y: auto;
            z-index: 9999;
            display: none;
        }
        
        .module-table-container.visible {
            display: block;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .module-table {
            width: 100%;
            border-collapse: collapse;
            font-size: var(--font-size-sm);
        }
        
        .module-table th {
            background: rgba(50, 50, 50, 0.8);
            color: var(--ed-purple);
            padding: var(--spacing-sm);
            text-align: left;
            border-bottom: var(--border-width) solid var(--ed-purple);
            font-weight: bold;
            text-transform: uppercase;
            font-size: var(--font-size-xs);
        }
        
        .module-table td {
            padding: var(--spacing-sm);
            border-bottom: var(--border-width) dashed rgba(221, 51, 255, 0.3);
            color: var(--ed-text);
        }
        
        .module-table tr:nth-child(even) {
            background: rgba(30, 30, 30, 0.5);
        }
        
        .warning {
            background: rgba(255, 102, 0, 0.1);
            border: var(--border-width) solid var(--ed-orange);
            border-radius: var(--border-radius);
            padding: var(--spacing-lg);
            margin: var(--spacing-lg) 0;
            color: var(--ed-orange);
            text-align: center;
            font-size: var(--font-size-lg);
            text-shadow: 0 0 var(--spacing-sm) rgba(255, 102, 0, 0.3);
        }
        
        .watermark {
            position: fixed;
            bottom: var(--spacing-sm);
            left: var(--spacing-sm);
            font-size: var(--font-size-xs);
            color: var(--ed-subtle);
            opacity: 0.3;
            pointer-events: none;
        }
        
        #content {
            min-height: 80vh;
            padding: var(--spacing-md);
        }
        
        @media (max-width: 768px) {
            body {
                padding: var(--spacing-sm);
            }
            
            .container {
                padding: var(--spacing-md);
            }
            
            .module-table-container {
                max-width: 90vw;
                bottom: var(--spacing-sm);
                right: var(--spacing-sm);
            }
        }
    </style>
</head>
<body>
    <div class="watermark">Elite Dangerous • CMDR Katzzero</div>
    
    <div class="container">
        <h1>🚀 Elite Dangerous Dashboard</h1>
        
        <div class="controls">
            <button class="btn btn-modules" id="toggleModules">📦 Módulos</button>
        </div>
        
        <div id="content"></div>
    </div>
    
    <div id="modules-box" class="module-table-container"></div>
    
    <script>"""
        let updateCount = 0;
        let modulesVisible = false;
        
        function toggleModules() {
            const container = document.getElementById('modules-box');
            modulesVisible = !modulesVisible;
            container.classList.toggle('visible');
        }
        
        function formatCoordinate(value, type) {
            if (value === null || value === undefined) return 'N/A';
            const direction = type === 'lat' 
                ? (value >= 0 ? 'N' : 'S')
                : (value >= 0 ? 'E' : 'W');
            return `${Math.abs(value).toFixed(2)}° ${direction}`;
        }
        
        function getVehicleStatus(v) {
            if (v.in_srv) return '🚙 SRV';
            if (v.in_fighter) return '✈️ Fighter';
            if (v.docked) return '🔒 Acoplado';
            if (v.landed) return '🛬 Pousado';
            if (v.supercruise) return '⚡ Supercruise';
            if (v.in_flight) return '🚀 Em Voo';
            return '❓ Desconhecido';
        }
        
        function renderModules(m) {
            const c = document.getElementById('modules-box');
            if (!m || m.length === 0) {c.innerHTML = '';return;}
            let h = '<table class="module-table"><thead><tr>';
            h += '<th>Slot</th><th>Módulo</th><th>Saúde</th><th>P</th></tr></thead><tbody>';
            m.forEach(x => {
                const k = x.health != null ? (x.health * 100).toFixed(0) : '--';
                h += `<tr><td>${x.slot ? x.slot.slice(0,8) : '-'}</td>`;
                h += `<td>${(x.item || '-').split('_').pop().slice(0,12)}</td>`;
                h += `<td>${k}%</td><td>${x.priority || '-'}</td></tr>`;
            });
            h += '</tbody></table>';
            c.innerHTML = h;
        }
        
        function update() {
            updateCount++;
            fetch(`/api/data?_=${Date.now()}`, {cache:'no-cache',headers:{'Pragma':'no-cache'}})
            .then(r => r.ok ? r.json() : {})
            .then(d => {
                if (!Object.keys(d).length) return;
                let h = '';
                const v = d.vehicle_state || {};
                const co = d.planetary_coordinates || {};
                h += `<div class="status-box"><div class="info-label">Status</div><div class="info-value">${d.status}</div></div>`;
                if (d.waiting_for_files) {
                    h += `<div class="warning">⏳ Aguardando Elite Dangerous...</div>`;
                } else {
                    h += `<div class="info-grid">`;
                    [['Comandante', d.commander], ['Nave', d.ship], ['Sistema', d.system],
                     ['Veículo', getVehicleStatus(v)], ['Créditos', `${d.credits.toLocaleString()} CR`]].forEach(([l, v]) => {
                        h += `<div class="info-item"><div class="info-label">${l}</div><div class="info-value">${v}</div></div>`;
                    });
                    if (co.on_surface && co.latitude !== null) {
                        h += `<div class="info-item"><div class="info-label">Lat</div><div class="info-value">${formatCoordinate(co.latitude, 'lat')}</div></div>`;
                        h += `<div class="info-item"><div class="info-label">Lon</div><div class="info-value">${formatCoordinate(co.longitude, 'lon')}</div></div>`;
                    }
                    h += `</div>`;
                }
                if (d.last_update) {
                    const t = new Date(d.last_update).toLocaleString('pt-BR');
                    h += `<div style="text-align: center; color: var(--ed-subtle); font-size: var(--font-size-xs); margin-top: var(--spacing-lg);">Atualizado: ${t} | #${updateCount}</div>`;
                }
                document.getElementById('content').innerHTML = h;
                renderModules(d.modules);
            })
            .catch(e => {
                document.getElementById('content').innerHTML = `<div class="warning">❌ Erro: ${e.message}</div>`;
            });
        }
        
        document.getElementById('toggleModules').addEventListener('click', toggleModules);
        update();
        setInterval(update, 2000);
    </script>
</body>
</html>
"""
