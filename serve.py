from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import InputRequired, Email, Length
from forms import LoginForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy




application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@23.21.89.93:3306/sample schema'


db = SQLAlchemy(application)

application.config['SECRET_KEY'] = 'SECRETKEY'

bootstrap = Bootstrap(application)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "login_page"


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String(15), unique=True)
    user_email = db.Column(db.String(50), unique=True)
    user_password = db.Column(db.String(30))

    def get_id(self):
        return (self.user_id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@application.route('/', methods=['GET', 'POST'])
def home_page():
    print("LOG: home page loaded")
    if request.method == 'POST':
        if(request.form.get('login_page_redirect')):
            return login_page()

        elif(request.form.get('registration_page_redirect')):
            return registration_page()

        elif(request.form.get('profile_page_redirect')):
            return profile_page()

        elif(request.form.get('logout_user')):
            logout_user()
            return render_template('home_page.html')

        elif(request.form.get('quiz_page_redirect')):
            return quiz_page()
        
        elif(request.form.get('admin_page_redirect')):
            return admin_page()
            
        elif(request.form.get('video_add_edit_page_redirect')):
            return video_add_edit_page()

        elif(request.form.get('quiz_analytics_page_redirect')):
            return quiz_analytics_page()

        elif(request.form.get('video_analytics_page_redirect')):
            return video_analytics_page()
    if(current_user.is_authenticated):
        return render_template('home_page.html', username=current_user.user_username)
    else:
        return render_template('home_page.html')
    


@application.route('/login', methods=['GET', 'POST'])
def login_page():
    print("LOG: login page loaded")

    form = LoginForm()
    if request.method == 'POST':
        if(form.validate_on_submit()):
            print(form.username.data)
            user = User.query.filter_by(user_username=form.username.data).first()
            if user:
                print("bruh")
                if user.user_password == form.password.data:
                    login_user(user)
                    return render_template('login_page.html', login_output = "you are now signed in as" + str(form.username), form=form)
                else:
                    return render_template('login_page.html', login_error = "Incorrect password, please try again", form=form)
            else:
                return render_template('login_page.html', login_error = "Incorrect username/password, please try again", form=form)
        if(request.form.get('home_page_redirect')):
            return home_page()

        

    return render_template('login_page.html', form=form)


@application.route('/registration', methods=['GET', 'POST'])
def registration_page():
    print("LOG: registration page loaded")


    form = RegisterForm()
    if request.method == 'POST':
        
        if(form.validate_on_submit()):
            # Need to hash the password here
            user = User.query.filter_by(user_username=form.username.data).first()

            if user:
                return render_template('registration_page.html', registration_error="That username already exists", form=form)
            else:
                new_user = User(user_username=form.username.data, user_email=form.email.data, user_password=form.password.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return home_page()
        

        if(request.form.get('home_page_redirect')):
            return home_page()


    return render_template('registration_page.html', form=form)


@application.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    print("LOG: profile page loaded")
    if request.method == 'POST':
        if(request.form.get('home_page_redirect')):
            return home_page()
    
    return render_template('profile_page.html', username=current_user.user_username)


@application.route('/quiz', methods=['GET', 'POST'])
def quiz_page():
    print("LOG: profile page loaded")
    if request.method == 'POST':
        if(request.form.get('home_page_redirect')):
            return home_page()
    return render_template('quiz_page.html')


@application.route('/admin', methods=['GET', 'POST'])
def admin_page():
    print("LOG: admin page loaded")
    if request.method == 'POST':
        if(request.form.get('home_page_redirect')):
            return home_page()
    return render_template('admin_page.html')

@application.route('/video_add_edit', methods=['GET', 'POST'])
def video_add_edit_page():
    print("LOG: video_add_edit page loaded")
    if request.method == 'POST':
        if(request.form.get('home_page_redirect')):
            return home_page()
    return render_template('video_add_edit_page.html')


@application.route('/quiz_analytics', methods=['GET', 'POST'])
def quiz_analytics_page():
    print("LOG: quiz_analytics page loaded")
    if request.method == 'POST':
        if(request.form.get('home_page_redirect')):
            return home_page()
    return render_template('quiz_analytics_page.html')


@application.route('/video_analytics', methods=['GET', 'POST'])
def video_analytics_page():
    print("LOG: video_analytics page loaded")
    if request.method == 'POST':
        if(request.form.get('home_page_redirect')):
            return home_page()
    return render_template('video_analytics_page.html')

 
## Change this during aws deployment
application.run(host="localhost", port="5000")