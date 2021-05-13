import loja_funcoes_auxiliares as aux


def adicionar_produto_carrinho(estoque, carrinho):
    """
    Adiciona um produto do estoque ao carrinho (se nao estiver adicionado ainda)
    :param estoque: lista com o estoque mais atualizado
    :param carrinho: lista com carrinho de compras mais atualizado
    :return: carrinho
    """
    repetir = True
    while repetir:
        aux.ver_estoque_ou_carrinho(estoque)

        if not aux.checa_vazio(carrinho):
            print()
            aux.ver_estoque_ou_carrinho(carrinho, 'Carrinho')

        produtos_no_carrinho = [produto['Produto'] for produto in carrinho]

        num_produto_para_add = input('Digite o numero do produto a ser '
                                     'adicionado ao carrinho (0 (zero) para cancelar): ')

        produto_valido, num_produto = aux.valida_produto(num_produto_para_add, estoque)

        if produto_valido:
            if num_produto == 0:  # Cancelar operacao
                print('Operacao cancelada')
                return carrinho
            else:
                # Tem que remover 1 de num_produto pois o indice de lista comeca em zero
                if estoque[num_produto - 1]["Produto"] in produtos_no_carrinho:
                    print('Este produto ja estah no carrinho.')
                else:
                    carrinho.append(estoque[num_produto - 1].copy())
                    carrinho = alterar_quantidade_carrinho(estoque, carrinho, True)
                    carrinho.sort(key=lambda dict_produto: dict_produto['Produto'])

            # Pergunta se o usuario deseja repetir a operacao
            print('\nDeseja repetir a operacao?')
            repetir = aux.confirmacao()

    return carrinho


def remover_produto_carrinho(carrinho):
    """
    Funcao para remover produtos do carrinho
    :param carrinho: lista de carrinho de compras
    :return: lista de carrinho de compras sem os produtos removidos
    """
    repetir = True
    while repetir:
        if not aux.checa_vazio(carrinho):
            aux.ver_estoque_ou_carrinho(carrinho, 'Carrinho')

            num_produto_remover = input('Digite o numero do produto a ser '
                                        'removido do carrinho (0 (zero) para cancelar): ')

            produto_valido, num_produto = aux.valida_produto(num_produto_remover, carrinho)

            if produto_valido:
                if num_produto == 0:  # Cancelar operacao
                    print('Operacao cancelada')
                    return carrinho
                else:
                    # Tem que remover 1 de num_produto pois o indice de lista comeca em zero
                    produto_removido = carrinho.pop(num_produto - 1)

                # Pergunta se o usuario deseja repetir a operacao
                print(f'O produto {produto_removido["Produto"]} foi removido.')
                print('\nDeseja repetir a operacao?')
                repetir = aux.confirmacao()
        else:
            print('O carrinho estah vazio')
            break

    return carrinho


def alterar_quantidade_carrinho(estoque, carrinho, adicionando=False):
    # Se o produto estah sendo adicionado ao carrinho, nao eh necessario pedir o numero do produto
    # O numero sera -1 (ultimo da lista, que depois sera ordenada) e sera um produto valido
    indice_produto = -1
    produto_valido = True
    repetir = True

    while repetir:
        # Se nao estah adicionando (estah so alterando) um produto, eh preciso pedir o numero do produto e validar
        if not adicionando:
            aux.ver_estoque_ou_carrinho(estoque)
            aux.ver_estoque_ou_carrinho(carrinho, 'Carrinho')

            num_produto_para_alterar = input('Digite o numero do produto a ser '
                                             'alterado no carrinho (0 (zero) para cancelar): ')

            produto_valido, indice_produto = aux.valida_produto(num_produto_para_alterar, carrinho)

            # Se zero, o usuario deseja cancelar
            if indice_produto == 0:
                print('Operacao cancelada.')
                return carrinho

            indice_produto -= 1  # O indice da lista comeca em zero

        if produto_valido:
            while True:
                quantidade = input(f'Digite a quantidade de {carrinho[indice_produto]["Produto"]} '
                                   f'que deseja manter no carrinho: ')

                try:
                    # Transforma em float para conseguir validar se a informacao do usuario eh int ou float
                    quantidade = float(quantidade)

                    if quantidade < 0 or quantidade > carrinho[indice_produto]["Em estoque"]:
                        raise ValueError
                    elif int(quantidade) != float(quantidade):
                        raise ValueError
                except ValueError:
                    print(f'Digite um numero valido (inteiro entre 0 e {carrinho[indice_produto]["Em estoque"]}).')
                else:
                    quantidade = int(quantidade)
                    carrinho[indice_produto]['Carrinho'] = quantidade
                    carrinho[indice_produto]['Total'] = carrinho[indice_produto]['Preco'] * \
                                                        carrinho[indice_produto]['Carrinho']
                    break

            # Se o produto esta sendo adicionado ao carrinho, o loop deve ser executado so uma vez
            if adicionando:
                break
            else:
                # Pergunta se o usuario deseja repetir a operacao
                print('\nDeseja repetir a operacao?')
                repetir = aux.confirmacao()

    # Loop para retirar produtos com quantidade = 0
    carrinho = [item for item in carrinho if item['Carrinho'] != 0]

    return carrinho


def fechar_compra(carrinho, estoque, arquivo_com_estoque):
    """
    Funcao para remover a quantidade de cada produto comprada do estoque e salvar o novo estoque
    :param carrinho: lista com os produtos a serem comprados
    :param estoque:  lista com os produtos em estoque
    :param arquivo_com_estoque: arquivo ".txt" contendo o estoque
    :return: None
    """
    print('Compras finalizadas!')
    if not aux.checa_vazio(carrinho):
        aux.ver_estoque_ou_carrinho(carrinho, 'Carrinho')

        # Loop para remover os produtos comprados do estoque
        indice_inicial = 0
        for item_carrinho in carrinho:
            for indice in range(indice_inicial, len(estoque)):
                if estoque[indice]['Produto'] == item_carrinho['Produto']:
                    estoque[indice]['Em estoque'] -= item_carrinho['Carrinho']
                    # No proximo item do carrinho, pode procurar a partir de onde parou no estoque
                    # para economizar alguns loops (porque as listas estao em ordem alfabetica)
                    indice_inicial = indice + 1
                    break

        # Salvando o estado atual do estoque
        aux.atualiza_arquivo(arquivo_com_estoque, estoque)


# "TESTES"
if __name__ == '__main__':
    from loja_adm import recupera_estoque
    arquivo_teste_estoque = 'teste_loja_estoque.txt'

    ######################################################################

    print('TESTANDO A FUNCAO PARA ADICIONAR PRODUTOS AO CARRINHO')

    # Um estoque generico para testar
    estoque_teste = [{'Produto': 'Arroz', 'Preco': 6.5, 'Em estoque': 10},
                     {'Produto': 'Biscoito', 'Preco': 3.0, 'Em estoque': 10},
                     {'Produto': 'Cafe', 'Preco': 6.0, 'Em estoque': 10},
                     {'Produto': 'Cerveja', 'Preco': 3.0, 'Em estoque': 10},
                     {'Produto': 'Chocolate', 'Preco': 7.5, 'Em estoque': 10},
                     {'Produto': 'Farinha de trigo', 'Preco': 3.75, 'Em estoque': 10},
                     {'Produto': 'Feijao', 'Preco': 6.0, 'Em estoque': 10},
                     {'Produto': 'Leite', 'Preco': 3.5, 'Em estoque': 10},
                     {'Produto': 'Suco', 'Preco': 4.5, 'Em estoque': 10}]
    aux.atualiza_arquivo('teste_loja_estoque.txt', estoque_teste)
    estoque = recupera_estoque(arquivo_teste_estoque)
    carrinho = []

    carrinho = adicionar_produto_carrinho(estoque, carrinho)
    print('\n' * 3, 'RESULTADO:', sep='\n')
    aux.ver_estoque_ou_carrinho(carrinho, 'carrinho')
    aux.separar_comandos_print()

    ######################################################################

    print('TESTANDO A FUNCAO PARA REMOVER PRODUTOS DO CARRINHO')

    # Um carrinho generico para testar
    carrinho = [{'Produto': 'Cafe', 'Preco': 6.0, 'Em estoque': 20, 'Carrinho': 10, 'Total': 60},
                {'Produto': 'Cerveja', 'Preco': 3.0, 'Em estoque': 20, 'Carrinho': 10, 'Total': 30},
                {'Produto': 'Chocolate', 'Preco': 7.5, 'Em estoque': 20, 'Carrinho': 10, 'Total': 75},
                {'Produto': 'Suco', 'Preco': 4.5, 'Em estoque': 20, 'Carrinho': 10, 'Total': 45}]

    carrinho = remover_produto_carrinho(carrinho)
    print('\n' * 3, 'RESULTADO:', sep='\n')
    aux.ver_estoque_ou_carrinho(carrinho, 'carrinho')
    aux.separar_comandos_print()

    ######################################################################

    print('TESTANDO A FUNCAO PARA ALTERAR PRODUTOS DO CARRINHO')

    # Um estoque generico para testar
    estoque_teste = [{'Produto': 'Arroz', 'Preco': 6.5, 'Em estoque': 10},
                     {'Produto': 'Biscoito', 'Preco': 3.0, 'Em estoque': 10},
                     {'Produto': 'Cafe', 'Preco': 6.0, 'Em estoque': 10},
                     {'Produto': 'Cerveja', 'Preco': 3.0, 'Em estoque': 10},
                     {'Produto': 'Chocolate', 'Preco': 7.5, 'Em estoque': 10},
                     {'Produto': 'Farinha de trigo', 'Preco': 3.75, 'Em estoque': 10},
                     {'Produto': 'Feijao', 'Preco': 6.0, 'Em estoque': 10},
                     {'Produto': 'Leite', 'Preco': 3.5, 'Em estoque': 10},
                     {'Produto': 'Suco', 'Preco': 4.5, 'Em estoque': 10}]

    # Um carrinho generico para testar
    carrinho = [{'Produto': 'Cafe', 'Preco': 6.0, 'Em estoque': 20, 'Carrinho': 10, 'Total': 60},
                {'Produto': 'Cerveja', 'Preco': 3.0, 'Em estoque': 20, 'Carrinho': 10, 'Total': 30},
                {'Produto': 'Chocolate', 'Preco': 7.5, 'Em estoque': 20, 'Carrinho': 10, 'Total': 75},
                {'Produto': 'Suco', 'Preco': 4.5, 'Em estoque': 20, 'Carrinho': 10, 'Total': 45}]

    carrinho = alterar_quantidade_carrinho(estoque_teste, carrinho)
    print('\n' * 1, 'RESULTADO:', sep='\n')
    aux.ver_estoque_ou_carrinho(carrinho, 'carrinho')
    aux.separar_comandos_print()

    ######################################################################

    print('TESTANDO A FUNCAO PARA FINALIZAR COMPRAS')

    # Um estoque generico para testar
    estoque_teste = [{'Produto': 'Arroz', 'Preco': 6.5, 'Em estoque': 10},
                     {'Produto': 'Biscoito', 'Preco': 3.0, 'Em estoque': 10},
                     {'Produto': 'Cafe', 'Preco': 6.0, 'Em estoque': 10},
                     {'Produto': 'Cerveja', 'Preco': 3.0, 'Em estoque': 10},
                     {'Produto': 'Chocolate', 'Preco': 7.5, 'Em estoque': 10},
                     {'Produto': 'Farinha de trigo', 'Preco': 3.75, 'Em estoque': 10},
                     {'Produto': 'Feijao', 'Preco': 6.0, 'Em estoque': 10},
                     {'Produto': 'Leite', 'Preco': 3.5, 'Em estoque': 10},
                     {'Produto': 'Suco', 'Preco': 4.5, 'Em estoque': 10}]

    # Atualiza o arquivo com estoque
    aux.atualiza_arquivo(arquivo_teste_estoque, estoque_teste)

    # Um carrinho generico para testar
    carrinho = [{'Produto': 'Cafe', 'Preco': 6.0, 'Em estoque': 10, 'Carrinho': 10, 'Total': 60},
                {'Produto': 'Cerveja', 'Preco': 3.0, 'Em estoque': 10, 'Carrinho': 10, 'Total': 30},
                {'Produto': 'Chocolate', 'Preco': 7.5, 'Em estoque': 10, 'Carrinho': 10, 'Total': 75},
                {'Produto': 'Suco', 'Preco': 4.5, 'Em estoque': 10, 'Carrinho': 10, 'Total': 45}]

    # Vendo o estoque antes de finalizar a compra
    aux.ver_estoque_ou_carrinho(estoque_teste)

    # Finalizando a compra
    print('\n\nFinalizando a compra\n\n')
    fechar_compra(carrinho, estoque_teste, arquivo_teste_estoque)

    print('\n' * 3, 'RESULTADO:', sep='\n')
    aux.ver_estoque_ou_carrinho(recupera_estoque(arquivo_teste_estoque))
