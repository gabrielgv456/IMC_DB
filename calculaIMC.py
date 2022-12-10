import tkinter, firebirdsql
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

def caculaIMC():
    try:
        nomePaciente = varNome.get()
        enderecoPaciente = varEndereco.get()
        alturaPaciente = float(varAltura.get().replace(',', '.'))
        pesoPaciente = float(varPeso.get().replace(',', '.'))

        if len(nomePaciente) <= 0 :
            raise ValueError('Insira um nome valido!')
        if len(enderecoPaciente) <= 0 :
            raise ValueError('Insira um endereço valido!')
        if alturaPaciente <= 0 :
            raise ValueError('Insira uma altura valida!')
        if pesoPaciente <= 0 :
            raise ValueError('Insira um peso valido!')

        IMC = round((pesoPaciente/(alturaPaciente * alturaPaciente)),2);

        qInsertConsulta = f"INSERT INTO IMC_CADASTRO (ID,NOME,ENDERECO,ALTURA,PESO,IMC_RESULTADO) VALUES(NULL,'{nomePaciente}','{enderecoPaciente}',{alturaPaciente},{pesoPaciente},{IMC})"
        executeDB(qInsertConsulta)

        qBuscaCondicaoIMC = f"SELECT ic.CONDICAO FROM IMC_CONDICAO ic WHERE {IMC} >= ic.MINIMO  AND {IMC} <= ic.MAXIMO"
        condicaoPaciente = executeDB(qBuscaCondicaoIMC)
        condicaoPaciente = ''.join(condicaoPaciente[0])

        resultLabel = Label(janela, text=f"IMC igual à: {IMC}kg/m²\n{condicaoPaciente}", font="3", borderwidth=2, relief="ridge", width=20, height=4)
        resultLabel.grid(row=2, column=2, padx=10, pady=10, rowspan=2)

    except Exception as e:
        messagebox.showerror(title="Falha ao calcular IMC", message=f"{str(e)}")

def reset():
    enderecoEntry.delete(0,END)
    nomeEntry.delete(0,END)
    alturaEntry.delete(0,END)
    pesoEntry.delete(0,END)
    resultLabel = Label(janela, text=f"Resultado", font="3", borderwidth=2,
                        relief="ridge", width=20, height=4)
    resultLabel.grid(row=2, column=2, padx=10, pady=10, rowspan=2)
    nomeEntry.focus()

def exibe_historico():
    historico = tkinter.Toplevel()
    historico.title('Historico de Consultas')
    historico.resizable(False, False)
    historico.focus_force()
    historico.grab_set()
    groupBox = LabelFrame(historico,text='Histórico')
    groupBox.pack(fill='both',expand='yes',padx=10,pady=10)
    dbView=ttk.Treeview(groupBox,columns=('Paciente','Endereco','Altura','Peso','IMC'),show='headings')
    dbView.column('Paciente',minwidth=100,width=100)
    dbView.column('Endereco', minwidth=100, width=100)
    dbView.column('Altura', minwidth=50, width=50)
    dbView.column('Peso', minwidth=50, width=50)
    dbView.column('IMC', minwidth=100, width=170)
    dbView.heading('Paciente',text='Paciente')
    dbView.heading('Endereco', text='Endereco')
    dbView.heading('Altura', text='Altura')
    dbView.heading('Peso', text='Peso')
    dbView.heading('IMC', text='IMC')
    dbView.pack()
    dbView.delete(*dbView.get_children())
    query = """SELECT cd.NOME,cd.ENDERECO,cd.ALTURA,cd.PESO,CAST(cd.IMC_RESULTADO AS NUMERIC(7,2))||' - '||ic.CONDICAO AS IMC
            FROM IMC_CADASTRO cd
            INNER JOIN IMC_CONDICAO ic ON (cd.IMC_RESULTADO >= ic.MINIMO  AND cd.IMC_RESULTADO <= ic.MAXIMO)
            ORDER BY cd.ID"""
    resultado = executeDB(query)
    for i in resultado:
        dbView.insert('','end',values=i)
    print(resultado)

def executeDB(query):
    try:
        con = firebirdsql.connect(host=f"localhost", database=r"C:\firebirdbd\BANCO.FDB", user="SYSDBA", password="masterkey", port=3050 )
        cur = con.cursor()
        cur.execute(f"{query}")
        retorno = cur.fetchall()
        con.commit()
        con.close()
        return retorno
    except Exception as e:
        messagebox.showerror(title="Falha de conexão", message=f"Falha ao conectar com o banco de dados: {e}")
        return


janela = Tk()
janela.eval('tk::PlaceWindow . center')
janela.title("Cálculo do IMC - Indice de Massa Corporal")
#janela.iconbitmap('image.ico')
janela.resizable(False,False)

#variables
varNome = StringVar();
varEndereco = StringVar();
varAltura = StringVar();
varPeso = StringVar();


nomeLabel = Label(janela, text= "Nome do paciente:", font="6")
nomeLabel.grid(row=0,column=0,padx=10,pady=10,sticky=W)
nomeEntry = Entry(janela, textvariable=varNome, width=65)
nomeEntry.grid(row=0,column=1,padx=10,pady=10,columnspan=2,sticky=W)
nomeEntry.get()


enderecoLabel = Label(janela, text= "Endereço do paciente:", font="6")
enderecoLabel.grid(row=1,column=0,padx=10,pady=0,sticky=W)
enderecoEntry = Entry(janela, textvariable=varEndereco, width=65)
enderecoEntry.grid(row=1,column=1,padx=10,pady=10,columnspan=2,sticky=W)
enderecoEntry.get()


alturaLabel = Label(janela, text= "Altura(cm):", font="6")
alturaLabel.grid(row=2,column=0,padx=10,pady=0,sticky=W)
alturaEntry = Entry(janela, textvariable=varAltura, width=30)
alturaEntry.grid(row=2,column=1,padx=10,pady=10,sticky=W)
alturaEntry.get()


pesoLabel = Label(janela, text= "Peso(kg):", font="6")
pesoLabel.grid(row=3,column=0,padx=10,pady=0,sticky=W)
pesoEntry = Entry(janela, textvariable=varPeso, width=30)
pesoEntry.grid(row=3,column=1,padx=10,pady=10,sticky=W)
pesoEntry.get()


resultLabel = Label(janela, text= "Resultado", font="6", borderwidth=2, relief="ridge", width=20,height=4)
resultLabel.grid(row=2,column=2,padx=10,pady=10,rowspan=2)


btCalcular = Button (janela, width=20, text="Calcular", command=caculaIMC)
btCalcular.grid(column=0,row=4,padx=0,pady=0)

btReiniciar = Button (janela, width=20, text="Reiniciar", command=reset)
btReiniciar.grid(column=1,row=4,padx=0,pady=0)

btSair = Button (janela, width=20, text="Histórico", command=exibe_historico)
btSair.grid(column=2,row=4,padx=10,pady=20)


janela.mainloop()