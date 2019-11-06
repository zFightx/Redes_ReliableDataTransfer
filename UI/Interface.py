import tkinter as tk
import Protocolos

class Interface:
    def __init__(self, nome, largura, altura):
        #------ Atributos
        ## um dicionário para guardar as configurações (auto-explicativo)
        self.__configuracoes = dict()
        
        #------ constantes para controlar o layout dos botões ------
        # button_width = 6
        self.button_padx = "2m"
        self.button_pady = "1m"
        # buttons_frame_padx = "3m"
        # buttons_frame_pady = "2m"
        self.buttons_frame_ipadx = "10m"
        self.buttons_frame_ipady = "10m"
        # -------------- fim das constantes ----------------

        # cria uma aplicação tkinter ( provavelmente falta o Frame )
        self.root = tk.Tk()
        self.root.title(nome)  # titulo
        self.root.geometry(str(largura)+"x"+str(altura))  # dimensão
        
        # desenhar tela inicial
        self.__telaInicial()
        
        # Loop tkinter interface
        self.root.mainloop()


    def __telaInicial(self):
        # Containers
        self.myMainContainer = tk.Frame(self.root)
        self.myMainContainer.pack(expand=tk.YES, fill=tk.BOTH)
        
        ## Title and some options
        self.topContainer = tk.Frame(self.myMainContainer)
        self.topContainer.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx= self.button_padx,
            pady= self.button_pady)
        
        ## Will display all the contents of the program
        self.middleContainer = tk.Frame(self.myMainContainer)
        self.middleContainer.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        ## Status and notifications
        self.bottomContainer = tk.Frame(self.myMainContainer)
        self.bottomContainer.pack(side=tk.BOTTOM, expand=tk.YES, fill=tk.BOTH)
        
        # Frames
        # middleContainter Frames
        self.leftMiddleFrame_middleContainer = tk.Frame(self.middleContainer)
        self.leftMiddleFrame_middleContainer.pack(side= tk.LEFT, anchor=tk.CENTER, expand=tk.YES,
            padx= self.button_padx, pady= self.button_pady, ipady=self.buttons_frame_ipady,
            ipadx=self.buttons_frame_ipadx)

        self.rightMiddleFrame_middleContainer = tk.Frame(self.middleContainer)
        self.rightMiddleFrame_middleContainer.pack(side= tk.RIGHT)
        

        # Widgets
        ## topContainer
        self.labelTitle_topContainer = tk.Label(self.topContainer, text="UnB - Simulador de protocolos de transporte", fg="blue", font=("Arial", 16, "bold"))
        self.labelTitle_topContainer.pack(side=tk.TOP, anchor=tk.CENTER, pady=(10,0))
        
        ## middleContainer
        ### leftMiddleFrame_middleContainer - Botões
        # self.optionMenu = tk.IntVar()
        self.labelBotoes_leftMiddleFrame = tk.Label(self.leftMiddleFrame_middleContainer, text="Configurações:")
        self.labelBotoes_leftMiddleFrame.pack(pady=(0,20))

        self.menuButton_leftMiddleFrame = tk.Menubutton(self.leftMiddleFrame_middleContainer, text="Protocolos", relief=tk.RAISED, direction=tk.RIGHT,
            width=20, height=2, borderwidth=2, activebackground="gray")
        self.menuButton_leftMiddleFrame.pack(pady=(0,8))
        self.menuButton_leftMiddleFrame.menu = tk.Menu(self.menuButton_leftMiddleFrame, tearoff=0)
        self.menuButton_leftMiddleFrame["menu"] = self.menuButton_leftMiddleFrame.menu
        self.menuButton_leftMiddleFrame.menu.add_command(label="Stop-and-Wait", command= lambda: self.__opcoesProtocolos(0))
        self.menuButton_leftMiddleFrame.menu.add_command(label="Go-Back-N", command= lambda: self.__opcoesProtocolos(1))
        self.menuButton_leftMiddleFrame.menu.add_command(label="Selective-Repeat", command= lambda: self.__opcoesProtocolos(2))

        self.buttonCanal = tk.Button(self.leftMiddleFrame_middleContainer, text="Canal", width=15, command=self.__opcoesCanal)
        self.buttonCanal.pack(expand=tk.YES, pady=(0,5))

        self.buttonEmissor = tk.Button(self.leftMiddleFrame_middleContainer, text="Emissor", width=15, command=lambda: self.__opcoesEmissorReceptor(0))
        self.buttonEmissor.pack(expand=tk.YES, pady=(0,5))

        self.buttonReceptor = tk.Button(self.leftMiddleFrame_middleContainer, text="Receptor", width=15, command=lambda: self.__opcoesEmissorReceptor(1))
        self.buttonReceptor.pack(expand=tk.YES, pady=(0,5))

        self.buttonReceptor = tk.Button(self.leftMiddleFrame_middleContainer, text="Iniciar simulação", width=20, height=2, activebackground="gray", font=("bold"), command=self.__iniciarSimulacao)
        self.buttonReceptor.pack(expand=tk.YES, pady=(20,0))

        ### rightMiddleFrame_middleContainer - Text saída terminal
        self.labelBotoes_rightMiddleFrame = tk.Label(self.rightMiddleFrame_middleContainer, text="Console:", font=(14))
        self.labelBotoes_rightMiddleFrame.pack(pady=(0,2))

        self.sb = tk.Scrollbar(self.rightMiddleFrame_middleContainer)
        self.sb.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.textTerminal = tk.Text(self.rightMiddleFrame_middleContainer, borderwidth=2, padx= self.button_padx,
            relief=tk.GROOVE, width=80, height=30, state=tk.DISABLED,
            yscrollcommand=self.sb.set)
        
        self.textTerminal.pack(fill=tk.BOTH, expand=tk.YES)
        self.sb.config(command=self.textTerminal.yview)

        ### bottomContainer
        self.labelStatusBar = tk.Label(self.bottomContainer, text="", fg="red")
        self.labelStatusBar.pack(side=tk.LEFT, expand=tk.YES, anchor=tk.W, padx=(20,0))


    def __iniciarSimulacao(self):
        """ Executa o simulador com as configurações definidas."""
        pass


    def __opcoesProtocolos(self, opt):
        # 0 - Stop-and-Wait
        # 1 - Go-Back-N
        # 2 - Selective Repeat
        if opt == 0 or opt == 1 or opt == 2: 
            self.__configuracoes["protocolo"] = opt
        self.printarConfiguracoesConsole()  


    def __opcoesCanal(self):
        self.canalDistancia = tk.StringVar()
        self.canalProbErro = tk.StringVar()
        self.canalVazao = tk.StringVar()
    
        try:
            if self.newWindow.state() == "normal":
                self.newWindow.destroy()
                self.newWindow = tk.Toplevel(self.root)
                self.newWindow.minsize(500, 200)
                self.newWindow.focus()
        except:
            self.newWindow = tk.Toplevel(self.root)
            self.newWindow.minsize(500, 200)
            self.newWindow.focus()

        # Container
        mainContainer = tk.Frame(self.newWindow)
        mainContainer.pack(expand=tk.YES, fill=tk.BOTH)

        # Frames internos
        ## canal Distancia
        labelDistancia = tk.Label(mainContainer, text="Insira a distância do canal (Km):")
        labelDistancia.pack(side=tk.TOP)
        entryDistancia = tk.Entry(mainContainer, width=60, textvariable=self.canalDistancia)
        entryDistancia.pack(side=tk.TOP)

        ## canal Probabilidade de Erro
        labelProbErro = tk.Label(mainContainer, text="Insira a probabilidade de erro do canal (porcentagem):")
        labelProbErro.pack(side=tk.TOP)
        entryProbErro = tk.Entry(mainContainer, width=60, textvariable=self.canalProbErro)
        entryProbErro.pack(side=tk.TOP)
        
        ## canal Vazao
        labelVazao = tk.Label(mainContainer, text="Insira a vazão do canal (bytes):")
        labelVazao.pack(side=tk.TOP)
        entryVazao = tk.Entry(mainContainer, width=60, textvariable=self.canalVazao)
        entryVazao.pack(side=tk.TOP)

        ## botao salvar
        buttonDistancia = tk.Button(mainContainer, text="Salvar", command= lambda: self.salvarConfig(0))
        buttonDistancia.pack(side=tk.TOP, pady=(20,0))


    def __opcoesEmissorReceptor(self, mode):
        if mode != 0 and mode != 1: return
        # mode == 0: receptor
        # mode == 1: emissor

        self.tamanhoJanelaEmissorReceptor = tk.StringVar()
        self.timeOutEmissorReceptor = tk.StringVar()
    
        try:
            if self.newWindow.state() == "normal":
                self.newWindow.destroy()
                self.newWindow = tk.Toplevel(self.root)
                self.newWindow.minsize(500, 160)
                self.newWindow.focus()
        except:
            self.newWindow = tk.Toplevel(self.root)
            self.newWindow.minsize(500, 160)
            self.newWindow.focus()

        # Container
        mainContainer = tk.Frame(self.newWindow)
        mainContainer.pack(expand=tk.YES, fill=tk.BOTH)

        # Frames internos
        ## emissor/receptor tamanho
        labelTamanho = tk.Label(mainContainer, text="Insira o tamanho da janela (bytes):")
        labelTamanho.pack(side=tk.TOP)
        entryTamanho = tk.Entry(mainContainer, width=60, textvariable=self.tamanhoJanelaEmissorReceptor)
        entryTamanho.pack(side=tk.TOP)
        
        ## emissor/receptor Cálculo TimeOut
        labelTimeOut = tk.Label(mainContainer, text="Cálculo do TimeOut (ms):")
        labelTimeOut.pack(side=tk.TOP)
        entryTimeOut = tk.Entry(mainContainer, width=60, textvariable=self.timeOutEmissorReceptor)
        entryTimeOut.pack(side=tk.TOP)
        
        ## botao salvar
        if mode == 0: # emissor
            salvarConfigPos = 1
        elif mode == 1: # receptor
            salvarConfigPos = 2
        buttonDistancia = tk.Button(mainContainer, text="Salvar", command= lambda: self.salvarConfig(salvarConfigPos))
        buttonDistancia.pack(side=tk.TOP, pady=(20,0))


    def salvarConfig(self, opt):        
        if opt == 0:
            self.__configuracoes['canalDistancia'] = self.canalDistancia.get()
            self.__configuracoes['canalProbErro'] = self.canalProbErro.get()
            self.__configuracoes['canalVazao'] = self.canalVazao.get()
        elif opt == 1:
            self.__configuracoes['emissorTamanhoJanela'] = self.tamanhoJanelaEmissorReceptor.get()
            self.__configuracoes['emissorTimeOut'] = self.timeOutEmissorReceptor.get()
        elif opt == 2:
            self.__configuracoes['receptorTamanhoJanela'] = self.tamanhoJanelaEmissorReceptor.get()
            self.__configuracoes['receptorTimeOut'] = self.timeOutEmissorReceptor.get()

        # mostrando no console
        self.printarConfiguracoesConsole()
        # depois de salvar fechar a nova janela automaticamente (opcional)
        self.newWindow.destroy()


    def printarConsole(self, text):
        '''
            Recebe uma string a ser printada no terminal
        '''
        self.textTerminal.config(state=tk.NORMAL)       # permitindo escrita
        self.textTerminal.delete("1.0", tk.END)         # limpando console
        self.textTerminal.insert(tk.END, text)          # escrevendo
        self.textTerminal.config(state=tk.DISABLED)     # desabilitando escrita


    def printarConfiguracoesConsole(self):
        text = ""
        for key in self.configuracoes:
            def check(x):
                if (type(x) is not str): return str(x)
                else: return x

            text += "{0:_<30s} : {1} \n".format(key, check(self.configuracoes[key]))
        self.printarConsole(text)


    def printarBarraStatus(self, text):
        self.labelStatusBar.config(text=text)


    @property
    def configuracoes(self):
        return self.__configuracoes