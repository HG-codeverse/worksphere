from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    company_name = StringField(
        "Company Name",
        validators=[DataRequired(), Length(max=100)]
    )

    company_email = StringField(
        "Company Email",
        validators=[DataRequired(), Email()]
    )

    admin_name = StringField(
        "Admin Name",
        validators=[DataRequired(), Length(max=100)]
    )

    admin_email = StringField(
        "Admin Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")