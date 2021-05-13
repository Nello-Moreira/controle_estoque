import pandas as pd


def separar_comandos_print():
    """ Essa funcao serve para tornar o programa mais visual e separar as interacoes com o usuario"""
    print('\n' + ('*' * 70) + '\n')


def imprimir_comandos(lista_comandos):
    """ Essa funcao serve para imprimir a lista de comandos recebida, um comando por linha.
    Dessa forma, eh mais facil alterar os comandos."""
    for comando in lista_comandos:
        print(comando)


def checa_comando(lista_comandos):
    """
    Essa funcao recebe uma lista de comandos possiveis, pede que o usuario escolha uma opcao e
    confere se o valor passado esta na lista de comandos possiveis.
    Caso nao esteja, ele repete o pedido e a validacao ate que o valor seja valido
    """
    comando = False
    while not comando:
        try:
            comando = int(input('Digite a opcao desejada: '))
            print()

            # A opcao selecionada deve estar dentro da lista de comandos
            if comando < 0 or len(lista_comandos) - 1 < comando:
                raise ValueError
        # Se o comando digitado nao estiver na lista, emite uma mensagem de erro e repete o menu
        except ValueError:
            comando = False
            print(f'\nDigite uma opcao valida (inteiro de 0 a {len(lista_comandos) - 1}).')
            imprimir_comandos(lista_comandos)
        # Se o comando estiver na lista, retorna o numero do comando a ser executado
        else:
            return comando


def confirmacao():
    """
    Funcao para pedir a confirmacao para uma acao do usuario
    :return: Bool --> True para sim, False para nao
    """
    comandos_confirmacao = ['0 - Nao', '1 - Sim']

    imprimir_comandos(comandos_confirmacao)

    comando = checa_comando(comandos_confirmacao)

    if comando == 0:
        return False
    else:
        return True


def atualiza_arquivo(arquivo, conteudo):
    with open(arquivo, 'w') as arq:
        arq.write(str(conteudo))


def ver_estoque_ou_carrinho(lista, estoque_ou_carrinho='Estoque'):
    """
    Recebe uma lista de dicionarios e imprime um dataframe dela

    :param lista: lista de dicionarios (pode ser o estoque ou o carrinho)
    :param estoque_ou_carrinho: string com qual variavel estah sendo impressa
    :return: None
    """
    # Confere se a lista dada estah vazia
    if checa_vazio(lista):
        print(f'O {estoque_ou_carrinho} estah vazio.')
    else:
        # Cria um dataframe para imprimir o estoque/carrinho (se nao estiver vazio)
        indice = [i for i in range(1, len(lista) + 1)]
        lista_df = pd.DataFrame(lista, index=indice)
        print('-' * 30, f'{estoque_ou_carrinho}', '-' * 30)

        if estoque_ou_carrinho == 'Estoque':
            print(lista_df)
        else:
            lista_df = pd.DataFrame(lista_df, columns=['Produto', 'Preco', 'Carrinho', 'Total'])
            print(lista_df)

        if estoque_ou_carrinho != 'Estoque':
            carrinho_sum = lista_df.sum(axis=0, numeric_only=True)
            print(f'\nItens no carrinho: {int(carrinho_sum["Carrinho"])}')
            print(f'Total a pagar: {round(carrinho_sum["Total"], 2)}\n')


def checa_vazio(lista):
    """
    Funcao para verificar se o estoque ou o carrinho estao vazios
    :param lista: lista contendo o estoque ou o carrinho
    :return: bool -> True se o carrinho estiver vazio
    """
    if len(lista) == 0:
        return True
    else:
        return False


def valida_produto(numero_produto, estoque):
    """
    Funcao para verificar se o numero produto passado eh valido
    :param numero_produto: string dada como input pelo usuario contendo o numero do produto
    :param estoque: lista de estoque atualizado
    :return: produto_valido (bool), numero_produto (int)
    """
    try:
        numero_produto = float(numero_produto)

        if numero_produto < 0 or numero_produto > len(estoque):
            raise ValueError
        elif int(numero_produto) != float(numero_produto):
            raise ValueError
    except ValueError:
        print(f'Digite um numero valido (inteiro entre 0 e {len(estoque)}).')
        produto_valido = False
        numero_produto = -1
    else:
        produto_valido = True
        numero_produto = int(numero_produto)

    return produto_valido, numero_produto
