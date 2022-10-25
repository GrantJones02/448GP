from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField
### HTML forms###

# Login form
class login_form(FlaskForm):
    username = StringField(label="Username")
    password = PasswordField(label="Password")
