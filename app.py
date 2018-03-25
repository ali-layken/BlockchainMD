from flask import Flask, redirect, url_for, render_template, request, session
from forms import LoginForm
from tabledef import *
import helpers
import json
import os
import datetime
import updater
import downladUp

engine = db_connect ()
app = Flask(__name__)
app.config['UPLOADED_PATH'] = os.getcwd() + '/static/upload'

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
  if not session.get('logged_in'):
    form = LoginForm(request.form)
    if request.method == 'POST':
      username = request.form['username'].lower()
      password = request.form['password']
      if form.validate():
        if helpers.credentials_valid(username, password):
          session['logged_in'] = True
          session['username'] = username
          return json.dumps({'status': 'Login successful'})
        return json.dumps({'status': 'Invalid user/pass'})
      return json.dumps({'status': 'Both fields required'})
    return render_template('login.html', form=form)
  user = helpers.get_user()
  updater.update()
  return render_template('home.html', user=user)

@app.route("/logout")
def logout():
  session['logged_in'] = False
  return redirect(url_for('login'))

# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if not session.get('logged_in'):
    form = LoginForm(request.form)
    if request.method == 'POST':
      username = request.form['username'].lower()
      password = helpers.hash_password(request.form['password'])
      email = request.form['email']
      if form.validate():
        if not helpers.username_taken(username):
          helpers.add_user(username, password, email)
          session['logged_in'] = True
          session['username'] = username
          return json.dumps({'status': 'Signup successful'})
        return json.dumps({'status': 'Username taken'})
      return json.dumps({'status': 'User/Pass required'})
    return render_template('login.html', form=form)
  return redirect(url_for('login'))

# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
  if session.get('logged_in'):
    if request.method == 'POST':
      password = request.form['password']
      if password != "":
        password = helpers.hash_password(password)
      email = request.form['email']
      helpers.change_user(password=password, email=email)
      return json.dumps({'status': 'Saved'})
    user = helpers.get_user()
    return render_template('settings.html', user=user)
  return redirect(url_for('login'))

#------Upload-------------------------------------------------------------#
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if session.get('logged_in'):
      if request.method == 'POST':
        with open('temp.txt', 'r') as f:
          to = f.readline()
        user = helpers.get_user()
        for f in request.files.getlist('file'):
            f.save(os.path.join(app.config['UPLOADED_PATH'], str(datetime.datetime.now()) + ' from: ' + str(user.username) + ' to: ' + str(to) ))
      return render_template('upload.html')
    return redirect(url_for('login'))

@app.route('/recip', methods=['GET', 'POST'])
def recip():
    if session.get('logged_in'):
      if request.method == 'POST':
        to = request.form['recip']
        with open('temp.txt', 'w') as f:
          f.write(to)
        return render_template('upload.html')
      return render_template('recip.html')
    return redirect(url_for('login'))

#------Download-------------------------------------------------------------#
@app.route('/download', methods=['GET', 'POST'])
def download():
    if session.get('logged_in'):
      user = helpers.get_user().username
      downladUp.downlad(user)
      return render_template('download.html')
    return redirect(url_for('login'))

# ======== Main ============================================================== #
if __name__ == "__main__":
  app.secret_key = os.urandom(12) # Generic key for dev purposes only
  app.run(debug=True, use_reloader=True)