import pytumblr, operator
from flask import Flask, request, redirect, render_template
from itertools import combinations
from random import randrange, shuffle
from collections import OrderedDict

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/gifs', methods = ['POST'])
def findGif():
    try:
        tumurl = ''
        tumclient = pytumblr.TumblrRestClient('Kjr56gcuNUtyRDZfhy6rsmmv5cUatTzcVlGg2MsDh67Wq23MxM',)
        gifstring = request.values.get('string')

        punctuation = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
        no_punct = ''.join(char for char in gifstring if char not in punctuation)

        words = no_punct.split()
        if len(words) > 8:
            # to avoid calling tumblr with too many tags trim to 8 words
            words = words[0:8]

        finalists = []
        posts = {}
        # iteratively use less and less words till a gif is found with the tags the words
        for num in range(len(words)-1, -1, -1):
            if not finalists:
                for e in combinations(words, num+1):
                    tag = ' '.join(elem for elem in e)
                    tumresp = tumclient.tagged(tag+' gif')

                    for resp in tumresp:
                        if 'photos' in resp:
                            posts[resp['id']] = {
                                'note_count': resp['note_count'],
                                'url': resp['photos'][0]['original_size']['url']
                            }

                    # get top 6 posts based on note_count
                    if posts:
                        top = sorted(posts.items(), key=lambda x: x[1]['note_count'], reverse=True)[:6]
                        finalists = [d['url'] for _, d in top]

        # get random finalist from the top 6 posts
        if finalists:
            index = randrange(0, len(finalists), 1)

        tumurl = finalists[index]
    except IndexError:
        tumurl = 'Nope, either there\'s no relevant gif, or tumblr didn\'t like the dirty thing you searched...'
    except KeyError:
        tumurl = 'Nope, either there\'s no relevant gif, or tumblr didn\'t like the dirty thing you searched...'
    except UnboundLocalError:
        tumurl = 'Nope, either there\'s no relevant gif, or tumblr didn\'t like the dirty thing you searched...'
    except UnicodeEncodeError:
        tumurl = 'Nope, either there\'s no relevant gif, or tumblr didn\'t like the dirty thing you searched...'

    return render_template('gif.html', tumurl=tumurl, gifstring=gifstring)

if __name__ == '__main__':
    app.run(debug = True)
