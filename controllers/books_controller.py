
from flask import Flask, render_template, redirect, request
from flask import Blueprint
from repositories import author_repository
from repositories import book_repository
from models.book import Book
from models.author import Author

books_blueprint = Blueprint("books" , __name__)

@books_blueprint.route ("/books", methods=['GET'])
def books():
    books = book_repository.select_all()
    return render_template("books/index.html" , all_books = books)

@books_blueprint.route("/books/<id>/delete", methods=['POST'])
def delete_book(id):
    book_repository.delete(id)
    return redirect("/books")

@books_blueprint.route("/books/new", methods=["GET"])
def new_book():
    authors = author_repository.select_all()
    return render_template("books/add.html", all_authors = authors)

@books_blueprint.route("/books", methods=['POST'])
def add_new_book():
    title = request.form['title']
    blurb = request.form['blurb']
    price = request.form['price']
    author_id = request.form['author_id']
    if author_id == "text":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        author = Author(first_name, last_name)
        new_author = author_repository.save(author)

        book = Book(title, new_author, blurb, price)
        book_repository.save(book)
    else:
        author = author_repository.select(author_id)
        book = Book(title, author, blurb, price)
        book_repository.save(book)
    return redirect("/books")