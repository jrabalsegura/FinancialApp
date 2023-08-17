import os
import pickle


def loadDictionaries():
	if os.path.isfile('current_dict.pkl'):
		# Unpickling the dictionary

		with open('current_dict.pkl', 'rb') as f:
			current_dict = pickle.load(f)
	else:
		current_dict = {}
		current_dict['count'] = 1

	if os.path.isfile('last_dict.pkl'):
		# Unpickling the dictionary

		with open('last_dict.pkl', 'rb') as f:
			last_dict = pickle.load(f)
	else:
		last_dict = current_dict

	return current_dict, last_dict


def saveDictionaries(current_dict):
	# Pickling the dictionary

	if current_dict['count'] > 5:
		with open('last_dict.pkl', 'wb') as f:
			pickle.dump(current_dict, f)
		current_dict.clear()
		os.remove('current_dict.pkl')
		print("Last 5 dictionary updated.")
	else:
		current_dict['count'] = current_dict['count'] + 1
		with open('current_dict.pkl', 'wb') as f:
			pickle.dump(current_dict, f)



def saveTextToFile(text, filename):
	with open(filename + '.txt', 'w', encoding="utf-8") as f:
		f.write(text)
