from flask import Flask
from blueprints.userBlueprint import user_blueprint
from blueprints.bookBlueprint import book_blueprint

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(book_blueprint, url_prefix='/books')

if __name__ == "__main__":
    app.run(debug=True)