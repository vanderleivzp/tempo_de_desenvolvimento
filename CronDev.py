import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
from datetime import datetime
import psycopg2
from psycopg2 import sql
from configparser import ConfigParser
import pandas as pd

# Ler configurações do arquivo de configuração
config = ConfigParser()
config.read('bdcron.cfg')
db_config = config['database']

# Conexão inicial para verificar/criar o banco de dados
try:
    conn = psycopg2.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        dbname=db_config['dbname']
    )
except psycopg2.OperationalError:
    conn = psycopg2.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        dbname='postgres'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(sql.SQL(f"CREATE DATABASE {db_config['dbname']}"))
    conn.close()

    conn = psycopg2.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        dbname=db_config['dbname']
    )

cursor = conn.cursor()

# Criar tabelas se não existirem
cursor.execute("""
CREATE TABLE IF NOT EXISTS projetos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS registros (
    id SERIAL PRIMARY KEY,
    projeto_id INTEGER,
    data DATE,
    inicio TIMESTAMP,
    fim TIMESTAMP,
    observacao TEXT,
    FOREIGN KEY (projeto_id) REFERENCES projetos(id)
)
""")
conn.commit()

def excluir_projeto():
    def on_select(evt):
        global projeto_id
        projeto_id, nome_projeto = projetos_listbox.get(projetos_listbox.curselection())
        if projeto_id == projeto_atual:
            messagebox.showwarning("Operação não permitida", "Você não pode excluir o projeto que está atualmente selecionado.")
            return
        resposta = messagebox.askquestion("Excluir Projeto", f"Tem certeza que deseja excluir o projeto '{nome_projeto}'?")
        if resposta == 'yes':
            cursor.execute("DELETE FROM registros WHERE projeto_id = %s", (projeto_id,))
            cursor.execute("DELETE FROM projetos WHERE id = %s", (projeto_id,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Projeto excluído com sucesso")
            # Atualizar a lista de projetos na listbox
            projetos_listbox.delete(projetos_listbox.curselection())
        dialogo.destroy()

    dialogo = tk.Toplevel()  # Aqui criamos uma nova janela antes de chamar métodos nela
    dialogo.title("Selecionar Projeto")
    dialogo.title("Selecionar Projeto")
    projetos_listbox = tk.Listbox(dialogo, font=('Helvetica', 12))
    scrollbar = tk.Scrollbar(dialogo, orient="vertical")
    scrollbar.config(command=projetos_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    projetos_listbox.config(yscrollcommand=scrollbar.set)
    projetos_listbox.pack(fill="both", expand=True)

    cursor.execute("SELECT id, nome FROM projetos")
    projetos = cursor.fetchall()
    for projeto in projetos:
        projetos_listbox.insert(tk.END, projeto)

    projetos_listbox.bind('<<ListboxSelect>>', on_select)

        
def atualizar_data_hora():
    lbl_data_hora.config(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    root.after(1000, atualizar_data_hora)
    
def selecionar_projeto():
    global projeto_atual, lbl_nome_projeto

    def on_select(evt):
        global projeto_atual
        projeto_selecionado = projetos_listbox.get(projetos_listbox.curselection())
        projeto_atual = projeto_selecionado[0]
        lbl_nome_projeto.config(text=f"Projeto Atual: {projeto_selecionado[1]}")
        dialogo.destroy()
        # Atualize o estado dos botões aqui, depois que um projeto foi selecionado
        atualizar_estado_botoes()
    
    dialogo = tk.Toplevel()  # Aqui criamos uma nova janela antes de chamar métodos nela
    dialogo.title("Selecionar Projeto")
    dialogo.title("Selecionar Projeto")
    projetos_listbox = tk.Listbox(dialogo, font=('Helvetica', 12))
    scrollbar = tk.Scrollbar(dialogo, orient="vertical")
    scrollbar.config(command=projetos_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    projetos_listbox.config(yscrollcommand=scrollbar.set)
    projetos_listbox.pack(fill="both", expand=True)
    
    cursor.execute("SELECT id, nome FROM projetos")
    projetos = cursor.fetchall()
    for projeto in projetos:
        projetos_listbox.insert(tk.END, projeto)
    
    projetos_listbox.bind('<<ListboxSelect>>', on_select)

projeto_atual = None  # Certifique-se de que está definido no escopo global no início do script
trabalho_iniciado = False # Variável para rastrear se um trabalho foi iniciado

def iniciar_trabalho():
    global projeto_atual, trabalho_iniciado  # Adicionamos trabalho_iniciado aqui
    if projeto_atual or trabalho_iniciado:
        messagebox.showwarning("Operação não permitida", "Você não pode iniciar um novo trabalho enquanto um projeto está selecionado ou um trabalho está em andamento.")
        return
    resposta = messagebox.askquestion("Iniciar Trabalho", "Deseja iniciar um novo projeto?")
    lbl_data_hora.config(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    if resposta == 'yes':
        nome_projeto = simpledialog.askstring("Novo Projeto", "Informe o nome do novo projeto:")
        cursor.execute("INSERT INTO projetos (nome) VALUES (%s) RETURNING id", (nome_projeto,))
        projeto_id = cursor.fetchone()[0]
        conn.commit()
        projeto_atual = projeto_id  # Atualize projeto_atual aqui
        atualizar_estado_botoes()
    else:
        selecionar_projeto()

# Novo método para atualizar o estado dos botões
def atualizar_estado_botoes():
    global trabalho_iniciado  # Adicionamos trabalho_iniciado aqui
    if projeto_atual:
        cursor.execute("SELECT nome FROM projetos WHERE id = %s", (projeto_atual,))
        nome_projeto = cursor.fetchone()[0]
        lbl_nome_projeto.config(text=f"Projeto Atual: {nome_projeto}")
        iniciar['state'] = tk.NORMAL if not trabalho_iniciado else tk.DISABLED  # Modificamos esta linha
        parar['state'] = tk.NORMAL
        calcular['state'] = tk.NORMAL
    else:
        iniciar['state'] = tk.NORMAL if not trabalho_iniciado else tk.DISABLED  # Adicionamos esta linha para desativar o botão se um trabalho estiver em andamento
        parar['state'] = tk.DISABLED  # Modificamos esta linha para desativar o botão parar se nenhum projeto estiver selecionado
        calcular['state'] = tk.DISABLED  # Modificamos esta linha para desativar o botão calcular se nenhum projeto estiver selecionado

def iniciar():
    global hora_inicio, trabalho_iniciado  # Adicionamos trabalho_iniciado aqui
    trabalho_iniciado = True  # Definimos trabalho_iniciado como True aqui
    hora_inicio = datetime.now()
    observacao = simpledialog.askstring("Observação", "Informe uma observação para este registro:")  # Solicitar observação
    cursor.execute("INSERT INTO registros (projeto_id, data, inicio, observacao) VALUES (%s, %s, %s, %s)", 
                   (projeto_atual, hora_inicio.date(), hora_inicio, observacao))  # Inserir observação no banco de dados
    conn.commit()
    iniciar['state'] = tk.DISABLED
    lbl_informacao.config(text=f"Iniciado em: {hora_inicio}")
    messagebox.showinfo("Info", f"Registro iniciado em {hora_inicio}")

def parar():
    global trabalho_iniciado  # Adicionamos trabalho_iniciado aqui
    trabalho_iniciado = False  # Definimos trabalho_iniciado como False aqui
    hora_fim = datetime.now()
    cursor.execute("UPDATE registros SET fim = %s WHERE id = (SELECT MAX(id) FROM registros WHERE projeto_id = %s)", (hora_fim, projeto_atual))
    conn.commit()
    iniciar['state'] = tk.NORMAL
    lbl_informacao.config(text="")
    messagebox.showinfo("Info", f"Registro finalizado em {hora_fim}")

def calcular():
    cursor.execute("""
    SELECT 
        data, 
        inicio,
        fim,
        EXTRACT(EPOCH FROM fim - inicio) AS segundos,
        observacao   
    FROM registros 
    WHERE projeto_id = %s 
    ORDER BY data, inicio
    """, (projeto_atual,))
    resultados = cursor.fetchall()

    total_segundos = sum([res[3] for res in resultados if res[3] is not None])
    total_horas, resto = divmod(total_segundos, 3600)
    total_minutos = resto // 60

    dias = len(set(res[0] for res in resultados if res[3] is not None))

    resultado_str = "\n".join([f"{res[0]}: Entrada - {res[1].strftime('%H:%M:%S')} | Saída - {res[2].strftime('%H:%M:%S')} | Horas - {(res[3]//3600):.2f} | Minutos - {int(res[3]%3600//60)} | Observação - {res[4]}" for res in resultados if res[3] is not None])
    resultado_str += f"\n\nResumo:\nDias trabalhados: {dias}\nTotal de horas: {int(total_horas)}\nTotal de minutos: {int(total_minutos)}"
    
    resposta = messagebox.askquestion("Exportar", "Deseja exportar os resultados?")
    if resposta == 'yes':
        tipo_arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("Text files", "*.txt")])
        if tipo_arquivo:
            if tipo_arquivo.endswith(".xlsx"):
                # Aqui estamos especificando todas as 5 colunas
                df = pd.DataFrame(resultados, columns=['Data', 'Inicio', 'Fim', 'Segundos', 'Observacao'])
                df.to_excel(tipo_arquivo, index=False)
            else:
                with open(tipo_arquivo, 'w') as f: # Aqui mudamos para 'tipo_arquivo' em vez de 'relatorio.txt' para usar o nome do arquivo escolhido pelo usuário
                    for res in resultados:
                        if res[3] is not None:
                            f.write(f"{res[0]}: {(res[3]/3600):.2f} horas\n")  # Calculamos as horas antes de formatar a string
                    f.write(f"\nTotal: {total_horas} horas e {total_minutos} minutos")

    messagebox.showinfo("Resultado", resultado_str)
    
def sair():
    cursor.execute("SELECT fim FROM registros WHERE projeto_id = %s ORDER BY id DESC LIMIT 1", (projeto_atual,))
    ultimo_registro = cursor.fetchone()
    if ultimo_registro and ultimo_registro[0] is None:
        messagebox.showwarning("Operação Proibida", "Você não pode sair enquanto uma sessão está ativa. Por favor, pare a sessão antes de sair.")
        return
    root.quit()

# Criar a interface gráfica
root = tk.Tk()
root.title("Monitor de Horas")
root.configure(bg='#f0f0f0')

# Adicionando mensagem estática no cabeçalho
lbl_desenvolvedor = tk.Label(root, text="Desenvolvido by Vanderlei Rodrigues", font=('Helvetica', 14, 'italic'), bg='#f0f0f0')
lbl_desenvolvedor.pack(pady=10)

# Configure as fontes e cores dos seus labels para uma aparência mais limpa e moderna
lbl_nome_projeto = tk.Label(root, text="Nenhum projeto selecionado", font=('Helvetica', 14, 'bold'))
lbl_nome_projeto.pack(pady=10)

lbl_descricao = tk.Label(root, text="Este programa ajuda você a monitorar o tempo gasto em diferentes projetos. Você pode iniciar um novo projeto ou continuar um existente, registrando o tempo gasto em cada sessão.", font=('Helvetica', 10), wraplength=500)
lbl_descricao.pack(pady=10)

lbl_data_hora = tk.Label(root, text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), font=('Helvetica', 16, 'bold'))
lbl_data_hora.pack(pady=10)

# ...

# Use ttk.Button em vez de tk.Button para botões com um visual mais moderno
tk.Button(root, text="Iniciar Trabalho", command=iniciar_trabalho).pack(pady=20)
iniciar = ttk.Button(root, text="Iniciar", state=tk.DISABLED, command=iniciar)
iniciar.pack(pady=20)
parar = ttk.Button(root, text="Parar", state=tk.DISABLED, command=parar)
parar.pack(pady=20)
calcular = ttk.Button(root, text="Calcular", state=tk.DISABLED, command=calcular)
calcular.pack(pady=20)

# Adicionando um botão de saída
tk.Button(root, text="Sair", command=sair).pack(pady=20)

lbl_informacao = tk.Label(root, text="", font=('Helvetica', 12), bg='#f0f0f0')
lbl_informacao.pack(pady=10)

tk.Button(root, text="Excluir Projeto", command=excluir_projeto, font=('Helvetica', 12), bg='#d9534f', fg='white').pack(pady=20)


# Inicializando a atualização contínua da data e hora
atualizar_data_hora()

root.mainloop()