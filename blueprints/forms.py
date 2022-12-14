import wtforms
from wtforms.validators import length,email,EqualTo
from models import EmailCaptchaModel
from flask import flash
# check if email and password are valid
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6,max=20)])

# check if register information are valid
class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3,max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6,max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    # check if captcha is valid
    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            flash("Wrong Captcha！")
            raise wtforms.ValidationError("Wrong Captcha！")
    def validate_password(self,field):
        password = self.password.data
        if len(password)<6 or len(password)>20:
            flash("Password length should be in 6-20!")

    def validate_username(self,field):
        username = self.username.data
        if len(username)<3 or len(username)>20:
            flash("Username length should be in 3-20!")

class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=200)])
    content = wtforms.StringField(validators=[length(min=5)])
    city =  wtforms.StringField(validators=[length(min=0)])
    geolocation = wtforms.StringField(validators=[length(min=0)])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])

class ModifypasswordForm(wtforms.Form):
    old_password = wtforms.StringField(validators=[length(min=6,max=20)])
    new_password =wtforms.StringField(validators=[length(min=6,max=20)])
    # new_password_confirm = wtforms.StringField(validators=[EqualTo("password")])
    def validate_password(self,field):
        password = field.old_password.data
        if len(password)<6 or len(password)>20:
            print("Password length should be in 6-20!")
            flash("Password length should be in 6-20!")
        password = field.new_password.data
        if len(password) < 6 or len(password) > 20:
            print("Password length should be in 6-20!")
            flash("Password length should be in 6-20!")

class ModifyusernameForm(wtforms.Form):
    new_username = wtforms.StringField(validators=[length(min=3,max=20)])

class ModifyEmailForm(wtforms.Form):
    new_email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    def validate_captcha(self,field):
        captcha = field.data
        print(field)
        email = self.new_email.data
        print(email)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            flash("Wrong Captchas！")
            raise wtforms.ValidationError("Wrong Captcha！")






