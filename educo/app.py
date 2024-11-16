# from flask import Flask, request, jsonify
# from flask_cors import CORS  # Import CORS
# import google.generativeai as genai
# from flask import Flask, render_template, request, jsonify, session, redirect, url_for
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
# app.config['SECRET_KEY'] = 'secret_key'
# app.app_context().push()
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# CORS(app,origins=["http://127.0.0.1:5500"])
# # Models
# class NewUserLogin(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(50), nullable=False)
#     lastname = db.Column(db.String(50), nullable=False)
#     dob = db.Column(db.String(100), nullable=False)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     _phone_number = db.Column("phone_number", db.String(50), nullable=False)
#     password = db.Column(db.String(128), nullable=False)

#     @property
#     def phone_number(self):
#         return self._phone_number

#     @phone_number.setter
#     def phone_number(self, value):
#         if len(value) != 10 or not value.isdigit():
#             raise ValueError('Phone number must be 10 digits')
#         self._phone_number = value

# # Routes
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     first_name = data.get('first_name')
#     last_name = data.get('last_name')
#     dob = data.get('dob')
#     phone_number = data.get('phone_number')
#     email = data.get('email')
#     username = data.get('username')
#     password = data.get('password')
#     confirm_password = data.get('confirm_password')

#     if len(phone_number) != 10:
#         return jsonify({'error': 'Phone number must be 10 digits'}), 400

#     if password != confirm_password:
#         return jsonify({'error': 'Passwords do not match'}), 400

#     if NewUserLogin.query.filter((NewUserLogin.username == username) | (NewUserLogin.email == email)).first():
#         return jsonify({'error': 'Username or email already exists'}), 400

#     hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

#     new_user = NewUserLogin(
#         firstname=first_name,
#         lastname=last_name,
#         dob=dob,
#         username=username,
#         email=email,
#         phone_number=phone_number,
#         password=hashed_password
#     )

#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User registered successfully'}), 201

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     user = NewUserLogin.query.filter_by(username=username).first()

#     if not user or not check_password_hash(user.password, password):
#         return jsonify({'error': 'Invalid username or password'}), 401

#     # Set the session to keep the user logged in
#     session['user_id'] = user.id  # or any unique identifier for the user

#     return redirect(url_for('chat'))

# # Set your API key
# API_KEY = 'AIzaSyDtjAgKI9RQt3fSc0Rqb7B-oUbJWg_D0-o'
# genai.configure(api_key=API_KEY)

# # Define the initial prompt for the chatbot
# INITIAL_SYSTEM_PROMPT = "You are a mental health chatbot and your name is 'Careit'. Please respond to user queries with empathy and support, providing concise, helpful guidance in one sentence."

# # Initialize the Gemini model
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Try initializing the chat with the appropriate content structure, including "parts"
# chat = model.start_chat(history=[
#     {"role": "model", "parts": [{"text": INITIAL_SYSTEM_PROMPT}]}
# ])

# # # Function to get a response from the Gemini API
# # def get_gemini_response(message):
# #     try:
# #         # Send the user's message and receive the response
# #         response = chat.send_message({"role": "user", "parts": [{"text": message}]})
# #         return response.text
# #     except Exception as e:
# #         print(f"Error: {str(e)}")
# #         return f"Error: {str(e)}"

# # @app.route('/chat', methods=['POST'])
# # def chat_endpoint():
# #     user_message = request.json.get('message')
# #     if not user_message:
# #         return jsonify({'error': 'No message provided'}), 400

# #     bot_reply = get_gemini_response(user_message)
# #     return jsonify({'reply': bot_reply})

# def get_gemini_response(message):
#     try:
#         # Send the user's message and receive the response
#         response = chat.send_message({"role": "user", "parts": [{"text": message}]})
#         return response.text
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return "Sorry, I'm having trouble responding right now. Please try again later."

# @app.route('/chat', methods=['POST'])
# def chat_endpoint():
#     user_message = request.json.get('message')
#     if not user_message:
#         return jsonify({'error': 'No message provided'}), 400

#     bot_reply = get_gemini_response(user_message)
#     return jsonify({'reply': bot_reply})

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify, session, redirect, url_for,render_template
from flask_cors import CORS  # Import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# CORS setup
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500"]}})


# Models
class NewUserLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _phone_number = db.Column("phone_number", db.String(50), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError('Phone number must be 10 digits')
        self._phone_number = value

# Set your API key for Gemini
API_KEY = 'AIzaSyDtjAgKI9RQt3fSc0Rqb7B-oUbJWg_D0-o'
genai.configure(api_key=API_KEY)

# Define the initial prompt for the chatbot
INITIAL_SYSTEM_PROMPT = "You are a mental health chatbot and your name is 'Careit'. Please respond to user queries with empathy and support, providing concise, helpful guidance in one sentence. And it is very important for you to provide a response within 5 seconds as someone's life might be in danger"

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")

# Global chat context (for simplicity, but may need user-specific context in a real app)
chat = model.start_chat(history=[{"role": "model", "parts": [{"text": INITIAL_SYSTEM_PROMPT}]}])

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob = data.get('dob')
    phone_number = data.get('phone_number')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    # Validation checks
    if len(phone_number) != 10:
        return jsonify({'error': 'Phone number must be 10 digits'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    if NewUserLogin.query.filter((NewUserLogin.username == username) | (NewUserLogin.email == email)).first():
        return jsonify({'error': 'Username or email already exists'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = NewUserLogin(
        firstname=first_name,
        lastname=last_name,
        dob=dob,
        username=username,
        email=email,
        phone_number=phone_number,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = NewUserLogin.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401  # Return error with 401 status code

    # Set the session to keep the user logged in
    session['user_id'] = user.id  # Store user session

    return jsonify({'success': True, 'message': 'Login successful!'}), 200  # Return success with 200 status code


@app.route('/chat', methods=['GET', 'POST'])
def chat_endpoint():
    if request.method == 'POST':
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        bot_reply = get_gemini_response(user_message)
        return jsonify({'reply': bot_reply})
    
    # For GET request, render chat page if logged in
    if 'user_id' in session:
        return render_template('chatbot.html')  # Ensure chatbot.html exists in templates folder
    else:
        return redirect(url_for('login'))  # If not logged in, redirect to login

def get_gemini_response(message):
    try:
        # Send the user's message and receive the response
        response = chat.send_message({"role": "user", "parts": [{"text": message}]})
        return response.text
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Sorry, I'm having trouble responding right now. Please try again later."

if __name__ == '__main__':
    app.run(debug=True)
