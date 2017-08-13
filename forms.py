from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, optional



# Incident Form
class IncidentForm(FlaskForm):
    incident = StringField('Incident', validators=[DataRequired()])
    url = StringField("Url", validators=[DataRequired()] )
    description = TextAreaField("Description", validators=[DataRequired()] )
    is_closed = BooleanField("Closed?", validators=[optional()])
    
    
# Email Form
class MailForm(FlaskForm):
	title = StringField('Title')
	recipient = StringField('Recipient', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])