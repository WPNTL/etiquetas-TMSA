# PDF para Etiquetas

Conversor de arquivos **PDF** para imagens de **etiquetas** personalizadas em **PNG**.

Este projeto é uma **recriação em Python** do sistema original escrito em **Pascal/Lazarus** por [@guaracy](https://github.com/guaracy).

---

## ✨ Funcionalidades

- Converte PDF para texto usando **pdftotext** (Poppler).
- Gera etiquetas personalizadas em formato **PNG**.
- Interface gráfica minimalista em **Tkinter**.
- Preview integrado das etiquetas geradas.
- Botão **Excluir Imagens**: remove todas as etiquetas geradas.
- **Novo:** Botão **Salvar Imagens** → permite escolher a pasta de destino para salvar as etiquetas.
  - Após salvar, aparece um **popup de confirmação** informando a quantidade total de etiquetas geradas.
  - O diretório escolhido passa a ser usado como base para **pré-visualização** e **exclusão**.

---

## 🖼️ Layout das Etiquetas

- Inclui **logo da empresa** (`projelmec.png`) no topo.
- Bordas, título em destaque, e informações de produto/cliente/OS.
- Rodapé com dados de **Matriz**, **Filial** e **Website**.

---

## ⚙️ Requisitos

- Python 3.8+
- Dependências Python:
  - `tkinter`
  - `Pillow`
- `pdftotext` (parte do **Poppler**):
  - Linux (Ubuntu/Debian): `sudo apt-get install poppler-utils`
  - Windows: [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)

---

## 🚀 Como Usar

1. Clone este repositório ou baixe os arquivos.
2. Coloque o arquivo `projelmec.png` no mesmo diretório do script (ou junto ao PDF).
3. Execute o programa:

   ```bash
   python3 pdf2etiqueta.py
   ```

4. Clique em **Processar PDF** e selecione o arquivo desejado.
5. Visualize as etiquetas na interface.
6. Clique em **Salvar Imagens** para escolher o diretório de destino.
   - Após salvar, aparecerá uma mensagem:
     ```
     Imagens salvas com sucesso: 148 etiquetas geradas
     ```

---

## 📂 Estrutura de Arquivos

```
pdf2etiqueta.py       # Código principal
README.md             # Este arquivo
projelmec.png         # Logo (necessário para as etiquetas)
```

---

## 📝 Créditos

- Sistema original desenvolvido em **Pascal/Lazarus** por [@guaracy](https://github.com/guaracy).  
- Versão em **Python/Tkinter** adaptada e expandida com novas funcionalidades.

---

## 📜 Licença

Distribuído sob a licença MIT. Consulte `LICENSE` para mais informações.
