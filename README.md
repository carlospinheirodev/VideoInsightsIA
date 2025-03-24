# Video Insights - Extração e Análise de Transcrição de Vídeos do YouTube

## Visão Geral
Este projeto tem como objetivo realizar a análise de vídeos do YouTube, permitindo aos usuários extrair resumos, tópicos principais e ganchos persuasivos de uma transcrição. O processamento pode ser realizado de duas formas:

1. **Execução direta em Python**: mais rápido e eficiente;
2. **Execução via n8n**: mais flexível para integração com outras automações.

Os usuários podem fornecer a **URL do vídeo** ou a **transcrição textual** manualmente para processamento.

- Projeto N8N: https://n8n-service-qbul.onrender.com/ - por ser um servidor gratuíto (Render), o carregamento pode ser um pouco demorado.

---

## Tecnologias Utilizadas

### Bibliotecas e APIs Python
- **Transcrição de vídeo**: [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/)
- **Tradução para português**: [DeepL API](https://developers.deepl.com/docs#get-an-api-key-and-get-started)
  - Alternativa gratuita: API do Google Tradutor (qualidade inferior)
- **Gerenciamento de variáveis de ambiente**: [python-dotenv](https://pypi.org/project/python-dotenv/)
- **Análise de linguagem natural e geração de resumos**: [DeepSeek API](https://api-docs.deepseek.com/)

### Integração com n8n
- **Transcrição de vídeos alternativa**: [Kome AI](https://kome.ai/tools/youtube-transcript-generator)
  - Opção gratuita para evitar sobrecarga da API do DeepSeek.
- **Análise de linguagem natural e geração de resumos**: [DeepSeek API](https://api-docs.deepseek.com/)
---

## Estrutura do Projeto

1. **Entrada de dados**:
   - O usuário fornece uma URL do YouTube ou uma transcrição textual.

2. **Processamento**:
   - Extração da transcrição via API ou uso de entrada manual.
   - Tradução do texto para português.
   - Processamento da transcrição para extração de insights:
     - **Resumo**
     - **Tópicos centrais**
     - **Ganchos persuasivos**

3. **Saída de dados**:
   - Apresentação dos resultados de forma estruturada.

---

## Considerações Finais

O projeto fornece uma abordagem eficiente para extração automática de insights a partir de vídeos, podendo ser integrado a sistemas maiores. A abordagem Python é mais eficiente, enquanto a execução via n8n oferece flexibilidade para automações.

### Possíveis Melhorias:
- Melhorar a precisão da análise semântica dos ganchos persuasivos.
- Explorar modelos de IA mais sofisticados para sumarização e clustering.
- Ampliar o suporte para múltiplos idiomas.

---

## Como Usar

### Requisitos:
- Python 3.8+
- Bibliotecas listadas em `requirements.txt`

### Environment:
1. Criar arquivo .env
2. Inserir informações do  arquivo .env.example dentro do .env criado

### Instalação:
```bash
pip install -r requirements.txt
```

### Execução:
#### Modo Python:
```bash
python main.py
```
#### Modo n8n:
1. Configurar os webhooks no n8n.
2. Executar via automação configurada.

---

Este README documenta as principais funcionalidades e aspectos técnicos do projeto, servindo como referência para desenvolvimento e integração.

