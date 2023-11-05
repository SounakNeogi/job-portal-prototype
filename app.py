#MongoDb URL: mongodb://localhost:27017

from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase'  # Replace 'myDatabase' with your actual database name
mongo = PyMongo(app)  # Initialize PyMongo


@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'username' : request.form['username']})
    
    if login_user:
        # Verify the hashed password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))  # Redirect to the home page
    return 'Invalid username or password'




@app.route('/contact')
def contact():
    return render_template('contact.html')

#bcrypt = Bcrypt()

users = []

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Access the 'users' collection in your MongoDB
        users_collection = mongo.db.users

        # Insert user data into MongoDB
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password
        }
        users_collection.insert_one(user_data)

        return  render_template('index.html')
    else:
        return render_template('signup.html')
        



if __name__ == '__main__':
    app.secret_key='secretivekeyagain'
    app.run(debug=True)
