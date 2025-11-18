#!/usr/bin/env python3
"""
Elite Dangerous Real-time Information Server
Monitors the game journal and serves data via HTTP with GUI
"""

import socket
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser
from pathlib import Path

from ed_data import EDData
from journal_monitor import JournalMonitor
from http_server import ThreadedHTTPServer, EDRequestHandler  # CORRETO: http_server.py (com underscore), NÃO httpserver


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
