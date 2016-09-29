import requests
from flask import Flask
from flask import json
from flask import redirect
from flask import render_template
from flask import request
from pprint import PrettyPrinter

from search_form import *

app = Flask(__name__)
app.config['CROSSREF_URI'] = 'http://api.crossref.org/works'
app.secret_key = 'blah blah'


@app.route('/', methods=('GET', 'POST'))
def submit():
    form = CrossRefForm()
    if form.validate_on_submit():
        return redirect('/search')
    return render_template('form.html', form=form)


@app.route('/search', methods=['POST'])
def search():
    query = request.form['query'].strip()
    url = citation_lookup(query)
    return redirect(url)


def citation_lookup(citation):
    params = {'query': citation.strip()}
    url = app.config['CROSSREF_URI']
    pp = PrettyPrinter(indent=4)
    
    rv = requests.get(url, params=params).json()
    result = rv['message']['items'][0]['URL']
    pp.pprint(rv['message']['items'][0])

    return result


if __name__ == '__main__':
    app.run()
