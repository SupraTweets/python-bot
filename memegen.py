import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import random

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
IMGFLIP_USERNAME = os.getenv("IMGFLIP_USERNAME")
IMGFLIP_PASSWORD = os.getenv("IMGFLIP_PASSWORD")

def fetch_meme_templates():
    try:
        response = requests.get("https://api.imgflip.com/get_memes")
        response.raise_for_status()
        memes = response.json()["data"]["memes"]
        return memes
    except Exception as e:
        print(f"Error fetching meme templates: {e}")
        return []
    

def generate_meme_idea(topics, audience, template_name):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_API_KEY}"
    
    sys_prompt = (
        "You are a meme creator specializing in creating humorous, positive, and engaging content to highlight Supra's features. Focus on showcasing Supra’s strengths, such as its cross-chain capabilities, high-speed transactions, and secure infrastructure, while appealing to the given audience and template. Ensure the meme is funny, uplifting, and avoids negativity about other projects or the decentralization ecosystem. Just share a single meme\nOutput two line titled \"Top Text\": ..., \"Bottom Text\": ..."
    )
    user_prompt = f"Topics: {', '.join(topics)}\nAudience: {audience}\nTemplate: {template_name}"
    
    request_body = {
        "contents": [
            {
                "parts": [
                    {"text": f"{sys_prompt}\n\n{user_prompt}"}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, json=request_body)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Error generating meme idea: {e}")
        return ""
    
def extract_meme_text(content):
    try:
        top_text = content.split("**Top Text:**")[1].split("\n")[0].strip()
        print(top_text)
        bottom_text = content.split("**Bottom Text:**")[1].strip()
        print(bottom_text)
        return {"text0": top_text, "text1": bottom_text}
    except Exception as e:
        print(f"Error extracting meme text: {e}")
        return {"text0": "", "text1": ""}
    
def generate_meme_image(template_id, text0, text1):
    try:
        url = "https://api.imgflip.com/caption_image"
        params = {
            "template_id": template_id,
            "username": IMGFLIP_USERNAME,
            "password": IMGFLIP_PASSWORD,
            "text0": text0,
            "text1": text1,
        }
        response = requests.post(url, data=params)
        response.raise_for_status()
        return response.json()["data"]["url"]
    except Exception as e:
        print(f"Error generating meme image: {e}")
        return ""
    
def create_meme(topics, audience):
    # Fetch meme templates
    templates = fetch_meme_templates()
    if not templates:
        print("No meme templates found.")
        return

    # Select a random meme template with at most 2 text boxes
    filtered_templates = [t for t in templates if t["box_count"] <= 2]
    if not filtered_templates:
        print("No suitable meme templates found.")
        return
    
    rnd = random.randint(0, len(filtered_templates)-1)

    selected_template = filtered_templates[rnd]  # Select the first one for simplicity

    # Generate meme idea
    content = generate_meme_idea(topics, audience, selected_template["name"])
    print(content)
    if not content:
        print("Failed to generate meme idea.")
        return

    # Extract top and bottom text
    meme_text = extract_meme_text(content)
    if not meme_text["text0"] or not meme_text["text1"]:
        # print("Failed to extract meme text.")
        # return
        meme_text["text0"] = "hihi"
        meme_text["text1"] = "hehe"

    # Generate meme image
    meme_url = generate_meme_image(
        selected_template["id"], meme_text["text0"], meme_text["text1"]
    )
    if meme_url:
        print(f"Meme URL: {meme_url}")
    else:
        print("Failed to generate meme image.")

# Example usage
# print(fetch_meme_templates())
# meme_idea = generate_meme_idea(['web3', 'solana'],'college','Grim Reaper Knocking Door')
# print(extract_meme_text(meme_idea))
# if __name__ == "__main__":
topics = ["supra", "Cross-chain transactions", "speed", "security", "interoperability"]
audience = "Crypto enthusiasts, developers, blockchain professionals"
create_meme(topics, audience)