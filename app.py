from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u805562190_flask:=5uS^atGp+mW@217.21.74.101/u805562190_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, title, body):
        self.title = title
        self.body = body

class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)

# Route

@app.route('/get', methods=['GET'])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)

@app.route('/get/<id>/', methods=['GET'])
def get_article_id(id):
    get_article_id = Articles.query.get(id)
    # results_id = articles_schema.dump(get_articles_id)
    return article_schema.jsonify(get_article_id)

@app.route('/post', methods=['POST'])
def post_article():
    title = request.json['title']
    body = request.json['body']

    article = Articles(title, body)
    db.session.add(article)
    db.session.commit()
    return article_schema.jsonify(article)

@app.route('/update/<id>/', methods=['PUT'])
def update_article(id):
    article = Articles.query.get(id)
    title = request.json['title']
    body = request.json['body']

    article.title = title
    article.body = body
    db.session.commit()
    return article_schema.jsonify(article)

@app.route('/delete/<id>/', methods=['DELETE'])
def delete_article(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()

    return article_schema.jsonify("Delete Berhasil",article)

@app.route('/', methods=['GET'])
def get_hello():
    a = '<div><h1>Hello</h1></div>'
    return a

#
if __name__ == "__main__":
    app.run(debug=True)
