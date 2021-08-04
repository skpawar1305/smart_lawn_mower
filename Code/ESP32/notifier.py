import urequests

class Notifier():
    def robot_lifted():
        ifttt_url = 'https://maker.ifttt.com/trigger/mower_lifted/with/key/ECCmPEgWVIuP6O88PVuKa'
        send_message = urequests.get(ifttt_url)
        send_message.close()