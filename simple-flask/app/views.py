from flask import render_template, session, redirect, url_for, request, escape
from simplepam import authenticate
from .Uci import Uci
from app import app
from app.forms import LoginForm, PrivateNetworkParameters

@app.route('/', methods=['GET', 'POST'])
def index():
    simpleForm = PrivateNetworkParameters()
    simpleForm.ssid.data = 'prueba_de_valores_por_defecto'
    
    if 'username' in session:
        if simpleForm.validate_on_submit():
            ssid = simpleForm.ssid.data
            password = simpleForm.new_password.data
            vpn_config = simpleForm.vpn_config.data

            # Hacer cosas con las configuraciones provistas
            u = Uci()
            r = u.get('network', 'lan', 'type')
            print(r)

        return render_template('simpleForm.html', form=simpleForm)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if authenticate(str(username), str(password)):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    # Remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

