import socket
import pickle
import time

HEADERLEN= 9    #longeur d'entête de message, doit être pareil pour les clients

pingPong = {"ping": 0, "pong": 0}

#Création du server d'envoi
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Crée le socket de sortie
s.bind((socket.gethostname(),9001)) # crée le serveur local, it's over 9000!!!
s.listen(5) #limite le nombre de connexion ratée

#Receiver
r= socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #crée le socket de réception

fullMsg=b'' #variable de réception du message complet
new_msg=True        #booléen indiquant un nouveau message (le header a été détecté)
clientFound=False   #Un client a été trouvé et connecté au serveur de sortie
commandReceived=False   #Le message lu contient une commande
sendingCommand=True     #Phase d'envois de message
status= 'n'             #Status de réception (n= pas de commande, r= commande)
connectedForFeedback=False  #Connecté au client avec le receiver pour le feedback

#on roule en boucle constante
while True:

    if sendingCommand:
        #Si on est pas encore connecté à un client
        if not clientFound or not clientsocket :
            clientsocket, address = s.accept()  #on se connecte au client et on prend son adresse
            print("connection from {} has been estabished!".format(address))
            clientFound=True

        ready='r'   #Status indiquant que le message envoyé sera une commande
        pingPong["ping"]+=1 #on incremente ping
        msg = pickle.dumps(pingPong)  # transforme la strucutre en bytes
        #Transforme le Header en byte
        msg_head= bytes('{0:<{1}}{2}'.format(len(msg), HEADERLEN-1, ready), "utf-8")
        full_msg = msg_head+msg #message complet

        #ici msg est deja en bytes, prêt à être envoyé
        clientsocket.send(full_msg)
        sendingCommand=False #on a fini la phase d'envoi, on attend le feedback

    #On se connecte au client pour feedback
    if not connectedForFeedback and clientFound:
        r.connect((socket.gethostname(), 9002))  # serveur local, it's over 9000
        connectedForFeedback=True

    #Sinon on écoute pour un feedback
    else:
        msg = r.recv(10)    #on reçoit le message 10 bytes à la fois (peut être augmenté)
        #Si la commande n'a pas encore été recue, on regarde le header du status
        if not commandReceived:
            status = msg[HEADERLEN - 1:HEADERLEN].decode("utf-8")

        #Si le status est pour une commande ou que la commande est deja en lecture
        if status == 'r' or commandReceived:
            commandReceived = True
            #si c'est le debut d'un message
            if new_msg:
                #on prend la longeur de l'information (en bytes) dans le header
                msgLen = int(msg[:HEADERLEN - 2])
                print("new message Lenght : {}".format(msgLen))
                new_msg = False

            #on constitue le message
            fullMsg += msg

            #si on a tous le message
            if len(fullMsg) - HEADERLEN == msgLen:
                print("full msg received")

                #on décompresse le pickle pour avoir accès à l'info
                pingPong = pickle.loads(fullMsg[HEADERLEN:])
                print(pingPong)
                time.sleep(1)   #on fait une pause d'une seconde
                #on remets les valeurs par défaut pour la réception de nouveaux messages
                new_msg = True
                fullMsg = b''
                sendingCommand = True
