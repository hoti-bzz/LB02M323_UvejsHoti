from flask import Flask
from userBlueprint import user_blueprint
from bookBlueprint import book_blueprint

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(book_blueprint, url_prefix='/books')

if __name__ == "__main__":
    app.run(debug=True)