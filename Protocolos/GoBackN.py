import time
import random

class GoBackNSender:
    def __init__(self, tempo, janela):
        self.nextSeqNum = 0
        self.base = 0
        self.maxJanela = janela

        self.janela = []

        self.sendPackage = []
        self.rcvPackage = []

        self.timeout = tempo
        self.temporizador = 0
        self.isTimerRunning = False

    def has_data(self):
        return self.nextSeqNum < len(self.janela)

    def get_nextseq(self):
        return self.nextSeqNum
    
    def set_nextseq(self, value):
        self.nextSeqNum = value
    
    def get_base(self):
        return self.base
    
    def set_base(self, value):
        self.base = value

    def get_janela(self):
        return self.maxJanela

    def add_janela(self, data):
        self.janela.append(data)

    def make_pkt(self):
        self.sendPackage.append([self.nextSeqNum, self.janela[self.nextSeqNum], len(self.janela[self.nextSeqNum])])
        return self.sendPackage
    
    def has_send(self):
        return (self.nextSeqNum < self.base + self.maxJanela and len(self.janela) > self.nextSeqNum)
    
    def send_package(self, package):
        print("Sender: sending package ", package)
        self.rcvPackage = []

    def get_send(self):
        return self.sendPackage
    
    def receive_package(self, package):
        self.rcvPackage = package
        if package[0] == self.base:
            print("Sender: received ACK ", package[0])
            self.base = self.base + 1
        else:
            if package[0] < self.base:
                print("Sender: received Duplicated Package ", package)
            else:
                print("Sender: received a discarted package ", package)

    def has_receive(self):
        return (len(self.rcvPackage) > 0)

    def start_timer(self, timerSystem):
        self.temporizador = timerSystem + self.timeout
        self.isTimerRunning = True
    
    def stop_timer(self):
        self.isTimerRunning = False

    def isTimeOut(self, timerSystem):
        if self.temporizador < timerSystem and self.isTimerRunning:
            print("Sender: Time Out")
            return True
        else:
            return False

class GoBackNReceiver:
    def __init__(self):
        self.expectedSeqNum = 0

        self.sendPackage = []
        self.rcvPackage = []

        self.dataResult = ""

    def get_expectedseq(self):
        return self.expectedSeqNum
    
    def set_expectedseq(self, value):
        self.expectedSeqNum = value

    def make_pkt(self):
        self.sendPackage = [self.expectedSeqNum, 8]
        return self.sendPackage

    def send_package(self, package):
        print("Receiver: sending package ", package)
        self.rcvPackage = []

    def get_send(self):
        return self.sendPackage

    def receive_package(self, package):
        self.rcvPackage.append(package)

    def get_receive(self):
        return self.rcvPackage

    def has_receive(self):
        return ( len(self.rcvPackage) > 0 )

    def verify_discard(self,package):
        if package[0] == self.expectedSeqNum:
            print("Receiver: received package ", package)
            self.dataResult = self.dataResult + package[1]
            return False
        else:
            print("Receiver: discard package ", package) 
            return True

    def print_dataResult(self):
        print("Data Result: ", self.dataResult)
    
    def get_dataResult(self):
        return self.dataResult

class Canal:
    def __init__(self):
        self.lista_pacotes = []

    def udt_send(self, package, sender, receiver, timeSystem):
        sender.send_package(package)
        self.lista_pacotes.append([package, receiver, timeSystem+2])
    
    def rdt_rcv(self, package, receiver):        
        receiver.receive_package(package)

    def encaminhando(self, timeSystem):
        i = 0
        while i != len(self.lista_pacotes):
            if self.lista_pacotes[i][2] < timeSystem:
                self.probabilidade_perda = random.randint(0,100)
                if self.probabilidade_perda < 80:
                    self.rdt_rcv(self.lista_pacotes[i][0], self.lista_pacotes[i][1])

                self.lista_pacotes.pop(i)
                i = i - 1

            i = i + 1
    
    def hasEncaminhamento(self):
        return len(self.lista_pacotes) > 0

def main():
    print("Redes de Computadores - UnB")

    ## PROTOCOLOS ##
    sender = GoBackNSender(5,4)
    receiver = GoBackNReceiver()
    canal = Canal()
    #####################################

    ## DADOS QUE QUEREMOS ENVIAR ##
    dados = "Eduardo e Monica e Alexandre estavam numa festa"
    dados2 = "Eduardo e Monica e Alexandre estavam numa festa"
    
    while len(dados) > 0:
        if len(dados) >= 8:
            sender.add_janela(dados[:8])
            dados = dados[8:]
        else:
            sender.add_janela(dados[:len(dados)])
            dados = ""
    #####################################

    #### MAIN LOOP ####
    while receiver.get_dataResult() != dados2:
        startTime = time.time() # TIMER

        if sender.has_send():
            package = sender.make_pkt()[sender.get_nextseq()]
            # sender.send_package(package)
            canal.udt_send(package, sender,receiver, startTime)

            if sender.get_base() == sender.get_nextseq():
                sender.start_timer(startTime)
            
            sender.set_nextseq(sender.get_nextseq()+1)
        
        if sender.isTimeOut(startTime):
            base = sender.get_base()
            nextseq = sender.get_nextseq()
            sndpkt = sender.get_send()

            for i in range(base, nextseq):
                canal.udt_send(sndpkt[i], sender,receiver, startTime)
        
            sender.start_timer(startTime)
        
        if sender.has_receive():
            if sender.get_base() == sender.get_nextseq:
                sender.stop_timer()       

        if receiver.has_receive():
            rcvPkt = receiver.get_receive()
            for i in rcvPkt:
                if receiver.get_expectedseq() == 0 and i[0] != 0:
                    continue
                
                if not receiver.verify_discard(i):
                    sndpkt = receiver.make_pkt()
                    canal.udt_send(sndpkt, receiver,sender, startTime)
                    receiver.set_expectedseq(receiver.get_expectedseq()+1)
                else:
                    sndpkt = receiver.get_send()
                    canal.udt_send(sndpkt, receiver,sender, startTime)

        canal.encaminhando(startTime)
        ####### PROTOCOL LOGIC ############
    
    receiver.print_dataResult()
    # receiver.printData()
    ######################################

main()