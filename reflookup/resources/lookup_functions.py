from datetime import datetime

import requests
from werkzeug.exceptions import abort

from reflookup import app
from reflookup.utils.rating.rating import Rating
from reflookup.utils.standardize_json import crossref_to_standard, \
    mendeley_to_standard, scopus_to_standard


def cr_citation_lookup(citation, return_all=False):
    """
    This function does the actual CrossRef API call to search for a given
    citation, and returns the first (and thus, according to CR, the best)
    result.
    :param return_all: Optional parameter indicating to return whole list of results instead of only the first.
    :param citation: Citation to look up in CR.
    :return: A Python dict representing the best result offered by CrossRef.
    """
    params = {'query': citation}
    url = app.config['CROSSREF_URI']

    req = requests.get(url, params=params)
    if req.status_code != 200:
        abort(req.status_code, 'Remote API error.')

    rv = req.json()

    if len(rv['message']['items']) < 1:
        abort(404, 'No results found for query.')

    if return_all:
        result = []
        for r in rv['message']['items']:
            std = crossref_to_standard(r)
            std['rating'] = Rating(citation, std).value()
            result.append(std)
        return result

    else:
        result = rv['message']['items'][0]
        result = crossref_to_standard(result)
        result['rating'] = Rating(citation, result).value()
        return result


def cr_doi_lookup(doi):
    """
    This function retrieves the metadata for the specified CrossRef DOI
    :param doi: DOI to look up in CR.
    :return: A Python dict representing the metadata for the specified DOI.
    """
    url = app.config['CROSSREF_URI'] + "/" + doi
    req = requests.get(url)
    if req.status_code == 400:
        abort(404, 'Resource not found')
    elif req.status_code != 200:
        abort(req.status_code, 'Remote API error.')
    else:
        result = req.json()['message']
        result = crossref_to_standard(result)
        return result


def mendeley_lookup(citation, return_all=False):
    params = {'query': citation}
    # Note that Mendeley requires authentication:
    headers = {
        'Authorization': 'Bearer ' + get_mendeley_access_token(),
        'Accept': 'application/vnd.mendeley-document.1+json'
    }
    req = requests.get(app.config['MENDELEY_SEARCH_URI'],
                       params=params, headers=headers)

    if req.status_code != 200:
        if req.status_code == 401:
            refresh_mendeley_token()
            return mendeley_lookup(citation)
        else:
            abort(req.status_code, 'Remote API error.')

    rv = req.json()

    if len(rv) < 1:
        abort(404, 'No results found for query.')

    if return_all:
        result = []
        for r in rv:
            std = mendeley_to_standard(r)
            std['rating'] = Rating(citation, std).value()
            result.append(std)
        return result

    else:
        result = rv[0]
        result = mendeley_to_standard(result)
        result['rating'] = Rating(citation, result).value()
        return result


def mendeley_doi_lookup(doi):
    params = {'doi': doi}
    # Note that Mendeley requires authentication:
    headers = {
        'Authorization': 'Bearer ' + get_mendeley_access_token(),
        'Accept': 'application/vnd.mendeley-document.1+json'
    }
    req = requests.get(app.config['MENDELEY_CATALOG_URI'],
                       params=params, headers=headers)

    if req.status_code != 200:
        if req.status_code == 401:
            refresh_mendeley_token()
            return mendeley_doi_lookup(doi)
        else:
            abort(req.status_code, 'Remote API error.')

    rv = req.json()

    result = rv[0]
    result = mendeley_to_standard(result)
    return result


def refresh_mendeley_token():
    """
    Calls the Mendeley API to renew the access token and stores it.
    :return: A new access token.
    """
    r = requests.post(app.config['MENDELEY_AUTH_URI'],
                      data={'grant_type': 'client_credentials',
                            'scope': 'all'},
                      auth=app.config['MENDELEY_AUTH'])

    if r.status_code == 200:
        app.config['MENDELEY_ACCESS_TOKEN'] = {
            'token': r.json()['access_token'],
            'expires_in': r.json()['expires_in'],
            'created': datetime.now()
        }

        return app.config['MENDELEY_ACCESS_TOKEN']

    abort(500, 'Error when renewing Mendeley access token.')


def get_mendeley_access_token():
    """
    Helper function. Verifies the status of the current access token and
    renews it if necessary, storing it.
    TODO: Fix errors related to Mendeley not returning an access token.
    :return: A valid access token.
    """
    token = app.config.get('MENDELEY_ACCESS_TOKEN')
    if not token:
        token = refresh_mendeley_token()
    else:
        then = token['created']
        delta = token['expires_in'] - 100
        now = datetime.now()
        if (now - then).total_seconds() > delta:
            token = refresh_mendeley_token()
    return token['token']


def get_scopus_references(doi):
    params = {
        "apiKey": app.config["SCOPUS_API_KEY"]
    }
    headers = {
        "Accept": "text/xml"
    }
    resp = requests.get(app.config["SCOPUS_URI"] + doi, params=params, headers=headers)

    if resp.status_code == 200:
        return scopus_to_standard(resp.text, doi)
    elif resp.status_code == 404:
        abort(404, 'Resource not found.')
    else:
        abort(resp.status_code, "Couldn't retrieve references for DOI:" + doi)