import socket
import pickle

HEADERLEN=9

#receiver
r= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect((socket.gethostname(),9001)) # serveur local, it's over 9000

#Création du server d'envoi
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Crée le socket de sortie
s.bind((socket.gethostname(),9002)) # crée le serveur local, it's over 9000!!!
s.listen(5) #limite le nombre de connexion ratée


fullMsg=b''
new_msg=True
status= 'n'
readyForFeedBack=False
clientFound=False
commandReceived=False

while True :
    msg = r.recv(10)  # on reçoit le message 10 bytes à la fois (peut être augmenté)
    # Si la commande n'a pas encore été recue, on regarde le header du status
    if not commandReceived:
        status = msg[HEADERLEN - 1:HEADERLEN].decode("utf-8")

    # Si le status est pour une commande ou que la commande est deja en lecture
    if status == 'r' or commandReceived:
        commandReceived = True
        # si c'est le debut d'un message
        if new_msg:
            # on prend la longeur de l'information (en bytes) dans le header
            msgLen = int(msg[:HEADERLEN - 2])
            print("new message Lenght : {}".format(msgLen))
            new_msg = False

        # on constitue le message
        fullMsg += msg

        # si on a tous le message
        if len(fullMsg) - HEADERLEN == msgLen:
            print("full msg received")

            # on décompresse le pickle pour avoir accès à l'info
            d = pickle.loads(fullMsg[HEADERLEN:])
            print(d)

            # on remets les valeurs par défaut pour la réception de nouveaux messages
            new_msg = True
            fullMsg = b''
            readyForFeedBack=True

    if readyForFeedBack:
        #Sending feedback
        # Si on est pas encore connecté à un client
        if not clientFound or not clientsocket:
            clientsocket, address = s.accept()  # on se connecte au client et on prend son adresse
            print("connection from {} has been estabished!".format(address))
            clientFound = True

        ready = 'r'  # Status indiquant que le message envoyé sera une commande
        d["pong"] += 1  # on incremente ping
        msg = pickle.dumps(d)  # transforme la strucutre en bytes
        # Transforme le Header en byte
        msg_head = bytes('{0:<{1}}{2}'.format(len(msg), HEADERLEN - 1, ready), "utf-8")
        full_msg = msg_head + msg  # message complet

        # ici msg est deja en bytes, prêt à être envoyé
        clientsocket.send(full_msg)
        readyForFeedBack=False

