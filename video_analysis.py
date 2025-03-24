import os
import json
import re
import deepl
import base64
import requests
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def extract_video_id(videoUrl: str):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", videoUrl)
    return match.group(1) if match else None

def videoExtraction(videoUrl: str):
    videoId = extract_video_id(videoUrl)
    if not videoId:
        return None, 'Erro: URL inválida!'

    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(videoId, languages=['pt', 'en'])
        transcription = " ".join([entry['text'] for entry in transcript_data])

        translatedText = translateText(transcription)
        if translatedText is None:
            return None, "Erro na tradução!"

        analysis = ai_text_analysis(translatedText)
        if analysis is None:
            return None, "Erro na análise de IA!"

        return analysis
    except Exception as e:
        return None, f"Erro ao obter transcrição: {str(e)}"

def translateText(text: str):
    try:
        auth_key = os.getenv('DEEPL_API_KEY')
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang="PT-BR")
        return result.text
    except Exception as e:
        print(f"Erro na tradução: {str(e)}")
        return None

def ai_text_analysis(text: str):
    user_prompt = prompt = f"""
        Você é um especialista em análise de conteúdo de vídeos do YouTube.
        Sua tarefa é processar a transcrição fornecida e extrair informações-chave.
        Siga as instruções cuidadosamente e retorne a resposta no formato JSON.

        ### Entrada (Transcrição do Vídeo)
        ```transcript
        {text}
        ```

        ### Instruções
        1. Resumo: Gere um resumo conciso do vídeo, destacando as principais ideias em no máximo 5 frases.
        2. Tópicos Principais: Extraia de 3 a 6 tópicos essenciais abordados no vídeo.
        3. Ganchos para Atrair Atenção: Identifique de 3 a 5 frases curtas e impactantes que foram usadas como chamadas para prender a atenção do público.

        ### Exemplo de Saída
        ```json
        {{
            "resumo": "O vídeo explica como obter transcrições de vídeos do YouTube com Python, usando a API oficial e Selenium.",
            "topicos": [
                "Obtenção de transcrições do YouTube",
                "Uso de Selenium para automação",
                "Exportação de transcrições para arquivos"
            ],
            "ganchos": [
                "Quer extrair qualquer transcrição do YouTube em segundos?",
                "Descubra como automatizar a obtenção de legendas de vídeos!",
                "Transforme qualquer vídeo em texto sem complicação!"
            ]
        }}
        ```

        Importante: Retorne apenas o JSON válido, sem explicações extras.
        """

    messages = [{"role": "user", "content": user_prompt}]

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            response_format={
                'type': 'json_object'
            }
        )

        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return None, f"Erro ao analisar texto: {str(e)}"

def analysis_with_n8n(video: str, type: str):
    url = "https://n8n-service-qbul.onrender.com/webhook/video-insights"
    username = os.getenv('N8N_AUTH_USER')
    password = os.getenv('N8N_AUTH_PASSWORD')

    auth_header = base64.b64encode(f"{username}:{password}".encode()).decode()

    payload = {
        "video": video,
        "type": type
    }

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("output", {})
    else:
        return {"error": f"Erro {response.status_code}: {response.text}"}
