import pytumblr, operator
from flask import Flask, request, redirect, render_template
from itertools import combinations
from random import randrange

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
	return render_template('index.html')

@app.route('/gifs', methods = ['POST'])
def findGif():
	try:
		tumurl = ''
		tumclient = pytumblr.TumblrRestClient(
		  'Kjr56gcuNUtyRDZfhy6rsmmv5cUatTzcVlGg2MsDh67Wq23MxM',)
		gifstring = request.values.get('string')

		punctuation = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
		no_punct = ""
		for char in gifstring:
		   if char not in punctuation:
		       no_punct = no_punct + char
		
		words = no_punct.split()
		finalists = []
		index = 0
		posts = {}

		if len(words) > 8:
			return redirect('/')
			
		for num in range(len(words)-1,-1,-1):
			for e in combinations(words, num+1):
				if not finalists:
					d = ' '.join(elem for elem in e)
					tumresp = tumclient.tagged(d+' gif')

					for x in range(0,len(tumresp)):
						if 'photos' in tumresp[x]:
							posts[tumresp[x]['id']] = tumresp[x]['note_count']

					for count in range(0,6):
						if posts:
							key = max(posts.iteritems(), key=operator.itemgetter(1))[0]
							for ind in range(0,len(tumresp)):
								if key == tumresp[ind]['id']:
									finalists.append(tumresp[ind])
									break
							del posts[key]

		if finalists:
			index = randrange(0,len(finalists),1)

		tumurl = finalists[index]['photos'][0]['original_size']['url']
	except IndexError:
		tumurl = 'Nope, either there\'s no relevant gif, or tumblr didn\'t like the dirty thing you searched...'
	except KeyError:
		tumurl = 'Nope, either there\'s no relevant gif, or tumblr didn\'t like the dirty thing you searched...'
	except UnboundLocalError:
		tumurl = 'Nope, either there\'s no relevant gif, or tumblr didn\'t like the dirty thing you searched...'
	except UnicodeEncodeError:
		tumurl = 'Nope, either there\'s no relevant gif, or tumblr didn\'t like the dirty thing you searched...'

	# return redirect(tumurl)
	return render_template('gif.html', tumurl=tumurl, gifstring=gifstring)

if __name__ == '__main__':
	app.run(debug = True)