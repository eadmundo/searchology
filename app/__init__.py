from flask import Flask, request, abort, make_response, jsonify, render_template
import rawes
from app.helpers import Pagination

es = rawes.Elastic('localhost:9200')

app = Flask(__name__)

app.debug = True


@app.route('/')
def results():
    page = int(request.args.get('page', 1))
    qstr = request.args.get('q', '')
    count = request.args.get('count', 10)
    results = search_results('docs.djangoproject.dev', qstr, count, page)
    pagination = Pagination(page, count, results['hits']['total'], results['hits']['hits'])
    return render_template('srp.jinja', pagination=pagination, qstr=qstr)


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


@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'unauthorized'}), 401)


@app.route('/api/search')
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
