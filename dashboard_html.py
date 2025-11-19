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
}

body {
background-color: var(--ed-primary);
color: var(--ed-text);
font-family: 'Courier New', monospace;
line-height: 1.6;
overflow-x: hidden;
}

.container {
max-width: clamp(600px, 90vw, 1200px);
margin: 0 auto;
padding: clamp(1rem, 5vw, 2rem);
}

header {
border-bottom: clamp(2px, 0.5vw, 4px) solid var(--ed-accent);
padding-bottom: clamp(1rem, 3vw, 1.5rem);
margin-bottom: clamp(1rem, 5vw, 2rem);
}

h1 {
font-size: clamp(1.5rem, 6vw, 2.5rem);
color: var(--ed-cyan);
text-transform: uppercase;
letter-spacing: 0.15em;
text-shadow: 0 0 clamp(5px, 1vw, 10px) var(--ed-cyan);
}

.status-grid {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(clamp(150px, 40vw, 300px), 1fr));
gap: clamp(0.75rem, 3vw, 1.5rem);
margin-bottom: clamp(1.5rem, 5vw, 2rem);
}

.status-item {
border: clamp(1px, 0.3vw, 2px) solid var(--ed-accent);
padding: clamp(0.75rem, 2vw, 1.5rem);
background-color: var(--ed-dark);
}

.status-label {
font-size: clamp(0.7rem, 1.5vw, 0.9rem);
color: var(--ed-subtle);
text-transform: uppercase;
letter-spacing: 0.1em;
margin-bottom: clamp(0.3rem, 1vw, 0.5rem);
}

.status-value {
font-size: clamp(1.2rem, 3vw, 1.8rem);
color: var(--ed-orange);
font-weight: bold;
}

.controls {
display: flex;
flex-wrap: wrap;
gap: clamp(0.5rem, 2vw, 1rem);
margin-bottom: clamp(1rem, 5vw, 2rem);
}

.btn {
padding: clamp(0.5rem, 1.5vw, 0.75rem) clamp(0.75rem, 2vw, 1.25rem);
background-color: var(--ed-dark);
color: var(--ed-cyan);
border: clamp(1px, 0.3vw, 2px) solid var(--ed-cyan);
text-transform: uppercase;
font-family: 'Courier New', monospace;
font-size: clamp(0.8rem, 1.5vw, 1rem);
cursor: pointer;
transition: all 0.3s ease;
}

.btn:hover {
background-color: var(--ed-cyan);
color: var(--ed-primary);
box-shadow: 0 0 clamp(8px, 1vw, 15px) var(--ed-cyan);
}

.btn:active {
transform: scale(0.98);
}

.module-table-container {
display: none;
margin-top: clamp(1rem, 3vw, 1.5rem);
border: clamp(1px, 0.3vw, 2px) solid var(--ed-accent);
padding: clamp(1rem, 2vw, 1.5rem);
background-color: var(--ed-dark);
}

.module-table-container.visible {
display: block;
animation: slideDown 0.3s ease;
}

@keyframes slideDown {
from {
opacity: 0;
transform: translateY(clamp(-10px, -2vh, -20px));
}
to {
opacity: 1;
transform: translateY(0);
}
}

hr {
border: none;
border-top: clamp(1px, 0.3vw, 2px) solid var(--ed-accent);
margin: clamp(1rem, 3vw, 1.5rem) 0;
}

table {
width: 100%;
border-collapse: collapse;
margin-top: clamp(0.75rem, 2vw, 1rem);
}

th, td {
padding: clamp(0.5rem, 1.5vw, 0.75rem) clamp(0.5rem, 2vw, 1rem);
text-align: left;
font-size: clamp(0.8rem, 1.5vw, 1rem);
border-bottom: clamp(1px, 0.2vw, 1px) solid var(--ed-accent);
}

th {
color: var(--ed-cyan);
font-weight: bold;
background-color: rgba(0, 204, 255, 0.05);
text-transform: uppercase;
letter-spacing: 0.05em;
}

td {
color: var(--ed-text);
}

tr:hover {
background-color: rgba(255, 102, 0, 0.05);
}

.module-name {
color: var(--ed-orange);
font-weight: bold;
}

.module-health {
color: var(--ed-cyan);
}

.update-info {
font-size: clamp(0.75rem, 1.2vw, 0.85rem);
color: var(--ed-subtle);
margin-top: clamp(1rem, 3vw, 1.5rem);
padding-top: clamp(1rem, 2vw, 1rem);
border-top: clamp(1px, 0.3vw, 2px) dotted var(--ed-accent);
}

@media (max-width: 600px) {
.status-grid {
grid-template-columns: 1fr;
}

.controls {
flex-direction: column;
}

.btn {
width: 100%;
}
}
</style>
</head>
<body>
<div class="container">
<header>
<h1>Elite Dangerous</h1>
<p style="font-size: clamp(0.9rem, 1.5vw, 1rem); color: var(--ed-subtle); margin-top: clamp(0.5rem, 1vw, 0.75rem);">Dashboard</p>
</header>

<div class="status-grid">
<div class="status-item">
<div class="status-label">Status</div>
<div class="status-value" id="statusValue">Online</div>
</div>
<div class="status-item">
<div class="status-label">Localizacao</div>
<div class="status-value" id="locationValue">---</div>
</div>
<div class="status-item">
<div class="status-label">Nave</div>
<div class="status-value" id="shipValue">---</div>
</div>
<div class="status-item">
<div class="status-label">Creditos</div>
<div class="status-value" id="creditsValue">0</div>
</div>
</div>

<div class="controls">
<button class="btn" id="toggleModules">Modulos</button>
<button class="btn" id="refreshBtn">Atualizar</button>
</div>

<div class="module-table-container" id="moduleContainer">
<h2 style="font-size: clamp(1.1rem, 2vw, 1.4rem); color: var(--ed-orange); margin-bottom: clamp(0.75rem, 2vw, 1rem); text-transform: uppercase;">Modulos Instalados</h2>
<table id="modulesTable">
<thead>
<tr>
<th>Modulo</th>
<th>Saude</th>
<th>Status</th>
</tr>
</thead>
<tbody id="modulesTableBody">
<tr>
<td class="module-name">Power Plant</td>
<td class="module-health">100%</td>
<td>Operacional</td>
</tr>
<tr>
<td class="module-name">Thrusters</td>
<td class="module-health">100%</td>
<td>Operacional</td>
</tr>
<tr>
<td class="module-name">Frame Shift Drive</td>
<td class="module-health">100%</td>
<td>Operacional</td>
</tr>
<tr>
<td class="module-name">Life Support</td>
<td class="module-health">100%</td>
<td>Operacional</td>
</tr>
</tbody>
</table>
</div>

<div class="update-info">
<div>Updates: <span id="updateCount">0</span></div>
<div style="margin-top: clamp(0.25rem, 0.5vw, 0.5rem);">Last Update: <span id="lastUpdate">---</span></div>
</div>
</div>

<script>
let updateCount = 0;
let modulesVisible = false;

function toggleModules() {
const container = document.getElementById('moduleContainer');
modulesVisible = !modulesVisible;
if (modulesVisible) {
container.classList.add('visible');
} else {
container.classList.remove('visible');
}
}

document.getElementById('toggleModules').addEventListener('click', toggleModules);

document.getElementById('refreshBtn').addEventListener('click', function() {
updateCount++;
document.getElementById('updateCount').textContent = updateCount;
document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString('pt-BR');
});

function updateStatus() {
updateCount++;
document.getElementById('updateCount').textContent = updateCount;
document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString('pt-BR');
}

setInterval(updateStatus, 5000);
updateStatus();
</script>
</body>
</html>
"""
