from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, optional



class IncidentForm(FlaskForm):
    incident = StringField('Incident', validators=[DataRequired()])
    url = StringField("Url", validators=[DataRequired()] )
    description = TextAreaField("Description", validators=[DataRequired()] )
    is_closed = BooleanField("Closed?", validators=[optional()])