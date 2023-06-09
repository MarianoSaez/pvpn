from requests import get, RequestException
from subprocess import run

def getVPNDetails() -> dict:
    status = {}

    # Obtener datos de la IP publica
    try:
        response = get("https://ifconfig.co/json")
        if response.status_code == 200:
            status["ip"] = response.json()["ip"]
            status["country"] = response.json()["country"]
    except RequestException:
        status["ip"] = "Unknown"
        status["country"] = "Unknown"

    # Obtener datos del servicio openvpn
    output = run("ifconfig", shell=True, capture_output=True, text=True).stdout
    status["vpnstatus"] = "Enabled" if "tun" in output else "Disabled"

    return status


