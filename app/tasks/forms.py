from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    DateField,
    SubmitField
)
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    description = TextAreaField("Description")

    priority = SelectField(
        "Priority",
        choices=[
            ("Low", "Low"),
            ("Medium", "Medium"),
            ("High", "High")
        ]
    )

    status = SelectField(
        "Status",
        choices=[
            ("Pending", "Pending"),
            ("In Progress", "In Progress"),
            ("Completed", "Completed")
        ]
    )

    due_date = DateField(
        "Due Date",
        format="%Y-%m-%d"
    )

    project = SelectField(
        "Project",
        coerce=int
    )

    assignee = SelectField(
        "Assign To",
        coerce=int
    )

    submit = SubmitField("Create Task")