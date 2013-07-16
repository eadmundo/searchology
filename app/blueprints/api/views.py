import rawes
from flask import make_response, jsonify, request, abort
from app.blueprints.api import blueprint
from page_snippet import SearchQuerySnippet


es = rawes.Elastic('localhost:9200')


def auth(username, token):
    return True
    # return False


def search_results(index, q, count, page):
    if q == '':
        query = {
            'match_all': {}
        }
    else:
        query = {
            'term': {
                '_all': q
            }
        }

    raw_data = es[index]['page']._search.get(data={
        'version': True,
        'query': query,
        'fields': ['title', 'url', 'text'],
        'size': count,
        'from': (int(page) * int(count)) - int(count),
        'sort': {
            '_score': 'desc'
        }
    })

    results = []

    # print raw_data

    for hit in raw_data['hits']['hits']:
        text = hit['fields']['text']
        if len(q):
            sqs = SearchQuerySnippet(text, q, 170)
            snippet = sqs.snippet
        results.append({
            # '_id': hit['_id'],
            'score': hit['_score'],
            'title': hit['fields']['title'],
            'url': hit['fields']['url'],
            'snippet': snippet,
        })

    return {
        'total': raw_data['hits']['total'],
        'results': results,
    }


@blueprint.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'unauthorized'}), 401)


@blueprint.route('/search')
def search():
    # make sure we have auth
    username, token = request.args.get('auth_token', ':').split(':')
    username = None
    token = None
    if auth(username, token):
        q = request.args.get('q', '')
        count = request.args.get('count', 10)
        page = request.args.get('page', 1)

        results = search_results('docs.djangoproject.dev', q, count, page)
        return make_response(jsonify(results), 200)
    else:
        abort(401)
