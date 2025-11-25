import json
import os
import uuid
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box 

# Inicializa a consola do Rich
console = Console()

# Constante para o nome do arquivo JSON
ARQUIVO_JSON = 'inventario.json'

# --- Configurações de Tabela para Rich ---
# Definir as colunas para o Rich Table (Total de 10 Colunas)
COLUNAS_TABELA = [
    ("ID (Parcial)", 8, 'dim'), 
    ("Produto", 18, 'bold yellow'), # <--- COR ALTERADA PARA MAIOR VISIBILIDADE
    ("Descrição", 20, 'italic white'), 
    ("Quantidade", 8, 'green'), 
    ("Preço Compra", 8, 'dim red'), 
    ("Preço Venda", 8, 'cyan'), 
    ("Fornecedor", 10, 'magenta'), 
    ("Nº Série", 12, 'bold white'), 
    ("Data Aquisição", 10, 'blue'), 
    ("Localização", 8, 'dim') 
]

class Produto:
    """Representa um item de produto no inventário, agora com um ID único."""

    def __init__(self, nome, descricao, quantidade, preco_compra, preco_venda, 
                 fornecedor, data_aquisicao, numero_serie, localizacao_estoque, id=None):
        
        self.id = id if id else str(uuid.uuid4())
        self.nome = nome
        self.descricao = descricao
        # Garante que a quantidade é sempre int, mesmo que venha do JSON
        self.quantidade = int(quantidade) 
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.fornecedor = fornecedor
        self.data_aquisicao = data_aquisicao
        self.numero_serie = numero_serie
        self.localizacao_estoque = localizacao_estoque

    def to_dict(self):
        """Converte o objeto Produto para um dicionário para ser salvo em JSON."""
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "quantidade": self.quantidade,
            "preco_compra": self.preco_compra,
            "preco_venda": self.preco_venda,
            "fornecedor": self.fornecedor,
            "data_aquisicao": self.data_aquisicao.isoformat() if isinstance(self.data_aquisicao, datetime) else str(self.data_aquisicao),
            "numero_serie": self.numero_serie,
            "localizacao_estoque": self.localizacao_estoque
        }

    @staticmethod
    def from_dict(data):
        """Cria um objeto Produto a partir de um dicionário (carregado do JSON)."""
        data_aquisicao_obj = data.get("data_aquisicao")
        if data_aquisicao_obj and isinstance(data_aquisicao_obj, str):
            try:
                data_aquisicao_obj = datetime.fromisoformat(data_aquisicao_obj)
            except ValueError:
                pass 

        return Produto(
            id=data.get("id"),
            nome=data.get("nome"),
            descricao=data.get("descricao", "N/A"), # Default N/A
            quantidade=data.get("quantidade", 0), # Default 0
            preco_compra=data.get("preco_compra", 0.0), # Default 0.0
            preco_venda=data.get("preco_venda", 0.0), # Default 0.0
            fornecedor=data.get("fornecedor", "N/A"), # Default N/A
            data_aquisicao=data_aquisicao_obj,
            numero_serie=data.get("numero_serie", "N/A"), # Default N/A
            localizacao_estoque=data.get("localizacao_estoque")
        )

# --- Funções de persistência ---

def carregar_dados():
    """Lê o arquivo JSON e retorna uma lista de objetos Produto."""
    if not os.path.exists(ARQUIVO_JSON) or os.path.getsize(ARQUIVO_JSON) == 0:
        return []

    try:
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
            dados_dicts = json.load(f)
            return [Produto.from_dict(d) for d in dados_dicts]
    except json.JSONDecodeError:
        console.print("\n[bold red]Erro:[/bold red] ao decodificar JSON. O arquivo pode estar corrompido.", style="blink")
        return []
    except Exception as e:
        console.print(f"\n[bold red]Erro inesperado ao carregar dados:[/bold red] {e}")
        return []

def salvar_dados(produtos):
    """Salva uma lista de objetos Produto no arquivo JSON."""
    try:
        dados_dicts = [p.to_dict() for p in produtos]
        
        with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
            json.dump(dados_dicts, f, indent=4)
            console.print(f"\n[bold green]Sucesso:[/bold green] Arquivo '[cyan]{ARQUIVO_JSON}[/cyan]' atualizado.")
    except Exception as e:
        console.print(f"\n[bold red]Erro ao salvar o arquivo:[/bold red] {e}")

# --- Funções Auxiliares de Input e Output ---

def obter_numero_positivo(prompt, tipo=int):
    """Auxiliar para garantir que o input é um número positivo."""
    while True:
        try:
            valor = tipo(input(prompt))
            if valor >= 0:
                return valor
            else:
                console.print(f'[bold red]Atenção:[/bold red] O valor não pode ser um número negativo. Tente novamente.')
        except ValueError:
            console.print('[bold red]Atenção:[/bold red] Entrada inválida. Por favor, digite um número.')

def exibir_inventario_atual():
    """Exibe o inventário formatado usando Rich Table (10 colunas)."""
    produtos = carregar_dados() 

    if not produtos:
        console.print("\n[bold yellow]O inventário está vazio.[/bold yellow]")
        return

    table = Table(title="Inventário Atual de Produtos (Visão Detalhada)", show_header=True, header_style="bold magenta")
    table.row_styles = ["none", "dim"]
    table.box = box.ROUNDED 
    
    # Adicionar colunas
    for header, width, style in COLUNAS_TABELA:
        table.add_column(header, style=style, min_width=width, justify="left")

    # Adicionar linhas
    for produto in produtos:
        data_aquisicao_str = ""
        if produto.data_aquisicao and isinstance(produto.data_aquisicao, datetime):
            data_aquisicao_str = produto.data_aquisicao.strftime('%d-%m-%Y')
        else:
            data_aquisicao_str = str(produto.data_aquisicao)
            
        id_parcial = produto.id[:8] if produto.id else "N/A"
        
        table.add_row(
            id_parcial,
            produto.nome,
            produto.descricao, 
            str(produto.quantidade),
            f"R$ {produto.preco_compra:.2f}", 
            f"R$ {produto.preco_venda:.2f}",
            produto.fornecedor,
            produto.numero_serie,
            data_aquisicao_str,
            produto.localizacao_estoque
        )

    console.print(table)

# --- Funções de Inventário ---

def adicionar_produtos_ao_estoque():
    """Solicita inputs e cria um novo objeto Produto no inventário."""
    produtos = carregar_dados()

    console.print('\n[bold cyan]>>> Adicionando Produtos ao Estoque...[/bold cyan]')
    
    # Validação do Nome
    nome = input('Nome do Produto: ').strip()
    if not nome:
        console.print('[bold red]Erro:[/bold red] O nome do produto não pode ser vazio.')
        return

    descricao = input('Descrição: ').strip()
    quantidade = obter_numero_positivo('Quantidade: ')
    preco_compra = obter_numero_positivo('Preço de Compra: ', tipo=float)
    preco_venda = obter_numero_positivo('Preço de Venda: ', tipo=float)
    
    # Validação do Fornecedor
    while True:
        fornecedor = input('Fornecedor: ').strip()
        if fornecedor:
            break
        console.print('[bold red]Erro:[/bold red] O fornecedor é obrigatório.')

    data_obj = None
    while data_obj is None:
        data_de_aquisicao_str = input('Data de Aquisição (DD-MM-YYYY): ').strip()
        try:
            data_obj = datetime.strptime(data_de_aquisicao_str, '%d-%m-%Y')
        except ValueError:
            console.print("[bold red]Erro:[/bold red] no formato da data. Use o formato DD-MM-YYYY (Ex: 31-12-2023).")

    numero_serie = input('Número de Série: ').strip()
    localizacao_no_estoque = input('Localização no Estoque: ').strip()

    novo_produto = Produto(
        nome, descricao, quantidade, preco_compra, preco_venda, 
        fornecedor, data_obj, numero_serie, localizacao_no_estoque
    )
    
    produtos.append(novo_produto)
    salvar_dados(produtos)
    console.print(f'\n[bold green]Produto Adicionado:[/bold green] "{nome}" com ID: [dim]{novo_produto.id[:8]}[/dim]')


def atualizar_quantidade_disponivel(nome_produto, quantidade_atualizada):
    """Atualiza a quantidade de um produto específico. Se houver múltiplos nomes, atualiza o primeiro encontrado."""
    produtos = carregar_dados()
    produtos_encontrados = [p for p in produtos if p.nome.lower() == nome_produto.lower()]

    if not produtos_encontrados:
        console.print(f'\n[bold red]Erro:[/bold red] Produto "[yellow]{nome_produto}[/yellow]" não encontrado no inventário.')
        return

    if len(produtos_encontrados) > 1:
        console.print(f"\n[bold yellow]ATENÇÃO:[/bold yellow] Encontrados [cyan]{len(produtos_encontrados)}[/cyan] itens com o nome '{nome_produto}'.")
        for i, p in enumerate(produtos_encontrados):
            console.print(f"  [bold dim][{i+1}][/bold dim] ID: [dim]{p.id[:8]}[/dim] | Qtd: [green]{p.quantidade}[/green] | Fornecedor: {p.fornecedor}")
        
        produto_a_atualizar = produtos_encontrados[0]
        console.print(f"[bold dim]Atualizando apenas o primeiro item encontrado (ID: {produto_a_atualizar.id[:8]}).[/bold dim]")
    else:
        produto_a_atualizar = produtos_encontrados[0]

    console.print(f"\nProduto: [bold]{produto_a_atualizar.nome}[/bold] | Quantidade atual: [green]{produto_a_atualizar.quantidade}[/green]")
            
    if quantidade_atualizada >= 0:
        produto_a_atualizar.quantidade += quantidade_atualizada
        console.print(f"[bold green]Adicionadas[/bold green] {quantidade_atualizada} unidades. Nova quantidade: [green]{produto_a_atualizar.quantidade}[/green]")
    else:
        remocao = abs(quantidade_atualizada)
        if remocao <= produto_a_atualizar.quantidade:
            produto_a_atualizar.quantidade -= remocao
            console.print(f"[bold red]Removidas[/bold red] {remocao} unidades. Nova quantidade: [green]{produto_a_atualizar.quantidade}[/green]")
        else:
            console.print(f"[bold red]ATENÇÃO:[/bold red] Quantidade insuficiente (Tentar remover {remocao} de {produto_a_atualizar.quantidade}). Operação cancelada.")
    
    salvar_dados(produtos)


def excluir_produto_do_estoque(nome):
    """Remove um produto do inventário pelo nome (e solicita ID se houver duplicados)."""
    produtos = carregar_dados()
    produtos_encontrados = [p for p in produtos if p.nome.lower() == nome.lower()]
    
    if not produtos_encontrados:
        console.print(f"\n[bold red]Erro:[/bold red] Produto '[yellow]{nome}[/yellow]' não encontrado para exclusão.")
        return

    produto_a_remover = None

    if len(produtos_encontrados) > 1:
        console.print(f"\n[bold yellow]ATENÇÃO:[/bold yellow] Foram encontrados [cyan]{len(produtos_encontrados)}[/cyan] produtos com o nome '{nome}'.")
        for i, p in enumerate(produtos_encontrados):
            console.print(f"  [bold dim][{i+1}][/bold dim] ID: [dim]{p.id[:8]}[/dim] | Qtd: [green]{p.quantidade}[/green] | Fornecedor: {p.fornecedor}")
        
        id_parcial = input("Digite os 8 primeiros caracteres do ID do item que deseja EXCLUIR: ").strip()
        
        for p in produtos_encontrados:
            if p.id.startswith(id_parcial):
                produto_a_remover = p
                break
        
        if not produto_a_remover:
            console.print("[bold red]Erro:[/bold red] ID parcial não corresponde a nenhum item. Exclusão cancelada.")
            return
    else:
        produto_a_remover = produtos_encontrados[0]

    produtos_atualizados = [p for p in produtos if p.id != produto_a_remover.id]
    
    salvar_dados(produtos_atualizados)
    console.print(f"\n[bold green]Excluído:[/bold green] Produto '[yellow]{produto_a_remover.nome}[/yellow]' (ID: [dim]{produto_a_remover.id[:8]}[/dim]) removido com sucesso.")
        
def main():
    """Função principal que executa o loop do menu da aplicação."""
    
    # Cabeçalho estilizado com Rich
    console.print(Panel(
        Text("Gerenciamento de Estoque - CLI Power-up!", justify="center", style="bold white on #40B2D4"),
        title=Text("V1 | Legibilidade de Cores Ajustada e 10 Colunas", style="bold yellow"),
        border_style="cyan"
    ))
    
    # Aviso de dependência
    console.print("\n[bold yellow]Lembrete:[/bold yellow] Este programa requer a biblioteca [bold magenta]rich[/bold magenta] (Instalar com 'pip install rich').")
    
    while True:
        
        # Menu estilizado com Rich Panel
        menu_text = Text()
        menu_text.append("1. ", style="bold green")
        menu_text.append("Adicionar Produtos ao Estoque\n")
        menu_text.append("2. ", style="bold green")
        menu_text.append("Atualizar Quantidades Disponíveis\n")
        menu_text.append("3. ", style="bold green")
        menu_text.append("Exibir o Inventário Atual (Completo)\n")
        menu_text.append("4. ", style="bold green")
        menu_text.append("Eliminar um produto do estoque\n")
        menu_text.append("\n5. ", style="bold red")
        menu_text.append("Salvar e Sair\n")

        console.print(Panel(
            menu_text,
            title="[bold blue]Opções de Inventário[/bold blue]",
            border_style="blue",
            width=50
        ))

        saida = input('Sua opção: ').strip()
        
        match saida:
            case '1':
                adicionar_produtos_ao_estoque()
                
            case '2':
                console.print('\n[bold cyan]>>> Atualizando as quantidades disponíveis...[/bold cyan]')
                nome = input('Digite o nome do produto para atualizar a quantidade: ').strip()
                try:
                    quantidade = int(input("Digite a quantidade a ser adicionada (+) ou removida (-): "))
                    atualizar_quantidade_disponivel(nome_produto=nome, quantidade_atualizada=quantidade)
                except ValueError:
                    console.print('\n[bold red]Erro:[/bold red] A quantidade deve ser um número inteiro.')

            case '3':
                console.print('\n[bold cyan]>>> Inventário Atual da Loja de Informática:[/bold cyan]')
                exibir_inventario_atual()
                
            case '4':
                console.print('\n[bold cyan]>>> Eliminando produto do estoque...[/bold cyan]')
                nome = input("Digite o nome do produto a eliminar: ").strip()
                excluir_produto_do_estoque(nome=nome)
                
            case '5':
                console.print('\n[bold red]Encerrando o programa...[/bold red]')
                console.print('[bold white on red]Programa Encerrado.[/bold white on red]')
                break
                
            case _:
                console.print('\n[bold red]Opção inválida.[/bold red] Tente novamente.')


# Ponto de entrada do programa
if __name__ == '__main__':
    main()