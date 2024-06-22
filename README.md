# Manager App

Este projeto é parte da disciplina de Tópicos Especiais em Computação da Universidade Federal de Itajubá (UNIFEI). O Manager App é uma aplicação desenvolvida para gerenciar colaboradores, equipes, projetos e tarefas, facilitando a organização e o acompanhamento de atividades em um ambiente corporativo ou acadêmico.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

| Pasta/Arquivo                     | Descrição                                      |
|-----------------------------------|------------------------------------------------|
| `controllers/`                    | Contém os controladores do projeto.            |
| ├─ `__init__.py`                  | Arquivo de inicialização do pacote.            |
| ├─ `collaborator_controller.py`   | Controlador para os colaboradores.             |
| ├─ `team_controller.py`           | Controlador para as equipes.                   |
| ├─ `project_controller.py`        | Controlador para os projetos.                  |
| └─ `task_controller.py`           | Controlador para as tarefas.                   |
| `models/`                         | Define as estruturas de dados do projeto.      |
| ├─ `__init__.py`                  | Arquivo de inicialização do pacote.            |
| ├─ `collaborator.py`              | Modelo para os colaboradores.                  |
| ├─ `team.py`                      | Modelo para as equipes.                        |
| ├─ `project.py`                   | Modelo para os projetos.                       |
| └─ `task.py`                      | Modelo para as tarefas.                        |
| `views/`                          | Responsável pela interface gráfica do usuário. |
| ├─ `__init__.py`                  | Arquivo de inicialização do pacote.            |
| ├─ `collaborator_view.py`         | View para os colaboradores.                    |
| ├─ `team_view.py`                 | View para as equipes.                          |
| ├─ `project_view.py`              | View para os projetos.                         |
| └─ `task_view.py`                 | View para as tarefas.                          |
| `main.py`                         | Ponto de entrada da aplicação.                 |
| `database.db`                     | Banco de dados SQLite do projeto.              |
| `init_db.py`                      | Script paar criação do banco                   |

- **controllers/**: Contém os controladores que intermediam a comunicação entre as views e os modelos.
- **models/**: Define as estruturas de dados do projeto, representando colaboradores, equipes, projetos e tarefas.
- **views/**: Responsável pela interface gráfica do usuário, permitindo a interação com os dados do sistema.
- **main.py**: Ponto de entrada da aplicação, onde o loop principal é executado.
- **database.db**: Banco de dados SQLite onde os dados da aplicação são armazenados.

## Como Executar

Para executar o Manager App, siga os passos abaixo:

1. Certifique-se de ter o Python instalado em sua máquina.
2. Clone o repositório para o seu ambiente local.
3. Navegue até a pasta do projeto e instale as dependências necessárias utilizando o comando `pip install -r requirements.txt` (assumindo que um arquivo de dependências esteja presente).
4. Execute o arquivo `main.py` com o comando `python main.py`.

## Contribuições

Contribuições são bem-vindas! Se você deseja contribuir com o projeto, sinta-se à vontade para fazer um fork do repositório, realizar as alterações desejadas e submeter um Pull Request.

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Para mais informações, entre em contato com os desenvolvedores através dos e-mails disponíveis no perfil do GitHub.

---

Desenvolvido por estudantes da UNIFEI para a disciplina de Tópicos Especiais em Computação.
