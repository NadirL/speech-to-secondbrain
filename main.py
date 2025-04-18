# main.py
import os
import schedule
import time
import json
from dotenv import load_dotenv
from gdrive_utils import authenticate_gdrive, list_audio_files, download_file, move_file
from transcription import (
    transcribe_audio,
    process_with_gpt4o_mini,
    save_as_markdown,
    generate_name,
    generate_tags,
)

# Load environment variables
load_dotenv()

# Configuration
SOURCE_FOLDER_ID = os.getenv("SOURCE_FOLDER_ID")  # Folder to monitor
DESTINATION_FOLDER_ID = os.getenv("DESTINATION_FOLDER_ID")  # Folder for processed files
LOCAL_OUTPUT_FOLDER = os.getenv("LOCAL_OUTPUT_FOLDER")  # Path for .md files
TEMP_AUDIO_PATH = os.path.join(os.getcwd(), "temp_audio")

# Ensure directories exist
os.makedirs(TEMP_AUDIO_PATH, exist_ok=True)
os.makedirs(LOCAL_OUTPUT_FOLDER, exist_ok=True)

def process_new_files():
    """Checks for new audio files, processes them, and moves them to the transcribed folder."""
    print("Checking for new audio files...")
    service = authenticate_gdrive()
    files = list_audio_files(service, SOURCE_FOLDER_ID)
    
    if not files:
        print("No new audio files found.")
        return
    
    for file in files:
        file_id = file['id']
        file_name = file['name']
        print(f"Processing file: {file_name}")
        
        # Download the audio file locally
        local_audio_path = os.path.join(TEMP_AUDIO_PATH, file_name)
        download_file(service, file_id, file_name, local_audio_path)
        
        try:
            # Transcribe the audio
            transcript = transcribe_audio(local_audio_path)
            print(f"Transcription completed for {file_name}")
            
            # Process transcript with GPT-4o mini
            processed_content = process_with_gpt4o_mini(transcript)
            print(f"GPT-4o mini processing completed for {file_name}")

            # Generate AI-powered filename
            filename_json = generate_name(transcript)
            try:
                filename = json.loads(filename_json)["filename"]
            except Exception as e:
                print(f"Error parsing filename JSON: {e}")
                filename = os.path.splitext(file_name)[0]

            # Generate AI-powered tags
            tags_json = generate_tags(transcript)
            try:
                tags = json.loads(tags_json)["tags"]
            except Exception as e:
                print(f"Error parsing tags JSON: {e}")
                tags = []

            # Append tags section at the bottom of the document
            if tags:
                processed_content = f"{processed_content}\n\n## Tags\n{' '.join(tags)}"

            # Save as Markdown with AI-generated filename
            saved_path = save_as_markdown(processed_content, LOCAL_OUTPUT_FOLDER, filename)
            print(f"Saved Markdown to {saved_path}")
            
            # Move the file to the "transcribed" folder in Google Drive
            move_file(service, file_id, DESTINATION_FOLDER_ID)
            print(f"Moved {file_name} to transcribed folder")
            
            # Clean up temporary audio file
            os.remove(local_audio_path)
            print(f"Cleaned up temporary file: {local_audio_path}")
            
        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")
            continue


def run_daemon():
    """Runs the daemon to check for new files every 5 minutes."""
    schedule.every(20).seconds.do(process_new_files)
    print("Daemon started. Checking every 5 minutes...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_daemon()
