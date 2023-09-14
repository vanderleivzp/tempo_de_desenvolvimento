# tempo_de_desenvolvimento
Descrição Geral
Este script Python utiliza a biblioteca tkinter para criar uma interface gráfica para monitorar as horas trabalhadas em diferentes projetos. Ele interage com um banco de dados PostgreSQL para armazenar e recuperar informações sobre os projetos e os registros de tempo. O script também é capaz de calcular a soma total de tempo gasto em um projeto e exportar os dados para um arquivo Excel ou de texto.

Bibliotecas Utilizadas
tkinter: Usada para criar a interface gráfica do programa.
psycopg2: Uma biblioteca PostgreSQL que permite a interação com o banco de dados PostgreSQL.
datetime: Usada para trabalhar com datas e horas.
pandas: Utilizada para a manipulação de dados, especialmente útil ao exportar dados para um arquivo Excel.
configparser: Usada para ler um arquivo de configuração que contém as configurações do banco de dados.
Estrutura do Banco de Dados
O banco de dados contém duas tabelas:

projetos: Mantém informações sobre os projetos. Contém os campos:

id: um identificador único para cada projeto (chave primária).
nome: o nome do projeto.
registros: Mantém informações sobre os registros de tempo para cada projeto. Contém os campos:

id: um identificador único para cada registro (chave primária).
projeto_id: um identificador que liga o registro a um projeto específico (chave estrangeira).
data: a data de um registro específico.
inicio: o tempo de início do registro.
fim: o tempo de finalização do registro.
observacao: um campo para notas adicionais sobre o registro.
Funcionalidades do Programa
Conexão com o Banco de Dados: Estabelece conexão com o banco de dados e cria as tabelas se não existirem.

Gerenciamento de Projetos: Permite ao usuário criar novos projetos e selecionar ou excluir projetos existentes.

Monitoramento do Tempo de Trabalho: Permite ao usuário iniciar e parar o monitoramento do tempo de trabalho em um projeto selecionado, registrando o tempo de início e de fim, além de observações adicionais.

Cálculo e Exportação de Dados: Calcula o tempo total gasto em um projeto e permite a exportação desses dados para um arquivo Excel ou de texto.

Interface Gráfica: A interface gráfica contém vários componentes, incluindo botões para iniciar/parar o registro de tempo, calcular o tempo total gasto, e uma listbox para selecionar projetos.

Funções Principais
excluir_projeto(): Permite ao usuário excluir um projeto da lista.
atualizar_data_hora(): Atualiza a data e a hora exibidas na interface gráfica a cada segundo.
selecionar_projeto(): Permite ao usuário selecionar um projeto da lista.
iniciar_trabalho(): Permite ao usuário iniciar um novo trabalho, criando um novo projeto ou selecionando um existente.
atualizar_estado_botoes(): Atualiza o estado dos botões na interface gráfica com base nas ações do usuário.
iniciar(): Inicia o registro de tempo para o projeto selecionado.
parar(): Para o registro de tempo para o projeto selecionado.
calcular(): Calcula o tempo total gasto no projeto selecionado e oferece a opção de exportar os dados.
sair(): Permite ao usuário sair do programa, com uma verificação para garantir que não haja uma sessão ativa.
Pontos Notáveis
As configurações do banco de dados são lidas de um arquivo bdcron.cfg.
O script utiliza uma abordagem de conexão de banco de dados resiliente, criando o banco de dados se não existir na primeira execução.
As funções interagem diretamente com o banco de dados usando consultas SQL através do psycopg2 para realizar operações de CRUD.
A exportação de dados pode ser feita tanto em formato Excel quanto em texto.
A interface gráfica possui elementos para melhorar a usabilidade, incluindo mensagens de erro detalhadas e atualizações dinâmicas de elementos da interface com base no estado do programa.
Desenvolvedor
O programa foi desenvolvido por Vanderlei Pereira Rodrigues.
