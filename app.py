from flask import Flask, request, render_template, url_for, redirect, flash, session, logging
from peewee import *
from wtfpeewee.orm import model_form
from flask_mail import Mail, Message

import models
import forms

app = Flask(__name__)
app.secret_key = "big_secret123"


# Mail Config
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['SECURITY_EMAIL_SENDER'] = 'tak jak poniżej'
app.config['MAIL_DEFAULT_SENDER'] = 'jabil email'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "Email"
app.config['MAIL_PASSWORD'] = "Hasło"

mail = Mail(app)




# Index Route
@app.route('/')
def index():
    return render_template('index.html')


# Dasboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    incidents = models.Incident.select()
    form = forms.IncidentForm()
    if form.validate_on_submit():
        models.Incident.create(
            incident = form.incident.data,
            url = form.url.data,
            description = form.description.data,
            is_closed = form.is_closed.data
        )
        flash("Incident Added", "success")
        return redirect(url_for("dashboard"))
    return render_template('dashboard.html', form=form, incidents=incidents)


# View Incident
@app.route('/incident/<string:id>')
def view_incident(id):
    incident = models.Incident.select().where(models.Incident.id ** id).get()
    return render_template('incident.html', incident=incident)


# Edit Incident
@app.route('/incident/<int:id>/edit', methods=['GET', 'POST'])
def edit_incident(id):
    # Not working example
#    form = forms.IncidentForm()
#    incident = models.Incident.select().where(models.Incident.id ** id).get()
#    
#    # Populate incident form fields
#    form.incident.data = incident.incident
#    form.description.data = incident.description
#    form.url.data = incident.url
#    
#    if form.validate_on_submit():
#        models.Incident.get(id=id).update(
#            url = form.url.data,
#            description = form.description.data
#        ).execute()
#        
#
#        
#        flash("Incidend Updated", 'success')
#        return redirect(url_for('view_incident', id=incident.id))
#    return render_template('incident_edit.html', form=form, incident=incident)
    
    
# working example    
    ImForm = model_form(models.Incident)
    incident = models.Incident.get(id=id)
    
    if request.method == 'POST':
        form = ImForm(request.form, obj=incident)
        if form.validate():
            form.populate_obj(incident)
            incident.save()
            flash('Incident Updated', 'success')
            return redirect(url_for('view_incident', id=incident.id))
    else:
        form = ImForm(obj=incident)
    return render_template('incident_edit.html', form=form, incident=incident)


# Delete Incident
@app.route('/incident/<int:id>/delete', methods=['POST'])
def delete_incident(id):
    models.Incident.get(id = id).delete_instance()
    
    flash('Incident deleted', 'success')
    return redirect(url_for('dashboard'))


# Mail Sender
@app.route('/mail_sender', methods=['GET', 'POST'])
def mail_sender():
    form = forms.MailForm()
    if form.validate_on_submit():
        title = form.title.data
        recipient = form.recipient.data
        content = form.content.data
        msg = Message(title, recipients=[recipient], bcc=["jakub_stanio@jabil.com"])
        msg.html = content
        mail.send(msg)
        flash("Email Sent", "success")
        return redirect(url_for('mail_sender'))
    return render_template('mail_sender.html', form=form)


# App Init
if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)


