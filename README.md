📦 Sistema de Gerenciamento de Estoque (CLI)

Este é um sistema de linha de comando (CLI) construído em Python, utilizando a biblioteca `rich` para um output mais visual e amigável. O sistema é baseado em Programação Orientada a Objetos (POO) e utiliza um arquivo JSON (`inventario.json`) para persistência de dados.

🚀 Funcionalidades Atuais (V1)

A versão atual permite o gerenciamento completo do ciclo de vida dos produtos:

* Adição de Produtos: Insere novos itens com validação de dados críticos (quantidade positiva, preço positivo, fornecedor obrigatório).

* Atualização de Quantidades: Permite adicionar ou remover unidades do estoque.

* Exibição Detalhada do Inventário: Apresenta uma tabela completa e estilizada (10 colunas) com todos os detalhes do produto, incluindo ID, Descrição, Preço de Compra e Número de Série.

* Exclusão de Produtos: Remove itens do inventário, com desambiguação por ID em caso de nomes duplicados.

* Persistência de Dados: Todos os dados são salvos automaticamente no arquivo `inventario.json`.

⚙️ Instalação e Execução (RECOMENDADO)

Para rodar este projeto de forma correta e isolada, é fundamental utilizar um Ambiente Virtual.

1. Criar o Ambiente Virtual:

    ```bash
    python -m venv venv
    ```


2. Ativar o Ambiente Virtual:

* No Windows (PowerShell/CMD):

    ```bash
    .\venv\Scripts\activate
    ```


* No macOS/Linux (Bash/Zsh):

    ```bash
    source venv/bin/activate
    ```


(Você saberá que o ambiente está ativo quando vir `(venv)` no início da linha de comando.)

3. Instalar Dependências:
Instale a biblioteca rich e quaisquer futuras dependências usando o ficheiro requirements.txt:

    ```bash
    pip install -r requirements.txt
    ```


4. Executar o programa:

    ```bash
    python gerenciamento_inventario.py
    ```


🤝 Como Contribuir

Agradeço o seu interesse em melhorar este projeto! Para garantir um processo de colaboração suave, siga estas diretrizes.

📝 Guia de Estilo de Código (Python)

Por favor, adote as seguintes regras de codificação ao enviar o seu código:

1. Conformidade com PEP 8: O código deve seguir o Guia de Estilo para Código Python, especialmente o limite de 79 caracteres por linha.

2. Docstrings: Utilize docstrings concisas para explicar a funcionalidade de classes e funções (utilize a formatação standard do Python).

3. Tipagem: Sempre que possível, utilize anotações de tipo (`type hints`) para aumentar a clareza.

4. Variáveis e Nomes: Utilize `snake_case` para nomes de variáveis e funções, e `CamelCase` para classes.

5. Comentários: Use comentários apenas para explicar lógica complexa ou partes não óbvias do código.

6. Rich: Mantenha a utilização da biblioteca rich para todas as saídas de consola (`console.print()`) e evite o `print()` nativo.

🐛 Reportar Bugs

Se encontrar algum erro:

1. Verifique se o erro já foi reportado nas `Issues`.

2. Crie uma nova `Issue` com um título descritivo e inclua:

* Passos para reprodução: Como disparar o erro.

* Comportamento Esperado: O que deveria ter acontecido.

* Comportamento Atual: O que aconteceu (inclua a stack trace completa, se aplicável).

✨ Enviar Pull Requests (PRs)

1. Crie um fork (bifurcação) do repositório.

2. Crie uma branch nova para a sua funcionalidade (`git checkout -b feature/nome-da-funcionalidade`).

3. Faça os seus commits (confirmações), seguindo a convenção: `feat: Adiciona validação de preço de compra` ou `fix: Corrige erro na exibição da tabela`.

4. Envie as suas alterações (git push origin feature/nome-da-funcionalidade).

5. Abra um Pull Request para a branch `main` deste repositório, descrevendo claramente o que foi alterado e porquê.

🗺️ Roadmap de Expansão (Próximas Etapas)

Aqui estão as funcionalidades planeadas para futuras versões do sistema:

Fase 1: Análise e Relatórios (Próximo)

* 1.1 Cálculos de Lucro: Implementar a função para calcular o lucro potencial total (Preço Venda - Preço Compra) para cada produto e o inventário total.

* 1.2 Relatórios de Baixo Estoque: Adicionar uma função para listar todos os produtos cuja quantidade está abaixo de um limite definido pelo utilizador (alerta de estoque mínimo).

* 1.3 Pesquisa Detalhada: Melhorar a pesquisa permitindo procurar por Número de Série, Fornecedor ou ID parcial.

Fase 2: Interface e Usabilidade

* 2.1 Interface Interativa: Transição da simples entrada de texto (`input()`) para uma interface CLI mais interativa usando bibliotecas como `inquirer` ou `prompt_toolkit`.

* 2.2 Exportação de Dados: Adicionar opções para exportar os dados do inventário para formatos como CSV ou TXT.

* 2.3 Registo de Transações: Implementar uma funcionalidade básica para registar entradas e saídas de estoque num ficheiro de registo separado.

Fase 3: Recursos Avançados (Longo Prazo)

* 3.1 Sistema de Usuários: Adicionar autenticação básica para diferentes níveis de acesso (ex: gestor, funcionário).

* 3.2 Integração com Base de Dados: Migração da persistência de JSON para um banco de dados leve (ex: SQLite) para lidar com um volume maior de dados e consultas mais complexas.

* 3.3 Preços Dinâmicos: Adicionar um campo para cálculo automático do Preço de Venda com base numa margem de lucro percentual.