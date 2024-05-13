import secrets
from utils.common import *
from models import Base, User
from sqlalchemy import create_engine
from flask import Flask, render_template
from flask_login import LoginManager, login_required
from sqlalchemy.orm import scoped_session, sessionmaker


from auth.routes import auth_blueprint
from user.routes import user_blueprint
from loaded.routes import loaded_blueprint

app = Flask(__name__) 
app.config['images_path'] = '/app/images'
app.config['upload_path'] = '/app/uploads'
app.config['db_uri'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] =  secrets.token_hex(32)

# SQLAlchemy setup
engine = create_engine(app.config['db_uri'])
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine)) # Create a scoped session

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'


#Load data and train model
file = 'wfp_food_prices_nga.csv'
data = load_and_preprocess_data(file)
if data is not None:
    model, enc = train_model(data)


# Register the AuthBlueprint with the app
app.register_blueprint(auth_blueprint(login_manager, db_session))

# Register the UserBlueprint with the app
app.register_blueprint(user_blueprint(app, db_session))

# Register the Blueprint with the app and pass db_session
app.register_blueprint(loaded_blueprint(data,model, enc))


# Home route
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Dashboard route
@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# Get image route
@app.route('/get_image/<image_name>', methods=['GET'])
def get_image(image_name):
    # Return the requested image file
    return send_image_from_directory(app.config['images_path'], image_name)

# Main function
if __name__ == '__main__':
    app.run(debug=True)
