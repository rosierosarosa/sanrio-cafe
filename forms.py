from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField, IntegerField, TextAreaField, SubmitField, PasswordField, RadioField, SelectField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired, NumberRange, ValidationError, length, EqualTo, Email
from datetime import date
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize




class RegisterForm(FlaskForm):
    username = StringField("Enter your name", validators=[DataRequired()])
    email = StringField("Enter your email", validators=[DataRequired(), Email()])
    password = PasswordField("Enter your password", validators=[
        DataRequired(), length(min=8, max=64, message="Minimum length 8")])
    confirm_password = PasswordField("Repeat password", validators=[
        DataRequired(), EqualTo("password", message="Passwords must be the same")])
    register_button = SubmitField()







class LoginForm(FlaskForm):
    email = EmailField("Enter your Gmail", validators=[
        DataRequired(), Email(message="Enter a valid email address")])
    password = PasswordField("Enter your password", validators=[
        DataRequired(), length(min=8, max=64, message="Minimum length is 8 characters")])
    login_button = SubmitField("Log In")






class BookingForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    date = DateField("Booking Date", validators=[DataRequired()])
    guests = IntegerField("Number of Guests", validators=[DataRequired(), NumberRange(min=1)])
    comment = TextAreaField("Special Requests")
    submit = SubmitField("Submit Booking 🎀")


    def validate_date(self, field):
        if field.data < date.today():
            raise ValidationError("You can't book for a past date! 🎀🕰️")






class FoodForm(FlaskForm):
    name = StringField("Food Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    image = FileField("Image", validators=[
        FileRequired(message="You must upload an image!"),
        FileAllowed(['jpg', 'jpeg', 'png'], "Only .jpg, .jpeg, .png files are allowed!")
    ])
    submit = SubmitField("Add Food 🍱")






class ProfileForm(FlaskForm):
    age = IntegerField("Age", validators=[DataRequired()])
    gender = SelectField("Gender", choices=[
        ('male', 'Male'), ('female', 'Female'), ('other', 'Other')
    ])
    sanrio_character = RadioField("Sanrio Character", choices=[
        ('hello_kitty', 'Hello Kitty'),
        ('kuromi', 'Kuromi'),
        ('my_melody', 'My Melody'),
        ('cinnamoroll', 'Cinnamoroll'),
        ('pochacco', 'Pochacco'),
        ('keroppi', 'Keroppi'),
        ('badtz_maru', 'Badtz-Maru'),
        ('pompompurin', 'Pompompurin'),
        ('tuxedosam', 'Tuxedosam'),
        ('little_twins', 'Little Twin Stars'),
        ('chococat', 'Chococat')
    ])

    submit = SubmitField("Update")




from wtforms import RadioField

class RatingForm(FlaskForm):
    score = RadioField('Rate this food:', choices=[
        ('1', '1 ⭐'),
        ('2', '2 ⭐⭐'),
        ('3', '3 ⭐⭐⭐'),
        ('4', '4 ⭐⭐⭐⭐'),
        ('5', '5 ⭐⭐⭐⭐⭐'),
    ], validators=[DataRequired()])
    submit = SubmitField('Submit Rating')
