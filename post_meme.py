import tweepy
import os
import requests
from dotenv import load_dotenv
from memegen import create_meme

load_dotenv()

# Twitter API credentials
API_KEY = os.getenv("API_KEY2")
API_KEY_SECRET = os.getenv("API_KEY_SECRET2")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN2")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET2")
BEARER_TOKEN = os.getenv("BEARER_TOKEN2") 

client = tweepy.Client(bearer_token=BEARER_TOKEN, 
                       consumer_key=API_KEY,
                       consumer_secret=API_KEY_SECRET,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET)

def post_tweet_with_online_image(content, image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        
        from io import BytesIO
        image_file = BytesIO(response.content)
        image_file.name = "temp_image.jpg"  
        auth = tweepy.OAuth1UserHandler(
            consumer_key=API_KEY,
            consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET,
        )
        api = tweepy.API(auth)
        media = api.media_upload(filename=image_file.name, file=image_file)
        
        response = client.create_tweet(text=content, media_ids=[media.media_id])
        print(f"Tweet with image posted successfully! Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"Error posting tweet with online image: {e}")


if __name__ == "__main__":

    topics = ["supra", "Cross-chain transactions", "speed", "security", "interoperability"]
    audience = "Crypto enthusiasts, developers, blockchain professionals"
    image_path = create_meme(topics, audience)
    print("Image path:", image_path)
    post_tweet_with_online_image("", image_path)