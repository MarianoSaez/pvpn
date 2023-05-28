from crypt import methods
from flask import render_template, session, redirect, url_for, request, escape
from flask_login import LoginManager, login_user, login_required, logout_user
from simplepam import authenticate
from .Uci import Uci
from app import app
from app.forms import LoginForm, PrivateNetworkParameters, VpnParameters, PublicNetworkParameters
from .models import User
from subprocess import run

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    # Logic to retrieve the user object based on the user_id
    # Return the User object if found, or None if not found
    return User(user_id)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    simpleForm = PrivateNetworkParameters()
    if simpleForm.validate_on_submit():

        u = Uci()
        for k, v in request.form.items():
            if v == "" or v == None: continue
            r = u.set('wireless', 'wifinet1', k, v)

    return render_template('simpleForm.html', form=simpleForm)


@app.route('/pubnet')
def pubnet():
    pass


@app.route('/vpn', methods=['GET', 'POST'])
def vpn():
    vpnForm = VpnParameters()

    if vpnForm.validate_on_submit():
        # Manejo del archivo
        file = request.files["file"]
        path = "/etc/openvpn/client.conf"
        auth_path = "/etc/openvpn/client.auth"
        username = request.form["username"]
        password = request.form["password"]
        
        file.save(path)

        with open(path, "a") as f:
            f.write(f"auth-user-pass {auth_path}")

        # Modificacion del archivo de auth
        with open(auth_path, "w+") as f:
            f.write(username)
            f.write(password)

        # Aplicar los cambios realizados
        run("/etc/init.d/openvpn restart", shell=True, capture_output=True, text=True)

        return redirect(url_for('vpn'))
        


    return render_template('vpnSettings.html', form=vpnForm)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if authenticate(str(username), str(password)):
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    # Remove the username from the session if it's there
    logout_user()
    return redirect(url_for('index'))

@app.route('/restart')
def restart():
    Uci().hardCommit()
    return redirect(url_for('index'))
