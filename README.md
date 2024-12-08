# SupraTweets

Automating user engagement, effective communication and knowledge dissemination for protocols with the realms of AI. 

## What is it?
SupraTweets is an AI-powered Twitter bot currently tailored for the Supra Protocol, designed to revolutionize how protocols, dApps, services, and ecosystems engage with their communities. Leveraging cutting-edge AI technologies, including LLMs (Large Language Models) and RLNs (Reinforcement Learning Networks), SupraTweets automates content creation, user engagement, and analytics, ensuring seamless interaction with protocol users. From summarizing blogs and announcements to conducting user polls and staying updated with trending memes, SupraTweets covers all aspects of user engagement, providing a hassle-free solution for protocols to communicate effectively with their audiences.
### Features
#### 1. Automated educational/announcement tweets 
SupraTweets periodically posts curated threads summarizing architectural insights, technical updates, and major announcements about the Supra Protocol. By processing official resources such as blogs, whitepapers, and documentation, the bot transforms complex information into concise and engaging Twitter posts.
<img width="400" alt="Screenshot 2024-12-08 at 6 10 25 AM" src="https://github.com/user-attachments/assets/e5915cde-839a-47d3-9e0b-9f83049040e9">

#### 2. Periodic polls 
The bot also conducts polls on a periodic basis, enabling the protocol to make data-driven and user-centric decisions. By understanding which features or services resonate most with the community—such as oracle networks, cross-chain solutions, or interoperability tools—the protocol gets an insight on user sentiments.
<img width="400" alt="Screenshot 2024-12-08 at 6 09 23 AM" src="https://github.com/user-attachments/assets/fb60f68c-c52a-40af-abbb-54595f3ea07f">

#### 3. Keeping up with trendind memes
For the meme fans over there, the bot also keeps it updated with the trending memes and presents on the user's feeds when the content is relevant!

<img width="400" align="center" alt="Screenshot 2024-12-08 at 6 07 48 AM" src="https://github.com/user-attachments/assets/170753f3-fe98-46f8-8208-4d62d35405d0">

### Architecture
Below is the architectural flow:

#### 1. Data Gathering Layer:
* Scrapes and parses protocol resources, including blogs, announcements, whitepaper, and documentation. This is what forms the input to the LLms for learning about the protocol and summarizing contents.
#### 2. AI Processing Layer:
* Tha data scraped and gathered from over the resources goes to the AI input and the model learns and summarizes the content into technical threads for user's feeds.
* The twitter trends and latest updates in the ecosystem provide the prompt for the poll question which is then created for further analytics.
* Generates meme ideas using AI models trained on latest trends.
#### 3. Content Scheduler:
* Schedules and manages posts and polls with cron jobs.
* Periodically checks for new content to ensure fresh updates. (in progress)
#### 4. Engagement & Feedback Analysis:
* Monitors poll results and user interactions.
* Analyzes engagement metrics to guide future content.
* Analyses crypto twitter for more diverse fine tuning and content.
#### 5. Twitter API Integration:
* Posts threads, polls, and memes using Tweepy clients.

### Future work
* Currently, the developer twitter api doesn't provide search queries. However with other plans, we can make a search query and look for mentions of the bot and create the functionality of replying to tweets where the bot is tagged for a question or where Supra is being talked about. To keep the bot in context, fine tuning, sentiment analysis and feedback based learning models will be incorporated.
* The developer API doesn't provide scraping functionality as a result training the model on twitter feeds for diverse feeds isn't possible with the current free api.
* The AI should be able to adapt based on engagement metrics. If certain types of content (e.g., educational threads, news updates) receive more engagement, the AI could focus more on those types of posts.

### Challenges
* Majorly faced challenges with the limited functionalities and limits provided by the fee tier of twitter developer API, leading to account sbeing locked or stuck with 'Too Many Requests'.
* Similarly, finding appropriate LLMs and fine tuning them was challenging.
