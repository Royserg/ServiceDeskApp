from flask import Flask, request, render_template, url_for, redirect, flash, session, logging

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
@app.route('/view_incident/<int:incident_id>')
def view_incident(incident_id):
    incident = models.Incident.select().where(models.Incident.id ** incident_id).get()
    return render_template('view_incident.html', incident=incident)



# App Init
if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)


