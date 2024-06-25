import socket
import base64

class PlexusClient:
    def __init__(self, host:str, port:int, password:str, recv:int):
        self.host = host
        self.port = port
        self.password = password
        self.recv = recv
        self.version = "PyPlexusDB v1.0"
        self.ERR_REQUEST_MISS = "ERROR: Server miss the request."
        self.SUCCESS = "SUCCESS: Operation completed."
        self.ERR_WRONG_PWD = "ERROR: Wrong password for server."

    def exquery(self, command: str):
        command = command.replace(' ', ';s;')
        s = socket.socket()
        s.connect((self.host, self.port))
        s.send(f"{self.password};s;{command}".encode())
        if command.split("\n")[0] == "SETATTRIB" and command.split("\n")[3] == "sys-name":
            raise NameError("Attribute name 'sys-name' is not accepted.")
        r = s.recv(self.recv).decode()
        s.close()
        if r == "<pdb.SUCCESS>":
            return self.SUCCESS
        elif r == "<pdb.ERR_REQUEST_MISS>":
            return self.ERR_REQUEST_MISS
        elif r == "<pdb.ERR_WRONG_PWD>":
            return self.ERR_WRONG_PWD
        else:
            return r

    def ping(self):
        s = socket.socket()
        try:
            s.connect((self.host, self.port))
            s.close()
            return True
        except:
            s.close()
            return False


    def query(self, command: str):
        command = command.replace(' ', ';s;')
        s = socket.socket()
        s.connect((self.host, self.port))
        s.send(f"{self.password};s;{command}".encode())
        if command.split("\n")[0] == "SETATTRIB" and command.split("\n")[3] == "sys-name":
            raise NameError("Attribute name 'sys-name' is not accepted.")
        s.close()
