from subprocess import run
from re import findall, search, MULTILINE
from json import loads



class WLAN:
    def __init__(self, ssid, security, strength) -> None:
        self.ssid = ssid
        self.security = security
        self.strength = strength

    def to_dict(self) -> dict:
        return {
            "ssid": self.ssid,
            "security": self.security,
            "strength": self.strength
        }


def scan() -> list[WLAN]:
    raw_scan = run("iw wlan1 scan", shell=True, capture_output=True, text=True)
    if raw_scan.returncode != 0:
        run("uci delete wireless.@wifi-iface[2].ssid", shell=True, capture_output=True, text=True)
        run("uci delete wireless.@wifi-iface[2].key", shell=True, capture_output=True, text=True)
        run("uci commit wireless", shell=True, capture_output=True, text=True)
        
    raw_wlan_list = raw_scan.stdout.split("BSS")
    wlan_list = []
    for raw_wlan in raw_wlan_list:
        ssid = search(r"SSID:(.+)", raw_wlan)
        security = search(r"RSN|WPA", raw_wlan)
        strength = search(r"signal:(.+)", raw_wlan)
        
        if ssid and security and strength:
            wlan_list.append(WLAN(ssid.group(1).strip(), security.group(0).strip(), strength.group(1).strip()))

    return wlan_list

def getPubWLANDetails() -> dict:
    status = {}
    output = run("wifi status", shell=True, capture_output=True, text=True).stdout
    data = loads(output)
    # Obtener estado referido a la red publica
    if data["radio1"]["up"] == False and data["radio1"]["pending"] == False:
        status["pubwlanstatus"] = "Disabled"
    elif data["radio1"]["up"] == False and data["radio1"]["pending"] == True:
        status["pubwlanstatus"] = "Pending"
    else:
        status["pubwlanstatus"] = "Enabled"

    # Obtener nombre de la red
    wlan_config = data["radio1"]["interfaces"][0]["config"]
    status["pubwlanssid"] = wlan_config["ssid"]

    return status

def getPrivWLANSDetails() -> dict:
    status = {}
    output = run("wifi status", shell=True, capture_output=True, text=True).stdout
    data = loads(output)
    # Obtener estado referido a la red publica
    if data["radio0"]["up"] == False and data["radio0"]["pending"] == False:
        status["privwlanstatus"] = "Disabled"
    elif data["radio0"]["up"] == False and data["radio0"]["pending"] == True:
        status["privwlanstatus"] = "Pending"
    else:
        status["privwlanstatus"] = "Enabled"

    # Obtener nombre de la red
    wlan_config = data["radio0"]["interfaces"][0]["config"]
    status["privwlanssid"] = wlan_config["ssid"]

    output = run("iwinfo wlan0 assoclist", shell=True, capture_output=True, text=True).stdout
    clients = findall(r"(?:[0-9A-F]{2}:){5}[0-9A-F]{2}.*", output)
    status["clients"] = clients


    return status
