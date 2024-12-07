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

class SupraScraper:
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

    def scrape_supra_blogs(self, params, context):
        keywords = params.get('keywords', [])
        num_pages = int(params.get('num_pages', 1))

        response = requests.get(f'https://supra.com/news/')

        with open('response_content.html', 'wb') as file:
            file.write(response.content)
        bs = BeautifulSoup(response.text, "html.parser")
        script_tag = bs.find('script', {'id': '__NEXT_DATA__'})
        json_data = script_tag.string.strip()
        data = json.loads(json_data)
        # print(data)

        posts = data["props"]["pageProps"]["posts"]
        
        title_link_dict = {}
        base_url = "https://supra.com/news/"

        for post in posts:
            node = post["node"]
            title = node["title"]
            slug = node["slug"]
            blog_url = f"{base_url}{slug}"
            title_link_dict[title] = blog_url

        return title_link_dict

    def summarize_blogs(self, blog_url):
        response = requests.get(blog_url)
        bs = BeautifulSoup(response.text, "html.parser")

        content = []
        for tag in bs.find_all(['header', 'p', 'u']):  
            content.append(tag.get_text(strip=True))  

        article_content = "\n".join(content)
        article_content = re.sub(r"(?i)(Disclaimer:.*?)(RECENT POSTS.*|©2024Supra.*|$)", "", article_content, flags=re.DOTALL)
        # article_content = "Read more: ".join(blog_url)

        article_content = article_content.strip()
        # print(article_content)

        prompt = f'Summarize this article in technical terms, talking about the technical things and not more general talk as if explaining someone over twitter without them needing to know about the article. do not add words like \'summary\' \'article\', \'key takeways\', \'Twitter\', \'thread\'. Start with a small sentence which talks about the new thing the article is about in an interactive way say, "Let us talk about.." and then talking about technicalities. Do not add any hash tags, create it in a form that can be added as twitter thread of 5 tweets but each tweet is strictly less than 35 words and starts with 1/6 and so on and has technical information rather than addressing the reader. in the last tweets talk about how the technology can be leveraged more and any neutral unbiased conclusion the blog on a whole delivers: {article_content}'
        # req_url = f'http://195.179.229.119/gpt/api.php?prompt={requests.utils.quote(prompt)}&api_key={requests.utils.quote(api_key)}&model={requests.utils.quote(model)}'
       
        # response = requests.get(req_url)
        # print(response.text)
        # response.raise_for_status()  
        # summary = response.json()


        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        # print(response)

        # message = client.messages.create(
        #     model="claude-3-5-sonnet-20241022",
        #     max_tokens=200,
        #     temperature=0,
        #     system="Supra is a Layer 1 (L1) blockchain network that acts as a cross-chain protocol to allow different blockchain ecosystems to interact with each other. It is designed to help developers build on a single chain and create new types of dApps. You are responsible for onboarding more developers and users to Supra and deliver information and education about Supra over twitter, making their social presence nice",
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": [
        #                 {
        #                     "type": "text",
        #                     "text": prompt
        #                 }
        #             ]
        #         }
        #     ]
        # )
        # print(message.content)
        
        summary = response.choices[0].message.content
        # summary = f"{summary}\n\nRead more: {blog_url}"
        print(summary)
        return summary

    def post_tweet(self, content, url):
        # content = "1/1 abc\n\n2/2 big\n\n3/3 cat"
        tweets = self.split_into_tweets(content)
        tweets.append(f"Read more: {url}")
        first_tweet = self.client.create_tweet(text=tweets[0])
        previous_tweet_id = first_tweet.data['id']
        # second_tweet = self.client.create_tweet(text=tweets[1], in_reply_to_tweet_id=previous_tweet_id)
        for tweet_text in tweets[1:]:
            tweet = self.client.create_tweet(text=tweet_text, in_reply_to_tweet_id=previous_tweet_id)
            print(f"Tweet posted: {tweet.data['id']}")
            previous_tweet_id = tweet.data['id']
            # response = self.client.create_tweet(text=content)
        print("Tweeted successfully")
        # try:
            # first_tweet = self.client.create_tweet(text=tweets[0])
            # previous_tweet_id = first_tweet.data['id']
            # # second_tweet = self.client.create_tweet(text=tweets[1], in_reply_to_tweet_id=previous_tweet_id)
            # for tweet_text in tweets[1:]:
            #     tweet = self.client.create_tweet(text=tweet_text, in_reply_to_tweet_id=previous_tweet_id)
            #     print(f"Tweet posted: {tweet.data['id']}")
            #     previous_tweet_id = tweet.data['id']
            # # response = self.client.create_tweet(text=content)
            # print("Tweeted successfully")
        # except Exception as e:
        #     print("Error in Tweeting: ", e)

    def save_processed_url(self, url):
        with open(self.processed_file, "a") as file:
            file.write(f"{url}\n")
    
    def is_processed(self, url):
        if not os.path.exists(self.processed_file):
            return False  # No processed file yet
        with open(self.processed_file, "r") as file:
            return url in file.read()

    def process_and_tweet_blogs(self):
        params = {
            'keywords': ['supra'],
            'num_pages': 1  
        }
        blogs = self.scrape_supra_blogs(params, {})
        flag=0
        for title, url in blogs.items():
            if not self.is_processed(url):
                summary = self.summarize_blogs(url)
                self.post_tweet(summary, url)
                self.save_processed_url(url)
                flag=1
            if flag==1:
                break

    def split_into_tweets(self, text, char_limit=280):

        # tweets = text.split('\n')
        sections = re.split(r'(?=\d+/\d+)', text.strip())
        tweets = []

        for section in sections:
            section = section.strip()
            if section:
                tweets.append(section)
        
        # current_tweet = ""
        prompt=f"Refactor the content to fit the character limit of 250 by shortening the tweet without chaning the meaning or important details. {tweets[0]}"
        for i, tweet in enumerate(tweets):
            if len(tweet) > char_limit :
                prompt=f"Refactor the content to fit the character limit of 250 by shortening the tweet without chaning the meaning or important details. {tweets[0]}"
                res = openai.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000
                )
                tweets[i] = res.choices[0].message.content
            
        if tweets:
            tweets[0] = f"{tweets[0]} 🧵"

        print(tweets)

        return tweets

    def announcements(self, params, context):
        pass

    def replies(self, params, context):
        pass


if __name__ == "__main__": 
    scraper = SupraScraper()
    scraper.process_and_tweet_blogs()

# import requests
# import json
# from openai import OpenAI
# import re
# from bs4 import BeautifulSoup
# from os import getenv      
# import tweepy
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Twitter API credentials
# API_KEY = os.getenv("API_KEY")
# API_KEY_SECRET = os.getenv("API_KEY_SECRET")
# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
# BEARER_TOKEN = os.getenv("BEARER_TOKEN")  # v2 API requires a Bearer Token

# model = "meta-llama/llama-3.2-3b-instruct:free"
# processed_file = "processed_blogs.txt"
# openai = OpenAI(
#     base_url=getenv("OPENROUTER_BASE_URL"),
#     api_key=getenv("OPENROUTER_API_KEY"),
# )

# # Authenticate with the v2 API
# client = tweepy.Client(bearer_token=BEARER_TOKEN, 
#                        consumer_key=API_KEY,
#                        consumer_secret=API_KEY_SECRET,
#                        access_token=ACCESS_TOKEN,
#                        access_token_secret=ACCESS_TOKEN_SECRET)

# def summarize_blogs( blog_url):
#     response = requests.get(blog_url)
#     bs = BeautifulSoup(response.text, "html.parser")

#     content = []
#     for tag in bs.find_all(['header', 'p', 'u']):  
#         content.append(tag.get_text(strip=True))  

#     article_content = "\n".join(content)
#     article_content = re.sub(r"(?i)(Disclaimer:.*?)(RECENT POSTS.*|©2024Supra.*|$)", "", article_content, flags=re.DOTALL)
#     # article_content = "Read more: ".join(blog_url)

#     article_content = article_content.strip()
#     prompt = f'Summarize this article in technical terms, talking about the technical things and not more general talk as if explaining someone over twitter without them needing to know about the article. do not add words like \'summary\' \'article\', \'key takeways\'. Start with a small sentence which talks about the new thing the article is about in an interactive way say, "Let us talk about.." and then talking about technicalities: {article_content}'
#         # req_url = f'http://195.179.229.119/gpt/api.php?prompt={requests.utils.quote(prompt)}&api_key={requests.utils.quote(api_key)}&model={requests.utils.quote(model)}'
       
#         # response = requests.get(req_url)
#         # print(response.text)
#         # response.raise_for_status()  
#         # summary = response.json()


#     response = openai.chat.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=200
#     )
#         # print(response)

#         # message = client.messages.create(
#         #     model="claude-3-5-sonnet-20241022",
#         #     max_tokens=200,
#         #     temperature=0,
#         #     system="Supra is a Layer 1 (L1) blockchain network that acts as a cross-chain protocol to allow different blockchain ecosystems to interact with each other. It is designed to help developers build on a single chain and create new types of dApps. You are responsible for onboarding more developers and users to Supra and deliver information and education about Supra over twitter, making their social presence nice",
#         #     messages=[
#         #         {
#         #             "role": "user",
#         #             "content": [
#         #                 {
#         #                     "type": "text",
#         #                     "text": prompt
#         #                 }
#         #             ]
#         #         }
#         #     ]
#         # )
#         # print(message.content)
        
#     summary = response.choices[0].message.content
#     summary = f"{summary}\nRead more: {blog_url}"
#     print(summary)
#     return summary

# def save_processed_url(url):
#     with open(processed_file, "a") as file:
#         file.write(f"{url}\n")

# def scrape_supra_blogs():

#     response = requests.get(f'https://supra.com/news/')

#     with open('response_content.html', 'wb') as file:
#         file.write(response.content)
#     bs = BeautifulSoup(response.text, "html.parser")
#     script_tag = bs.find('script', {'id': '__NEXT_DATA__'})
#     json_data = script_tag.string.strip()
#     data = json.loads(json_data)
#         # print(data)

#     posts = data["props"]["pageProps"]["posts"]
        
#     title_link_dict = {}
#     base_url = "https://supra.com/news/"

#     for post in posts:
#         print("***************\n")
#         print(post)
#         node = post["node"]
#         title = node["title"]
#         slug = node["slug"]
#         blog_url = f"{base_url}{slug}"
#         title_link_dict[title] = blog_url

#     return title_link_dict

# def is_processed(url):
#     if not os.path.exists("processed_blogs.txt"):
#         return False  # No processed file yet
#     with open("processed_blogs.txt", "r") as file:
#         return url in file.read()

# def post_tweet(content):
#     try:
#         response = client.create_tweet(text=content)
#         print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
#     except Exception as e:
#         print(f"Error: {e}")
        
# def process_and_tweet_blogs():
#     blogs = scrape_supra_blogs()
#     flag=0
#     for title, url in blogs.items():
#         if not is_processed(url):
#             summary = summarize_blogs(url)
#             # summary = "The quiet hum of the wind was a melody that played across the barren fields, whispering secrets to the grasses that swayed lazily in response. There was a serenity to the scene, an unspoken understanding between nature and the passage of time. Yet, as the moments ticked by, a faint tension lingered beneath the surface, as though the earth itself was waiting for something momentous to unfold. In the heart of the valley, a small, forgotten cabin stood, its wooden planks weathered by decades of rain and sun. The once-bright red paint had faded to a dull rust, and the windows, now fogged and cracked, reflected the dim light of the setting sun. The cabin had stories etched into its walls, though no one remained to tell them.It was here that Eleanor found herself on an afternoon that felt like it belonged in another era. She was a wanderer by nature, always seeking places that told stories without speaking. Her boots crunched against the gravel path as she approached the cabin, her curiosity a magnet pulling her toward the unknown. She pushed open the creaky door, its hinges groaning in protest, and stepped inside.Dust motes danced in the air, illuminated by the sunlight filtering through the cracks in the walls. The room smelled of aged wood and memories, an aroma both comforting and melancholic. On a rickety table near the window lay an old journal, its leather cover cracked with age. Eleanor hesitated for a moment before reaching out to pick it up. The journal’s pages were filled with neat, looping handwriting, each word penned with care. The entries told the tale of a man who had lived alone in the cabin, his days spent farming and his nights writing poetry by the light of an oil lamp. His words were raw and vivid, painting a picture of a life lived in solitude but not without purpose. Eleanor felt a strange kinship with the man whose words she read. She had always believed that the most profound connections were the ones formed through shared understanding, even if they spanned decades and were with someone she would never meet. As the sun dipped below the horizon, painting the sky in hues of orange and purple, Eleanor closed the journal and placed it back on the table. She lingered in the cabin a while longer, her mind swirling with thoughts and emotions she couldn’t quite name. When she finally stepped outside, the cool night air greeted her, carrying with it the scent of wildflowers. The stars above were scattered like diamonds on a velvet canvas, their brilliance a reminder of the vastness of the universe. Eleanor took a deep breath and began her journey back down the path, the journal’s words etched in her mind like an old song rediscovered. The valley returned to its silence, the cabin once again standing alone. But something intangible had changed, as though the earth itself had exhaled in relief. The stories it held were not forgotten—they were simply waiting for the right soul to uncover them."
#             post_tweet(summary)
#             save_processed_url(url)
#             flag=1
#         if flag==1:
#             break


# # Main
# if __name__ == "__main__":
#     process_and_tweet_blogs()
