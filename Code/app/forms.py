from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField
### HTML forms###

# Login form
class login_form(FlaskForm):
    username = StringField(label="Username")
    password = PasswordField(label="Password")
    login_submit = SubmitField('submit', render_kw={'value': 'Log In'})
# Login form
class signup_form(FlaskForm):
    new_name = StringField(label="New Username")
    new_pass = PasswordField(label="New Password")
    confirm_pass = PasswordField(label="Confirm Password")
    signup_submit = SubmitField('submit', render_kw={'value': 'Sign Up'})
