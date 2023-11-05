#MongoDb URL: mongodb://localhost:27017

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from pymongo import MongoClient
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase'  
mongo = PyMongo(app)  # Initialize PyMongo

client = MongoClient('mongodb://localhost:27017/')
db = client['myDatabase']  # Replace 'myDatabase' with your actual database name
collection = db['job_data']

@app.route('/search_job_description', methods=['POST'])
def search_job_description():
    job_description = request.form.get('job_description')

    # Search the MongoDB collection for the job description
    # Adjust the search query based on your MongoDB schema and how you store job descriptions
    result = collection.find_one({'job': job_description})
    print(result)
    return jsonify({'result': result})

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login_page', methods=['POST', 'GET'])
def login_page():
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
            return redirect(url_for('dashboard'))  # Redirect to the home page
    return 'Invalid username or password'

@app.route('/dashboard')
def dashboard():
    # Your dashboard logic
    return render_template("dashboard.html")



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
        phone = request.form['phone']
        job = request.form['job']
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Access the 'users' collection in your MongoDB
        users_collection = mongo.db.users
        job_collection = mongo.db.job_data

        # Insert user data into MongoDB
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'phone':phone,
        }
        #job_datas = {}
        users_collection.insert_one(user_data)
       # job_collection.insert_one(job_datas)

        return  render_template('index.html')
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return render_template('index.html')




if __name__ == '__main__':
    app.secret_key='secretivekeyagain'
    app.run(debug=True)
