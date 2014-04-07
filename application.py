import pytumblr
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

		punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
		no_punct = ""
		for char in gifstring:
		   if char not in punctuation:
		       no_punct = no_punct + char

		if no_punct:
			words = no_punct.split()
		else: 
			words = []

		if len(words) == 1 and words[0] == 'gifflr':
			return redirect('http://24.media.tumblr.com/d9ae3dc755c0fd52cd2f883c7d8c719d/tumblr_n10ym69M5i1tro5x0o1_500.gif')

		finalists = []
		notecount = []
		index = 0

		if len(words) > 1:
				tumresp = tumclient.tagged(no_punct+' gif', limit = 20)
				for x in xrange(0,len(tumresp)):
			 			if 'photos' in tumresp[x]:
			 				notecount.append(tumresp[x]['note_count'])
				if notecount:	
		 			notecount.sort()

		 			for i in xrange(0,len(tumresp)):
		 				if(tumresp[i]['note_count'] == notecount[-1]):
		 					return redirect(tumresp[i]['photos'][0]['original_size']['url'])

		for num in range(len(words)-1,-1,-1):
			if not finalists:
				for e in combinations(words, num+1):
					d = ' '.join(elem for elem in e)
					tumresp = tumclient.tagged(d+' gif', limit = 20)
					notecount = []

					for x in xrange(0,len(tumresp)):
						if 'photos' in tumresp[x]:
							notecount.append(tumresp[x]['note_count'])
					
					if notecount:
						notecount.sort()

						for i in xrange(0,len(tumresp)):
							if(tumresp[i]['note_count'] == notecount[-1]):
								finalists.append(tumresp[i])

		if finalists:
			notecount = []
			for x in xrange(0,len(finalists)):
				notecount.append(finalists[x]['note_count'])

			notecount.sort()
			notecount.reverse()

			if len(notecount) < 5:
				maximum = len(notecount)
			else:
				maximum = 5

			num = randrange(0,maximum,1)
			for i in xrange(0,len(finalists)):
				if(finalists[i]['note_count'] == notecount[num]):
					index = i

		tumurl = finalists[index]['photos'][0]['original_size']['url']
	except IndexError:
		tumurl = '/'
	except KeyError:
		tumurl = '/'
	except UnboundLocalError:
		tumurl = '/'
	except UnicodeEncodeError:
		tumurl = '/'

	return redirect(tumurl)

if __name__ == '__main__':
	app.run(debug = True)