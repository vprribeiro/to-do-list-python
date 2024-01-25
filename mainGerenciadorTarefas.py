from tkinter import*
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import mysql.connector

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

# ----------------------- TEXTO DE ORIENTAÇÃO
lblOrientacao = Label(janela, text="Informe a tarefa abaixo:", font=("Arial", 14))
lblOrientacao.config(height=1, bg=corCinzaClaro, fg=corVinho)
lblOrientacao.pack(pady = 20)

# ----------------------- ENTRADA DA TAREFA + BOTÃO
frameInput = Frame(janela)
frameInput.config(bg=corCinzaClaro)
frameInput.pack(pady=10)

#-Função de Selecionar tarefa
def selecionarTarefa():
    # Encontrar as tarefas selecionadas e destruir os Checkbuttons correspondentes
    for tarefa, var in list(vars_controle.items()):
        if var.get() == "true":
            tarefaSelecionada = checkbuttons[tarefa].cget("text")
            
            # Alterando a cor da tarefa concluída
            checkbuttons[tarefa].configure(foreground="blue")

            # Alterando o STATUS do COMBOBOX
            comboboxes[tarefa].current(2)

            # Alterando a Data de Conclusão
            if datas_de_conclusao[tarefa].cget("text") == "":
                dataConclusao = datetime.now().strftime("%d/%m/%Y %H:%M")
                datas_de_conclusao[tarefa].configure(text=dataConclusao)

        # Ações ao desmarcar o checkbutton            
        elif var.get() == "true"and comboboxes[tarefa].get() == "Em andamento":
            checkbuttons[tarefa].configure(foreground="black")
            comboboxes[tarefa].current(1)
            datas_de_conclusao[tarefa].configure(text = "")
        else:
            if comboboxes[tarefa].get() == "Em Andamento":
                comboboxes[tarefa].current(1)
            else:
                comboboxes[tarefa].current(0)
            checkbuttons[tarefa].configure(foreground="black")
            datas_de_conclusao[tarefa].configure(text = "")
            

#- Função alterar com o Combobox
def alterarCheckPeloCombobox(event):
    for tarefa, combo in list(comboboxes.items()):
        if combo.get() == "Concluído":
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

linha = 1 #contador que vai indicar em qual linha serão inseridas as tarefas e etc

#-Função de adicionar tarefa
def adicionarTarefa():
    novaTarefa = entryTarefa.get()
    global linha
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

# ----------------------- FRAME + BOTÃO PARA SALVAR TAREFAS E CARREGAR
frameSaveLoad = Frame(janela)
frameSaveLoad.config(bg=corCinzaClaro)
frameSaveLoad.pack(pady=0)

#-Função para SALVAR as Tarefas
def salvarTarefa():
    if vars_controle == {}: #-Testando se há tarefas
        messagebox.showwarning("Erro", "Não há tarefas para salvar")    
    else:
        #- Criando e conectando banco de dados e tabela
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456lol"
        )

        mycursor = mydb.cursor()

        mycursor.execute("CREATE DATABASE if not exists banco_gerenciador_tarefas")
        mycursor.execute("use banco_gerenciador_tarefas")
        table = "vars_controle varchar(10), checkbuttons varchar(80), comboboxes varchar(20), datas_de_inicio varchar (30), datas_de_conclusao varchar (30)"
        mycursor.execute(f"create table if not exists tabela_gerenciador_tarefas({table})")
        mycursor.execute("truncate table tabela_gerenciador_tarefas")

        #- Pegando os valores e inserindo na tabela do banco de dados
        for tarefa, var in list(vars_controle.items()):
            
            variavel_controle_save = vars_controle[tarefa].get()
            tarefa_save = checkbuttons[tarefa].cget("text")
            status_save = comboboxes[tarefa].get()
            data_inicial_save = datas_de_inicio[tarefa].cget("text")
            data_conclusao_save = datas_de_conclusao[tarefa].cget("text")
            mycursor.execute("INSERT INTO tabela_gerenciador_tarefas (vars_controle, checkbuttons, comboboxes, datas_de_inicio, datas_de_conclusao) VALUES (%s, %s, %s, %s, %s)" , (variavel_controle_save, tarefa_save,status_save, data_inicial_save, data_conclusao_save))
            
            mydb.commit()
        
        #- Conclusão da ação
        messagebox.showinfo(title="Sucesso", message="Tarefas salvas com sucesso!")

#-Botão para SALVAR as tarefas
btnSalvar = Button(frameSaveLoad, text="Salvar Tarefas", command=salvarTarefa, fg=corBranco, bg=corVinho, font=("Arial", 11))
btnSalvar.pack(fill=BOTH, expand=True, side=LEFT, ipadx=100, padx=3)

#-Função para CARREGAR as tarefas
def carregarTarefas():
    global linha
    linha = 1

    #-Primeiro a lista e visualização das tarefas serão zerados
    for tarefa, var in list(vars_controle.items()):
        checkbuttons[tarefa].destroy()
        comboboxes[tarefa].destroy()
        datas_de_inicio[tarefa].destroy()
        datas_de_conclusao[tarefa].destroy()
        del vars_controle[tarefa]
        del checkbuttons[tarefa]
        del comboboxes[tarefa]
        del datas_de_inicio[tarefa]
        del datas_de_conclusao[tarefa]
    
    #- conectando ao banco de dados e tabela
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456lol",
    database="banco_gerenciador_tarefas"
    )
    mycursor = mydb.cursor()
    sql_select_query = "select* FROM tabela_gerenciador_tarefas"
    mycursor.execute(sql_select_query)
    dadosCarregados = mycursor.fetchall()

    #- Importando os dados
    for dados in dadosCarregados:        
        tarefa = dados[1]

        # Criar uma nova variável de controle
        var = StringVar()
        var.set(dados[0])
        vars_controle[tarefa] = var

        # Criar um novo Checkbutton e armazená-lo no dicionário checkbuttons
        check = Checkbutton(frameLista, text=tarefa, variable=var, onvalue=f"true", offvalue="false", font=fonteAtividades ,command=selecionarTarefa)
        check.grid(row=linha, column=0, columnspan=3, padx=2, sticky="w")
        checkbuttons[tarefa] = check
        if var.get() == "true":
            checkbuttons[tarefa].configure(foreground="blue")
        
        # Criar um combobox
        combo = ttk.Combobox(frameLista, values=statusCombobox, width=1, font=fonteAtividades)
        combo.bind('<<ComboboxSelected>>', alterarCheckPeloCombobox)
        combo.grid(row=linha, column=1, ipadx=2, sticky="EW")
        status = dados[2]
        if status == "A Fazer":
            combo.current(0)
        elif status == "Em Andamento":
            combo.current(1)
        else:
            combo.current(2)
        combo ['state'] = 'readonly'
        comboboxes[tarefa] = combo
        
        # Data de criação
        dataInicial = dados[3]       
        lbl_Data_Inicial = Label(frameLista, text=dataInicial, width=1, font=fonteAtividades)
        lbl_Data_Inicial.grid(row=linha, column=2, ipadx=2, sticky="EW")
        datas_de_inicio[tarefa] = lbl_Data_Inicial

        # Data de conclusão
        dataConclusao = dados[4]
        lbl_data_conclusao = Label(frameLista, text=dataConclusao, width=1, font=fonteAtividades)
        lbl_data_conclusao.grid(row=linha, column=3, ipadx=2, sticky="EW")
        datas_de_conclusao[tarefa] = lbl_data_conclusao
    
        linha = linha+1

    messagebox.showinfo(title="Sucesso", message=f"Tarefas carregadas com sucesso!")

#-Botão para CARREGAR as tarefas
btnCarregar = Button(frameSaveLoad, text="Carregar Tarefas", command=carregarTarefas, fg=corBranco, bg=corVinho, font=("Arial", 11))
btnCarregar.pack(fill=BOTH, expand=False, side=LEFT, ipadx=100)

# ----------------------- FRAME PARA INSERIR O CHECKBUTTON
frameLista = Frame(janela)
frameLista.pack(pady=10, padx=10, fill=BOTH)
frameLista.config(
    width=30,
    height=200
)

frameLista.columnconfigure(0, weight=3)
frameLista.columnconfigure(1, weight=1)
frameLista.columnconfigure(2, weight=1)
frameLista.columnconfigure(3, weight=1)

#-Header das Colunas
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