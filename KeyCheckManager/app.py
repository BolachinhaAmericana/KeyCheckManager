from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from master_user import login_user

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a strong secret key
jwt = JWTManager(app)

@app.route('/login', methods=['GET', 'POST'])  # Handle both GET and POST requests
def login():
    if request.method == 'GET':
        # This can be a simple HTML form to render in the browser for users to input credentials
        return render_template('login.html')  # Render the login.html template for GET requests

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        authenticated = login_user(username, password)
        print(f'Authenticated: {authenticated}')

        if authenticated:
            access_token = create_access_token(identity=username)
            return jsonify({"msg": "Login successful", "access_token": access_token}), 200  # Include access token in the JSON response
        else:
            return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/home', methods=['GET'])
@jwt_required()  # Protect the /home endpoint
def home():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)
