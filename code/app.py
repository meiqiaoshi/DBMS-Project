from flask import Flask, render_template, request, jsonify
from external_data_provider import ExternalDataProvider

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


data_provider = ExternalDataProvider()


@app.route('/search', methods=['POST', 'GET'])
def search():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('pageSize', 10))
    people = []

    if request.method == 'POST':
        query = request.form.get('query', '')
    else:
        query = request.args.get('query', '')

    if not query:  # empty query
        return jsonify({})

    if query.startswith('#'):  # search by hashtag
        query = query.lstrip('#')
        tweets = data_provider.get_tweets_by_hashtag(query, page, per_page)
    else:  # free search, show both people and tweets
        people = data_provider.get_user(query)  # 保证POST请求也可以获取people数据
        tweets = data_provider.get_tweets_by_text(query, page, per_page)

    return jsonify(people=people, tweets=tweets)


if __name__ == '__main__':
    app.run(debug=True, port=5000)