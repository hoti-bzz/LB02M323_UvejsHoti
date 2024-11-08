"""
BookBlueprint
"""

from flask import Blueprint, request, jsonify
from functools import reduce

from userBlueprint import users

# Blueprint für Bücher
book_blueprint = Blueprint('books', __name__)

# Globale Bücherliste
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


@book_blueprint.route('/list_uppercase', methods=['GET'])
def list_books_uppercase():
    if not books:
        return jsonify({"message": "No books available."})

    # Funktion, um den Titel in Großbuchstaben zu konvertieren
    def to_uppercase(book):
        return book['title'].upper()

    # Verwende map, um die Titel in Großbuchstaben zu konvertieren
    titles_uppercase = list(map(to_uppercase, books))

    return jsonify({"titles_uppercase": titles_uppercase})


@book_blueprint.route('/add_review', methods=['POST'])
def add_review():
    data = request.get_json()
    username = data.get("username")
    title = data.get("title")
    rating = data.get("rating")
    comment = data.get("comment", "")

    # Suche nach dem Buch
    book = next((b for b in books if b["title"] == title), None)
    if book is None:
        return jsonify({"message": "Book not found."}), 404

    # Füge die Bewertung hinzu
    book['reviews'].append({"username": username, "rating": rating, "comment": comment})

    # Nach dem Hinzufügen einer Bewertung aktualisieren wir die Benutzerübersicht
    user_review_summary()

    return jsonify({"message": "Review added successfully."})


def user_review_summary():
    # Benutzer mit Rezensionen ermitteln
    users_with_reviews = list(
        filter(lambda user: any(user['username'] == r['username'] for book in books for r in book['reviews']), users))
    usernames = list(map(lambda user: user['username'], users_with_reviews))
    review_count = reduce(
        lambda acc, user: acc + sum(1 for book in books for r in book['reviews'] if r['username'] == user['username']),
        users_with_reviews, 0)

    print("Benutzer mit Rezensionen:", usernames)
    print("Gesamtanzahl der Rezensionen:", review_count)


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


@book_blueprint.route('/filter', methods=['POST'])
def filter_books():
    data = request.get_json()
    min_reviews = data.get("min_reviews", 0)
    min_rating = data.get("min_rating", 0)

    # Lambda-Ausdruck mit mehreren Argumenten, um Bücher zu filtern
    filtered_books = list(filter(
        lambda book, min_reviews=min_reviews, min_rating=min_rating: len(book['reviews']) >= min_reviews and
                                                                     (sum(r['rating'] for r in book['reviews']) / len(
                                                                         book['reviews']) >= min_rating if book[
                                                                         'reviews'] else False),
        books
    ))

    return jsonify({"filtered_books": filtered_books})
