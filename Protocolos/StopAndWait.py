import time
import random

class StopAndWaitSender:
    def __init__(self, tempo):
        self.timeout = tempo        # Tempo maximo de espera
        self.isTimerRunning = False # Se o tempo esta rodando
        self.temporizador = 0       #  Tempo do Sistema + time out

        self.waitingCall = True     # Sinaliza que espera enviar algo de cima
        self.ack = 0                # Primeiro envio tera seq 0

        self.sendPackage = []       # Sem pacotes para serem enviados de inicio
        self.receivedPackage = []   # Sem pacotes recebidos inicialmente

    def isWaitingCall(self):        # Esta esperando enviar algo?
        return self.waitingCall

    def make_pkt(self, data):
        self.sendPackage = [self.ack, data, len(data)] # cria pacote ( Ack, Data, CheckSum )
        return self.sendPackage
    
    def has_send(self):
        return (len(self.sendPackage) > 0)              # retorna verdadeiro se tem pacote a ser enviado

    def get_send(self):
        return self.sendPackage

    def send_package(self):
        self.waitingCall = False                            # Muda o estado para Wait Ack 0/1
        print("Sender: Sending Package ", self.sendPackage) 
        print("Sender: Now is waiting for Ack ", self.ack, "\n")

        self.receivedPackage = []   # reseta pacotes recebidos

    def receive_package(self, package):
        self.receivedPackage = package  # salva pacote recebido

        if(package[0] == self.ack):     # se recebeu o Ack aguardado
            print("Sender: received ACK ", package[0])

            if self.ack == 0:
                self.ack = 1
            else:
                self.ack = 0

        else:                           # se recebeu um Nak
            print("Sender: receveid Duplicated Package ", package, "\n")
    
    def has_received(self):
        return (len(self.receivedPackage) > 0)          # retorna verdadeiro se tem pacote recebido
    
    def isNak(self):
        return ( self.sendPackage[0] != self.receivedPackage[0] )
    
    def isCorrupt(self):
        return ( self.sendPackage[2] != self.receivedPackage[1] )

    def setWaitingCall(self, value):
        self.waitingCall = value
    
    def start_time(self, timerSystem):
        self.temporizador = timerSystem + self.timeout
        self.isTimerRunning = True

    def stop_time(self):
        self.isTimerRunning = False

    def isTimeOut(self, timerSystem):
        if (self.isTimerRunning and self.temporizador < timerSystem):
            print ("Sender: Time Out for package", self.sendPackage, "\n")
            return True
        else:
            return False


class StopAndWaitReceiver:
    def __init__(self):
        self.waitingCall = False     # Sinaliza que espera enviar algo de cima
        self.seq = 0                # Primeiro envio tera ack 0

        self.sendPackage = []       # Sem pacotes para serem enviados de inicio
        self.receivedPackage = []   # Sem pacotes recebidos inicialmente

        self.dataResult = ""        # Data Result apos o envio de todos os pacotes
        self.lastDuplicate = False

    def isWaitingCall(self):        # Esta esperando enviar algo?
        return self.waitingCall

    def make_pkt(self):
        self.sendPackage = [self.seq, len(self.receivedPackage[1])] # cria pacote ( Ack, Data, CheckSum )
        return self.sendPackage
    
    def has_send(self):
        return (len(self.sendPackage) > 0)              # retorna verdadeiro se tem pacote a ser enviado

    def get_send(self):
        return self.sendPackage

    def send_package(self):
        self.waitingCall = False                            # Muda o estado para Wait Ack 0/1
        print("Receiver: Sending Package ", self.sendPackage)

        if not self.lastDuplicate:
            if self.seq == 0:
                self.seq = 1
            else:
                self.seq = 0

        print("Receiver: Now is waiting for Seq ", self.seq, "\n")

        self.receivedPackage = []   # reseta pacotes recebidos

    def receive_package(self, package):
        self.receivedPackage = package  # salva pacote recebido

        if(package[0] == self.seq):     # se recebeu o Ack aguardado
            self.dataResult = self.dataResult + package[1]
            print("Receiver: received package ", package, "\n")
            self.lastDuplicate = False
        else:                           # se recebeu um Nak
            print("Receiver: receveid Duplicated Package ", package, "\n")
            self.lastDuplicate = True
    
    def has_received(self):
        return (len(self.receivedPackage) > 0)          # retorna verdadeiro se tem pacote recebido
    
    def isSeq(self):
        return ( self.seq == self.receivedPackage[0] )
    
    def setWaitingCall(self, value):
        self.waitingCall = value
    # def isCorrupt(self):
    #     return ( self.sendPackage[2] == self.receivedPackage[1] )

    def print_dataResult(self):
        print("Data Result: ", self.dataResult)
        

class Canal:
    def __init__(self):
        self.lista_pacotes = []

    def udt_send(self, package, sender, receiver, timeSystem):
        sender.send_package()
        self.lista_pacotes.append([package, receiver, timeSystem+2])
    
    def rdt_rcv(self, package, receiver):        
        receiver.receive_package(package)

    def encaminhando(self, timeSystem):
        i = 0
        while i != len(self.lista_pacotes):
            if self.lista_pacotes[i][2] < timeSystem:
                self.probabilidade_perda = random.randint(0,100)
                if self.probabilidade_perda < 50:
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
    sender = StopAndWaitSender(5)
    receiver = StopAndWaitReceiver()
    canal = Canal()
    #####################################

    #### MAIN LOOP ####
    while len(lista_dados) > 0 or not sender.isWaitingCall() or canal.hasEncaminhamento():
        startTime = time.time() # TIMER

        if sender.isWaitingCall():
            if len(lista_dados) > 0:
                package = sender.make_pkt(lista_dados.pop(0))
                canal.udt_send(package, sender, receiver, startTime)
                sender.start_time(startTime)

        else:
            if sender.has_received():
                sender.stop_time()
                if not sender.isNak() and not sender.isCorrupt():
                    sender.setWaitingCall(True)
                else:
                    package = sender.get_send()
                    canal.udt_send(package, sender, receiver, startTime)
                    sender.start_time(startTime)
            else:
                if sender.isTimeOut(startTime):
                    package = sender.get_send()
                    canal.udt_send(package, sender, receiver, startTime)
                    sender.start_time(startTime)
            
        if receiver.isWaitingCall():
            if receiver.has_received():
                package = receiver.make_pkt()
                canal.udt_send(package, receiver, sender, startTime)

        else:
            if receiver.has_received():
                if receiver.isSeq():
                    receiver.setWaitingCall(True)
                else:
                    package = receiver.get_send()
                    canal.udt_send(package, receiver, sender, startTime)

        canal.encaminhando(startTime)
        ####### PROTOCOL LOGIC ############
    
    receiver.print_dataResult()
    # receiver.printData()
    ######################################

main()