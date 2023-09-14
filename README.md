Programa de Monitoramento de Horas Trabalhadas em Projetos

O programa desenvolvido por Vanderlei Pereira Rodrigues serve para monitorar as horas trabalhadas em diferentes projetos. Utiliza uma interface gráfica criada com a biblioteca tkinter e interage com um banco de dados PostgreSQL para armazenar e recuperar informações sobre os projetos e os registros de tempo. É capaz de calcular a soma total de tempo gasto em um projeto e exportar os dados para um arquivo Excel ou de texto.

Instalação
Pré-requisitos
Python 3.x
PostgreSQL
Bibliotecas Python: tkinter, psycopg2, datetime, pandas e configparser.
Instalação das Bibliotecas
Utilize o seguinte comando para instalar todas as bibliotecas necessárias:

#pip install tkinter psycopg2 datetime pandas configparser

Funcionalidades
Conexão com o Banco de Dados: Estabelece conexão com o banco de dados e cria as tabelas se não existirem.
Gerenciamento de Projetos: Possibilita a criação de novos projetos e a seleção ou exclusão de projetos existentes.
Monitoramento do Tempo de Trabalho: Facilita o início e a parada do monitoramento do tempo de trabalho em um projeto selecionado, registrando o tempo de início e de fim, bem como observações adicionais.
Cálculo e Exportação de Dados: Calcula o tempo total gasto em um projeto e possibilita a exportação desses dados para um arquivo Excel ou de texto.
Interface Gráfica: Contém múltiplos componentes, como botões para iniciar/parar o registro de tempo e calcular o tempo total gasto, além de uma lista para selecionar projetos.
Estrutura do Banco de Dados
O banco de dados contém duas tabelas principais:

projetos: Mantém informações sobre os projetos, com os campos:

id: Identificador único para cada projeto (chave primária).
nome: Nome do projeto.
registros: Contém informações sobre os registros de tempo para cada projeto, com os campos:

id: Identificador único para cada registro (chave primária).
projeto_id: Identificador que liga o registro a um projeto específico (chave estrangeira).
data: Data de um registro específico.
inicio: Tempo de início do registro.
fim: Tempo de finalização do registro.
observacao: Campo para notas adicionais sobre o registro.
Funções Principais
excluir_projeto(): Exclui um projeto da lista.
atualizar_data_hora(): Atualiza a data e a hora exibidas na interface gráfica a cada segundo.
selecionar_projeto(): Seleciona um projeto da lista.
iniciar_trabalho(): Inicia um novo trabalho, criando um novo projeto ou selecionando um já existente.
atualizar_estado_botoes(): Atualiza o estado dos botões na interface gráfica com base nas ações do usuário.
iniciar(): Começa o registro de tempo para o projeto selecionado.
parar(): Interrompe o registro de tempo para o projeto selecionado.
calcular(): Calcula o tempo total gasto no projeto selecionado e oferece a opção de exportar os dados.
sair(): Encerra o programa, com uma verificação para garantir que não haja uma sessão ativa.
Uso
Execute o script Python no seu ambiente de desenvolvimento de preferência. Utilize a interface gráfica para gerenciar projetos e registrar o tempo gasto em cada um deles.

Contribuição
Sinta-se à vontade para contribuir com o projeto, fazendo fork e submetendo pull requests.

Licença
Este projeto está sob a licença MIT.

Contato
Desenvolvedor: Vanderlei Pereira Rodrigues

Email: vanderlei060393@gmail.com
LinkedIn: https://www.linkedin.com/in/vanderlei-pereira-rodrigues-40546a202
Suporte
Se você encontrar algum problema ou tiver alguma sugestão, por favor, abra uma issue no GitHub.

Agradecimentos
Agradeço por utilizar e contribuir com este projeto!
