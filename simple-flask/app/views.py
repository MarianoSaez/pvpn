from flask import render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user
from simplepam import authenticate

from app.utils.wireless.wireless import scan
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
    return User(user_id)

# Autenticacion

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
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Dashboard

@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")


# Red privada

@app.route('/privnet', methods=['GET', 'POST'])
@login_required
def index():
    simpleForm = PrivateNetworkParameters()
    if simpleForm.validate_on_submit():

        u = Uci()
        for k, v in request.form.items():
            if v == "" or v == None: continue
            r = u.set('wireless', 'wifinet1', k, v)

    return render_template('simpleForm.html', form=simpleForm)


# Red publica

@app.route('/pubnet', methods=["GET", "POST"])
@login_required
def pubnet():
    pubForm = PublicNetworkParameters()
    wlan_list = scan()
    if request.method == "POST":
        u = Uci()
        u.set("wireless", "wifinet2", "ssid", request.form["ssid"])
        u.set("wireless", "wifinet2", "key", request.form["key"])
        u.hardCommit()
    return render_template('publicNetworkSettings.html', form=pubForm, wlan_list=wlan_list)


# VPN

@app.route('/vpn', methods=['GET', 'POST'])
@login_required
def vpn():
    vpnForm = VpnParameters()

    if vpnForm.validate_on_submit():
        file = request.files["file"]
        base_path = "/etc/openvpn/"
        conf = "client.conf"
        auth = "client.auth"
        username = request.form["username"]
        password = request.form["password"]
        
        file.save(base_path + conf)

        with open(base_path + conf, "a") as f:
            f.write(f"auth-user-pass {auth}")

        with open(base_path + auth, "w+") as f:
            f.write(username + "\n")
            f.write(password)

        run("/etc/init.d/openvpn restart", shell=True, capture_output=True, text=True)

        return redirect(url_for('vpn'))

    return render_template('vpnSettings.html', form=vpnForm)

@app.route('/restart')
@login_required
def restart():
    Uci().hardCommit()
    return redirect(url_for('index'))
