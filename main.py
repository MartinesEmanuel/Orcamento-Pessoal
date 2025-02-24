from tkinter import *
from tkinter import Tk, ttk, CENTER,messagebox
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkcalendar import Calendar,DateEntry
from datetime import date

from View import * 

# cores
c00 = "#2e2d2b"  # Preta
c01 = "#ffffff"  # Branca
c02 = "#4fa882"  # Verde
c03 = "#38576b"  # Azul Escuro
c04 = "#40b3d3"  # Azul Claro
c05 = "#e06636"  # Laranja
c06 = "#038cfc"  # Azul Vivo
c07 = "#3fbfb9"  # Ciano
c08 = "#262328"  # Preto Acinzentado
c09 = "#e9edf5"  # Cinza Claro
c10 = "#300a38"  # Ubuntu

colors = [
    '#5588bb',  # Azul Médio
    '#66bbbb',  # Verde Azulado
    '#99bb55',  # Verde Claro
    '#ee9944',  # Laranja Claro
    '#444466',  # Roxo Escuro
    '#bb5555'   # Vermelho Médio
]

entry_width = 12
button_width = 73


# Porcentagem
def porcent():
    l_nome = Label(frameMiddle, text="Porcentagem da Receita gasta", height=1, anchor=NW, 
                   font=("Verdana 12 bold italic"), bg=c01, fg=c00)
    l_nome.place(x=7, y=5)
    
    style = ttk.Style()
    style.theme_use('default')

    style.configure("custom.Horizontal.TProgressbar", 
                    thickness=25, 
                    troughcolor="#e0e0e0",   # Cor do fundo do progress bar
                    background="#4CAF50")    # Cor do progresso

    bar = Progressbar(frameMiddle, length=180, style="custom.Horizontal.TProgressbar")
    bar.place(x=10, y=35)
    
    valor = percentagem_valor()[0]
    bar['value'] = valor  

    l_porcentagem = Label(frameMiddle, text="{:,.2f}%".format(valor), height=1, anchor=NW, 
                          font=("Verdana 12"), bg=c01, fg=c00)
    l_porcentagem.place(x=200, y=35)

def bar_graph():
    lista_categorias = ['Renda', 'Despesas', 'Saldo']
    lista_valores = bar_valores()
    
    figure = plt.figure(figsize=(4, 3.45), dpi=60)
    ax = figure.add_subplot(111)
    
    ax.bar(lista_categorias, lista_valores, color=colors, width=0.9) 

    c = 0
    for i in ax.patches:
        ax.text(i.get_x() - 0.001, i.get_height() + 0.5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=12, 
                fontstyle='italic', verticalalignment='bottom')  
        c += 1

    ax.set_xticks(range(len(lista_categorias)))  
    ax.set_xticklabels(lista_categorias, fontsize=12)

    ax.patch.set_facecolor('#ffffff')

    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)  

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)  
    ax.spines['left'].set_visible(False)

    ax.tick_params(bottom=False, left=False) 

    ax.set_axisbelow(True)
    ax.yaxis.grid(color='#EEEEEE')  
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figure, frameMiddle) 
    canva.draw()  
    canva.get_tk_widget().place(x=10, y=80)  
    
def resum():
    valor = bar_valores()
    l_renda = Label(frameMiddle, text="TOTAL RENDA MENSAL", font=("Verdana", 10, "bold"), fg=c06, bg=c01)
    l_renda.place(x=300, y=20)
    
    v_renda = Label(frameMiddle, text=" R$ {:,.2f}".format(valor[0]), font=("Verdana", 14, "bold"), fg=c00, bg=c01)
    v_renda.place(x=300, y=40)

    l_despesas = Label(frameMiddle, text="TOTAL DESPESAS MENSAIS", font=("Verdana", 10, "bold"), fg=c05, bg=c01)
    l_despesas.place(x=300, y=80)

    v_despesas = Label(frameMiddle, text="R$ {:,.2f}".format(valor[1]), font=("Verdana", 14, "bold"), fg=c00, bg=c01)
    v_despesas.place(x=300, y=100)

    l_saldo = Label(frameMiddle, text="TOTAL SALDO DA CAIXA", font=("Verdana", 10, "bold"), fg=c02, bg=c01)
    l_saldo.place(x=300, y=140)

    v_saldo = Label(frameMiddle, text="R$ {:,.2f}".format(valor[2]), font=("Verdana", 14, "bold"), fg=c00, bg=c01)
    v_saldo.place(x=300, y=160)

def pie_graph():
    figure = plt.Figure(figsize=(5,3),dpi=90)
    ax = figure.add_subplot(111)
    
    valor = pie_valores()[1]
    
    lista_categorias = pie_valores()[0]
    explode = []
    
    for i in lista_categorias:
        explode.append(0.05)
    wedges,texts,autotexts =  ax.pie(valor,explode=explode,autopct='%1.1f%%', colors=colors,shadow=True, startangle=140, wedgeprops={'edgecolor': 'white','width':0.3})
    ax.legend(lista_categorias, loc="center left", bbox_to_anchor=(1, 0.5))   
       
    for text in texts:
        text.set_fontsize(8)
    for autotext in autotexts:
        autotext.set_fontsize(9)


    canva = FigureCanvasTkAgg(figure, frame_graphPie)
    canva.get_tk_widget().grid(row=0,column=0)
    
def show_renda():
    tabela_head = ['#Id','Categoria','Data','Quantia']
    lista_itens = tabela()
    global tree

    tree = ttk.Treeview(frame_renda, selectmode="extended",columns=tabela_head, show="headings")
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0
    
    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n],anchor=hd[n])
        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)
    
global tree 
def inserir_categoria_b():
    nome = e_categoria.get()    
    lista_inserir = [nome]
    for i in lista_inserir:
        if i =='':
            messagebox.showerror('Erro','Preencha todos os campos')
            return
    insert_categoria(lista_inserir)
    messagebox.showinfo('Sucesso','Os dados foram inseridos com sucesso')
    e_categoria.delete(0,'end')
    categorias_funcao = view_categoria()
    category = []
    for i in categorias_funcao:
        category.append(i[1])
    combo_category_despesa['values'] = (category)

def inserir_receitas_b():
    nome = 'Receita'
    data = e_cal_receita.get()
    qtd = e_valor_receitas.get()
    
    list_inserir = [nome,data,qtd]
    for i in list_inserir:
        if i == '':
            messagebox.showerror('Erro','Preencha todos os campos')
            return
    insert_receita(list_inserir)
    messagebox.showinfo('Sucesso','Os dados foram inseridos com sucesso')
    
    e_cal_receita.delete(0,'end')
    e_valor_receitas.delete(0,'end')
    show_renda()
    porcent()
    bar_graph()
    pie_graph()
    resum() 


def inserir_despesas_b():
    nome = combo_category_despesa.get()
    data = e_cal_despesas.get()
    qtd = e_valor_despesas.get()
    
    list_inserir = [nome,data,qtd]
    for i in list_inserir:
        if i == '':
            messagebox.showerror('Erro','Preencha todos os campos')
            return
    insert_gastos(list_inserir)
    messagebox.showinfo('Sucesso','Os dados foram inseridos com sucesso')
    
    combo_category_despesa.delete(0,'end')
    e_cal_despesas.delete(0,'end')
    e_valor_despesas.delete(0,'end')
    show_renda()
    porcent()
    bar_graph()
    pie_graph()
    resum() 
    
def delete_b():
    try:
        treev_dados = tree.focus()
        if not treev_dados:  # Nenhum item selecionado
            return  

        treev_dicionario = tree.item(treev_dados)
        tree_lista = treev_dicionario.get('values', [])

        if not tree_lista:
            return  
        
        valor = tree_lista[0]
        nome = tree_lista[1]

        if nome == 'Receita':
            delete_receitas([nome])
        else:
            delete_gastos([valor])

        tree.delete(treev_dados)
        messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')

        show_renda()
        porcent()
        bar_graph()
        pie_graph()
        resum()

    except Exception as e:
        messagebox.showerror('Erro', f'Ocorreu um erro: {e}')
        

# Criando janela
window = Tk()
window.title("Controle de Orçamento")  
window.geometry('900x660')
window.configure(background=c09)
window.resizable(width=False, height=False)

style = ttk.Style(window)
style.theme_use("clam")

# Frames
frameUP = Frame(window, width=1043, height=50, bg=c01, relief="flat")
frameUP.grid(row=0, column=0)

frameMiddle = Frame(window, width=1043, height=361, bg=c01, pady=20, relief="raised")
frameMiddle.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

frameDown = Frame(window, width=1043, height=300, bg=c01, relief="flat")
frameDown.grid(row=2, column=0, pady=1, padx=10, sticky=NSEW)

frame_graphPie = Frame(frameMiddle,width=580,height=250,bg=c02)
frame_graphPie.place(x=415,y=5)

# Trabalhando no frameUP
try:
    app_img = Image.open('logo.png')
    app_img = app_img.resize((45, 45))
    app_img = ImageTk.PhotoImage(app_img)

    app_logo = Label(frameUP, image=app_img, text=" Orçamento Pessoal", width=900, compound=LEFT,
                     padx=5, relief=RAISED, anchor=NW, font=("Verdana 20 bold italic"), bg=c01, fg=c00)
    app_logo.place(x=0, y=0)
except Exception as e:
    print("Erro ao carregar a imagem:", e)

# Chamando funções
porcent()
bar_graph()
resum()
pie_graph()

#Frames dentro do FrameDown
frame_renda = Frame(frameDown, width=300, height=250, bg=c01, relief="flat")
frame_renda.grid(row=0, column=0)
      
frame_operacoes = Frame(frameDown, width=220, height=250, bg=c01, relief="flat")
frame_operacoes.grid(row=0, column=1,padx=5)

frame_config = Frame(frameDown, width=300, height=250, bg=c01, relief="flat")
frame_config.grid(row=0, column=2,padx=5)

#Tabela RENDA MENSAL
app_tabela = Label(frameMiddle, text="Tabela de Receitas e Despesas", anchor=NW, font=("Verdana 12 bold italic"), bg=c01, fg=c00)
app_tabela.place(x=5, y=309)

show_renda()

#Configurações Despesas
l_info = Label(frame_operacoes,text='Insira novas despesas',height=1,anchor=NW,font=('Verdana 10 bold'),bg=c01,fg=c00)
l_info.place(x=10,y=10)

#Configurações Categoria
l_category = Label(frame_operacoes,text='Categoria',height=1,anchor=NW,font=('Ivy 10'),bg=c01,fg=c00)
l_category.place(x=10,y=40)


category_fuction = view_categoria()
category = []
for i in category_fuction:
    category.append(i[1])
combo_category_despesa = ttk.Combobox(frame_operacoes,width=10,font=('Ivy 10'))
combo_category_despesa['values'] = (category)
combo_category_despesa.place(x=110,y=41)

#Configurações Despesas
l_cal_despesas= Label(frame_operacoes,text='Data',height=1,anchor=NW,width=entry_width,font=('Ivy 10'),bg=c01,fg=c00)
l_cal_despesas.place(x=10,y=70)

e_cal_despesas = DateEntry(frame_operacoes,width=entry_width,background='darkblue',foreground='white',borderwitdh=2,year=2022)
e_cal_despesas.place(x=110,y=71)

#Configurações Valor
l_valor_despesas= Label(frame_operacoes,text='Quantia Total',height=1,anchor=NW,font=('Ivy 10'),bg=c01,fg=c00)
l_valor_despesas.place(x=10,y=100)

e_valor_despesas = Entry(frame_operacoes,width=entry_width,justify='left',relief='solid')
e_valor_despesas.place(x=110,y=101)

#Botão ADD
img_add_despesas = Image.open('add.png')
img_add_despesas = img_add_despesas.resize((17, 17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)

add_despesas = Button(frame_operacoes,command=inserir_despesas_b, image=img_add_despesas, text="ADD", width=button_width, compound=LEFT,
                    anchor=NW, font=("Ivy 7 bold"), bg=c01, fg=c00,overrelief=RIDGE)
add_despesas.place(x=110, y=131)



#Botão Delete
l_remove= Label(frame_operacoes,text='Excluir ação',height=1,anchor=NW,font=('Ivy 10 bold'),bg=c01,fg=c00)
l_remove.place(x=10,y=190)

button_remove = Image.open('excluir.png')
button_remove = button_remove.resize((17, 17))
button_remove = ImageTk.PhotoImage(button_remove)

remove = Button(frame_operacoes, image=button_remove, text="DELETE", width=button_width, compound=LEFT,
                    anchor=NW, font=("Ivy 7 bold"), bg=c01, fg=c00,overrelief=RIDGE, command=delete_b)
remove.place(x=110, y=190)


#Configurando receitas
l_info_receita = Label(frame_config,text='Inserir nova receita',height=1,anchor=NW,font=('Verdana 10 bold'),bg=c01,fg=c00)
l_info_receita.place(x=10,y=10)


#Calendario
l_cal_receita = Label(frame_config,text='Data',height=1,anchor=NW,font=('Ivy 10'),bg=c01,fg=c00)
l_cal_receita.place(x=10,y=40)
e_cal_receita = DateEntry(frame_config,width=entry_width,background='darkblue',foreground='white',borderwitdh=2,year=2022)
e_cal_receita.place(x=110,y=41)


l_valor_receitas= Label(frame_config,text='Quantia Total',height=1,anchor=NW,font=('Ivy 10'),bg=c01,fg=c00)
l_valor_receitas.place(x=10,y=70)
e_valor_receitas = Entry(frame_config,width=entry_width,justify='left',relief='solid')
e_valor_receitas.place(x=110,y=71)

#Botão ADD
img_add_receitas = Image.open('add.png')
img_add_receitas = img_add_receitas.resize((17, 17))
img_add_receitas = ImageTk.PhotoImage(img_add_receitas)

add_receitas = Button(frame_config,command=inserir_receitas_b,image=img_add_receitas, text="ADD", width=button_width, compound=LEFT,
                    anchor=NW, font=("Ivy 7 bold"), bg=c01, fg=c00,overrelief=RIDGE)
add_receitas.place(x=110, y=111)

#Nova categoria
l_categoria = Label(frame_config,text='Categoria',height=1,anchor=NW,font=('Verdana 10 bold'),bg=c01,fg=c00)
l_categoria.place(x=10,y=160)
e_categoria = Entry(frame_config,width=entry_width,justify='left',relief='solid')
e_categoria.place(x=110,y=160)

#Botão ADD
img_add_categoria = Image.open('add.png')
img_add_categoria = img_add_categoria.resize((17, 17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)

add_receitas = Button(frame_config,command=inserir_categoria_b, image=img_add_categoria, text="ADD", width=button_width, compound=LEFT,
                    anchor=NW, font=("Ivy 7 bold"), bg=c01, fg=c00,overrelief=RIDGE)
add_receitas.place(x=110, y=190)


window.mainloop()