import requests
import json
from openai import OpenAI
import re, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import getenv
import tweepy

load_dotenv()

# gets API Key from environment variables
openai = OpenAI(
    base_url=getenv("OPENROUTER_BASE_URL"),
    api_key=getenv("OPENROUTER_API_KEY"),
)

model = "meta-llama/llama-3.2-3b-instruct:free"
API_KEY = os.getenv("API_KEY2")
API_KEY_SECRET = os.getenv("API_KEY_SECRET2")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN2")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET2")
BEARER_TOKEN = os.getenv("BEARER_TOKEN2")

class SupraPoll:
    def __init__(self):
        self.processed_file = "processed_blogs.txt"  
        # self.twitter_api_key = getenv("TWITTER_API_KEY")  
        # self.twitter_api_secret = getenv("TWITTER_API_SECRET")
        # # auth = tweepy.OAuthHandler(self.twitter_api_key, self.twitter_api_secret)
        # # auth.set_access_token(getenv("TWITTER_ACCESS_TOKEN"), getenv("TWITTER_ACCESS_TOKEN_SECRET"))
        # self.client = tweepy.Client(bearer_token=getenv("TWITTER_BEARER_TOKEN"), consumer_key=self.twitter_api_key, consumer_secret=self.twitter_api_secret, access_token=getenv("TWITTER_ACCESS_TOKEN"), access_token_secret=getenv("TWITTER_ACCESS_TOKEN_SECRET"))
        self.client = tweepy.Client(bearer_token=BEARER_TOKEN, 
                       consumer_key=API_KEY,
                       consumer_secret=API_KEY_SECRET,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET)

    def poll(self):
        prompt1 = f'Generate a concise and engaging Twitter poll question for the Supra Protocol to capture user feedback and increase engagement. The question should be relevant to blockchain technology, DeFi, or Supra’s services (such as oracles, cross-chain solutions, or decentralized applications). Include 4 options for users to choose from, and ensure the tone is professional yet approachable to encourage participation. Remove response related sentences and give oly question and options'
        res = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt1}],
            max_tokens=150
        )
        res = res.choices[0].message.content
        # print(res)
        # prompt2 = f'for the given twitter poll question, provide 4 options for the poll, the response should just be the options: {question}'
        # response = openai.chat.completions.create(
        #     model=model,
        #     temperature=0.7,
        #     messages=[{"role": "user", "content": prompt2}],
        #     max_tokens=150
        # )
        # options = response.choices[0].message.content
        # print(options)
        duration_minutes = 720  # Duration for 24 hours
        parts = re.split(r'(?=\b[A-D]\))', res.strip(), maxsplit=1)
    
        if len(parts) < 2:
            raise ValueError("Poll text is not formatted correctly with options.")

        question = parts[0].strip()  
        options_text = parts[1].strip()  

        options = re.findall(r'[A-D]\)\s*(.+)', options_text)
        for i, option in enumerate(options):
            prompt=f"Shorten the option to fit the character limit of 15 letters by refactoring the option in 2-3 words or phrases only. {option}"
            res = openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4
            )
            options[i] = res.choices[0].message.content
        print(question)
        print(options)
        # Tweet the poll using the client
        poll = self.client.create_tweet(
            text=question,
            poll_options=options,
            poll_duration_minutes=duration_minutes
        )
        print("Poll posted successfully:", poll.data['text'])


if __name__ == "__main__": 
    scraper = SupraPoll()
    scraper.poll()
