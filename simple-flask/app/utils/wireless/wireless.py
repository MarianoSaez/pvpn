from subprocess import run
from re import findall, search, MULTILINE



class WLAN:
    def __init__(self, ssid, security, strength) -> None:
        self.ssid = ssid
        self.security = security
        self.strength = strength


def scan() -> list[WLAN]:
    raw_scan = run("iw wlan1 scan", shell=True, capture_output=True, text=True).stdout
    raw_wlan_list = raw_scan.split("BSS")
    wlan_list = []
    for raw_wlan in raw_wlan_list:
        ssid = search(r"SSID:(.+)", raw_wlan)
        security = search(r"RSN|WPA", raw_wlan)
        strength = search(r"signal:(.+)", raw_wlan)
        
        if ssid and security and strength:
            wlan_list.append(WLAN(ssid.group(1).strip(), security.group(0).strip(), strength.group(1).strip()))

    return wlan_list
