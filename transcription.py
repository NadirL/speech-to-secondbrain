from openai import OpenAI
import os
from prompts import GPT4O_MINI_PROMPT
from prompts import tag_generation_prompt
from prompts import filename_generation_prompt

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
print(f"[DEBUG] Using API key: {api_key[:10]}...{api_key[-5:]}")
client = OpenAI(api_key=api_key) 

def transcribe_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription.text

def process_with_gpt4o_mini(transcript):
    prompt = f"{GPT4O_MINI_PROMPT}\n\n{transcript}"
    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=15000
    )
    return response.choices[0].message.content

def generate_name(transcript):
    prompt = f"{filename_generation_prompt}\n\n{transcript}"
    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content

def generate_tags(transcript):
    prompt = f"{tag_generation_prompt}\n\n{transcript}"
    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content

def save_as_markdown(content, output_path, filename):
    md_filename = os.path.splitext(filename)[0] + ".md"
    full_path = os.path.join(output_path, md_filename)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return full_path
