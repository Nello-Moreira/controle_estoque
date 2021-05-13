import loja_funcoes_auxiliares as aux
import loja_adm as adm
import loja_cliente as cli


def main_loja():
    """
    Esta funcao serve para direcionar o fluxo do programa.
    (acessar como adm ou cliente e chamar as funcoes de acordo com o usuario)
    """
    comandos_acesso = ['1 - Acessar como administrador',
                       '2 - Acessar como cliente',
                       '0 - Sair']
    comandos_adm = ['1 - Ver estoque',
                    '2 - Cadastrar novo produto',
                    '3 - Remover um produto da lista',
                    '4 - Alterar preco de um produto',
                    '5 - Atualizar estoque de um produto',
                    '6 - Adicionar novo administrador',
                    '7 - Remover administrador',
                    '0 - Sair']
    comandos_cliente = ['1 - Ver carrinho',
                        '2 - Adicionar um produto ao carrinho',
                        '3 - Remover um produto do carrinho',
                        '4 - Alterar quantidade de um produto',
                        '5 - Fechar a compra',
                        '0 - Sair']
    arquivo_cadastros_adms = 'loja_login_adm.txt'
    arquivo_estoque = 'loja_estoque.txt'

    # Saudacao
    print('Seja bem-vindo!')

    while True:
        # Imprime os comandos para logar como adm ou acessar como cliente
        aux.imprimir_comandos(comandos_acesso)

        # Pede que o usuario escolha uma opcao ate ser dado um comando valido
        comando = aux.checa_comando(comandos_acesso)

        # Acessa como adm, cliente ou sai (else)
        if comando == 1:
            adm_acesso(comandos_adm, arquivo_cadastros_adms, arquivo_estoque)
        elif comando == 2:
            cliente_acesso(comandos_cliente, arquivo_estoque)
        elif comando == 0:
            break

        # Print para separar os comandos
        aux.separar_comandos_print()


def adm_acesso(lista_comandos, arquivo_adms, arquivo_estoque):
    """
    Funcao com o fluxo de um adm

    :param lista_comandos: lista com os comandos possiveis para os adms
    :param arquivo_adms: string com o nome do arquivo ".txt" com os cadastros do usuario.
                         O arquivo deve conter um dicionario com chave = nome do usuario
                         e valor = senha criptografada
    :param arquivo_estoque: string com o nome do arquivo ".txt" com os cadastros do usuario.
                            O arquivo deve conter uma lista de dicionarios com chaves = Produto, Preco, Em estoque
    :return:
    """
    # Print para separar os comandos
    aux.separar_comandos_print()

    # Primeira coisa a ser feita eh recuperar os adms cadastrados
    adms = adm.dados_registrados(arquivo_adms)

    # Se nao tiver nenhum cadastrado, pedir para cadastrar o primeiro
    if len(adms) == 0:
        print('Ainda nao ha administradores cadastrados. Eh necessario cadastrar o primeiro administrador.')
        # Cadastrando
        adms, usuario_cadastrado = adm.cadastrar_adm(arquivo_adms)
        logado, usuario_ativo = True, usuario_cadastrado
    else:
        logado, usuario_ativo = adm.login(adms)

    # Se nao logou, eh pra sair e voltar pro menu principal
    if not logado:
        # Retornando None pra sair da funcao
        return None

    # Se logou, entra no menu dos administradores
    while True:
        # Se o usuario remover todos os adms (possivel), deve sair da area de adm
        if len(adms) == 0:
            # Retornando None pra sair da funcao
            return None

        # Print para separar os comandos
        aux.separar_comandos_print()

        # Imprime os comandos para administradores
        print(f'Acessado como administrador ({usuario_ativo})')
        aux.imprimir_comandos(lista_comandos)

        # Pede que o usuario escolha uma opcao ate ser dado um comando valido
        comando = aux.checa_comando(lista_comandos)
        print()

        # Chama a funcao que o usuario pediu
        if comando == 1:  # Ver estoque
            estoque = adm.recupera_estoque(arquivo_estoque)
            aux.ver_estoque_ou_carrinho(estoque)
        elif comando == 2:  # Cadastrar novo produto
            adm.cadastrar_produto(arquivo_estoque)
        elif comando == 3:  # Remover um produto da lista
            adm.remover_produto(arquivo_estoque)
        elif comando == 4:  # Alterar preco de um produto
            adm.alterar_preco_ou_quantidade('loja_estoque.txt', 'preco')
        elif comando == 5:  # Atualizar estoque de um produto
            adm.alterar_preco_ou_quantidade('loja_estoque.txt', 'quantidade')
        elif comando == 6:  # Adicionar novo administrador
            adms, usuario_cadastrado = adm.cadastrar_adm(arquivo_adms)
        elif comando == 7:  # Remover administrador
            adms, usuario_removido = adm.remover_adm(arquivo_adms)

            # Se o adm se removeu do cadastro, deve voltar para a funcao principal e pedir novo login
            if usuario_ativo == usuario_removido:
                print()
                print('O usuario ativo foi removido do cadastro. Eh necessaria nova autenticacao.')
                break
        elif comando == 0:  # Sair
            break


def cliente_acesso(lista_comandos, arquivo_com_estoque):
    # Recuperando o estoque
    estoque = adm.recupera_estoque(arquivo_com_estoque)

    # Se o estoque estah vazio, retorna None para voltar ao menu principal
    # Eh necessario ter itens no estoque para que o cliente possa comprar
    if aux.checa_vazio(estoque):
        print('O estoque estah vazio. Eh necessario adicionar itens ao estoque primeiro.')
        return None

    # Criando o carrinho
    carrinho = []

    # Loop de rotina de cliente
    while True:
        # Print para separar os comandos
        aux.separar_comandos_print()

        # Imprime os comandos para administradores
        print(f'Acessado como cliente.')
        aux.imprimir_comandos(lista_comandos)

        # Pede que o usuario escolha uma opcao ate ser dado um comando valido
        comando = aux.checa_comando(lista_comandos)
        print()

        # Chama a funcao que o usuario pediu
        if comando == 1:  # Ver carrinho
            aux.ver_estoque_ou_carrinho(carrinho, 'Carrinho')
        elif comando == 2:  # Adicionar um produto ao carrinho
            carrinho = cli.adicionar_produto_carrinho(estoque, carrinho)
        elif comando == 3:  # Remover um produto do carrinho
            carrinho = cli.remover_produto_carrinho(carrinho)
        elif comando == 4:  # Alterar quantidade de um produto
            if not aux.checa_vazio(carrinho):
                carrinho = cli.alterar_quantidade_carrinho(estoque, carrinho)
            else:
                print('O carrinho estah vazio')
        elif comando == 5:  # Fechar a compra
            cli.fechar_compra(carrinho, estoque, arquivo_com_estoque)
            break
        elif comando == 0:  # Sair
            break


if __name__ == '__main__':
    main_loja()
