from flask import Flask
from flask_graphql import GraphQLView
from models import db  # Import the db instance
from schema import schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Add the GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable the GraphiQL interface
    )
)

if __name__ == '__main__':
    app.run(debug=True)
