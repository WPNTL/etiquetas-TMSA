#!/usr/bin/env python3
"""
PDF para Etiquetas - Conversor de PDF para imagens de etiquetas
Versão Python do programa original em Pascal/Lazarus

Funcionalidades:
- Converte PDF para texto usando pdftotext
- Gera etiquetas personalizadas em formato PNG
- Interface gráfica minimalista com Tkinter
- Remove dependência da fonte Antonio-Bold

Baseado no sistema original de [@guaracy](https://github.com/guaracy)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
from PIL import Image, ImageDraw, ImageFont
import time
from shutil import move

class PDFToEtiquetaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF para Etiquetas")
        self.root.geometry("800x600")

        self.total_etiquetas = 0
        self.base_dir = ""
        self.etiquetas_list = []

        self.setup_ui()
        self.check_pdftotext()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(2, weight=1)

        ttk.Button(main_frame, text="Processar PDF", 
                  command=self.processar_pdf).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        ttk.Button(main_frame, text="Excluir Imagens", 
                  command=self.excluir_imagens).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Button(main_frame, text="Salvar Imagens", 
                  command=self.salvar_imagens).grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)

        list_frame = ttk.LabelFrame(content_frame, text="Etiquetas Geradas", padding="5")
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        self.listbox = tk.Listbox(list_frame, width=30)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)

        self.listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.listbox.bind('<<ListboxSelect>>', self.on_select_etiqueta)

        preview_frame = ttk.LabelFrame(content_frame, text="Preview da Etiqueta", padding="5")
        preview_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.preview_label = ttk.Label(preview_frame, text="Selecione uma etiqueta para visualizar")
        self.preview_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

    def check_pdftotext(self):
        try:
            subprocess.run(['pdftotext', '-v'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showwarning(
                "Aviso", 
                "pdftotext não encontrado. Instale o poppler-utils:\n"
                "Ubuntu/Debian: sudo apt-get install poppler-utils\n"
                "Windows: Baixe do https://github.com/oschwartz10612/poppler-windows/releases"
            )

    def processar_pdf(self):
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )

        if not filename:
            return

        self.status_var.set(f"Processando: {os.path.basename(filename)}")
        self.root.update()

        self.base_dir = os.path.dirname(filename)
        start_time = time.time()

        try:
            self.gerar_etiquetas(filename)
            elapsed_time = time.time() - start_time
            self.status_var.set(f"{self.total_etiquetas} Etiquetas em {elapsed_time:.2f}s (aguardando salvar)")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar PDF: {str(e)}")
            self.status_var.set("Erro no processamento")

    def pdf_to_text(self, filename):
        try:
            subprocess.run(['pdftotext', '-fixed', '800', filename],
                           capture_output=True, text=True, check=True)
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            return txt_filename if os.path.exists(txt_filename) else None
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erro ao converter PDF: {e}")

    def gerar_etiquetas(self, pdf_filename):
        txt_filename = self.pdf_to_text(pdf_filename)
        if not txt_filename or not os.path.exists(txt_filename):
            raise Exception("Arquivo não pode ser processado pelo pdftotext")

        with open(txt_filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        pages = content.split('\x0c')

        self.total_etiquetas = 0
        self.listbox.delete(0, tk.END)
        self.etiquetas_list.clear()

        for page in pages:
            lines = [ln for ln in page.splitlines()]
            while lines and not lines[0].strip():
                lines.pop(0)
            while lines and not lines[-1].strip():
                lines.pop()
            if not lines:
                continue

            etiqueta = self.extrair_dados_etiqueta(lines)
            if etiqueta:
                try:
                    self.criar_imagem_etiqueta(etiqueta)
                    self.etiquetas_list.append(etiqueta)
                    self.listbox.insert(tk.END, etiqueta['os'])
                    self.total_etiquetas += 1
                    self.root.update()
                except Exception as e:
                    print(f"Erro ao criar imagem da etiqueta: {e}")
                    continue

    def extrair_dados_etiqueta(self, page_lines):
        if not page_lines:
            return None
        try:
            titulo = page_lines[0].strip()
            codigo = ""
            cod_cliente = "Cód.Cliente:"
            os_item = ""

            for i in range(1, len(page_lines)):
                linha = page_lines[i].strip()
                if not linha:
                    continue
                if linha.startswith("Cód.:"):
                    codigo = linha
                elif linha.startswith("Cód.Cliente:"):
                    cod_cliente = linha
                elif linha.startswith("O.S./Item:"):
                    found = ""
                    for j in range(i+1, len(page_lines)):
                        prox = page_lines[j].strip()
                        if prox and not prox.startswith(("Matriz:", "Filial:", "www.")):
                            found = prox
                            break
                    if found:
                        os_item = found
                    else:
                        os_item = linha.replace("O.S./Item:", "").strip()
                    break

            if not codigo:
                codigo = "Cód.: N/A"
            if not os_item:
                os_item = f"OS{self.total_etiquetas + 1:03d}/001"

            return {
                'titulo': titulo,
                'codigo': codigo,
                'codcli': cod_cliente,
                'os': os_item
            }
        except Exception as e:
            print(f"Erro ao extrair dados: {e}")
            return None

    def criar_imagem_etiqueta(self, etiqueta):
        width, height = 640, 400
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)

        try:
            font_title = ImageFont.truetype("arialbd.ttf", 30)
            font_large = ImageFont.truetype("arialbd.ttf", 22)
            font_medium = ImageFont.truetype("arial.ttf", 18)
            font_small = ImageFont.truetype("arial.ttf", 14)
            font_website = ImageFont.truetype("arialbd.ttf", 16)
        except Exception:
            font_title = font_large = font_medium = font_small = font_website = ImageFont.load_default()

        draw.rectangle([5, 5, width-5, height-5], outline='black', width=2)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        possible_logo_paths = [
            os.path.join(script_dir, 'projelmec.png'),
            os.path.join(os.getcwd(), 'projelmec.png'),
            'projelmec.png',
            os.path.join(self.base_dir, 'projelmec.png'),
        ]
        for logo_path in possible_logo_paths:
            if os.path.exists(logo_path):
                try:
                    logo = Image.open(logo_path).convert("RGBA")
                    logo = logo.resize((320, 93), Image.Resampling.LANCZOS)
                    logo_x = (width - 320) // 2
                    img.paste(logo, (logo_x, 15), logo if logo.mode == "RGBA" else None)
                    break
                except Exception as e:
                    print(f"Erro ao carregar logo de {logo_path}: {e}")
                    continue

        y_pos = 120
        margin = 25

        draw.text((margin, y_pos), etiqueta['titulo'], fill='black', font=font_title)
        y_pos += 45

        draw.text((margin, y_pos), etiqueta['codigo'], fill='black', font=font_medium)
        try:
            codcli_width = draw.textlength(etiqueta['codcli'], font=font_medium)
            codcli_x = width - margin - codcli_width
        except Exception:
            codcli_x = width // 2
        draw.text((codcli_x, y_pos), etiqueta['codcli'], fill='black', font=font_medium)
        y_pos += 30

        os_text = f"O.S./Item: {etiqueta['os']}"
        draw.text((margin, y_pos), os_text, fill='black', font=font_medium)

        matriz_text = "Matriz: Sapucaia do Sul/RS (51)3451.5100"
        filial_text = "Filial: São Paulo/SP (11)5571.6329"
        website_text = "www.projelmec.com.br"

        bottom_y = height - 60
        draw.text((margin, bottom_y), matriz_text, fill='black', font=font_small)

        try:
            filial_width = draw.textlength(filial_text, font=font_small)
            filial_x = width - filial_width - margin
        except Exception:
            filial_x = width - 300
        draw.text((filial_x, bottom_y), filial_text, fill='black', font=font_small)

        website_y = height - 25
        try:
            website_width = draw.textlength(website_text, font=font_website)
            website_x = (width - website_width) // 2
        except Exception:
            website_x = width // 2 - 100
        draw.text((website_x, website_y), website_text, fill='black', font=font_website)

        safe_filename = "".join(c for c in etiqueta['os'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        if not safe_filename:
            safe_filename = f"etiqueta_{self.total_etiquetas + 1}"
        filename = os.path.join(self.base_dir, f"{safe_filename}.png")
        img.save(filename)

    def salvar_imagens(self):
        if not self.etiquetas_list:
            messagebox.showinfo("Info", "Nenhuma etiqueta para salvar")
            return

        destino = filedialog.askdirectory(title="Selecionar pasta para salvar as etiquetas")
        if not destino:
            return

        try:
            os.makedirs(destino, exist_ok=True)
            for etiqueta in self.etiquetas_list:
                safe_filename = "".join(c for c in etiqueta['os'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                if not safe_filename:
                    safe_filename = f"etiqueta_{self.total_etiquetas + 1}"
                origem = os.path.join(self.base_dir, f"{safe_filename}.png")
                destino_arquivo = os.path.join(destino, f"{safe_filename}.png")
                if os.path.exists(origem):
                    move(origem, destino_arquivo)

            messagebox.showinfo("Sucesso", f"Imagens salvas com sucesso: {self.total_etiquetas} etiquetas geradas")
            self.status_var.set(f"{self.total_etiquetas} imagens salvas em {destino}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar imagens: {e}")

    def on_select_etiqueta(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if index < len(self.etiquetas_list):
            etiqueta = self.etiquetas_list[index]
            safe_filename = "".join(c for c in etiqueta['os'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = os.path.join(self.base_dir, f"{safe_filename}.png")
            if os.path.exists(filename):
                try:
                    img = Image.open(filename)
                    img.thumbnail((400, 250), Image.Resampling.LANCZOS)
                    from PIL import ImageTk
                    photo = ImageTk.PhotoImage(img)
                    self.preview_label.configure(image=photo, text="")
                    self.preview_label.image = photo
                except Exception as e:
                    self.preview_label.configure(image="", text=f"Erro ao carregar imagem: {e}")

    def excluir_imagens(self):
        if not self.etiquetas_list:
            messagebox.showinfo("Info", "Nenhuma etiqueta para excluir")
            return
        result = messagebox.askyesno("Confirmar", "Deseja apagar todas as imagens deste diretório?")
        if result:
            try:
                for etiqueta in self.etiquetas_list:
                    safe_filename = "".join(c for c in etiqueta['os'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    filename = os.path.join(self.base_dir, f"{safe_filename}.png")
                    if os.path.exists(filename):
                        os.remove(filename)
                self.listbox.delete(0, tk.END)
                self.etiquetas_list.clear()
                self.preview_label.configure(image="", text="Selecione uma etiqueta para visualizar")
                self.status_var.set("Imagens excluídas")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir imagens: {e}")

def main():
    root = tk.Tk()
    app = PDFToEtiquetaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
