from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email

class CheckoutForm(FlaskForm):
    fullName = StringField("Full Name", validators=[InputRequired()])
    phone = StringField("Phone Number", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    country = StringField("Country", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    suburb = StringField("Suburb", validators=[InputRequired()])
    city = StringField("City", validators=[InputRequired()])
    submit = SubmitField("Submit Request")