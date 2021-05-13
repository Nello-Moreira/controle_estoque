import loja_funcoes_auxiliares as aux
import bcrypt as bc


def dados_registrados(arquivo_dados):
    """
    Essa funcao checa se já tem o arquivo com os dados. Se não tem, cria.
    Se ja tem, tenta ler os dados (dicionario).
    Se o arquivo estiver vazio ou não for um dicionário, cria um dicionario vazio e SOBRESCREVE o arquivo.
    Essa funcao serve para qualquer arquivo ".txt" armazenando um dicionario

    :param arquivo_dados: string com o nome do arquivo ".txt" com os cadastros de dados.
                                  O arquivo deve conter uma lista de dicionarios

    :return: lista com os dados cadastrados
    """
    try:
        arq = open(arquivo_dados, 'r+')
        # Carrega o login de todos os administradores
        dados_cadastrados = eval(arq.readline())

        # Gera um erro se não for dicionario
        if type(dados_cadastrados) != dict:
            raise ValueError
    # Se não achar o arquivo, cria
    except FileNotFoundError:
        dados_cadastrados = {}
        aux.atualiza_arquivo(arquivo_dados, dados_cadastrados)
    # Se o arquivo estiver vazio, cria um dicionario vazio
    except SyntaxError:
        dados_cadastrados = {}
        arq.write(str(dados_cadastrados))
        arq.close()
    # Se o tipo não for um dicionario
    except ValueError:
        # Fecha o arquivo para evitar problemas
        arq.close()

        # Tenta transformar em dicionario
        try:
            # Tenta transformar em dict
            dados_cadastrados = dict(dados_cadastrados)
        # Se não conseguir transformar em dicionario, pede ao usuario a confirmacao do nome do arquivo
        except ValueError:
            print('O arquivo com o cadastro dos adms esta no formado errado.')
            arquivo_dados = input('Por favor, digite o nome do arquivo com os cadastros em forma de dicionario: ')
            # E realiza nova validacao
            dados_cadastrados = dados_registrados(arquivo_dados)
        else:
            # Se transformou em dict, sobrescreve o arquivo na forma correta
            aux.atualiza_arquivo(arquivo_dados, dados_cadastrados)

    return dados_cadastrados


def recupera_estoque(arquivo_dados):
    """
    Essa funcao checa se já tem o arquivo com os dados. Se não tem, cria.
    Se ja tem, tenta ler os dados (lista de dicionarios).
    Se o arquivo estiver vazio ou não for um dicionário, cria uma lista vazia e SOBRESCREVE o arquivo.
    Essa funcao serve para qualquer arquivo ".txt" armazenando
    uma lista de dicionarios (chaves: Produto, Preco, Em estoque)

    :param arquivo_dados: string com o nome do arquivo ".txt" com os cadastros de dados.
                                  O arquivo deve conter uma lista de dicionarios

    :return: lista com os dados cadastrados
    """
    try:
        arq = open(arquivo_dados, 'r+')
        # Carrega o login de todos os administradores
        estoque = eval(arq.readline())

        # Se os dados não estiverem em lista, tenta converter em lista.
        # Gera ValueError se não conseguir transformar
        if type(estoque) != list:
            estoque = list(estoque)

        # Se os itens da lista não forem dicionarios, tenta converter em dicionario.
        # Gera ValueError se não conseguir transformar
        for item in estoque:
            item = dict(item)

            # Se as chaves do dicionario nao estiverem corretas, impoe ValueError
            if list(item.keys()) != ['Produto', 'Preco', 'Em estoque']:
                raise ValueError
    # Se não achar o arquivo, cria com uma lista vazia
    except FileNotFoundError:
        estoque = []
        aux.atualiza_arquivo(arquivo_dados, estoque)
    # Se o arquivo estiver vazio, cria uma lista vazia
    except SyntaxError:
        estoque = []
        arq.write(str(estoque))
        arq.close()
    # Se o tipo não for uma lista ou os itens da lista
    # nao forem dicionarios com as chaves "Produto", "Preco", "Em estoque"
    except ValueError:
        # Fecha o arquivo para evitar problemas
        arq.close()

        print('O arquivo com o cadastro do estoque esta no formado errado.')
        print('O arquivo deve conter uma lista com dicionarios com chaves "Produto", "Preco", "Em estoque"')
        arquivo_dados = input('Por favor, digite o nome do arquivo com os cadastros em forma de dicionario: ')
        # E realiza nova validacao
        estoque = dados_registrados(arquivo_dados)
    else:
        # Coloca o estoque em ordem alfabetica de produto
        estoque.sort(key=lambda dic_prod: dic_prod['Produto'])

        # Salva o estoque organizado no arquivo
        aux.atualiza_arquivo(arquivo_dados, estoque)

    return estoque


def cadastrar_adm(arquivo_com_cadastros):
    """
    Funcao para cadastrar um administrador do sistema em um dicionario que sera salvo em um arquivo ".txt"

    :param arquivo_com_cadastros: arquivo ".txt" onde será salvo o dicionario dos adms cadastrados
    :return: dicionario de adms_cadastrados atualizado
    """
    # Buscando a lista de adms atualizada
    adms_cadastrados = dados_registrados(arquivo_com_cadastros)

    # Cadastrando o usuario
    usuario = False
    while not usuario:
        # Pede o usuario
        usuario = input('Digite o nome do usuario (0 (zero) para cancelar): ')
        usuario_cadastrado = False

        if usuario == '0':
            # Aqui nao alterou o cadastro
            print()
            print('Operacao cancelada')
            return adms_cadastrados, usuario_cadastrado
        # Se ja tem o usuario cadastrado, pede para cadastrar outro nome
        elif usuario in adms_cadastrados:
            print('Ja existe um cadastro com esse nome de usuario. Por favor, escolha outro.')
            usuario = False

    # Cadastrando a senha
    senha_igual = False
    while not senha_igual:
        senha = input('Digite a senha para cadastrar: ')
        senha_verificacao = input('Repita a senha para verificacao: ')

        # Se o usuario digitou a senha errada, repete o procedimento
        if senha == senha_verificacao:
            senha_igual = True
        else:
            print('Senhas informadas diferentes. Por favor, cadastre a senha de novo.')

    # Encriptografando a senha
    senha_encriptografada = bc.hashpw(senha.encode('utf-8'), bc.gensalt())

    # Salvando no dicionario
    adms_cadastrados[usuario] = senha_encriptografada

    # Salvando no arquivo (sobrescreve)
    aux.atualiza_arquivo(arquivo_com_cadastros, adms_cadastrados)

    # Retorna o usuario cadastrado
    usuario_cadastrado = usuario

    print()
    print('Usuario cadastrado com sucesso')
    return adms_cadastrados, usuario_cadastrado


def remover_adm(arquivo_com_cadastros):
    """
    Essa funcao vai remover um adm cadastrado e atualizar o arquivo de cadastro
    :return: dicionario de adms atualizado e o usuario removido
    """
    # Buscando a lista de adms atualizada
    adms_cadastrados = dados_registrados(arquivo_com_cadastros)

    # Listando os adms cadastrados
    ver_adms(adms_cadastrados)

    # Removendo um adm cadastrado
    usuario = False
    usuario_removido = False

    while not usuario:
        # Pede o usuario
        usuario = input('Digite o nome do usuario (0 (zero) para cancelar): ')

        if usuario == '0':
            print()
            print('Operacao cancelada')
            return adms_cadastrados, usuario_removido
        # Se nao acha o usuario dado, pede para tentar de novo
        elif usuario not in adms_cadastrados:
            print('Usuario nao identificado. Por favor, digite de novo.')
            print()
            usuario = False
        else:
            print(f'\nConfirma a remocao de {usuario} dos administradores cadastrados?')

            # Se o adm confirmar
            if aux.confirmacao():
                # remove o usuario
                adms_cadastrados.pop(usuario)
                usuario_removido = usuario

                # Salva no arquivo (SOBRESCREVE)
                with open(arquivo_com_cadastros, 'w') as arq:
                    arq.write(str(adms_cadastrados))

                # E retorna a lista atualizada
                print()
                print('Usuario removido com sucesso')
                return adms_cadastrados, usuario_removido
            else:
                print()
                print('Operacao cancelada')
                return adms_cadastrados, usuario_removido


def login(adms_cadastrados):
    """
    Confere se o usuario possui um login
    :return: bool e nome do usuario logado
    """
    # Aviso sobre login
    print('Eh necessario que seja feito o login')

    # Pede e confere o usuario
    usuario = False
    while not usuario:
        usuario = input('Digite o nome do usuario (0 (zero) para sair): ')

        if usuario == '0':
            return False, False
        elif usuario not in adms_cadastrados:
            usuario = False
            print('Usuario nao cadastrado.')
            ver_adms(adms_cadastrados)
            print()

    # Pede e confere a senha
    senha = False
    tentativas = 3
    while not senha:
        senha = input('Digite a senha do usuario ("sair" para sair): ')
        senha = senha.encode('utf-8')

        if senha == 'sair':
            return False, False
        # Se nao sair, confere a senha do usuario informado
        else:
            senha_salva = adms_cadastrados[usuario]

            # Se a senha for igual, retorna Logado = True
            if bc.hashpw(senha, senha_salva) == senha_salva:
                return True, usuario
            else:
                tentativas -= 1

                # Controle de tentativas
                if tentativas > 0:
                    print('A senha digitada estah incorreta. Por favor, tente de novo.')
                    print(f'Voce tem mais {tentativas} tentativa(s)')
                    senha = False, False
                # Caso nao consiga logar em 3 tentativas, volta ao menu principal
                else:
                    return False, False


def cadastrar_produto(arquivo_estoque):
    """
    Essa funcao cadastra novos produtos no estoque e salva o arquivo atualizado
    :param arquivo_estoque: string com o nome do arquivo ".txt" com os cadastros do usuario.
                            O arquivo deve conter uma lista de dicionarios com chaves = Produto, Preco, Em estoque
    :return: estoque atualizado
    """
    # Recupera o estoque mais atualizado
    estoque = recupera_estoque(arquivo_estoque)
    aux.ver_estoque_ou_carrinho(estoque)

    # Produtos ja cadastrados para evitar repeticao
    produtos_cadastrados = [dic_produto['Produto'].capitalize() for dic_produto in estoque]

    # Sequencia para cadastrar produtos
    repetir = True
    while repetir:
        produto = input('\nDigite o produto a ser adicionado (0 (zero) para cancelar): ')

        # Se usuario digitou para sair, volta ao menu
        if produto == "0":
            return estoque
        else:
            produto = produto.capitalize()

        # Se o produto ja esta cadastrado, nao cadastra de novo
        if produto in produtos_cadastrados:
            print('Esse produto ja esta cadastrado.')
            print(f'Os produtos cadastrados sao: {", ".join(produtos_cadastrados)}')
        else:
            # Se nao tem esse produto, pede preco e quantidade para adicionar
            while True:
                preco = input('Digite o preco, em reais, do produto: ')

                # Checa se o preco passado eh numero
                try:
                    preco = float(preco)

                    # O preco nao deve ser negativo (zero foi deixado intencionalmente)
                    if preco < 0:
                        raise ValueError
                except ValueError:
                    print('O preco informado deve ser um numero positivo.')
                # Se deu tudo certo, sai do loop do preco
                else:
                    break

            # Adicionando a quantidade
            while True:
                quantidade = input(f'Digite a quantidade de {produto} em estoque: ')

                # Checa se a quantidade passada eh numero inteiro
                try:
                    quantidade = float(quantidade)

                    # A quantidade nao deve ser negativa
                    if quantidade < 0:
                        raise ValueError
                    elif int(quantidade) != float(quantidade):
                        raise ValueError
                except ValueError:
                    print('A quantidade informada deve ser um numero inteiro igual ou maior que zero.')
                # Se deu tudo certo, sai do loop da quantidade
                else:
                    quantidade = int(quantidade)
                    break

            # Adicionando ao estoque
            dic_produto = {'Produto': produto, 'Preco': preco, 'Em estoque': quantidade}
            estoque.append(dic_produto)
            estoque.sort(key=lambda dic_produto: dic_produto['Produto'])

            # Salvando no arquivo
            aux.atualiza_arquivo(arquivo_estoque, estoque)

            # Pergunta se o usuario deseja repetir a operacao
            print('\nDeseja repetir a operacao?')
            repetir = aux.confirmacao()

    # Quando o usuario nao quiser mais adicionar produtos, deve retornar o estoque final
    return estoque


def remover_produto(arquivo_estoque):
    """
    Essa funcao remove produtos do estoque e salva o arquivo atualizado
    :param arquivo_estoque: string com o nome do arquivo ".txt" com os cadastros do usuario.
                            O arquivo deve conter uma lista de dicionarios com chaves = Produto, Preco, Em estoque
    :return: estoque atualizado
    """
    # Sequencia para cadastrar produtos
    while True:
        # Recupera o estoque mais atualizado
        print()
        estoque = recupera_estoque(arquivo_estoque)

        # Se o estoque esta vazio volta para o menu anterior
        if len(estoque) == 0:
            return estoque

        # Imprime o estoque na tela
        aux.ver_estoque_ou_carrinho(estoque)

        num_produto = input('\nDigite o numero do produto a ser removido: (0 (zero) para cancelar) ')

        produto_valido, num_produto = aux.valida_produto(num_produto, estoque)

        if produto_valido:
            # Zero para cancelar a remocao
            if num_produto == 0:
                return estoque
            else:
                print(f'\nConfirma a remocao de {estoque[num_produto - 1]["Produto"]} do estoque?')

                if aux.confirmacao():
                    # Removendo o produto. (Como o indice comeca em zero, tem que retirar um de "produto")
                    dic_produto = estoque.pop(num_produto - 1)
                    print(f'\nO produto ({dic_produto["Produto"]}) foi removido com sucesso.')

                    # Atualizando o arquivo de estoque
                    aux.atualiza_arquivo(arquivo_estoque, estoque)

                    # Pergunta se o usuario deseja repetir a operacao
                    print('\nDeseja repetir a operacao?')
                    if not aux.confirmacao():
                        break

    return estoque


def alterar_preco_ou_quantidade(arquivo_estoque, preco_ou_quantidade='quantidade'):
    """
    Essa funcao altera o preco ou a quantidade em estoque de um produto e salva o arquivo atualizado
    :param arquivo_estoque: string com o nome do arquivo ".txt" com os cadastros do usuario.
                            O arquivo deve conter uma lista de dicionarios com chaves = Produto, Preco, Em estoque
    :param preco_ou_quantidade: String 'quantidade' ou 'preco' para indical qual variavel sera alterada
    :return: estoque atualizado
    """
    repetir = True
    while repetir:
        # Recupera o estoque mais atualizado
        print()
        estoque = recupera_estoque(arquivo_estoque)
        aux.ver_estoque_ou_carrinho(estoque)

        # Se o estoque esta vazio volta para o menu anterior
        if len(estoque) == 0:
            return estoque

        if preco_ou_quantidade == 'quantidade':
            num_produto = input('\nDigite o numero do produto para alterar a quantidade (0 (zero) para cancelar): ')
        else:  # Preco
            num_produto = input('\nDigite o numero do produto para alterar o preco (0 (zero) para cancelar): ')

        produto_valido, num_produto = aux.valida_produto(num_produto, estoque)

        if produto_valido:
            # Zero para cancelar a remocao
            if num_produto == 0:
                return estoque
            # Pedindo o novo preco ou nova quantidade
            else:
                while True:
                    if preco_ou_quantidade == 'quantidade':
                        nova_variavel = input(f'Digite a nova quantidade do produto '
                                              f'({estoque[num_produto - 1]["Produto"]}): ')
                    else:
                        nova_variavel = input(f'Digite o novo preco '
                                              f'do produto ({estoque[num_produto - 1]["Produto"]}): ')

                    try:
                        if preco_ou_quantidade == 'quantidade':
                            nova_variavel = float(nova_variavel)

                            # A quantidade deve ser um numero inteiro
                            if not float(nova_variavel) == int(nova_variavel):
                                raise ValueError
                            else:
                                nova_variavel = int(nova_variavel)
                        else:  # Preco
                            nova_variavel = float(nova_variavel)

                        # Zero deixado intencionalmente
                        if nova_variavel < 0:
                            raise ValueError
                    except ValueError:
                        if preco_ou_quantidade == 'quantidade':
                            print(f'Digite um numero valido (inteiro nao-negativo).')
                        else:
                            print(f'Digite um numero valido (nao-negativo).')
                    else:
                        break

            # Alterando o preco (tem que remover 1 pois o indice de lista comeca em zero)
            if preco_ou_quantidade == 'quantidade':
                estoque[num_produto - 1]['Em estoque'] = nova_variavel
            else:
                estoque[num_produto - 1]['Preco'] = nova_variavel

            # Salvando as alteracoes no arquivo
            aux.atualiza_arquivo(arquivo_estoque, estoque)

            # Pergunta se o usuario deseja repetir a operacao
            print('\nDeseja repetir a operacao?')
            repetir = aux.confirmacao()

    return estoque


def ver_adms(adms_cadastrados):
    """
    Funcao para facilitar o print dos adms cadastrados
    :param adms_cadastrados: dicionario de adms cadastrados
    :return: None
    """
    print(f'Administradores cadastrados: {", ".join(list(adms_cadastrados.keys()))}')


# Testes
if __name__ == '__main__':
    arquivo_teste_adm = 'teste_loja_adm.txt'
    arquivo_teste_estoque = 'teste_loja_estoque.txt'

    ######################################################################

    print('TESTANDO A FUNCAO PARA CADASTRAR ADMS')
    # Comecando vazio
    aux.atualiza_arquivo(arquivo_teste_adm, {})

    # Cadastrando
    dicionario_adms_cadastrados, adm_cadastrado = cadastrar_adm(arquivo_teste_adm)

    print('\n' * 1, 'RESULTADO:', sep='\n')
    print(f'Usuario cadastrado: {adm_cadastrado}')
    print(f'Dicionario de adms registrados: {dicionario_adms_cadastrados}')
    aux.separar_comandos_print()

    ######################################################################

    print('TESTANDO A FUNCAO PARA REMOVER ADMS')
    # Comecando com um cadastro generica
    dicionario_adms_cadastrados = {'teste1': 'senha1', 'teste2': 'senha2', 'teste3': 'senha3'}
    aux.atualiza_arquivo(arquivo_teste_adm, dicionario_adms_cadastrados)

    # Removendo
    dicionario_adms_cadastrados, adm_removido = remover_adm(arquivo_teste_adm)

    print('\n' * 1, 'RESULTADO:', sep='\n')
    print(f'Usuario removido: {adm_removido}')
    print(f'Dicionario de adms registrados: {dicionario_adms_cadastrados}')
    aux.separar_comandos_print()

    ######################################################################

    print('TESTANDO A FUNCAO PARA CADASTRAR PRODUTOS')
    # Um estoque generico para testar
    estoque_teste = [{'Produto': 'Arroz', 'Preco': 5, 'Em estoque': 10},
                     {'Produto': 'Biscoito', 'Preco': 5, 'Em estoque': 10}]

    # Salvando no estoque de teste
    aux.atualiza_arquivo(arquivo_teste_estoque, estoque_teste)

    # Cadastrando novo produto
    estoque_teste = cadastrar_produto(arquivo_teste_estoque)

    print('\n' * 1, 'RESULTADO:', sep='\n')
    aux.ver_estoque_ou_carrinho(estoque_teste)
    aux.separar_comandos_print()

    ######################################################################

    print('TESTANDO A FUNCAO PARA REMOVER PRODUTOS')
    # Um estoque generico para testar
    estoque_teste = [{'Produto': 'Arroz', 'Preco': 5, 'Em estoque': 10},
                     {'Produto': 'Biscoito', 'Preco': 5, 'Em estoque': 10},
                     {'Produto': 'Cafe', 'Preco': 5, 'Em estoque': 10},
                     {'Produto': 'Cerveja', 'Preco': 5, 'Em estoque': 10},
                     {'Produto': 'Chocolate', 'Preco': 5, 'Em estoque': 10},
                     {'Produto': 'Farinha de trigo', 'Preco': 5, 'Em estoque': 10}]

    # Salvando no estoque de teste
    aux.atualiza_arquivo(arquivo_teste_estoque, estoque_teste)

    # Cadastrando novo produto
    estoque_teste = remover_produto(arquivo_teste_estoque)

    print('\n' * 1, 'RESULTADO:', sep='\n')
    aux.ver_estoque_ou_carrinho(estoque_teste)
    aux.separar_comandos_print()

    ######################################################################

    print('TESTANDO A FUNCAO PARA ALTERAR A QUANTIDADE DE UM PRODUTO')
    # Um estoque generico para testar
    estoque_teste = [{'Produto': 'Arroz', 'Preco': 5, 'Em estoque': 10},
                     {'Produto': 'Biscoito', 'Preco': 5, 'Em estoque': 10},
                     {'Produto': 'Cafe', 'Preco': 5, 'Em estoque': 10},
                     {'Produto': 'Cerveja', 'Preco': 5, 'Em estoque': 10}]

    # Salvando no estoque de teste
    aux.atualiza_arquivo(arquivo_teste_estoque, estoque_teste)

    # Cadastrando novo produto
    estoque_teste = alterar_preco_ou_quantidade(arquivo_teste_estoque)

    print('\n' * 1, 'RESULTADO:', sep='\n')
    aux.ver_estoque_ou_carrinho(estoque_teste)
    aux.separar_comandos_print()

    ######################################################################

    print('TESTANDO A FUNCAO PARA ALTERAR O PRECO DE UM PRODUTO')
    # Um estoque generico para testar
    estoque_teste = [{'Produto': 'Arroz', 'Preco': 5, 'Em estoque': 10},
                     {'Produto': 'Biscoito', 'Preco': 5, 'Em estoque': 10},
                     {'Produto': 'Cafe', 'Preco': 5, 'Em estoque': 10},
                     {'Produto': 'Cerveja', 'Preco': 5, 'Em estoque': 10}]

    # Salvando no estoque de teste
    aux.atualiza_arquivo(arquivo_teste_estoque, estoque_teste)

    # Cadastrando novo produto
    estoque_teste = alterar_preco_ou_quantidade(arquivo_teste_estoque, 'preco')

    print('\n' * 1, 'RESULTADO:', sep='\n')
    aux.ver_estoque_ou_carrinho(estoque_teste)
    aux.separar_comandos_print()
