from fetch import getArticles
from filesService import loadDictionaries, saveDictionaries, saveTextToFile
from openAIFile import getSummary, getDecision


def main():
	articles = getArticles()
	print("Length of articles: ", len(articles))
	
	entities_dict = {}
 
	numberOfCounts = 10

	current_dict, last_dict = loadDictionaries()

	print("Current count: " + str(current_dict['count']))

	for article in articles:
		entities = article.get('entities', [])
		#print(entities)

		#Add one to entity count in entities_dict

		#Get symbol from entity

		for entity in entities:
			symbolIndexes = entity.get('symbol', '')
			symbol = entity.get('name', '')
			if '^' not in symbolIndexes and 'INDEX' not in symbolIndexes:
				symbol = symbol.replace('.', '').replace(',', '').upper()
				if symbol in entities_dict:
					entities_dict[symbol]['count'] = entities_dict[symbol]['count'] + 1

					entities_dict[symbol]['articles'].append(article.get('url', ''))

				else:
					entities_dict[symbol] = {
					 'siglas': symbolIndexes,
					 'count': 1,
					 'articles': [article.get('url', '')]
					}

	#Loop through entities_dict and compare the sentiment with last_dict
	for symbol in entities_dict.keys():
		
		if symbol in last_dict:
			if entities_dict[symbol]['count'] != None:
				if entities_dict[symbol]['count'] > (numberOfCounts / 3) * (
				 (last_dict[symbol]['count']) /
				  (last_dict['count'] - 1)) and entities_dict[symbol]['count'] > numberOfCounts:
					print("\nEMPRESA:")
					print(symbol)
					print(entities_dict[symbol]['siglas'])
					print(entities_dict[symbol]['count'])

					print(f"Acumulada: {last_dict[symbol]['count']}")
					
					
					text = summarizeArticles(symbol, entities_dict)
						
					decision = getDecision(text, symbol)
					print("\nDECISION: ")
					print(decision)
					

					
		else:
			if entities_dict[symbol]['count'] != None and entities_dict[
			  symbol]['count'] > numberOfCounts:
				print("\nEMPRESA:")
				print(symbol)
				print(entities_dict[symbol]['count'])
				
    			
				
				text = summarizeArticles(symbol, entities_dict)
					
				decision = getDecision(text, symbol)
				print("\nDECISION: ")
				print(decision)

		if symbol in current_dict:

			current_dict[symbol][
			 'count'] = current_dict[symbol]['count'] + entities_dict[symbol]['count']
			

		else:

			current_dict[symbol] = {
			 'count': entities_dict[symbol]['count']
	
		}

	#Order entities_dict by sentiment_score inserting them in a list
	#ordered_entities_dict = dict(sorted(entities_dict.items(), key=lambda x: x[1]['sentiment_score'], reverse=True))
	
	saveDictionaries(current_dict)


def summarizeArticles(symbol, dict):
	articles = dict[symbol]['articles']
	name = symbol
	siglas = dict[symbol]['siglas']
	
	text = ""
	count = 0
	for article in articles:

		#10 articles should be enough to have the idea
		if count > 10:
			break

		count = count + 1

		newSummary = getSummary(article, name, siglas)
		if newSummary != None:
			text = text + newSummary + '\n\n'
   
	
	filename = symbol.replace('/', '') # Modify the filename to remove the slash
	saveTextToFile(text, filename)
	return text
 

main()
