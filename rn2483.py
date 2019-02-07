import serial
import time
import binascii

# Gateway IDs
DEV_UI = "0004A30B001B44A6"
APP_UI = "0000000000000000"
APP_KEY = "d0e946f00cff1103a79e9a0196d8dcff"

# Serial propriety
SERIAL_PORT = "/dev/ttyUSB0"
BAUDRATE = 57600

# Config lora
config = [

    "mac set deveui " + DEV_UI,
    "mac set appeui " + APP_UI,
    "mac set appkey " + APP_KEY,

    "mac set dr 0",
    "mac set adr on",
    "mac set bat 127",
    "mac set retx 2",
    "mac set linkchk 100",
    "mac set rxdelay1 1000",
    "mac set ar on",
    "mac get rx2 868",
    "mac set rx2 3 869525000",

    # set DC to 50%
    "mac set ch dcycle 0 1",
    "mac set ch dcycle 1 1",
    "mac set ch dcycle 2 1",

    "mac save",
]


class Lora():

    def __init__(self):

        print("initialisation port serial ...")
        self.ser = serial.Serial(
                    port=SERIAL_PORT,
                    baudrate=BAUDRATE)

        print("terminé ")

    def get_info_device(self):
        """
        Retourne les informations du module RN2483
        """

        self.exec_serial_cmd("sys get ver")
        self.exec_serial_cmd("sys get vdd")
        self.exec_serial_cmd("sys get hweui")

    def get_keys(self):
        """
        Retourne les clefs enregistrés sur le module RN2483
        """

        self.exec_serial_cmd("mac get deveui")
        self.exec_serial_cmd("mac get appkey")
        self.exec_serial_cmd("mac get appeui")

    def exec_serial_cmd(self, cmd, get_response=False):
        """
        Exécute des commandes sur le port usb serial, et affiche la réponse
        Si get_response=True, la fonction renvoie la réponse
        """

        # execute cmd
        self.ser.write(str.encode(cmd+"\r\n"))
        cmd.rstrip()
        print(cmd)

        time.sleep(0.1)

        # get response
        rdata = self.readline()
        print(rdata)

        if get_response:
            return rdata

    def factory_reset(self):
        """
        Reset le module RN2483
        """

        self.exec_serial_cmd("sys factoryRESET")

        print("Reset effectué, il faut reconfigurer la couche mac")

    def config__mac(self):
        """
        Configure le module RN2483 selon les commandes dans la variable globale config
        """

        for conf_cmd in config:
            self.exec_serial_cmd(conf_cmd)

    def join(self):
        """
        Effectue un 'mac join otaa' pour 'se connecter' avec le gateway
        """

        rdata = self.exec_serial_cmd("mac join otaa", get_response=True)

        if rdata == "ok":

            print("wait for response ...")
            rdata = self.readline()
            print(rdata)

            if rdata != "accepted":
                print("new try...")
                self.join()

    def test_uplink(self):
        """
        Procédure de test d'envoie de data
        """

        self.exec_serial_cmd("mac tx cnf 1 01020304")
        rdata = self.readline()
        print(rdata)

        print("wait for 2nd test ...")
        time.sleep(5)

        self.exec_serial_cmd("mac tx uncnf 1 05060708")
        rdata = self.readline()
        print(rdata)

    def pause(self):
        """
        Execute 'mac pause'
        """

        self.exec_serial_cmd("mac pause")

    def resume(self):
        """
        Execute 'mac resume'
        """

        self.exec_serial_cmd("mac resume")

    def send_radio(self, data):
        """
        Envoie des data avec la commande radio tx
        """

        rdata= self.exec_serial_cmd("radio tx {}".format(binascii.hexlify(data.encode('utf-8')).decode()), get_response=True)
        if rdata == 'ok':
            rdata = self.readline()
            print(rdata)
        print("wait 5s before sending next message ...")
        time.sleep(5)

    def send(self, data):
        """
        Envoie des data avec la commande max tx cnf 1
        """

        rdata = self.exec_serial_cmd("mac tx cnf 1 {}".format(binascii.hexlify(data.encode('utf-8')).decode()),
                                     get_response=True)
        while rdata != 'ok':
            rdata = self.readline()
            time.sleep(5)
            print(rdata)
            rdata = self.exec_serial_cmd("mac tx cnf 1 {}".format(binascii.hexlify(data.encode('utf-8')).decode()),
                                         get_response=True)

        rdata = self.readline()
        time.sleep(5)
        print(rdata)


    def readline(self):
        """
        Retourne les réponses du port serial
        """

        return self.ser.readline()[:-2].decode('UTF-8')
