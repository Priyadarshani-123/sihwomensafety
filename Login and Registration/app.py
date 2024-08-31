from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt
from pymongo import MongoClient

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Setup MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # MongoDB URI yaha daalna h
db = client['user_management']  # Database name
users_collection = db['users']  # Schema name

# login page
@app.route('/')
def login_page():
    return render_template('login.html')

# registration page
@app.route('/register')
def register_page():
    return render_template('register.html')

# Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.form

    name = data.get('name')
    email = data.get('email')
    gender = data.get('gender')
    age = data.get('age')
    password = data.get('password')

    existing_user = users_collection.find_one({'email': email})
    if existing_user:
        return 'Email already registered', 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user_data = {
        'name': name,
        'email': email,
        'gender': gender,
        'age': age,
        'password': hashed_password
    }

    users_collection.insert_one(user_data)

    return redirect(url_for('login_page'))

# login
@app.route('/login', methods=['POST'])
def login():
    data = request.form

    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({'email': email})

    if user and bcrypt.check_password_hash(user['password'], password):
        return 'Login successful', 200
    else:
        return 'Invalid email or password', 401

if __name__ == '__main__':
    app.run(debug=True)