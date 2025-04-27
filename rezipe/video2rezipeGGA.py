from google import genai
import os
import time

# Initialize the client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    with open(path, 'rb') as f:
        file = client.files.upload(
            display_name=os.path.basename(path),
            file=f,
            mime_type=mime_type
        )
    print(f"Uploaded file '{file.display_name}' as: {file.name}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = client.files.get(name)
        while file.state == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = client.files.get(name)
        if file.state != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

# Create generation config
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

# System instruction for the model
system_instruction = """This project contains markdown of reproducable recipe  
- obsidian markdown
- add mermaid diagram for pipelining split into parallel line, 
  - node is set of ingredients
  - frame(group of node and edge) is active session(cooking actively no wait) and the duration 
  - edge is process() and details 
- use metric, prefer weight over volume, but no implicit convertion, must mention original unit in parenthesis
- use English or Thai, if not these 2 language, add the original language in paralethesis
- don't put video timestamp in 
- also elabrate thought process for the recipe 
- add key success using callout
- add credit/reference to the original recipe 

# Extract tips
## for short
for a video/short, in shorts, also focus on visual to extract missing/skip tips"""

# Upload files
files = [
    upload_to_gemini("joke.mp4", mime_type="video/mp4"),
]

# Wait for files to be processed
wait_for_files_active(files)

# Create chat
chat = client.chats.create(
    model='gemini-1.5-pro',
    config=genai.types.GenerateContentConfig(
        temperature=generation_config["temperature"],
        top_p=generation_config["top_p"],
        top_k=generation_config["top_k"],
        max_output_tokens=generation_config["max_output_tokens"],
        system_instruction=system_instruction,
    )
)

# Send initial messages
response = chat.send_message(files[0])
response = chat.send_message("create recipe for this")

print(response.text)