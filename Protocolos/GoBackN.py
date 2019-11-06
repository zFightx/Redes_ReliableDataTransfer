import time
import random
class GoBackNSender:
    def __init__(self, tempo, janela, func):
        self.func = func
        self.nextSeqNum = 0         # proxima sequencia a ser enviada
        self.base = 0               # posicao atual na janela
        self.maxJanela = janela     # tamanho maximo da janela

        self.janela = []            # janela

        self.sendPackage = []       # lista de pacotes enviados
        self.rcvPackage = []        # lista de pacotes recebidos

        self.timeout = tempo        # tempo maximo de espera
        self.temporizador = 0       # Timer
        self.isTimerRunning = False # is running?

    ## verifica se ainda temos que enviar algum dado
    def has_data(self):
        return self.nextSeqNum < len(self.janela)

    ## pega a proxima sequencia a ser enviada
    def get_nextseq(self):
        return self.nextSeqNum
    
    ## seta a proxima sequencia a ser enviada
    def set_nextseq(self, value):
        self.nextSeqNum = value
    
    ## pega posicao atual atual na janela
    def get_base(self):
        return self.base
    
    ## seta a posicao atual na janela
    def set_base(self, value):
        self.base = value

    ## pega o tamanho maximo da janela
    def get_janela(self):
        return self.maxJanela

    ## adicionar um elemento na janela de dados
    def add_janela(self, data):
        self.janela.append(data)

    ## monta um pacote [ackSeq, data, checksum]
    def make_pkt(self):
        self.sendPackage.append([self.nextSeqNum, self.janela[self.nextSeqNum], len(self.janela[self.nextSeqNum])])
        return self.sendPackage
    
    ## verifica se tem dado a ser enviado no momento
    def has_send(self):
        return (self.nextSeqNum < self.base + self.maxJanela and len(self.janela) > self.nextSeqNum)
    
    ## sinaliza o envio de um dado
    def send_package(self, package):
        self.func("Sender: sending package {0}\n".format(package))
        self.rcvPackage = []

    ## pega a lista de pacotes montados
    def get_send(self):
        return self.sendPackage
    
    ## sinaliza que recebeu um pacote
    def receive_package(self, package):
        self.rcvPackage = package
        if package[0] == self.base:
            self.func("Sender: received ACK {0}\n".format(package[0]))
            self.base = self.base + 1
        else:
            if package[0] < self.base:
                self.func("Sender: received Duplicated Package (ignored) {0}\n".format(package))
            else:
                self.func("Sender: received ACK {0}\n".format(package[0]))
                self.func("Sender: ACKs [{0}, ... , {1}] confirmed with based in confirmation ack {2}\n".format(self.base, package[0], package[0]))
                self.base = package[0]

    ## verifica se tem recebido um pacote
    def has_receive(self):
        return (len(self.rcvPackage) > 0)

    ## inicia o Timer (timeout)
    def start_timer(self, timerSystem):
        self.temporizador = timerSystem + self.timeout
        self.isTimerRunning = True
    
    ## para o Timer
    def stop_timer(self):
        self.isTimerRunning = False

    ## verifica se tempo esgotou
    def isTimeOut(self, timerSystem):
        if self.temporizador < timerSystem and self.isTimerRunning:
            self.func("Sender: Time Out\n")
            return True
        else:
            return False

    ## verifica se todos os pacotes foram enviados
    def notFinish(self):
        return self.base < len(self.janela)

class GoBackNReceiver:
    def __init__(self, func):
        self.func = func            # Printar no Console
        self.expectedSeqNum = 0     # inicia esperando uma seq 0

        self.sendPackage = []       # lista de pacotes montados
        self.rcvPackage = []        # lista de pacotes recebidos

        self.dataResult = ""        # delivery package

    ## pega a seq que espera
    def get_expectedseq(self):
        return self.expectedSeqNum
    
    ## seta a seq que espera
    def set_expectedseq(self, value):
        self.expectedSeqNum = value

    ## monta um pacote [ ack, checksum ]
    def make_pkt(self):
        self.sendPackage = [self.expectedSeqNum, 8]
        return self.sendPackage

    ## sinaliza o envio de um pacote
    def send_package(self, package):
        self.func("Receiver: sending package {0}\n".format(package))
        self.rcvPackage = []

    ## pega a lista de pacotes montados
    def get_send(self):
        return self.sendPackage

    ## sinaliza o recebimento de pacotes
    def receive_package(self, package):
        self.rcvPackage.append(package)

    ## pega os pacotes recebidos
    def get_receive(self):
        return self.rcvPackage

    ## verifica se recebeu pacotes
    def has_receive(self):
        return ( len(self.rcvPackage) > 0 )

    ## verifica se um pacotes eh descatavel
    def verify_discard(self,package):
        if package[0] == self.expectedSeqNum:
            self.func("Receiver: received package {0}\n".format(package))
            self.dataResult = self.dataResult + package[1]
            return False
        else:
            self.func("Receiver: discard package {0}\n".format(package)) 
            return True

    ## printa o resultado da comunicacao
    def print_dataResult(self):
        self.func("Data Result: {0}\n".format(self.dataResult))
    
    ## pega o resultado da comunicacao
    def get_dataResult(self):
        return self.dataResult

class Canal:
    def __init__(self, timeTransfer, probabilidadeError):
        self.lista_pacotes = []     # pacotes circulando na rede
        self.timeTransfer = timeTransfer
        self.probabilidadeError = probabilidadeError

    ## envia um pacote pelo canal
    def udt_send(self, package, sender, receiver, timeSystem):
        sender.send_package(package)                                    ## sinaliza que ha um pacote enviado
        self.lista_pacotes.append([package, receiver, timeSystem + self.timeTransfer])    ## poe na lista de pacotes na rede
    
    ## recebe um pacote pelo canal
    def rdt_rcv(self, package, receiver):        
        receiver.receive_package(package)                               ## sinaliza que ha um pacotece recebido

    ## circulacao de pacotes na rede
    def encaminhando(self, timeSystem):
        i = 0
        while i != len(self.lista_pacotes):

            ## Se tempo de chegada do pacote acabou
            if self.lista_pacotes[i][2] < timeSystem:

                ## probabilidade do pacote ter sido perdido no caminho
                self.probabilidade_perda = random.randint(0,100)
                ## se nao se perdeu no caminho, pacote chega ao destino
                if self.probabilidade_perda < 100 - self.probabilidadeError:
                    self.rdt_rcv(self.lista_pacotes[i][0], self.lista_pacotes[i][1])    # [ package, destino ]

                ## remove pacote da rede
                self.lista_pacotes.pop(i)
                i = i - 1

            i = i + 1
    
    ## verifica se tem pacotes circulando
    def hasEncaminhamento(self):
        return len(self.lista_pacotes) > 0

    # tamanhoJanela, canalDistancia, canalVazao, canalProbErro,
def StartGoBackN(dados, janela, canalDistancia, canalVazao, probabilidadeError, func, refresh):
    # func -> printar no Console
    # refresh -> atualizar interface
    func("Redes de Computadores - UnB\n")

    ## DADOS QUE QUEREMOS ENVIAR ##
    dados2 = dados
    
    timeout = (canalDistancia*1000/(2.1*10**7) + 8/canalVazao) * 2 + 0.05
    timeTransfer = canalDistancia*1000/(2.1*10**7)

    ## PROTOCOLOS ##
    sender = GoBackNSender(timeout, janela, func)
    receiver = GoBackNReceiver(func)
    canal = Canal(timeTransfer, probabilidadeError)
    #####################################

    ## dados sao adicionados na janela do sender
    while len(dados) > 0:
        if len(dados) >= 8:
            sender.add_janela(dados[:8])
            dados = dados[8:]
        else:
            sender.add_janela(dados[:len(dados)])
            dados = ""
    #####################################

    #### MAIN LOOP ####
    while receiver.get_dataResult() != dados2 or canal.hasEncaminhamento() or sender.has_data() or sender.notFinish():
        startTime = time.time() # TIMER

        ## SENDER FSM
        if sender.has_send(): # se tem pacote a ser enviado
            package = sender.make_pkt()[sender.get_nextseq()]   # monta o pacote
            # sender.send_package(package)
            canal.udt_send(package, sender,receiver, startTime) # manda para a rede

            if sender.get_base() == sender.get_nextseq():       # se base == nextseq ( se enviou a N-janela )
                sender.start_timer(startTime)                   # inicia o temporizador
            
            sender.set_nextseq(sender.get_nextseq()+1)          # proxima seq
        
        if sender.isTimeOut(startTime): # se deu timeout
            base = sender.get_base()            # base
            nextseq = sender.get_nextseq()      # nextseq
            sndpkt = sender.get_send()          # sndpkt

            for i in range(base, nextseq):      # para cada pacote da N-janela nao enviados
                canal.udt_send(sndpkt[i], sender,receiver, startTime)   # enviar
        
            sender.start_timer(startTime)       # reinicia o temporizador
        
        if sender.has_receive():        # se recebeu algum pacote
            if sender.get_base() == sender.get_nextseq: # se base == nextseq
                sender.stop_timer()     # evita de dar timeout quando todos os pacotes da N-janela foram confirmados
        #################################

        ## RECEIVER FSM
        if receiver.has_receive():      # se recebeu pacote
            rcvPkt = receiver.get_receive() # pacotes recebidos
            for i in rcvPkt:            # para cada pacote recebido
                if receiver.get_expectedseq() == 0 and i[0] != 0:   # se nao for o primeiro pacote seq 0
                    continue
                
                if not receiver.verify_discard(i):  # verifica se pacote esta deboas
                    sndpkt = receiver.make_pkt()    # monta um Ack
                    canal.udt_send(sndpkt, receiver,sender, startTime)  # envia o Ack
                    receiver.set_expectedseq(receiver.get_expectedseq()+1)  # proxima seq esperada
                else:                               # se pacote nao esta deboas
                    # if(i[0] < receiver.get_expectedseq()):
                    #     sndpkt = [i[0], len(i[1])]
                    # else:
                    sndpkt = receiver.get_send()
                    canal.udt_send(sndpkt, receiver,sender, startTime)  # reenvia ack mais alto
        ####################################
        refresh()
        ## ENCAMINHAMENTO DE PACOTES ##
        canal.encaminhando(startTime)
        #####################################
    
    receiver.print_dataResult()
    # receiver.printData()
    ######################################