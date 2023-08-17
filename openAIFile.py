import os
import openai
import requests
from bs4 import BeautifulSoup
import cloudscraper
import time

openai.api_key = os.environ["OPENAI_API_KEY"]


def getArticleFromUrl(url):
	scraper = cloudscraper.create_scraper(delay=10, browser='chrome')

	info = scraper.get(url).text
	soup = BeautifulSoup(info, 'html.parser')
	# Find the tag : <p> - paragraph tag
	p_tags = soup.find_all('p')

	# Get the text from each tag and join them.
	text = [tag.get_text().strip() for tag in p_tags]
	text = " ".join(text)

	return text


def getSummary(url, name, symbol):

    article = getArticleFromUrl(url)

    # Pongo 50000 porque 1 token son 4 caracteres y el maximo son 16385 tokens en este modelo
    if (len(article) > 14000):
        article = article[:14000]

    for attempt in range(3): # specify the number of retries you want
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "You are a helpful assistant."
                }, {
                    "role": "user",
                    "content": f"Summarize the following text: {article} around {name} and {symbol}. You should provide a title first for the summary. The output should be: Title: (chosen title)  Summary: (summary)"
                }])
            return response['choices'][0]['message']['content']

        except openai.OpenAIError as e:
            print(f"An error occurred: {e}. Retrying in 10 seconds...")
            time.sleep(10)
        else:
            break
    else:
        return "Failed to get summary after multiple attempts."

def getDecision(text, symbol):
    for attempt in range(10): # specify the number of retries you want
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": "You are a helpful assistant, expert in finances and stocks."
                }, {
                    "role": "user",
                    "content": f"You will be provided with a text containing around 20 articles about the company {symbol}, each with a title and a summary. Your task will be to classify these articles in the following categories: - New discoveries or developments in the industry or company. - Price stock related.  - Upcoming events, like dividends, benefits, etc.  - Buying or selling another company. - Projected growth.  When you are done classifying them, give me a brief summary of your discoveries, and produce what is for you the general idea of the articles. I mean, of the listed categories which is the more important in the given articles and what effect it can have in the price of the {symbol} in the following days. Think about the effect of these news in the stock step by step. The articles are: {text}. You do not need to write the categorization of each article, just the summary of your discoveries and the general idea and main category. You should give me a score between -1 and 1 based on the effect you think it will have in the price of the {symbol} stock. -1 is very negative, 1 is very positive."
                }])
            return response['choices'][0]['message']['content']

        except openai.OpenAIError as e:
            # You might want to narrow down to specific error codes related to server errors
            print(f"An error occurred: {e}. Retrying in 10 seconds...")
            time.sleep(10)
        else:
            break
    else:
        return "Failed to get decision after multiple attempts."

# getSummary(
#  'https://www.livemint.com/mutual-fund/mf-news/uti-amc-stake-sale-state-bank-of-india-sbi-lic-punjab-national-bank-and-bank-of-baroda-look-for-bids-says-report-11686794420778.html',
#  'Bank of India', 'SBI')


#getDecision('Title: Global Automotive Brake Fluid Market to Reach $1.9 Billion by 2032, Reports Market Research Future Summary: The global automotive brake fluid market is projected to grow at a CAGR of 5.00% from 2023 to 2032, reaching a value of $1.9 billion. Automotive brake fluids play a crucial role in the hydraulic braking system, ensuring smooth operation and safe deceleration of vehicles. The market is driven by increasing vehicle sales, urbanization, rising disposable income, and growing safety consciousness. However, the introduction of advanced technologies like brake-by-wire may limit market growth. The Asia Pacific region dominates the market, with rapid urbanization and government regulations promoting the usage of electric vehicles. Major companies in the market include Royal Dutch Shell and RDS-B. Title: Significant Growth Predicted for the Automotive Brake Fluid Market by 2030 Summary: According to a comprehensive research report by Market Research Future (MRFR), the global market for automotive brake fluid is projected to reach USD 1.9 billion by 2032, with a growth rate of 5.00% from 2023 to 2032. Automotive brake fluids play a crucial role in hydraulic braking systems, enhancing performance and ensuring safe deceleration of vehicles. Factors driving market growth include increased vehicle sales, urbanization, rising disposable incomes, and government regulations promoting safety. However, the market could face limitations due to the introduction of new braking technologies. The Asia Pacific region currently holds the largest market share, driven by rapid urbanization and economic growth, particularly in China and India. Other significant players in the market include Royal Dutch Shell PLC and RDS-B. Title: Automotive Brake Fluid Market Set to Reach $1.9 Billion by 2032 Summary: The global automotive brake fluid market is projected to grow from $1.3 billion in 2023 to $1.9 billion by 2032, with a compound annual growth rate of 5.00% during the forecast period. Automotive brake fluids are essential for the hydraulic braking system, ensuring smooth operation and safe deceleration of vehicles. Increased vehicle sales, rising safety consciousness, and government regulations on automotive safety are driving the market growth. However, the introduction of advanced technologies like brake-by-wire may limit the expansion. The Asia Pacific region currently leads the market, supported by growing vehicle production and government initiatives promoting electric vehicles.')