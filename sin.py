import sys
import re
import lex
from collections import namedtuple


tabela = {
    #Producao inicial 
    "<prog>": {
        "BEGIN": ["BEGIN", "ENDL", "<stmts>", "END", "ENDL"]
    },
    #statments
    "<stmts>": {
        "TYPE_INT": ["<stmt>", "<stmts>"],
        "TYPE_FLOAT": ["<stmt>", "<stmts>"],
        "TYPE_BOOL": ["<stmt>", "<stmts>"],
        "TYPE_STRING": ["<stmt>", "<stmts>"],
        "ID": ["<stmt>", "<stmts>"],
        "IF": ["<stmt>", "<stmts>"],
        "WHILE": ["<stmt>", "<stmts>"],
        "FOR": ["<stmt>", "<stmts>"],
        "IN": ["<stmt>", "<stmts>"],
        "OUT": ["<stmt>", "<stmts>"],
        "CHAE": ["<stmt>", "<stmts>"],
        "END": ["ε"],
        "CHAD": ["ε"]
    },
    #statment
    "<stmt>": {
        "TYPE_INT": ["<vardecl>"],
        "TYPE_FLOAT": ["<vardecl>"],
        "TYPE_BOOL": ["<vardecl>"],
        "TYPE_STRING": ["<vardecl>"],
        "ID": ["<assign>"],
        "IF": ["<ifstmt>"],
        "WHILE": ["<whilestmt>"],
        "FOR": ["<forstmt>"],
        "IN": ["<instmt>"],
        "OUT": ["<outstmt>"],
        "CHAE": ["<block>"],
        "ENDL": ["ENDL"]
    },
    #declaracao de var
    "<vardecl>": {
        "TYPE_INT": ["<type>", "ID", "ATR", "<expr>", "ENDL"],
        "TYPE_FLOAT": ["<type>", "ID", "ATR", "<expr>", "ENDL"],
        "TYPE_BOOL": ["<type>", "ID", "ATR", "<expr>", "ENDL"],
        "TYPE_STRING": ["<type>", "ID", "ATR", "<expr>", "ENDL"]
    },
    #atribuicao
    "<assign>": {
        "ID": ["ID", "ATR", "<expr>", "ENDL"]
    },
    #if
    "<ifstmt>": {
        "IF": ["IF", "PARE", "<expr>", "PARD", "<block>", "<ifelse>"]
    },
    #else
    "<ifelse>": {
        "ELSE": ["ELSE", "<block>"],
        "TYPE_INT": ["ε"],
        "TYPE_FLOAT": ["ε"], 
        "TYPE_BOOL": ["ε"], 
        "TYPE_STRING": ["ε"],
        "ID": ["ε"], 
        "IF": ["ε"], 
        "WHILE": ["ε"], 
        "FOR": ["ε"], 
        "IN": ["ε"], 
        "OUT": ["ε"],
        "CHAE": ["ε"], 
        "END": ["ε"], 
        "CHAD": ["ε"], 
        "EOF": ["ε"], 
        "ENDL": ["ε"]
    },

    #bloco (por decisão de proejeto vai ser obrigatorio o ENDL)
    "<block>": {
    "CHAE": ["CHAE", "<stmts>", "CHAD", "<opt_endl>"]
    },
        "<opt_endl>": {
        "ENDL": ["ENDL"],
        #"ELSE": ["ε"], 
        #"END": ["ε"], 
        #"EOF": ["ε"], 
        #"CHAD": ["ε"],
        #"TYPE_INT": ["ε"], 
        #"TYPE_FLOAT": ["ε"], 
        #"TYPE_BOOL": ["ε"], 
        #"TYPE_STRING": ["ε"],
        #"ID": ["ε"], 
        #"IF": ["ε"], 
        #"WHILE": ["ε"], 
        #"FOR": ["ε"], 
        #"IN": ["ε"], 
        #"OUT": ["ε"]
    },


    # While
    "<whilestmt>": {
        "WHILE": ["WHILE", "PARE", "<expr>", "PARD", "<block>"]
    },

    # For
    "<forstmt>": {
        "FOR": ["FOR", "PARE", "<forinit>", "ENDL", "<forcond>", "ENDL", "<forincr>", "PARD", "<block>"]
    },
    #forinit (inicialicacao (int i:0))
    "<forinit>": {
        "TYPE_INT": ["<type>", "ID", "ATR", "<expr>"],
        "ID": ["ID", "ATR", "<expr>"]
    },
    #forcond (condicao (i<10))
    "<forcond>": {
        "PARE": ["<expr>"],
        "ID": ["<expr>"],
        "INT": ["<expr>"], 
    },
    #forincr (incremento (i++))

    "<forincr>": {
        "ID": ["ID", "ATR", "<expr>"]
    },

    # In
    "<instmt>": {
        "IN": ["IN", "PARE", "ID", "PARD", "ENDL"]
    },

    # Out
    "<outstmt>": {
        "OUT": ["OUT", "PARE", "<expr>", "PARD", "ENDL"]
    },

    # Tipos aceitos
    "<type>": {
        "TYPE_INT": ["TYPE_INT"],
        "TYPE_FLOAT": ["TYPE_FLOAT"],
        "TYPE_BOOL": ["TYPE_BOOL"],
        "TYPE_STRING": ["TYPE_STRING"]
    },

    # Expressoes
    "<expr>": {
        "ID": ["<logical_or>"],
        "INT": ["<logical_or>"],
        "FLOAT": ["<logical_or>"],
        "STRING": ["<logical_or>"],
        "BOOL": ["<logical_or>"],
        "PARE": ["<logical_or>"],
        "SUB": ["<logical_or>"],
        "NOT": ["<logical_or>"],
        "TIL": ["<logical_or>"]
    },

    # ||
    "<logical_or>": {
        "ID": ["<logical_and>", "<logical_or_prime>"], 
        "INT": ["<logical_and>", "<logical_or_prime>"],
        "FLOAT": ["<logical_and>", "<logical_or_prime>"], 
        "STRING": ["<logical_and>", "<logical_or_prime>"],
        "BOOL": ["<logical_and>", "<logical_or_prime>"], 
        "PARE": ["<logical_and>", "<logical_or_prime>"],
        "SUB": ["<logical_and>", "<logical_or_prime>"], 
        "NOT": ["<logical_and>", "<logical_or_prime>"]
    },

    "<logical_or_prime>": {
        "OR": ["OR", "<logical_and>", "<logical_or_prime>"],
        "PARD": ["ε"], 
        "ENDL": ["ε"] 
    },

    # && 
    "<logical_and>": {
        "ID": ["<equality>", "<logical_and_prime>"], 
        "INT": ["<equality>", "<logical_and_prime>"],
        "FLOAT": ["<equality>", "<logical_and_prime>"], 
        "STRING": ["<equality>", "<logical_and_prime>"],
        "BOOL": ["<equality>", "<logical_and_prime>"], 
        "PARE": ["<equality>", "<logical_and_prime>"],
        "SUB": ["<equality>", "<logical_and_prime>"], 
        "NOT": ["<equality>", "<logical_and_prime>"]
    },
    "<logical_and_prime>": { # ALTERADO
        "AND": ["AND", "<equality>", "<logical_and_prime>"],
        "OR": ["ε"], "PARD": ["ε"], "ENDL": ["ε"]
    },

    # == || $ (comparacao (igual(=) ou diferente($))
    "<equality>": {
        "ID": ["<relational>", "<equality_prime>"], 
        "INT": ["<relational>", "<equality_prime>"],
        "FLOAT": ["<relational>", "<equality_prime>"], 
        "STRING": ["<relational>", "<equality_prime>"],
        "BOOL": ["<relational>", "<equality_prime>"], 
        "PARE": ["<relational>", "<equality_prime>"],
        "SUB": ["<relational>", "<equality_prime>"], 
        "NOT": ["<relational>", "<equality_prime>"]
    },

    "<equality_prime>": { 
        "EQ": ["EQ", "<relational>", "<equality_prime>"], 
        "NIG": ["NIG", "<relational>", "<equality_prime>"],
        "AND": ["ε"], 
        "OR": ["ε"], 
        "PARD": ["ε"], 
        "ENDL": ["ε"]
    },
    # < >
    "<relational>": {
        "ID": ["<additive>", "<relational_prime>"], 
        "INT": ["<additive>", "<relational_prime>"],
        "FLOAT": ["<additive>", "<relational_prime>"], 
        "STRING": ["<additive>", "<relational_prime>"],
        "BOOL": ["<additive>", "<relational_prime>"], 
        "PARE": ["<additive>", "<relational_prime>"],
        "SUB": ["<additive>", "<relational_prime>"], 
        "NOT": ["<additive>", "<relational_prime>"]
    },

    "<relational_prime>": { 
        "LES": ["LES", "<additive>", "<relational_prime>"],
        "MOR": ["MOR", "<additive>", "<relational_prime>"],
        "EQ": ["ε"], 
        "NIG": ["ε"], 
        "AND": ["ε"], 
        "OR": ["ε"], 
        "PARD": ["ε"], 
        "ENDL": ["ε"]
    },

    # + -
    "<additive>": {
        "ID": ["<term>", "<additive_prime>"], 
        "INT": ["<term>", "<additive_prime>"],
        "FLOAT": ["<term>", "<additive_prime>"], 
        "STRING": ["<term>", "<additive_prime>"],
        "BOOL": ["<term>", "<additive_prime>"], 
        "PARE": ["<term>", "<additive_prime>"],
        "SUB": ["<term>", "<additive_prime>"], 
        "NOT": ["<term>", "<additive_prime>"]
    },
    "<additive_prime>": { 
        "ADD": ["ADD", "<term>", "<additive_prime>"],
        "SUB": ["SUB", "<term>", "<additive_prime>"],
        "LES": ["ε"], 
        "MOR": ["ε"], 
        "EQ": ["ε"], 
        "NIG": ["ε"], 
        "AND": ["ε"], 
        "OR": ["ε"], 
        "PARD": ["ε"], 
        "ENDL": ["ε"]
    },

    # * / %
    "<term>": {
        "ID": ["<factor>", "<term_prime>"], 
        "INT": ["<factor>", "<term_prime>"],
        "FLOAT": ["<factor>", "<term_prime>"], 
        "STRING": ["<factor>", "<term_prime>"],
        "BOOL": ["<factor>", "<term_prime>"], 
        "PARE": ["<factor>", "<term_prime>"],
        "SUB": ["<factor>", "<term_prime>"], 
        "NOT": ["<factor>", "<term_prime>"]
    },

    "<term_prime>": { 
        "MUL": ["MUL", "<factor>", "<term_prime>"],
        "DIV": ["DIV", "<factor>", "<term_prime>"],
        "MOD": ["MOD", "<factor>", "<term_prime>"],
        "ADD": ["ε"], 
        "SUB": ["ε"], 
        "LES": ["ε"], 
        "MOR": ["ε"], 
        "EQ": ["ε"], 
        "NIG": ["ε"], 
        "AND": ["ε"], 
        "OR": ["ε"], 
        "PARD": ["ε"], 
        "ENDL": ["ε"]
    },
    
    # Fatores
    "<factor>": {
        "ID": ["ID"],
        "INT": ["INT"],
        "FLOAT": ["FLOAT"],
        "STRING": ["STRING"],
        "BOOL": ["BOOL"],
        "PARE": ["PARE", "<expr>", "PARD"],
        "SUB": ["SUB", "<factor>"],
        "NOT": ["NOT", "<factor>"],
        "TIL": ["TIL", "<factor>"]
    }
}

Token = namedtuple('Token', ['tipo', 'valor', 'linha'])



def ler_tokens_arquivo(nome_arquivo):
    regex_token = re.compile(r"([A-Z_]+):\s+'(.*?)'\s+\(linha\s+(\d+)\)") #pega o tipo, valor e linha
    tokens = []
    
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            for num_linha, linha_texto in enumerate(f, 1):
                linha_texto = linha_texto.strip()
                if not linha_texto or linha_texto.startswith("ERRO"):
                    continue

                match = regex_token.match(linha_texto)
                if match:
                    tipo, valor, linha_num_str = match.groups()
                    token = Token(tipo, valor, int(linha_num_str))
                    tokens.append(token)
                else:
                    print(f"AAAAAAAAAAAAA linha {num_linha} em formato inesperado: '{linha_texto}'") #para debbug pode deixar como comentario
    
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        sys.exit(1)

    ultima_linha = tokens[-1].linha if tokens else 1
    tokens.append(Token('EOF', 'EOF', ultima_linha))
    return tokens

def analisar(tokens):
    
    CONJUNTO_SINCRONIZACAO = {"ENDL", "CHAD", "END", "IF", "WHILE", "FOR", "EOF"}

    pilha = ["<prog>"]
    i = 0
    erros = []
    sucesso = True

    while pilha:
        topo = pilha[-1]
        token_atual = tokens[i]
        entrada = token_atual.tipo

        if topo == entrada:
            pilha.pop()
            #print(f"[Linha {token_atual.linha}] Consome '{token_atual.valor}' (tipo: {entrada})") #debug da pilha
            i += 1
        
        elif topo in tabela:
            if entrada in tabela[topo]:
                producao = tabela[topo][entrada]
              #  print(f"Expandindo {topo} -> {producao}") #debug da pilha
                pilha.pop()
                if producao != ["ε"]:
                    pilha.extend(reversed(producao))
            else:
                sucesso = False
                erro_msg = (
                    f"[Linha {token_atual.linha}] ERRO: Inesperado '{token_atual.valor}' (tipo: {entrada}). "
                    f"Não há regra para expandir {topo}."
                )
                erros.append(erro_msg)
                
                print(f"🔥🔥 🔥 🔥 🔥 Ativando modo pânico: procurando por {CONJUNTO_SINCRONIZACAO}") #pode emoji? no mac tá funcionando kkkkk
                while i < len(tokens) -1 and tokens[i].tipo not in CONJUNTO_SINCRONIZACAO:
                    i += 1
                
                if topo in pilha:
                    pilha.pop()
                
                if i >= len(tokens) - 1:
                    break

        else:
            sucesso = False
            erro_msg = (
                f"[Linha {token_atual.linha}] ERRO: Inesperado '{token_atual.valor}' (tipo: {entrada}). "
                f"Esperava '{topo}'."
            )
            erros.append(erro_msg)
            pilha.pop()

    if i < len(tokens) -1:
        sucesso = False
        while i < len(tokens) -1:
            erros.append(f"[Linha {tokens[i].linha}] ERRO: Tokens extras no final do arquivo, começando com '{tokens[i].valor}'.")
            i += 1
            
    if not erros and sucesso:
        print("\n✅ ANÁLISE SINTÁTICA CONCLUÍDA SEM ERROS") #emoji ok?
    else:
        print("\n❌ ANÁLISE SINTÁTICA CONCLUÍDA COM ERROS:") #emoji ok?
        for e in erros:
            print(f"   - {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 sin.py [nome_arquivo].cruim") # forma de usar o arquivo
    else:
        nome_arquivo = sys.argv[1]
        #print(type(nome_arquivo)) #debug tava dando errado antes(DEIXAR COMENTADO)
        #lista_de_tokens = ler_tokens_arquivo(nome_arquivo) #caso queira usar o  arquivo de tokens 
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                codigo = f.read()
        except FileNotFoundError:
            print(f"Erro: o arquivo '{nome_arquivo}' não foi encontrado.")
            sys.exit(1)

        ttlista_de_tokens = lex.analisar(codigo, nome_arquivo)
        lista_de_tokens = ler_tokens_arquivo(f"tokens{nome_arquivo}.txt")


        if lista_de_tokens:
            print("*"*50)
            print("--- INICIANDO ANÁLISE SINTÁTICA ---\n")
            analisar(lista_de_tokens)
            print("\n\n--- FIM DA ANÁLISE ---")
            print("*"*50)