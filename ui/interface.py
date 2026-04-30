"""
Módulo para a interface gráfica do sistema de informações de hardware.
Utiliza Tkinter para criar uma interface desktop moderna e responsiva.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import logging
from typing import Optional

from services.hardware_info import HardwareCollector
from utils.helpers import export_to_txt, export_to_pdf, get_label_for_key

# Configuração de logging
logger = logging.getLogger(__name__)


class HardwareInfoApp:
    """Aplicação gráfica para exibir informações de hardware."""

    def __init__(self, root: tk.Tk):
        """
        Inicializa a aplicação.
        
        Args:
            root (tk.Tk): Janela raiz do Tkinter
        """
        self.root = root
        self.collector = HardwareCollector()
        self.data = {}
        self.info_labels = {}  # Armazena labels para atualização
        
        # Configuração da janela
        self.root.title("Sistema de Informações de Hardware")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)  # Tamanho mínimo para responsividade
        self.root.resizable(True, True)  # Permitir redimensionamento
        
        # Cores personalizadas
        self.bg_color = "#f0f0f0"
        self.header_color = "#1f4788"
        self.button_color = "#28a745"
        self.button_hover = "#218838"
        
        self.root.configure(bg=self.bg_color)
        
        # Configurar grid para responsividade
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Criar interface
        self.create_widgets()
        
        # Centralizar janela na tela
        self.center_window()
        
        # Vincular evento de redimensionamento
        self.root.bind('<Configure>', self.on_window_resize)

    def on_window_resize(self, event) -> None:
        """Executado quando a janela é redimensionada."""
        # Pode ser usado para ajustes de layout se necessário
        pass

    def center_window(self) -> None:
        """Centraliza a janela na tela."""
        self.root.update_idletasks()
        
        # Obter dimensões
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calcular posição
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self) -> None:
        """Cria os widgets da interface com layout responsivo."""
        
        # ===== HEADER =====
        header_frame = tk.Frame(self.root, bg=self.header_color)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(0, weight=1)
        
        title_label = tk.Label(
            header_frame,
            text="📊 INFORMAÇÕES DE HARDWARE",
            font=("Arial", 16, "bold"),
            bg=self.header_color,
            fg="white",
            pady=15
        )
        title_label.pack(fill=tk.X)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Clique em 'Coletar Informações' para atualizar os dados do sistema",
            font=("Arial", 9),
            bg=self.header_color,
            fg="#e0e0e0"
        )
        subtitle_label.pack(pady=(0, 10))
        
        # ===== MAIN CONTENT COM SCROLL =====
        # Frame para conter canvas e scrollbar
        container_frame = tk.Frame(self.root, bg=self.bg_color)
        container_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        container_frame.grid_rowconfigure(0, weight=1)
        container_frame.grid_columnconfigure(0, weight=1)
        
        # Canvas para scroll vertical
        canvas = tk.Canvas(
            container_frame,
            bg=self.bg_color,
            highlightthickness=0,
            width=700
        )
        canvas.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            container_frame,
            orient="vertical",
            command=canvas.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame dentro do canvas para conter os widgets
        content_frame = tk.Frame(canvas, bg=self.bg_color)
        canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")
        content_frame.grid_columnconfigure(0, weight=1, uniform="col")
        content_frame.grid_columnconfigure(1, weight=1, uniform="col")
        
        # Ajustar largura interna ao redimensionar
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
            canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.bind("<Configure>", _on_canvas_configure)
        
        # ===== INFO FIELDS =====
        info_fields = [
            ("serial", "Número de Série (BIOS)"),
            ("manufacturer", "Fabricante"),
            ("model", "Modelo do Computador"),
            ("host", "Nome do Host"),
            ("cpu", "Processador (CPU)"),
            ("ram", "Memória RAM"),
            ("mac", "Endereço MAC"),
            ("os", "Sistema Operacional"),
            ("battery", "Saúde da Bateria")
        ]
        
        for idx, (key, label) in enumerate(info_fields):
            row = idx // 2
            col = idx % 2
            self.create_info_field(content_frame, key, label, row, col)
        
        # Adicionar espaçamento no final
        spacer = tk.Frame(content_frame, bg=self.bg_color, height=10)
        spacer.grid(row=(len(info_fields) + 1) // 2, column=0, columnspan=2, sticky="ew")
        
        # Atualizar tamanho do scroll
        content_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Vincular evento de mouse wheel para scroll
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        content_frame.bind("<MouseWheel>", on_mousewheel)
        
        # ===== BUTTON FRAME (FIXO NO RODAPÉ) =====
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=15)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)
        button_frame.grid_columnconfigure(3, weight=0)
        
        # Botão Coletar
        collect_button = tk.Button(
            button_frame,
            text="🔄 Coletar Informações",
            command=self.on_collect_clicked,
            bg=self.button_color,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=9,
            relief=tk.RAISED,
            cursor="hand2"
        )
        collect_button.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Bind para hover effect
        collect_button.bind("<Enter>", lambda e: collect_button.config(bg=self.button_hover))
        collect_button.bind("<Leave>", lambda e: collect_button.config(bg=self.button_color))
        
        # Botão Exportar TXT
        export_txt_button = tk.Button(
            button_frame,
            text="📄 Exportar TXT",
            command=self.on_export_txt_clicked,
            bg="#007bff",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=9,
            relief=tk.RAISED,
            cursor="hand2"
        )
        export_txt_button.grid(row=0, column=2, padx=5, sticky="ew")
        export_txt_button.bind("<Enter>", lambda e: export_txt_button.config(bg="#0056b3"))
        export_txt_button.bind("<Leave>", lambda e: export_txt_button.config(bg="#007bff"))
        
        # Botão Exportar PDF
        export_pdf_button = tk.Button(
            button_frame,
            text="📊 Exportar PDF",
            command=self.on_export_pdf_clicked,
            bg="#dc3545",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=9,
            relief=tk.RAISED,
            cursor="hand2"
        )
        export_pdf_button.grid(row=0, column=3, padx=5, sticky="ew")
        export_pdf_button.bind("<Enter>", lambda e: export_pdf_button.config(bg="#c82333"))
        export_pdf_button.bind("<Leave>", lambda e: export_pdf_button.config(bg="#dc3545"))

    def create_info_field(self, parent: tk.Frame, key: str, label: str, row: int, column: int) -> None:
        """
        Cria um campo de informação responsivo.
        
        Args:
            parent (tk.Frame): Frame pai
            key (str): Chave da informação
            label (str): Rótulo do campo
            row (int): Posição da linha
            column (int): Posição da coluna
        """
        field_frame = tk.Frame(parent, bg="white", relief=tk.FLAT, bd=1)
        field_frame.grid(row=row, column=column, sticky="nsew", padx=10, pady=8)
        field_frame.grid_columnconfigure(0, weight=1)
        
        # Label
        label_widget = tk.Label(
            field_frame,
            text=f"{label}:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg=self.header_color,
            anchor="w"
        )
        label_widget.pack(fill=tk.X, padx=12, pady=(10, 2))
        
        # Value Label (será atualizado) - com wraplength responsivo
        value_label = tk.Label(
            field_frame,
            text="Carregando...",
            font=("Arial", 10),
            bg="white",
            fg="#555555",
            anchor="w",
            wraplength=360,
            justify=tk.LEFT
        )
        value_label.pack(fill=tk.X, padx=12, pady=(2, 12))
        
        # Armazenar referência
        self.info_labels[key] = value_label

    def on_collect_clicked(self) -> None:
        """Executado quando o botão 'Coletar' é clicado."""
        # Desabilitar botão durante coleta
        self.root.after(0, self.disable_collect_button)
        
        # Executar em thread separada para não travar a UI
        thread = threading.Thread(target=self.collect_hardware_info)
        thread.daemon = True
        thread.start()

    def collect_hardware_info(self) -> None:
        """Coleta informações de hardware em thread separada."""
        try:
            self.data = self.collector.collect_all()
            
            # Atualizar UI na thread principal
            self.root.after(0, self.update_ui)
            self.root.after(0, self.enable_collect_button)
            
        except Exception as e:
            logger.error(f"Erro ao coletar informações: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror(
                "Erro",
                f"Erro ao coletar informações: {str(e)}"
            ))
            self.root.after(0, self.enable_collect_button)

    def update_ui(self) -> None:
        """Atualiza a interface com os dados coletados."""
        for key, value in self.data.items():
            if key in self.info_labels:
                self.info_labels[key].config(text=str(value))

    def disable_collect_button(self) -> None:
        """Desabilita o botão de coleta."""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button) and "Coletar" in child.cget("text"):
                        child.config(state=tk.DISABLED)

    def enable_collect_button(self) -> None:
        """Habilita o botão de coleta."""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button) and "Coletar" in child.cget("text"):
                        child.config(state=tk.NORMAL)

    def on_export_txt_clicked(self) -> None:
        """Executado quando o botão 'Exportar TXT' é clicado."""
        if not self.data:
            messagebox.showwarning(
                "Aviso",
                "Nenhum dado coletado. Clique em 'Coletar Informações' primeiro."
            )
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de Texto", "*.txt"), ("Todos os arquivos", "*.*")],
            initialfile="hardware_info.txt"
        )
        
        if file_path:
            if export_to_txt(self.data, file_path):
                messagebox.showinfo("Sucesso", f"Arquivo exportado com sucesso:\n{file_path}")
            else:
                messagebox.showerror("Erro", "Erro ao exportar arquivo TXT.")

    def on_export_pdf_clicked(self) -> None:
        """Executado quando o botão 'Exportar PDF' é clicado."""
        if not self.data:
            messagebox.showwarning(
                "Aviso",
                "Nenhum dado coletado. Clique em 'Coletar Informações' primeiro."
            )
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivo PDF", "*.pdf"), ("Todos os arquivos", "*.*")],
            initialfile="hardware_info.pdf"
        )
        
        if file_path:
            if export_to_pdf(self.data, file_path):
                messagebox.showinfo("Sucesso", f"Arquivo exportado com sucesso:\n{file_path}")
            else:
                messagebox.showerror(
                    "Erro",
                    "Erro ao exportar arquivo PDF.\n"
                    "Verifique se a biblioteca 'reportlab' está instalada."
                )

    def run(self) -> None:
        """Executa a aplicação."""
        self.root.mainloop()
