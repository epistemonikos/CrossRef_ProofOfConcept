import requests
from flask_restful import Resource, reqparse
from reflookup import app
from urllib.parse import unquote


def cr_citation_lookup(citation):
    params = {'query': citation}
    url = app.config['CROSSREF_URI']

    rv = requests.get(url, params=params).json()
    result = rv['message']['items'][0]

    return result


class CrossRefLookupResource(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('ref', type=str, required=True,
                                      location='values')

    def post(self):
        data = self.post_parser.parse_args()
        ref = unquote(data['ref']).strip()

        return cr_citation_lookup(ref)

# @app.route('/', methods=('GET', 'POST'))
# def submit():
#     form = CrossRefForm()
#     if form.validate_on_submit():
#         return redirect('/search')
#     return render_template('form.html', form=form)
#
#
# @app.route('/search', methods=['POST'])
# def search():
#     query = request.form['query'].strip()
#     url = citation_lookup(query)
#     return redirect(url)
#
#
