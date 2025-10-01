import re

tokens = [
    ("TYPE_INT", r"\bint\b"),
    ("TYPE_FLOAT", r"\bfloat\b"),
    ("TYPE_BOOL", r"\bbool\b"),
    ("TYPE_STRING", r"\bstring\b"),
    ("IF", r"\bif\b"),
    ("ELSE", r"\belse\b"),
    ("FOR", r"\bfor\b"),
    ("WHILE", r"\bwhile\b"),
    ("IN", r"\bin\b"),
    ("OUT", r"\bout\b"),
    ("BEGIN", r"\bbegin\b"),
    ("END", r"\bend\b"),
    ("FLOAT", r"~?\d+\.\d+"),
    ("INT", r"~?\d+"),
    ("BOOL", r"\btrue\b|\bfalse\b"),
    ("ADD", r"\+"),
    ("SUB", r"-"),
    ("MUL", r"\*"),
    ("DIV", r"/"),
    ("MOD", r"%"),
    ("OR", r"\|"),
    ("AND", r"&"),
    ("NOT", r"!"),
    ("EQ", r"="),
    ("NIG", r"\$"),
    ("LES", r"<"),
    ("MOR", r">"),
    ("ATR", r":"),
    ("ENDL", r";"),
    ("PARE", r"\("),
    ("PARD", r"\)"),
    ("CHAE", r"\{"),
    ("CHAD", r"\}"),
    ("STRING", r'"[^"]*"'),
    ("ID", r"\b[a-zA-Z][a-zA-Z0-9]*\b"),
    ("IGNORAR", r"[ \t\n]+"),
]



token_regex = '|'.join(f"(?P<{name}>{pattern})" for name, pattern in tokens)

def analisar(codigo, nome_arquivo):
    linha = 1
    pos = 0
    tokens_reconhecidos = []
    tokens_sin=[]

    for match in re.finditer(token_regex, codigo):
        tipo = match.lastgroup
        valor = match.group()
        inicio = match.start()

        if pos < inicio:
            trecho_invalido = codigo[pos:inicio].strip()
            if trecho_invalido:
                print(f"\n Erro léxico na linha {linha}: símbolo inválido -> '{trecho_invalido}'")
                tokens_reconhecidos.append(f"ERRO: símbolo inválido na linha {linha}: '{trecho_invalido}'")

        if tipo == "IGNORAR":
            linha += valor.count("\n")
        else:
            resultado = f"{tipo}: '{valor}' (linha {linha})"
           # print(resultado) #caso queira mostrar o token no terminal na execucao descomentar aquiiiiiiiiiiiiiii
            tokens_reconhecidos.append(resultado)
            tokens_sin.append((tipo, valor, linha))

        pos = match.end()

    if pos < len(codigo):
        trecho_restante = codigo[pos:].strip()
        if trecho_restante:
            print(f"\n Erro léxico no final do arquivo: símbolo inválido -> '{trecho_restante}'")
            tokens_reconhecidos.append(f"ERRO: símbolo inválido no final: '{trecho_restante}'")

    with open(f"tokens{nome_arquivo}.txt", "w", encoding="utf-8") as f:
        for t in tokens_reconhecidos:
            f.write(t + "\n")

    #print("\n anal. lex. concluída. Tokens salvos em 'tokens{nome_arquivo}.txt'.")

    return tokens_sin

if __name__ == "__main__":
    nome_arquivo = input("Digite o nome do arquivo de cod C Ruim (ex: codigo.txt): ")

    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            codigo = f.read()
        analisar(codigo, nome_arquivo)
    except FileNotFoundError:
        print(f"Erro: o arquivo '{nome_arquivo}' não foi encontrado.")

