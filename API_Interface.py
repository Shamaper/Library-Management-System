from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'  # SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    total_copies = db.Column(db.Integer, nullable=False)
    available_copies = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(50), nullable=False)
    published_year = db.Column(db.String(50), nullable=False)
    check_out_date = db.Column(db.String(50))
    due_date = db.Column(db.String(50)) 
    issued_to = db.Column(db.String(50))

# http://127.0.0.1:5000/GET/api/books 
@app.route("/GET/api/books")
def get():
    try:
        books = Book.query.all()
        payload = []
        if not books:
            # Empty Data
            return jsonify({
                "success":True,
                "payload":[],
                "code":204
            }),204
                
        for book in books:
            data = {
                'book_id' : book.book_id,
                'title' : book.title,
                'author' : book.author,
                'total_copies' : book.total_copies,
                'available_copies' : book.available_copies,
                'publisher' : book.publisher,
                'published_year' : book.published_year,
                'check_out_date' : book.check_out_date,
                'due_date' : book.due_date,
                'issued_to' : book.issued_to
            }
            payload.append(data)

        return jsonify({
            "success":True,
            "payload":payload,
            "code":200
        }),200
    except Exception as e:
        return jsonify({
            "success":False,
            "payload":[],
            "error":"Bad Request : "+e,
            "code":400
        }),400
    

# http://127.0.0.1:5000/POST/api/books?title=Book%201&author=Author%201&publisher=Publisher%201&published_year=01/01/1999
@app.route('/POST/api/books')
def add():
    
    try:
        data = {"title":request.args.get('title'),
            "author":request.args.get('author'),
            "publisher":request.args.get('publisher'),
            "published_year":request.args.get('published_year'),
            "total_copies" : request.args.get('total_copies'),
            "available_copies" : request.args.get('available_copies'),
            "check_out_date" : request.args.get('check_out_date'),
            "due_date" : request.args.get('due_date') ,
            "issued_to" : request.args.get('issued_to')
            }
        
        check = ['title','author','publisher','published_year']
        missing = []
        for param in check:
            if data[param]==None:
                missing.append(param)
        if missing:
            return jsonify({
            'success': False,
            'payload': {},
            'error': f'Missing parameters : {missing}',
            'code':422
            }), 422

        # Create a new book instance
        new_book = Book(
            title=data['title'],
            author=data['author'],
            total_copies=data['total_copies'] if data['total_copies']!=None else 1,  # default to 0 if not provided
            available_copies=data['available_copies'] if data['available_copies']!=None else 1,  # default to 0 if not provided
            publisher = data['publisher'],
            published_year=data['published_year'],
            check_out_date = data['check_out_date'] if data['check_out_date']!=None else "NULL",
            due_date = data['due_date'] if data['due_date']!=None else "NULL",
            issued_to = data['published_year'] if data['published_year']!=None else "NULL"
        )

        # Add the new book to the database
        db.session.add(new_book)
        db.session.commit()

        data['book_id'] = new_book.book_id
        return jsonify({
            'success': True,
            'payload': data,
            'code':200
            }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success":False,
            "payload":[],
            "error":"Bad Request : "+e,
            "code":400
        }),400

# http://127.0.0.1:5000//PUT/api/books/1?title=UpdatedTitle
@app.route('/PUT/api/books/<int:book_id>')
def update(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({
                "success":False,
                "payload":[],
                "error":"Book Not Found! ",
                "code":404
            }),404
        
        title = request.args.get('title')
        author = request.args.get('author')
        publisher = request.args.get('publisher')
        published_year = request.args.get('published_year')
        total_copies = request.args.get('total_copies')
        available_copies = request.args.get('available_copies')
        check_out_date = request.args.get('check_out_date')
        due_date = request.args.get('due_date') 
        issued_to = request.args.get('issued_to')

        data = {'book_id':book_id}
        data['title']=book.title = book.title if title == None else title
        data['author']=book.author = book.author if author == None else author
        data['publisher']=book.publisher = book.publisher if publisher == None else publisher
        data['published_year']=book.published_year = book.published_year if published_year == None else published_year
        data['total_copies']=book.total_copies = book.total_copies if total_copies == None else total_copies
        data['available_copies']=book.available_copies = book.available_copies if available_copies == None else available_copies
        data['check_out_date']=book.check_out_date = book.check_out_date if check_out_date == None else check_out_date
        data['due_date']=book.due_date = book.due_date if due_date == None else due_date
        data['issued_to']=book.issued_to = book.issued_to if issued_to == None else issued_to
        
        db.session.commit()
        return jsonify({
            'success': True,
            'payload': data,
            'code':200
            }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success":False,
            "payload":[],
            "error":"Bad Request : "+e,
            "code":400
        }),400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # for i in range(100):
        #     book = Book()
        #     book.title = 'book'+str(i)
        #     book.author = 'author'+str(i)
        #     book.total_copies = str(i)
        #     book.available_copies = str(i)
        #     book.publisher = 'publisher'+str(i)
        #     book.published_year = '01/01/1999'
        #     book.check_out_date = 'NULL'
        #     book.due_date = 'NULL'
        #     book.issued_to = 'NULL'
        #     db.session.add(book)
        #     db.session.commit()
        app.run(debug=True)
    
