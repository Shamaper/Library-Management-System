# Library management system 

This project implements a basic RESTful API for managing a library system using Flask and SQLAlchemy.
The API supports three main endpoints for retrieving all books, adding a new book, and updating book details.

# How to use?
    •	Clone the repository
    •	Install the dependencies: flask, sqlite

# Run the Application
    1.	Navigate to the Project directory: cd library-management-system
    2.	Run the flask application: python app.py

The application will run on http://127.0.0.1:5000/ by default.

# Insert dummy data in the table

    for i in range(100):
         book = Book()
         book.title = 'book'+str(i)
         book.author = 'author'+str(i)
         book.total_copies = str(i)
         book.available_copies = str(i)
         book.publisher = 'publisher'+str(i)
         book.published_year = '01/01/1999'
         book.check_out_date = 'NULL'
         book.due_date = 'NULL'
         book.issued_to = 'NULL'
         db.session.add(book)
         db.session.commit()

    Commented in the code

# REST API

The REST API to this app is described below.

## Retrieve all Books

### Request

`GET/api/books`

    Example: http://127.0.0.1:5000/GET/api/books

### Response

    {
        "code": 200,
        "payload": [{
                    "author": "Author 1",
                    "available_copies": 1,
                    "book_id": 1,
                    "check_out_date": "NULL",
                    "due_date": "NULL",
                    "issued_to": "01/01/1999",
                    "published_year": "01/01/1999",
                    "publisher": "Publisher 1",
                    "title": "UpdatedTitle",
                    "total_copies": 1
                    }],
        "success": true
    }

## Add a new book

### Request

`POST/api/books`

    Example: http://127.0.0.1:5000/POST/api/books?title=New%20Book%201&author=New%20Author%201&publisher=New%20Publisher%201&published_year=01/01/1999

### Response

    {
    "code": 200,
    "payload": {
            "author": "Author 1",
            "available_copies": null,
            "book_id": 4,
            "check_out_date": null,
            "due_date": null,
            "issued_to": null,
            "published_year": "01/01/1999",
            "publisher": "Publisher 1",
            "title": "Book 1",
            "total_copies": null
             },
  "success": true
}


## Update a book details

### Request

`PUT/api/books`

    Example: http://127.0.0.1:5000//PUT/api/books/1?title=UpdatedTitle?publisher=UpdatedPublisher

### Response

    {
    "code": 200,
    "payload": {
                "author": "Author 1",
                "available_copies": 1,
                "book_id": 1,
                "check_out_date": "NULL",
                "due_date": "NULL",                   
                "issued_to": "01/01/1999",
                "published_year": "01/01/1999",
                "publisher": "Publisher 1",
                "title": "UpdatedTitle",
                "total_copies": 1
                },
  "success": true
}

## Attempt to add a new book using partial parameters

### Request

`POST/API/books`

    Example: http://127.0.0.1:5000/POST/api/books?title=Book%201&author=Author%201

### Response

    {
        "code": 422,
        "error": "Missing parameters : ['publisher', 'published_year']",
        "payload": {},
        "success": false
    }

## Attempt to update a book details using invalid book id

### Request

`PUT/API/books`

    Example: http://127.0.0.1:5000//PUT/api/books/new

### Response

    {
        "code": 404,
        "error": "Book Not Found! ",
        "payload": [],
        "success": false
    }

## Exception handling

### Response

    {            
            "code":400,
            "error":"Bad Request : " + exception,
            "payload":[],
            "success":False      
    }

Notes

This project uses SQLite for simplicity.
Ensure that you have Python and pip installed on your system.
