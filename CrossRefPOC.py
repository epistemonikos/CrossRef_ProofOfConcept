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
    rv = requests.get(app.config['CROSSREF_URI'], params=params).json()

    return rv['message']['items'][0]['URL']


if __name__ == '__main__':
    app.run()
