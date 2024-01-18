""" Status atual do projeto: 
11/01 - ativado a funcionalidade do checkbutton (Creditos ao monitor Victor Hugo)
11/01 - ajustado a função de apagar tarefas selecionadas
11/01 - adicionado o campo de COMBOBOX e funcionalidades
12/01 - adicionado o campo de DATA DE CRIAÇÃO DA TAREFA e funcionalidades
12/01 - adicionado o campo de DATA DE ENCERRAMENTO DA TAREFA e funcionalidades
12/01 -[ERRO] CORRIGIDO SOBRESCREVER LINHA*
        * Esse erro ocorre ao adicionar a tarefa1, adocionar tarefa2, apagar tarefa1 e criar uma tarefa3, que ficará por cima da tarefa2
        * E assim por diante
12/01 -[ERRO] CORRIGDO ALTERAR APENAS UMA DATA DE CONCLUSÃO
12/01 - estilizar paletas: PRETO, VERMELHO, BRANCO
- integrar com o MYSQL"""

from tkinter import*
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime


# ----------------------- DICIONARIOS 
vars_controle = {}
checkbuttons = {}
comboboxes = {}
statusCombobox = ["A Fazer", "Em Andamento" , "Concluído"] #->Lista com as opções do Combobox
datas_de_inicio = {}
datas_de_conclusao = {}


# ----------------------- ESTILOS - Cores + Fontes 
corVinho = "#8c160e"
corVinhoEscuro = "#660903"
corVermelhoLeve = "#c73228"
corPreto = "#000000"
corBranco = "#ffffff"
corCinzaClaro = "#cccaca"
corCinzaLeve = "#e6e3e3"
fonteAtividades = ("Arial", 10)

# ----------------------- JANELA
janela = Tk()

janela.title("Gerenciador de Tarefas")
janela.geometry("800x700+500+10")
janela.config(bg=corCinzaClaro)
janela.resizable(width=False, height=False)

# ----------------------- TITULO
lblTitulo = Label(janela, text="Gerenciador de Tarefas - Stark Corporation", font=("Arial", 18))
lblTitulo.config(height=1, bg=corVinho, fg=corBranco)
lblTitulo.pack(ipady = 1, fill="x")

# ----------------------- ORIENTAÇÃO
lblOrientacao = Label(janela, text="Informe a tarefa abaixo:", font=("Arial", 14))
lblOrientacao.config(height=1, bg=corCinzaClaro, fg=corVinho)
lblOrientacao.pack(pady = 20)

# ----------------------- ENTRADA DA TAREFA + BOTÃO
frameInput = Frame(janela)
frameInput.config(bg=corCinzaClaro)
frameInput.pack(pady=5)

#-Função de Selecionar tarefa
def selecionarTarefa():
    # Encontrar as tarefas selecionadas e destruir os Checkbuttons correspondentes
    for tarefa, var in list(vars_controle.items()):
        if var.get() == "true":
            tarefaSelecionada = checkbuttons[tarefa].cget("text")
            print(f"Tarefa selecionada: {tarefaSelecionada}")
            
            # Alterando a cor da tarefa concluída
            checkbuttons[tarefa].configure(foreground="blue")

            # Alterando o STATUS do COMBOBOX
            comboboxes[tarefa].current(2)

            # Alterando a Data de Conclusão
            if datas_de_conclusao[tarefa].cget("text") == "":
                dataConclusao = datetime.now().strftime("%d/%m/%Y %H:%M")
                datas_de_conclusao[tarefa].configure(text=dataConclusao)

        # Ações ao desmarcar o checkbutton            
        else:
            checkbuttons[tarefa].configure(foreground="black")
            comboboxes[tarefa].current(0)
            datas_de_conclusao[tarefa].configure(text = "")
            

#- Função alterar com o Combobox
def alterarCheckPeloCombobox(event):
    for tarefa, combo in list(comboboxes.items()):
        if combo.get() == "Concluído":
            print("Tarefa Concluída pelo COMBOBOX")
            checkbuttons[tarefa].configure(foreground="blue")
            vars_controle[tarefa].set("true")
            
            # Alterando a Data de Conclusão
            if datas_de_conclusao[tarefa].cget("text") == "":
                dataConclusao = datetime.now().strftime("%d/%m/%Y %H:%M")
                datas_de_conclusao[tarefa].configure(text=dataConclusao)
        else:
            checkbuttons[tarefa].configure(foreground="black")
            vars_controle[tarefa].set("false")
            datas_de_conclusao[tarefa].configure(text="")

linha = 1 #contador que vai indicar em qual linha serão inseridos as tarefas e etc

#-Função de adicionar tarefa
def adicionarTarefa():
    novaTarefa = entryTarefa.get()
    global linha
    print(linha)
    if novaTarefa in vars_controle:
        messagebox.showwarning("Erro", "Tarefa ja cadastrada")
        # Comando para limpar o INPUT de tarefa
        while (entryTarefa.get()) != "":
            entryTarefa.delete(ANCHOR)

    elif novaTarefa != "":
        # Criar uma nova variável de controle
        var = StringVar()
        var.set("false")
        vars_controle[novaTarefa] = var


        # Criar um novo Checkbutton e armazená-lo no dicionário checkbuttons
        check = Checkbutton(frameLista, text=str(novaTarefa), variable=var, onvalue=f"true", offvalue="false", font=fonteAtividades ,command=selecionarTarefa)
        check.grid(row=linha, column=0, columnspan=3, padx=2, sticky="w")
        checkbuttons[novaTarefa] = check


        # Criar um combobox
        combo = ttk.Combobox(frameLista, values=statusCombobox, width=1, font=fonteAtividades)
        combo.bind('<<ComboboxSelected>>', alterarCheckPeloCombobox)
        combo.grid(row=linha, column=1, ipadx=2, sticky="EW")
        combo.current(0)
        combo ['state'] = 'readonly'
        comboboxes[novaTarefa] = combo

        # Data de criação
        dataInicial = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        lbl_Data_Inicial = Label(frameLista, text=dataInicial, width=1, font=fonteAtividades)
        lbl_Data_Inicial.grid(row=linha, column=2, ipadx=2, sticky="EW")
        datas_de_inicio[novaTarefa] = lbl_Data_Inicial
        print(dataInicial)

        # Campo que vai receber a data de conclusão
        lbl_data_conclusao = Label(frameLista, text="", width=1, font=fonteAtividades)
        lbl_data_conclusao.grid(row=linha, column=3, ipadx=2, sticky="EW")
        datas_de_conclusao[novaTarefa] = lbl_data_conclusao
    
        linha = linha+1

        messagebox.showinfo(title="Sucesso", message=f"Tarefa adicionada com sucesso: {novaTarefa}")
        # Comando para limpar o INPUT de tarefa
        while (entryTarefa.get()) != "":
            entryTarefa.delete(ANCHOR)

    else:
        messagebox.showwarning("Erro", "Por favor informe uma tarefa")
        # Comando para limpar o INPUT de tarefa
        while (entryTarefa.get()) != "":
            entryTarefa.delete(ANCHOR)

#-Campo para digitar a tarefa
entryTarefa = Entry(frameInput, background=corCinzaLeve, width=40, font=("Arial", 11))
entryTarefa.pack(fill=BOTH, expand=True, side=LEFT, padx=2)

#-Botão para adicionar a tarefa
btnEnviar = Button(frameInput, text="Adicionar Tarefa", command=adicionarTarefa, fg=corBranco, bg=corVinhoEscuro, font=("Arial", 11))
btnEnviar.pack(fill=BOTH, expand=True, side=LEFT)

# ----------------------- FRAME PARA INSERIR O CHECKBUTTON
frameLista = Frame(janela)
frameLista.pack(pady=20, padx=10, fill=BOTH)
frameLista.config(
    width=30,
    height=200
)

frameLista.columnconfigure(0, weight=3)
frameLista.columnconfigure(1, weight=1)
frameLista.columnconfigure(2, weight=1)
frameLista.columnconfigure(3, weight=1)

#-Header das Colunas (Atividade / Status -> Futuramente adicionar as Datas)
header_atividades = ttk.Label(frameLista, text="Atividade" , background=corVermelhoLeve, foreground=corBranco, font=("Arial", 13), relief= RIDGE).grid(row=0, column= 0, sticky=NSEW)
header_status = ttk.Label(frameLista, text="Status", background=corVermelhoLeve, foreground=corBranco, font=("Arial", 13), relief= RIDGE).grid(row=0, column= 1, sticky=EW)
header_data_inicial = ttk.Label(frameLista, text="Criada em", background=corVermelhoLeve, foreground=corBranco, font=("Arial", 13), relief= RIDGE).grid(row=0, column= 2, sticky=EW)
header_data_final = ttk.Label(frameLista, text="Encerrada em", background=corVermelhoLeve, foreground=corBranco, font=("Arial", 13), relief= RIDGE).grid(row=0, column= 3, sticky=EW)

# ----------------------- BOTÃO APAGAR TAREFAS SELECIONADAS

def apagarTarefasSelecionadas():
    # Encontrar as tarefas selecionadas e destruir os Checkbuttons correspondentes
    for tarefa, var in list(vars_controle.items()):
        if var.get() == "true":
            checkbuttons[tarefa].destroy()
            comboboxes[tarefa].destroy()
            datas_de_inicio[tarefa].destroy()
            datas_de_conclusao[tarefa].destroy()
            del vars_controle[tarefa]
            del checkbuttons[tarefa]
            del comboboxes[tarefa]
            del datas_de_inicio[tarefa]
            del datas_de_conclusao[tarefa]
  
btnApagar = Button(janela, text="Apagar Tarefas Concluídas", command=apagarTarefasSelecionadas, background=corVinho, fg=corBranco, font=("Arial",13))
btnApagar.pack(pady= 0, fill="x", padx=10)

# ----------------------- MAINLOOP
janela.mainloop()

