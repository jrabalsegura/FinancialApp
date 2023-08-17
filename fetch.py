import requests
from datetime import datetime
import os


def getArticles():
	# Define the endpoint
	url = "https://api.marketaux.com/v1/news/all?"
	marketaux_api_key = os.environ["MARKETAUX_API_KEY"]

	# Define the current date
	date_today = datetime.now().strftime('%Y-%m-%d')

	# Initialize the page number and requests count
	page = 1
	requests_count = 0

	# Create a list to store the articles
	articles_list = []

	#Modificar a 100 cuando vea que funciona el tema de contar
	#las empresas mencionadas y eso.
	while requests_count < 1000:

		# Define the parameters
		params = {
		 "language": "en,es",
		 "api_token": marketaux_api_key,
		 "published_on": date_today,
		 "countries": "us,ca,es",
		 "must_have_entites": "true",
		 "page": page,
		}

		# Make a GET request to the endpoint
		response = requests.get(url, params=params)
		# Check if the request was successful
		if response.status_code == 200:
			# Increment the requests count
			requests_count += 1

			# Parse the JSON response
			data = response.json()

			# Get the articles and add them to the list
			articles = data.get('data', [])
			articles_list.extend(articles)

			# Check if there are no more articles to fetch
			if not articles:
				break

			# Increment the page number
			page += 1
		else:
			print("Failed to fetch the news, status code:", response.status_code)
			break
	return articles_list


# Now, articles_list contains all the articles
