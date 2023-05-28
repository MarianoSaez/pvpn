from subprocess import run


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
        r = run("reboot", shell=True, capture_output=True, text=True)
        return

