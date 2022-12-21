from tkinter import *
from obj import PessoaFisicaReceitaFederal 
fields = ('Rendimentos', 'Deducoes')
calculadora = PessoaFisicaReceitaFederal()

def calcula_imposto(entries):
   calculadora.calcula_imposto()
   
   entries['Base de Calculo'].delete(0,END)
   entries['Base de Calculo'].insert(0, calculadora.base_de_calculo())
   entries['Imposto'].delete(0,END)
   entries['Imposto'].insert(0, calculadora.imposto)
   entries['Aliquota Efetiva'].delete(0,END)
   entries['Aliquota Efetiva'].insert(0, calculadora.calcular_aliquota_efetiva()) 
def add_rendimento(entries):
   valor = float(entries[1].get())
   descricao = str(entries[0].get())
   if valor < 0:
      valor = 0
   calculadora.cadastrar_rendimentos(valor, descricao)
   
def add_deducao(entries):
   valor = float(entries[1].get())
   descricao = str(entries[0].get())
   if valor < 0:
      valor = 0
   calculadora.insere_deducao(valor, descricao)

def add_dependente(entries):
   nome = str(entries[1].get())
   datanascimento = str(entries[0].get())
   
   calculadora.cadastra_dependentes(nome, datanascimento)

def makeform(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      ent2 = Entry(row)
      ent2.insert(0,"0")
      ent.insert(0,"Descricao")
      row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
      lab.pack(side = LEFT)
      ent.pack(side = RIGHT, expand = YES, fill = X)
      ent2.pack(side = RIGHT, expand = YES, fill = X)    
      entries[field] = [ent, ent2]
      if field == "Rendimentos":
         b1 = Button(root, text = 'Adiciona',
         command=(lambda e = entries[field] : add_rendimento(e)))
         b1.pack()
      else:
         b1 = Button(root, text = 'Adiciona',
         command=(lambda e = entries[field] : add_deducao(e)))
         b1.pack()
      
   row = Frame(root)
   lab = Label(row, width=22, text=field+": ", anchor='w')
   ent = Entry(row)
   ent2 = Entry(row)
   ent2.insert(0,"Nome")
   ent.insert(0,"Data Nascimento")
   row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
   lab.pack(side = LEFT)
   ent.pack(side = RIGHT, expand = YES, fill = X)
   ent2.pack(side = RIGHT, expand = YES, fill = X)    
   entries["Dependentes"] = [ent, ent2]
   b1 = Button(root, text = 'Adiciona',
   command=(lambda e = entries["Dependentes"] : add_dependente(e)))
   b1.pack()
   for field in ('Base de Calculo', 'Imposto', 'Aliquota Efetiva'):
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,"0")
      row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
      lab.pack(side = LEFT)
      ent.pack(side = RIGHT, expand = YES, fill = X)
      entries[field] = ent
   
   return entries
if __name__ == '__main__':
   root = Tk()
   root.title("Calculadora IRPF")
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e = ents: fetch(e)))
   b1 = Button(root, text = 'Calcula',
      command=(lambda e = ents: calcula_imposto(e)))
   b1.pack(side = LEFT, padx = 5, pady = 5)
   b3 = Button(root, text = 'Quit', command = root.quit)
   b3.pack(side = LEFT, padx = 5, pady = 5)
   root.mainloop()