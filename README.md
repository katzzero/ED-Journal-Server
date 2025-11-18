# 🚀 Elite Dangerous Local Server

Servidor local em Python que monitora os arquivos de journal do Elite Dangerous em tempo real e disponibiliza as informações através de uma interface web interativa.

## 📝 Índice

- [Características](#-características)
- [Informações Disponíveis](#-informações-disponíveis)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Dashboard Web](#-dashboard-web)
- [API REST](#-api-rest)
- [Debug](#-debug)
- [Solução de Problemas](#-solução-de-problemas)
- [Estrutura do Projeto](#-estrutura-do-projeto)

## ✨ Características

- **📶 Monitoramento em Tempo Real**: Acompanha automaticamente os arquivos de journal do jogo
- **🌐 Dashboard Web**: Interface visual elegante e responsiva para visualizar dados do jogo
- **⏳ Modo Offline**: Inicia mesmo sem encontrar os arquivos do Elite Dangerous
- **🔍 Auto-detecção**: Encontra automaticamente o diretório de journals em Windows, Linux e macOS
- **🔌 API REST**: Endpoint JSON para integração com outras aplicações
- **🖥️ Interface Gráfica**: GUI amigável para configuração e controle do servidor
- **🌍 Acesso Remoto**: Acesse de qualquer dispositivo na mesma rede

## 📊 Informações Disponíveis

O servidor rastreia e exibe:

### Informações Básicas
- 👤 **Comandante**: Nome do seu personagem
- 🚀 **Nave**: Tipo de nave atual
- 🌌 **Sistema**: Sistema estelar atual
- 🏢 **Estação**: Estação onde está ancorado (se aplicável)
- 💰 **Créditos**: Saldo atual de créditos

### Estado do Veículo
- 🔒 **Acoplado**: Se está acoplado em uma estação
- 🛬 **Pousado**: Se está pousado em superfície
- 🚙 **No SRV**: Se está pilotando o SRV
- ✈️ **No Fighter**: Se está pilotando um fighter
- ⚡ **Supercruise**: Se está em supercruise
- 🚀 **Em Voo**: Status geral de voo

### Coordenadas Planetárias
- 🌍 **Latitude/Longitude**: Posição exata na superfície
- 📍 **Altitude**: Altura acima da superfície
- 🧭 **Direção**: Heading atual
- 🏛️ **Assentamento Próximo**: Se houver

### Sistema Atual
- 🪐 **Corpos Celestes**: Todos os planetas e estrelas escaneados
- 🏢 **Estações**: Todas as estações do sistema com distâncias
- 🌱 **Estado de Terraformação**: Informações sobre terraformação
- ✅ **Aterrisáveis**: Indica quais planetas podem ser pousados

## 🔧 Requisitos

### Sistema Operacional
- Windows 10/11
- Linux (com Steam/Proton)
- macOS

### Python
- Python 3.7 ou superior

### Bibliotecas
Todas as bibliotecas utilizadas são nativas do Python:
- `tkinter` (geralmente já incluído)
- `http.server`
- `threading`
- `json`
- `pathlib`

## 📥 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/katzzero/ED-Journal-Server.git
cd ED-Journal-Server
```

### 2. Verifique o Python

```bash
python --version
# ou
python3 --version
```

Se não tiver Python instalado, baixe em: [python.org](https://www.python.org/downloads/)

### 3. (Opcional) Crie um Ambiente Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

## 🚀 Como Usar

### Início Rápido

1. **Execute o servidor**:
   ```bash
   python ed_server.py
   # ou
   python3 ed_server.py
   ```

2. **Configure o diretório** (opcional):
   - Clique em "Auto-detectar" para encontrar automaticamente
   - Ou use "Procurar" para selecionar manualmente
   - **Não é obrigatório** - o servidor pode iniciar sem esta configuração

3. **Inicie o servidor**:
   - Escolha uma porta (padrão: 8080)
   - Clique em "Iniciar Servidor"

4. **Acesse o Dashboard**:
   - Clique em "Abrir Dashboard no Navegador"
   - Ou acesse manualmente: `http://localhost:8080`

### Modo de Espera

Se os arquivos do Elite Dangerous não forem encontrados:

- ⏳ O servidor inicia normalmente em **modo de espera**
- 📱 O dashboard exibe "Aguardando arquivos do Elite Dangerous..."
- 🎮 Basta iniciar o jogo para começar o monitoramento automático
- ✅ Nenhuma configuração adicional é necessária

### Acessando de Outros Dispositivos

#### Na Mesma Rede

1. Na interface do servidor, anote o endereço "URL Rede" (exemplo: `http://192.168.1.100:8080`)
2. Em qualquer dispositivo na mesma rede Wi-Fi, abra o navegador
3. Digite o endereço anotado
4. Pronto! Você pode acompanhar seus dados do Elite Dangerous em tablets, celulares, etc.

#### Configuração de Firewall

**Windows**: Permita o Python no Firewall quando solicitado

**Linux**:
```bash
sudo ufw allow 8080/tcp
```

**macOS**: Permita conexões de entrada quando solicitado

## 🌐 Dashboard Web

### Funcionalidades

- **Atualização Automática**: Refresh a cada 2 segundos
- **Design Responsivo**: Adapta-se a diferentes tamanhos de tela
- **Visual Temático**: Cores inspiradas no Elite Dangerous
- **Indicadores Visuais**: ✅/❌ para status ativo/inativo
- **Animações**: Pulsação quando aguardando arquivos

### Seções do Dashboard

1. **Status do Sistema**: Estado atual do monitoramento
2. **Estado do Veículo**: Situação atual (pousado, voando, etc)
3. **Coordenadas Planetárias**: Quando na superfície de planetas
4. **Informações do Comandante**: Nave, sistema, créditos, etc
5. **Estações do Sistema**: Lista de todas as estações
6. **Corpos Celestes**: Planetas e estrelas escaneados

## 🔌 API REST

### Endpoint de Dados

**URL**: `http://localhost:8080/api/data`

**Método**: `GET`

**Resposta** (JSON):
```json
{
  "commander": "CMDR Nome",
  "ship": "Krait Mk II",
  "system": "Sol",
  "station": "Abraham Lincoln",
  "credits": 15000000,
  "location": {
    "system": "Sol",
    "coords": [0, 0, 0],
    "body": "Earth"
  },
  "vehicle_state": {
    "docked": false,
    "landed": true,
    "in_srv": false,
    "in_flight": false,
    "supercruise": false
  },
  "planetary_coordinates": {
    "latitude": 51.5074,
    "longitude": -0.1278,
    "altitude": 100,
    "body_name": "Earth",
    "on_surface": true
  },
  "system_bodies": [
    {
      "name": "Sol",
      "type": "G (White-Yellow) Star",
      "is_landable": false
    }
  ],
  "system_stations": [
    {
      "name": "Abraham Lincoln",
      "type": "Orbis Starport",
      "distance": 496
    }
  ],
  "last_update": "2025-11-18T15:20:00",
  "waiting_for_files": false
}
```

### Exemplo de Uso

**JavaScript**:
```javascript
fetch('http://localhost:8080/api/data')
  .then(response => response.json())
  .then(data => {
    console.log('Sistema atual:', data.system);
    console.log('Nave:', data.ship);
    console.log('Pousado:', data.vehicle_state.landed);
  });
```

**Python**:
```python
import requests

response = requests.get('http://localhost:8080/api/data')
data = response.json()
print(f"Sistema: {data['system']}")
print(f"Nave: {data['ship']}")
print(f"Pousado: {data['vehicle_state']['landed']}")
```

**cURL**:
```bash
curl http://localhost:8080/api/data
```

## 🐞 Debug

### Ativar Debug Visual no Dashboard

1. Abra o dashboard no navegador
2. Pressione a tecla **"D"**
3. Um painel aparecerá no canto inferior direito mostrando:
   - Número de atualizações
   - Comandante atual
   - Nave atual
   - Sistema atual

### Console do Navegador

1. Pressione **F12** no navegador
2. Vá na aba **Console**
3. Você verá logs de todas as atualizações:
   ```
   [15:20:15] Update #1 - CMDR: KatzZero, Ship: Krait Mk II, System: Sol
   [15:20:17] Update #2 - CMDR: KatzZero, Ship: Krait Mk II, System: Sol
   ```

### Limpar Cache do Navegador

Se o dashboard não atualizar:

- **Windows/Linux**: `Ctrl + Shift + R` ou `Ctrl + F5`
- **Mac**: `Cmd + Shift + R`

## ⚠️ Solução de Problemas

### O servidor não encontra os arquivos

**Solução 1**: Use o botão "Auto-detectar" na interface

**Solução 2**: Localize manualmente:
1. Procure por arquivos chamados `Journal.*.log` no seu computador
2. Use o botão "Procurar" para selecionar o diretório
3. Clique em "Iniciar Servidor"

**Solução 3**: Inicie mesmo assim:
- O servidor funciona em modo de espera
- Aguardará automaticamente até que o jogo seja iniciado

### Diretórios de Journal (Auto-detectados)

**Windows**:
```
%USERPROFILE%\Saved Games\Frontier Developments\Elite Dangerous\
```

**Linux (Steam/Proton)**:
```
~/.local/share/Steam/steamapps/compatdata/359320/pfx/drive_c/users/steamuser/Saved Games/Frontier Developments/Elite Dangerous/
```

**macOS**:
```
~/Library/Application Support/Frontier Developments/Elite Dangerous/
```

### Erro de porta já em uso

```
OSError: [Errno 98] Address already in use
```

**Solução**: Mude a porta (exemplo: 8081, 8082, 9000)

### O dashboard não atualiza

**Verificações**:
1. ✅ Servidor está rodando?
2. ✅ Elite Dangerous está aberto?
3. ✅ Você está em uma sessão de jogo (não no menu principal)?
4. 🔄 Recarregue a página do navegador (F5 ou Ctrl+Shift+R)
5. 🐞 Ative o debug visual (tecla "D") e verifique se está atualizando

### Não consigo acessar de outro dispositivo

**Verificações**:
1. ✅ Ambos os dispositivos estão na mesma rede Wi-Fi?
2. ✅ Firewall permite conexões na porta configurada?
3. ✅ Use o endereço "URL Rede" mostrado na interface, não "localhost"

### Dados não aparecem

1. Verifique se o Elite Dangerous está gerando eventos:
   - Faça algo no jogo (pouse, decole, pule para outro sistema)
2. Verifique a API diretamente: `http://localhost:8080/api/data`
3. Verifique os logs no console da GUI do servidor

## 📋 Estrutura do Projeto

```
ED-Journal-Server/
├── ed_server.py           # Arquivo principal - GUI e orquestração
├── ed_data.py             # Armazenamento de dados do jogo
├── journal_monitor.py     # Monitor de arquivos journal
├── http_server.py         # Servidor HTTP e handlers
├── dashboard_html.py      # Gerador do dashboard web
├── requirements.txt       # Dependências (todas nativas)
├── .gitignore            # Arquivos ignorados pelo git
└── README.md             # Este arquivo
```

### Módulos

- **ed_server.py**: Interface gráfica e inicialização do servidor
- **ed_data.py**: Classe para armazenamento thread-safe dos dados
- **journal_monitor.py**: Monitora e processa eventos dos journals
- **http_server.py**: Servidor HTTP com suporte a threads
- **dashboard_html.py**: Gera a interface web HTML/CSS/JavaScript

## 🔒 Segurança

⚠️ **Importante**:
- Este servidor é destinado para **uso em redes locais confiáveis**
- Não exponha o servidor diretamente à internet sem proteção adequada
- Para acesso remoto seguro, considere usar VPN

## 📝 Notas

- O servidor só rastreia informações disponíveis nos arquivos de journal do Elite Dangerous
- Alguns eventos podem ter atraso de até 1-2 segundos
- O Elite Dangerous deve estar em execução para gerar dados
- Os arquivos de journal são atualizados pelo jogo, não pelo servidor

## 🤝 Contribuindo

Sugestões, melhorias e correções são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
- Compartilhar suas personalizações

## 📜 Licença

Este projeto é fornecido "como está", sem garantias de qualquer tipo. Use por sua conta e risco.

## 🙏 Agradecimentos

- Frontier Developments pelo Elite Dangerous
- Comunidade de desenvolvedores do Elite Dangerous
- Todos os comandantes que testaram e forneceram feedback

---

**Fly safe, Commander! o7**

🌟 Se este servidor foi útil, considere deixar uma estrela no repositório!
