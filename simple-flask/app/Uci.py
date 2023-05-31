from subprocess import run, Popen
from shlex import split


class Uci:
    def get(self, configFile, section, option):
        command = f"uci get {configFile}.{section}.{option}"
        r = run(command, shell=True, capture_output=True, text=True)
        return r.stdout

    def set(self, configFile, section, option, value):
        command = f"uci set {configFile}.{section}.{option}='{value}' && uci commit {configFile}"
        r = run(command, shell=True, capture_output=True, text=True)
        return r.stdout

    def hardCommit(self):
        # r = run("reboot && /etc/init.d/flask_app stop", shell=True, capture_output=True, text=True)
        Popen(split("/sbin/reboot"))
        Popen(split("/etc/init.d/flask_app stop"))
        return

