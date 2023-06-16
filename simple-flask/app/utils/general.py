from subprocess import CalledProcessError, check_output


def getGeneralStatus() -> dict:
    status = {}
    try:
        check_output(['ping', '-c', '1', 'google.com'])
        status["internet"] = 'Online'
    except CalledProcessError:
        status["internet"] = 'Offline'

    return status