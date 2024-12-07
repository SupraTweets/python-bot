import tweepy
import os
import requests
from dotenv import load_dotenv
from memegen import create_meme

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

client = tweepy.Client(bearer_token=BEARER_TOKEN, 
                       consumer_key=API_KEY,
                       consumer_secret=API_KEY_SECRET,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET)

def post_tweet_with_online_image(content, image_url):
    """
    Post a tweet with an image downloaded from an online URL.
    
    Parameters:
    - content (str): The text content of the tweet.
    - image_url (str): URL of the image to be downloaded and posted.
    """
    try:
        # Download the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Save the image temporarily in memory
        from io import BytesIO
        image_file = BytesIO(response.content)
        image_file.name = "temp_image.jpg"  # Assign a file name for the API
        
        # Authenticate and upload the image using v1.1 API
        auth = tweepy.OAuth1UserHandler(
            consumer_key=API_KEY,
            consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET,
        )
        api = tweepy.API(auth)
        media = api.media_upload(filename=image_file.name, file=image_file)
        
        # Post the tweet with the uploaded media using v2 API
        response = client.create_tweet(text=content, media_ids=[media.media_id])
        print(f"Tweet with image posted successfully! Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"Error posting tweet with online image: {e}")

if __name__ == "__main__":
    tweet_content = ""
    topics = ["supra", "Cross-chain transactions", "speed", "security", "interoperability"]
    audience = "Crypto enthusiasts, developers, blockchain professionals"
    image_path = create_meme(topics, audience)
    print("Imgage path:", image_path)
    post_tweet_with_online_image(tweet_content, image_path)