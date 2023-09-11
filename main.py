from queue import PriorityQueue
import random

objetivo = [[0,1,2],[3,4,5],[6,7,8]]
caminho_total = []

def verificar_solucionabilidade(estado_inicial):
    elementos = []
    for linha in estado_inicial:
        elementos += linha
    # Nestas linhas, inicializamos a variável inversoes como zero. Em seguida, usamos dois loops for aninhados para
    # percorrer todas as combinações de pares de elementos na lista elementos. Se encontrarmos dois elementos não nulos
    # e em ordem inversa (ou seja, um elemento maior aparece antes de um elemento menor), incrementamos a variável
    # inversoes. Essa contagem de inversões é importante para determinar se o quebra-cabeça é solucionável.
    inversoes = 0
    for i in range(len(elementos)):
        for j in range(i+1, len(elementos)):
            if elementos[i] != 0 and elementos[j] != 0 and elementos[i] > elementos[j]:
                inversoes += 1
    return inversoes % 2 == 0

def encontrar_posicao_objetivo(valor):
    for i in range(3):
        for j in range(3):
            if objetivo[i][j] == valor:
                return i, j

def gerar_estados_sucessores(estado_atual):
    caminho_total.append(estado_atual)
    sucessores = []
    i, j = 0, 0
    # encontrar a posição do espaço em branco
    for x in range(3):
        for y in range(3):
            if estado_atual[x][y] == 0:
                i, j = x, y
                break
    # mover a peça acima do espaço em branco
    if i > 0:
        novo_estado = [linha[:] for linha in estado_atual]
        novo_estado[i][j], novo_estado[i-1][j] = novo_estado[i-1][j], novo_estado[i][j]
        sucessores.append(novo_estado)
    # mover a peça abaixo do espaço em branco
    if i < 2:
        novo_estado = [linha[:] for linha in estado_atual]
        novo_estado[i][j], novo_estado[i+1][j] = novo_estado[i+1][j], novo_estado[i][j]
        sucessores.append(novo_estado)
    # mover a peça à esquerda do espaço em branco
    if j > 0:
        novo_estado = [linha[:] for linha in estado_atual]
        novo_estado[i][j], novo_estado[i][j-1] = novo_estado[i][j-1], novo_estado[i][j]
        sucessores.append(novo_estado)
    # mover a peça à direita do espaço em branco
    if j < 2:
        novo_estado = [linha[:] for linha in estado_atual]
        novo_estado[i][j], novo_estado[i][j+1] = novo_estado[i][j+1], novo_estado[i][j]
        sucessores.append(novo_estado)
    return sucessores

def calcular_heuristica(estados_sucessores):
    # heurística 1: número de peças fora do lugar
    if heuristica == "h1":
        h = 0
        for i in range(3):
            for j in range(3):
                if estados_sucessores[i][j] != objetivo[i][j]:
                    h += 1
        return h

        print(valor_heuristica)
    # heurística 2:  heurística de Manhattan - A heurística de Manhattan é uma função de estimativa que calcula a
    # distância total percorrida por todas as peças para alcançarem suas posições no estado objetivo.
    elif heuristica == "h2":
        h = 0
        for i in range(3):
            for j in range(3):
                if estados_sucessores[i][j] != objetivo[i][j] and estados_sucessores[i][j] != 0:
                    valor = estados_sucessores[i][j]
                    objetivo_x, objetivo_y = encontrar_posicao_objetivo(valor)
                    h += abs(i - objetivo_x) + abs(j - objetivo_y)
        return h
    ## heurística 3: número de peças maiores que a peça à direita
    elif heuristica == "h3":
        count = 0
        for i in range(3):
            for j in range(2):
                if estados_sucessores[i][j] > estados_sucessores[i][j + 1]:
                    count += 1
        return count
    else:
        print("Heurística inválida.")
        return

def gerar_matriz_aleatoria():
    numeros = list(range(9))
    random.shuffle(numeros)
    matriz = []
    for i in range(3):
        linha = []
        for j in range(3):
            #Calcula o índice correto na lista numeros com base nos valores de i e j.
            linha.append(numeros[i * 3 + j])
        matriz.append(linha)
    return matriz

def puzzleSolver(estado_inicial, heuristica):
    if not verificar_solucionabilidade(estado_inicial):
        print("Não solucionável :(")
        return
    #Aqui, criamos uma fila de prioridade chamada fronteira usando a classe PriorityQueue(). Essa fila será usada para
    # armazenar os estados a serem explorados durante a busca. Inicialmente, colocamos o estado inicial na fila com uma
    # prioridade de 0 e um custo de 0.
    fronteira = PriorityQueue()
    fronteira.put((0, 0, estado_inicial))
    #Essas linhas criam um conjunto visitados para armazenar os estados já visitados durante a busca e uma lista caminho
    # para armazenar todos os estados percorridos até a solução.
    visitados = set()
    sequencia = []
    while not fronteira.empty():
        valor_heuristica, custo, estado = fronteira.get()
        print("ESTADO ATUAL:", estado)
        print("Soma heuristica e estado", valor_heuristica + custo)
        print("heuristica", valor_heuristica)
        print("Custo:",custo)

        sequencia.append(estado)
        if estado == objetivo:
            print("Ordem de resolução:")
            for estado in sequencia:
                for linha in estado:
                    print(linha)
                print("|")
                print("|")
            print("Custo do caminho: ", custo)
            caminho_total.clear()
            return
        if tuple(map(tuple, estado)) in visitados:
            continue
        visitados.add(tuple(map(tuple, estado)))
        sucessores = gerar_estados_sucessores(estado)
        print("SUCESSORES:", sucessores)
        novo_custo = custo + 1  # Incrementa o custo em 1
        for s in sucessores:
            if tuple(map(tuple, s)) not in visitados:
                valor_heuristica = calcular_heuristica(s)
                fronteira.put((valor_heuristica, novo_custo, s))
    print("Não foi possível encontrar uma solução.")


if __name__ == "__main__":
    while True:
        estado_inicial_tabuleiro = input("DIGÍTE O ESTADO INICIAL DA MATRIZ PARA SER SOLUCIONADA OU DIGITE 'R' PARA UMA MATRIZ ALEATÓRIA: ")

        if estado_inicial_tabuleiro.upper() == "R":
            estado_inicial_tabuleiro = gerar_matriz_aleatoria()
            print(estado_inicial_tabuleiro)
        else:
            try:
                estado_inicial_tabuleiro = eval(estado_inicial_tabuleiro)
            except:
                print("Entrada inválida. Certifique-se de fornecer uma matriz válida ou 'R' para matriz aleatória.")
                continue

        print("-------------------------------------------------------")
        print("Heurística 1: Número de peças fora do lugar \n"
              "Heurística 2: Manhattan distance \n"
              "Heurística 3: Número de peças maiores que a peça à direita")
        print("-------------------------------------------------------")
        heuristica = input("DIGÍTE A HEURÍSTICA A SER UTILIZADA (h1, h2 ou h3): ")
        puzzleSolver(estado_inicial_tabuleiro, heuristica)
        print("-------------------------------------------------------")
        novamente = input("Deseja resolver outro quebra-cabeça? (S/N): ")
        if novamente.upper() != "S":
            break
        print("-------------------------------------------------------")

ex = [[0, 4, 2], [1, 7, 5], [3, 6, 8]]

