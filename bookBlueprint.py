from flask import Blueprint, request, jsonify
from functools import reduce

book_blueprint = Blueprint('books', __name__)

# Global books list
books = [
    {"title": "Schimmelreiter", "author": "Theodor Storm", "reviews": []},
    {"title": "Die Marquise von O...", "author": "Heinrich von Kleist", "reviews": []}
]

@book_blueprint.route('/add', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    books.append({"title": title, "author": author, "reviews": []})
    return jsonify({"message": f"Book '{title}' by {author} added successfully."})

@book_blueprint.route('/list', methods=['GET'])
def list_books():
    if not books:
        return jsonify({"message": "No books available."})
    return jsonify(books)

@book_blueprint.route('/sort', methods=['POST'])
def sort_books():
    data = request.get_json()
    criterion = data.get("criterion", "").strip().lower()
    if criterion in ["title", "author"]:
        books.sort(key=lambda book: book[criterion])
        return jsonify({"message": f"Books sorted by {criterion}."})
    return jsonify({"message": "Invalid sorting criterion."}), 400

@book_blueprint.route('/uppercase', methods=['GET'])
def list_books_uppercase():
    titles_upper = [book['title'].upper() for book in books]
    return jsonify({"titles_uppercase": titles_upper})

@book_blueprint.route('/high-rated', methods=['GET'])
def calculate_high_rated_books():
    high_rated_books = list(filter(
        lambda book: any(r['rating'] >= 4 for r in book['reviews']), books
    ))
    total_ratings = reduce(
        lambda acc, book: acc + sum(r['rating'] for r in book['reviews']),
        high_rated_books,
        0
    )
    total_reviews = reduce(
        lambda acc, book: acc + len(book['reviews']),
        high_rated_books,
        0
    )
    average_rating = total_ratings / total_reviews if total_reviews > 0 else 0
    return jsonify({"average_rating": average_rating})
