from subprocess import run


class Uci:
    def get(self, configFile, section, option):
        command = f"uci get {configFile}.{section}.{option}"
        r = run(command)
        return r.stdout

    def set(self, configFile, section, option, value):
        command = f"uci set {configFile}.{section}.{option}='{value}' && uci commit {configFile}"
        r = run(command)
        return r.stdout
