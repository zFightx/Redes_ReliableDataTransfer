import threading
import time
import random

class StopAndWaitSender:
    def __init__(self, tempo):
        self.waiting0 = False
        self.waiting1 = False
        self.waitingCall = True
        self.tempo = tempo
        
        self.rcvPkt = []        # pacote recebido
        self.hasRcvPkt = False

        self.sndpackage = []    # pacote enviado

        self.isTimeRuning = False

    def isWaiting0(self):
        return self.waiting0
    
    def isWaiting1(self):
        return self.waiting1
    
    def isWaitingCall(self):
        return self.waitingCall
    
    def start_time(self, timerSystem):
        self.temporizador = timerSystem + self.tempo
        self.isTimeRuning = True
    
    def stop_time(self):
        self.isTimeRuning = False

    def make_pkt(self, ack, data, checksum):
        self.sndpackage = [ack, data, checksum]

    def getSndPackage(self):
        return self.sndpackage

    def sendPackage(self, package):
        self.rcvPkt = []
        self.hasRcvPkt = False

        if package[0] == 0:
            self.waiting0 = True
        else:
            self.waiting1 = True
        
        self.waitingCall = False

        print("Sender: Sending Package " , package, "\n")

    def receiverPackage(self, package):
        self.rcvPkt = package
        self.hasRcvPkt = True
        
        if self.rcvPkt[1] != self.sndpackage[2]:
            print("Sender: Receive Package Corrupt ", self.rcvPkt, )

        else:
            if self.rcvPkt[0] == 0 and self.waiting0:
                self.waiting0 = False
                self.waitingCall = True
                self.isTimeRuning = False
                print("Sender: Received Package " , package, "\n")
            elif self.rcvPkt[0] == 1 and self.waiting1:
                self.waiting1 = False
                self.waitingCall = True
                self.isTimeRuning = False
                print("Sender: Received Package " , package, "\n")
            else:
                print("Sender: Received Duplicated Package " , package, "\n")
            

    def hasReceivedPackage(self):
        return self.hasRcvPkt
    
    def isNak(self):
        if self.waiting0 and self.rcvPkt[0] == 0:
            return False
        elif self.waiting1 and self.rcvPkt[0] == 1:
            return False
        else:
            return True

    def isCorrupted(self):
        return self.rcvPkt[1] != self.sndpackage[2]

    def isTimeOut(self, timerSystem):
        if self.temporizador < timerSystem and self.isTimeRuning:
            print("Sender: Time Out Package ", self.sndpackage)
            return True
        else:
            return False


class StopAndWaitReceiver:
    def __init__(self):
        self.waiting0 = True
        self.waiting1 = False
        self.waitingCall = False
        self.dataResult = ""

        self.rcvPkt = []
        self.hasRcvPkt = False

    def isWaiting0(self):
        return self.waiting0
    
    def isWaiting1(self):
        return self.waiting1
    
    def isWaitingCall(self):
        return self.waitingCall

    def make_pkt(self, ack, checksum):
        self.sndpackage = [ack, checksum]

    def getSndPackage(self):
        return self.sndpackage

    def sendPackage(self, package):
        self.rcvPkt = []
        self.hasRcvPkt = False

        if package[0] == 0:
            self.waiting1 = True
        else:
            self.waiting0 = True
        
        self.waitingCall = False
        print("Receiver: Sending Package " , package, "\n")

    def receiverPackage(self, package):        
        self.rcvPkt = package
        self.hasRcvPkt = True

        if self.rcvPkt[0] == 0 and self.waiting0:
            self.waiting0 = False
            self.waitingCall = True
            self.dataResult = self.dataResult + self.rcvPkt[1]
            
            print("Receiver: Received Package " , package, "\n")
        elif self.rcvPkt[0] == 1 and self.waiting1:
            self.waiting1 = False
            self.waitingCall = True
            self.dataResult = self.dataResult + self.rcvPkt[1]
        
            print("Receiver: Received Package " , package, "\n")
        else:
            self.sendPackage(self.rcvPkt)
            print("Receiver: Received Duplicated Package " , package, "\n")

    def hasReceivedPackage(self):
        return self.hasRcvPkt
    
    def hasSeq(self):
        if len(self.rcvPkt) == 0:
            return True

        if self.waiting0 and self.rcvPkt[0] == 0:
            return False
        elif self.waiting1 and self.rcvPkt[0] == 1:
            return False
        else:
            return True
    
    def getRcvPkt(self):
        return self.rcvPkt

    def printData(self):
        print("Data: " , self.dataResult)

class Canal:
    def __init__(self):
        self.lista_pacotes = []

    def udt_send(self, package, sender, receiver, timeSystem):
        self.tempo_chegada = random.randint(2,4)
        sender.sendPackage(package)
        self.lista_pacotes.append([package, receiver, timeSystem+self.tempo_chegada])
    
    def rdt_rcv(self, package, receiver):        
        receiver.receiverPackage(package)

    def encaminhando(self, timeSystem):
        i = 0
        while i != len(self.lista_pacotes):
            if self.lista_pacotes[i][2] < timeSystem:
                self.probabilidade_perda = random.randint(0,4)
                if self.probabilidade_perda != 3:
                    self.rdt_rcv(self.lista_pacotes[i][0], self.lista_pacotes[i][1])

                self.lista_pacotes.pop(i)
                i = i - 1

            i = i + 1
    
    def hasEncaminhamento(self):
        return len(self.lista_pacotes) > 0

def main():
    print("Redes de Computadores - UnB")

    ## DADOS QUE QUEREMOS ENVIAR ##
    dados = "Eduardo e Monica e Alexandre estavam numa festa"
    lista_dados = []
    while len(dados) > 0:
        if len(dados) >= 8:
            lista_dados.append(dados[:8])
            dados = dados[8:]
        else:
            lista_dados.append(dados[:len(dados)])
            dados = ""
    #####################################

    ## PROTOCOLOS ##
    sender = StopAndWaitSender(8)
    receiver = StopAndWaitReceiver()
    canal = Canal()

    Ack = 0
    #####################################

    #### MAIN LOOP ####
    while len(lista_dados) > 0 or not sender.isWaitingCall():
        startTime = time.time() # TIMER

        if sender.isWaitingCall():
            if len(lista_dados) > 0:
                sender.make_pkt(Ack, lista_dados.pop(0), 8)
                canal.udt_send(sender.getSndPackage(), sender, receiver, startTime)
                sender.start_time(startTime)

                if Ack == 0:
                    Ack = 1
                else:
                    Ack = 0
        else:
            if sender.hasReceivedPackage():
                if sender.isCorrupted() or sender.isNak():
                    canal.udt_send(sender.getSndPackage(), sender, receiver, startTime)
                    sender.start_time(startTime)
            elif sender.isTimeOut(startTime):
                canal.udt_send(sender.getSndPackage(), sender, receiver, startTime)
                sender.start_time(startTime)

        if receiver.isWaitingCall():
            if receiver.hasReceivedPackage():
                if receiver.hasSeq():
                    receiver.make_pkt(receiver.getRcvPkt()[0], receiver.getRcvPkt()[2])
                    canal.udt_send(receiver.getSndPackage(), receiver, sender, startTime)

        else:
            if receiver.hasReceivedPackage():
                if not receiver.hasSeq():
                    canal.udt_send(receiver.getSndPackage(), receiver, sender, startTime)


        canal.encaminhando(startTime)
        ####### PROTOCOL LOGIC ############
        
    receiver.printData()
    ######################################

main()