import time
import random

class GoBackNSender:
    def __init__(self, tempo):
        self.timeout = tempo        # Tempo maximo de espera
        self.isTimerRunning = False # Se o tempo esta rodando
        self.temporizador = 0       #  Tempo do Sistema + time out

        self.waitingCall = True     # Sinaliza que espera enviar algo de cima
        
        self.sendPackage = []      # Janela de Pacotes vazia
        self.sendedPackages = []    # Janela ja enviada
        self.receivePackages = []   # Janela de Acks vazia
        self.confirmedPackages = [] # Lista de pacotes confirmados em Ack

        self.seq = 0

    def isWaitingCall(self):        # Esta esperando enviar algo?
        return self.waitingCall

    def make_pkt(self, data):
        self.sendPackage = [self.seq, data, len(data)]   # Adiciona pacote na Janela
        self.seq = self.seq + 1                                 # seq++
        return self.sendPackage      # retorna o ultimo pacote adicionado ( este )

    def send_package(self):
        
        print("Sender: sending package ", self.sendPackage)
        self.sendedPackages.append(self.sendPackage)           # adicionar a Janela de ja enviado

        self.waitingCall = False
        self.sendPackage = []                      # reseta Janela de Pacotes

    def receive_package(self, package):
        self.receivePackages.append(package)
        confirmou = False
        for i in self.confirmedPackages:
            if i[0] == package[0]:
                confirmou = True
                break
        
        if not confirmou:
            print("Sender: received Ack ", package[0])
        else:
            print("Sender: received Package Duplicated ", package)
        

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


class GoBackNReceiver:
    def __init__(self):
        self.waitingCall = False     # Sinaliza que espera algum Dado
        
        self.sendPackage = []      # Janela de Pacotes vazia
        self.sendedPackages = []    # Janela ja enviada
        self.receivePackages = []   # Janela de Acks vazia
        self.confirmedPackages = [] # Lista de pacotes confirmados em Ack

        self.seq = 0

        self.dataResult = ""

    def isWaitingCall(self):        # Esta esperando enviar algo?
        return self.waitingCall

    def make_pkt(self, data):
        self.sendPackage = [self.seq, data, len(data)]   # Adiciona pacote na Janela
        self.seq = self.seq + 1                          # seq++
        return self.sendPackage                          # retorna o ultimo pacote adicionado ( este )

    def send_package(self):
        print("Receiver: sending package ", self.sendPackage)
        self.sendedPackages.append(self.sendPackage)           # adicionar a Janela de ja enviado

        self.waitingCall = False
        self.sendPackage = []                      # reseta Janela de Pacotes

    def receive_package(self, package):
        self.receivePackages.append(package)

        ## verifica se ja foi confirmado essa SEQ ##
        confirmou = False
        for i in self.confirmedPackages:
            if i[0] >= package[0]:
                confirmou = True
                break
            
        ## verifica se esta fora de sequencia ##
        if not confirmou and len(self.confirmedPackages) > 0:
            if package[0] > self.confirmedPackages[len(self.confirmedPackages)-1][0] + 1:
                confirmou = True

        if not confirmou:
            print("Receiver: received Seq ", package[0])
            
        else:
            print("Receiver: received Package Duplicated ", package)
        

    def setWaitingCall(self, value):
        self.waitingCall = value

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
                # if self.probabilidade_perda < 0:
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
    sender = GoBackNSender(5)
    receiver = GoBackNReceiver()
    canal = Canal()
    #####################################

    #### MAIN LOOP ####
    while len(lista_dados) > 0 or not sender.isWaitingCall() or canal.hasEncaminhamento():
        startTime = time.time() # TIMER

        if sender.isWaitingCall():
            i = 0
            while i != 4 and len(lista_dados) > 0:
                package = sender.make_pkt(lista_dados.pop(0))
                canal.udt_send(package, sender, receiver, startTime)
                sender.start_time(startTime)
                i = i + 1

        if receiver.isWaitingCall():
            break

        canal.encaminhando(startTime)
        ####### PROTOCOL LOGIC ############
    
    receiver.print_dataResult()
    # receiver.printData()
    ######################################

main()