from flask import Flask, request, render_template, url_for, redirect, flash, session, logging
from peewee import *
from wtfpeewee.orm import model_form

import models
import forms

app = Flask(__name__)
app.secret_key = "big_secret123"


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
#    form = forms.IncidentForm()
#    incident = models.Incident.select().where(models.Incident.id ** id).get()
    
    # Populate incident form fields
#    form.incident.data = incident.incident
#    form.description.data = incident.description
#    form.url.data = incident.url
    
    ImForm = model_form(models.Incident)
    
    
    incident = models.Incident.get(id=id)
    
    if request.method == 'POST':
        form = ImForm(request.form, obj=incident)
        if form.validate():
            form.populate_obj(incident)
            incident.save()
            flash('Your entry has been saved', 'success')
            return redirect(url_for('view_incident', id=incident.id))
    else:
        form = ImForm(obj=incident)
    return render_template('incident_edit.html', form=form, incident=incident)
    
    
#    if form.validate_on_submit():
#       
#        
#        incident.save()
#        
#        flash("Incidend Updated", 'success')
#        return redirect(url_for('view_incident', id=incident.id))
#    return render_template('incident_edit.html', form=form, incident=incident)

# App Init
if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)


