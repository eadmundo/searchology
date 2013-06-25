import rawes
from flask import make_response, jsonify, request, abort
from app.blueprints.api import blueprint


es = rawes.Elastic('localhost:9200')


def auth(username, token):
    return True


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
    return es[index]['page']._search.get(data={
        'version': True,
        'query': query,
        'fields': ['url'],
        'size': count,
        'from': (int(page) * int(count)) - int(count),
        'sort': {
            '_score': 'desc'
        }
    })


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
