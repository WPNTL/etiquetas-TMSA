# PDF para Etiquetas - Versão Python

Este programa é uma recriação em Python do sistema original desenvolvido em Pascal/Lazarus por [@guaracy](https://github.com/guaracy).  
A versão em Python mantém a ideia original, mas moderniza a interface e melhora a portabilidade.

## Funcionalidades

- **Conversão PDF para Texto**: Utiliza o `pdftotext` para extrair texto de arquivos PDF
- **Geração de Etiquetas**: Cria imagens PNG personalizadas com as informações extraídas
- **Interface Gráfica Minimalista**: Interface intuitiva desenvolvida com Tkinter
- **Preview de Etiquetas**: Visualização das etiquetas geradas
- **Gerenciamento de Arquivos**: Funcionalidade para excluir imagens geradas

## Principais Melhorias em Relação à Versão Pascal

### ✅ Remoção da Dependência de Fonte
- **Problema Original**: Necessitava instalação da fonte Antonio-Bold
- **Solução**: Utiliza fontes padrão do Windows (Arial, Arial Bold)
- **Fallback**: Fonte padrão do sistema caso as fontes específicas não estejam disponíveis

### ✅ Interface Modernizada
- Layout responsivo com frames organizados
- Lista de etiquetas com scrollbar
- Preview em tempo real das etiquetas
- Barra de status informativa

### ✅ Tratamento de Erros Robusto
- Validação de arquivos PDF
- Tratamento de caracteres especiais em nomes de arquivo
- Mensagens de erro informativas

### ✅ Parsing Aprimorado
- Agora o processamento é feito **página a página**, evitando erros causados por `\x0c` (formfeed)
- Extração mais confiável de título, código, cliente e número da O.S.

## Requisitos do Sistema

### Dependências Python
```bash
pip install pillow
```

### Dependências do Sistema
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt-get install python3-tk poppler-utils
  ```

- **Windows**:
  - Python 3.x com Tkinter (geralmente incluído)
  - Poppler for Windows: https://github.com/oschwartz10612/poppler-windows/releases

## Como Usar

1. **Executar o Programa**:
   ```bash
   python3 pdf2etiqueta.py
   ```

2. **Processar PDF**:
   - Clique em "Processar PDF"
   - Selecione o arquivo PDF desejado
   - Aguarde o processamento

3. **Visualizar Etiquetas**:
   - As etiquetas aparecerão na lista à esquerda
   - Clique em uma etiqueta para ver o preview

4. **Gerenciar Arquivos**:
   - Use "Excluir Imagens" para remover todas as etiquetas geradas

## Estrutura das Etiquetas

Cada etiqueta contém:
- **Logo da Empresa** (se disponível)
- **Título do Produto/Serviço**
- **Código do Produto**
- **Código do Cliente**
- **Número da O.S./Item**
- **Informações da Empresa**:
  - Matriz: Sapucaia do Sul/RS (51)3451.5100
  - Filial: São Paulo/SP (11)5571.6329
  - Website: www.projelmec.com.br

## Arquivos de Saída

- **Formato**: PNG (640x400 pixels)
- **Nomenclatura**: Baseada no número da O.S.
- **Localização**: Mesmo diretório do PDF original

## Diferenças da Versão Original

| Aspecto | Original (Pascal/Lazarus) | Nova Versão (Python/Tkinter) |
|---------|---------------------------|------------------------------|
| **Fonte** | Antonio-Bold (instalação obrigatória) | Arial/Arial Bold (padrão Windows) |
| **Interface** | Lazarus/LCL | Tkinter (nativo Python) |
| **Dependências** | Poppler + Fonte específica | Poppler + PIL |
| **Portabilidade** | Windows/Linux com dependências | Multiplataforma |
| **Manutenção** | Compilação necessária | Script Python direto |

## Créditos

- **Autor original**: [@guaracy](https://github.com/guaracy), criador da versão em Pascal/Lazarus.  
- **Versão em Python**: Adaptação e melhorias para portabilidade, interface gráfica e robustez no parsing de PDFs.

## Licença

Este programa é baseado na versão original de [@guaracy](https://github.com/guaracy) e distribuído de forma aberta para uso e adaptação.
