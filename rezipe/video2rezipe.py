import os
import time
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active.

    Some files uploaded to the Gemini API need to be processed before they can be
    used as prompt inputs. The status can be seen by querying the file's "state"
    field.

    This implementation uses a simple blocking polling loop. Production code
    should probably employ a more sophisticated approach.
    """
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

def video_to_recipe(video_path: str, metadata: dict) -> str:
    """Convert a cooking video to a markdown recipe format.
    
    Args:
        video_path: Path to the video file
        metadata: Dictionary containing:
            - source_url: URL of the original video
            - author: Creator of the video
            - title: Title of the recipe
            - description: Description of the recipe
            - comments: Additional comments/notes
            - thumbnail: URL of the video thumbnail
    
    Returns:
        str: Generated markdown recipe content
    """
    # Validate metadata
    required_fields = ['source_url', 'author', 'title', 'description', 'comments', 'thumbnail']
    if not all(field in metadata for field in required_fields):
        raise ValueError(f"Metadata must contain all fields: {required_fields}")

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-thinking-exp-1219",
        generation_config=generation_config,
        system_instruction="This project contains markdown of reproducable recipe  \n- obsidian markdown\n- add mermaid diagram for pipelining split into parallel line, \n  - node is set of ingredients\n  - frame(group of node and edge) is active session(cooking actively no wait) and the duration \n  - edge is process() and details \n- use metric, prefer weight over volume, but no implicit convertion, must mention original unit in parenthesis\n- use English or Thai, if not these 2 language, add the original language in paralethesis\n- don't put video timestamp in \n- also elabrate thought process for the recipe \n- add key success using callout\n- add credit/reference to the original recipe \n\n# Extract tips\n## for short\nfor a video/short, in shorts, also focus on visual to extract missing/skip tips",
    )

    # Upload and process video
    files = [upload_to_gemini(video_path, mime_type="video/mp4")]
    wait_for_files_active(files)

    # Start chat session with context
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [files[0]],
            },
        ]
    )

    # Generate recipe with metadata context
    prompt = f"""Create a recipe based on this video with the following information:
Title: {metadata['title']}
Author: {metadata['author']}
Date: {metadata['date']}
Description: {metadata['description']}
Additional Notes: {metadata['comments']}
Source: {metadata['source_url']}
Thumbnail: {metadata['thumbnail']}

Please include the thumbnail at the beginning of the markdown using this format:
![{metadata['title']}]({metadata['thumbnail']})
"""

    response = chat_session.send_message(prompt)
    
    # Create output directory if it doesn't exist
    output_dir = Path("recipes")
    output_dir.mkdir(exist_ok=True)
    
    # Create sanitized filename from title
    safe_title = "".join(c for c in metadata['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_title = safe_title.replace(' ', '-').lower()
    output_path = output_dir / f"{safe_title}.md"
    
    # Write the markdown content
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    return response.text

if __name__ == "__main__":
    # Example usage
    metadata = {
        "source_url": "https://example.com/video",
        "author": "Chef Name",
        "title": "Recipe Title",
        "description": "Recipe Description",
        "comments": "Additional notes about the recipe",
        "thumbnail": "https://example.com/thumbnail.jpg"
    }
    recipe_content = video_to_recipe("video.mp4", metadata)
