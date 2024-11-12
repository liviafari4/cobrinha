from typing import List, Tuple
import pygame
import random

LARGURA, ALTURA = 1200, 800  # Define a largura e altura da tela
tela = pygame.display.set_mode((LARGURA, ALTURA))  # Cria a tela com as dimensões definidas 

PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0) 
BRANCO = (255, 255, 255)
AZUL = (0, 0, 64)
ROXO = (64, 0, 64)

TAMANHO_QUADRADO = 20   # Tamanho de cada segmento da cobra
VELOCIDADE_COBRINHA = 8  # Velocidade inicial da cobrinha

def selecionar_velocidade(tecla: int, velocidade_x: int, velocidade_y: int) -> Tuple[int, int]:
    """
    Seleciona a nova velocidade da cobrinha com base na tecla pressionada pelo jogador.
    Retorna a nova velocidade no eixo x e y.
    """
    if tecla == pygame.K_DOWN:  # Pra baixo
        if velocidade_y < 0:  # impede de ir para direção oposta(pra cima)
            return velocidade_x, velocidade_y
        return 0, TAMANHO_QUADRADO  # Define a velocidade para mover para baixo
    elif tecla == pygame.K_UP:  # Pra cima
        if velocidade_y > 0: 
            return velocidade_x, velocidade_y
        return 0, -TAMANHO_QUADRADO # Define a velocidade para mover para cima
    elif tecla == pygame.K_RIGHT:  # Pra direita
        if velocidade_x < 0: 
            return velocidade_x, velocidade_y
        return TAMANHO_QUADRADO, 0  # Define a velocidade para mover para direita
    elif tecla == pygame.K_LEFT:  # Pra esquerda
        if velocidade_x > 0: 
            return velocidade_x, velocidade_y
        return -TAMANHO_QUADRADO, 0  # Define a velocidade para mover para esquerda

    return velocidade_x, velocidade_y  # Retorna as velocidades atuais caso nenhuma tecla relevante seja precionada

def carregar_maior_pontuacao() -> int:
    """
    Carrega a maior pontuação do arquivo
    Retorna a maior pontuação encontrada, ou 0 se não houver registro.
    """
    try:
        with open("recorde.txt", "r") as arquivo:
            conteudo = arquivo.read().strip()
            return int(conteudo) if conteudo else 0  # Retorna a pontuação  se o arquivo não estiver vazio 
    except (FileNotFoundError, ValueError):
        return 0  # Retorna 0 se o arquivo não for encontrado ou estiver corrompido

def salvar_maior_pontuacao(maior_pontuacao: int) -> None:
    """Salva a maior pontuação em um arquivo."""
    with open("recorde.txt","w") as arquivo:
        arquivo.write(str(maior_pontuacao))  # Salva a pontuação no arquivo

def rodar_eventos(fim_jogo: bool, reiniciar_jogo: bool, velocidade_x: int, velocidade_y: int, posicao_x: float, posicao_y: float, pixels: List[Tuple[int, int]], tamanho_cobra: int, comida1_x: float, comida1_y: float, comida2_x: float, comida2_y: float, maior_pontuacao: int, VELOCIDADE_COBRINHA: int) -> Tuple[bool, bool, int, int, float, float, List[Tuple[int, int]], int, float, float, float, float, int, int]:
    """
    Executa a lógica principal do jogo, atualiza a tela, verifica colisões, gera comida e calcula a pontuação.
    Retorna vários valores, incluindo o estado do jogo e novas posições.
    fim_jogo: Indica se o jogo deve terminar.
    reiniciar_jogo: Indica se o jogo deve ser reiniciado.
    velocidade_x: A velocidade atual no eixo x.
    velocidade_y: A velocidade atual no eixo y.
    posicao_x: A posição atual da cobrinha no eixo x.
    posicao_y: A posição atual da cobrinha no eixo y.
    pixels: Lista de posições ocupadas pela cobrinha.
    tamanho_cobra: O tamanho atual da cobrinha.
    comida1_x: A coordenada x da primeira comida.
    comida1_y: A coordenada y da primeira comida.
    comida2_x: A coordenada x da segunda comida.
    comida2_y: A coordenada y da segunda comida.
    maior_pontuacao: A maior pontuação registrada.
    VELOCIDADE_COBRINHA: A velocidade atual da cobrinha.
    """

    from interface import desenhar_comida

    fim_jogo, velocidade_x, velocidade_y = rodar_sair(fim_jogo, velocidade_x, velocidade_y)
    tela.fill(PRETO)  # Preenche a tela com a cor preta
    maior_pontuacao = verificar_pontuacao(tamanho_cobra, maior_pontuacao)  # Atualiza e verificar a maior pontuação até o momento  

	# Desenha as comidas na tela
    desenhar_comida(TAMANHO_QUADRADO, comida1_x, comida1_y)
    desenhar_comida(TAMANHO_QUADRADO, comida2_x, comida2_y)

	# Move a cobrinha e atualiza suas coordendas
    posicao_x, posicao_y, pixels = mover_cobra(posicao_x, posicao_y, velocidade_x, velocidade_y, pixels, tamanho_cobra)

	# Verifica a colisão com as bordas da tela
    reiniciar_jogo = verificar_bordas(posicao_x, posicao_y, reiniciar_jogo)
    # Verifica colisão da cobrinha com ela mesma
    reiniciar_jogo = verificar_colisao(pixels, posicao_x, posicao_y, reiniciar_jogo)
	# Verifica se a cobrinha comeu a comida e, se sim, atualiza as posições da comida e o tamanho da cobra
    tamanho_cobra, VELOCIDADE_COBRINHA, comida1_x, comida1_y, comida2_x, comida2_y = verificar_se_comeu(tamanho_cobra, VELOCIDADE_COBRINHA, posicao_x, posicao_y, comida1_x, comida1_y, comida2_x, comida2_y, pixels)

	# Retorna o estado atualizado do jogo
    return fim_jogo, reiniciar_jogo, velocidade_x, velocidade_y, posicao_x, posicao_y, pixels, tamanho_cobra, comida1_x, comida1_y, comida2_x, comida2_y, maior_pontuacao, VELOCIDADE_COBRINHA

def verificar_pontuacao(tamanho_cobra: int, maior_pontuacao: int) -> int:
    """
    Verifica e atualiza a maior pontuação do jogador.
    Se a pontuação atual ultrapassar a maior pontuação registrada, atualiza
    a maior pontuação e salva em um arquivo.
    Retorna a maior pontuação atualizada.
    """
    if tamanho_cobra - 1 > maior_pontuacao:
        maior_pontuacao = tamanho_cobra - 1
        salvar_maior_pontuacao(maior_pontuacao)  # Salvar a maior pontuação em um arquivo
    return maior_pontuacao

def rodar_sair(fim_jogo: bool, velocidade_x: int, velocidade_y: int) -> Tuple[bool, int, int]:
    """
    Processa eventos de saída do jogo.
    Retorna o estado do jogo e as velocidades atualizadas.
    """
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Se o jogador fechar a janela
            fim_jogo = True
        elif evento.type == pygame.KEYDOWN:
            # Atualiza as velocidades da cobrinha com base na tecla precionada
            velocidade_x, velocidade_y = selecionar_velocidade(evento.key, velocidade_x, velocidade_y)

    # Retorna o  estado jogo e as velocidades atualizadas
    return fim_jogo, velocidade_x, velocidade_y

def verificar_bordas(posicao_x: float, posicao_y: float, reiniciar_jogo: bool) -> bool:
    """
    Verifica se a cobrinha colidiu com as bordas da tela.
    Retorna True se colidiu, caso contrário, retorna o estado de reinício.
    """
    # Verificar se a posição da cobrinha está além dos limites da tela  
    if posicao_x < 20 or posicao_x >= LARGURA - 20 or posicao_y < 20 or posicao_y >= ALTURA - 20:
        return True  # Se a cobrinha  colidiu com as bordas, o jogo será reiniciado
    return reiniciar_jogo  # Caso contrário, o jogo continua

def mover_cobra(posicao_x: float, posicao_y: float, velocidade_x: int, velocidade_y: int, pixels: List[Tuple[int, int]], tamanho_cobra: int) -> Tuple[float, float, List[Tuple[int, int]]]:
    """
    Move a cobrinha, atualiza suas coordenadas e gerencia o crescimento.
    """
    # Atualiza a nova posição da cobrinha  somando a velocidade
    posicao_x += velocidade_x
    posicao_y += velocidade_y

	# Adiciona a nova posição da cobrinha à lista de pixels
    pixels.append([posicao_x, posicao_y])
    # Se a quantidade de pixels for maior que o tamanho da cobra, remova o último pixel
    if len(pixels) > tamanho_cobra:
        del pixels[0]

    # Retorna a nova posição e a lista atualizada de pixels 
    return posicao_x, posicao_y, pixels

def verificar_colisao(pixels: List[Tuple[int, int]], posicao_x: float, posicao_y: float, reiniciar_jogo: bool) -> bool:
    """
    Verifica se a cobrinha colidiu com si mesma.
    """
    for pixel in pixels[:-1]:
        if pixel == [posicao_x, posicao_y]:
            return True  # Se colidiu, retorna True
    return reiniciar_jogo  # Caso contrário, o jogo continua

def verificar_se_comeu(tamanho_cobra: int, VELOCIDADE_COBRINHA: int, posicao_x: float, posicao_y: float, comida1_x: float, comida1_y: float, comida2_x: float, comida2_y: float, pixels: List[Tuple[int, int]]) -> Tuple[int, int, float, float, float, float]:
    """
    Verifica se a cobrinha comeu a comida.
    """
    if posicao_x == comida1_x and posicao_y == comida1_y:
        tamanho_cobra += 1 # Aumenta o tamanho da cobra  
        comida1_x, comida1_y = gerar_comida(pixels)  # Gera uma nova posição para comida 
    elif posicao_x == comida2_x and posicao_y == comida2_y:
        tamanho_cobra += 1  # Aumenta o tamanho da cobra  
        comida2_x, comida2_y = gerar_comida(pixels)  # Gera uma nova posição para comida 

	# Retorna o tamanho atualizado da cobra, a velocidade e as novas posições das comidas
    return tamanho_cobra, VELOCIDADE_COBRINHA, comida1_x, comida1_y, comida2_x, comida2_y

def gerar_comida(pixels: List[Tuple[int, int]]) -> Tuple[float, float]:
    """
    Gera a posição da comida na tela, garantindo que não colida com a cobrinha.

    A função seleciona uma posição aleatória dentro das margens da tela e verifica
    se essa posição já está ocupada pelos segmentos da cobrinha. Se estiver,
    gera uma nova posição até encontrar uma posição livre. 

    Retorna as coordenadas (x, y) da comida gerada.
    """
    margem = TAMANHO_QUADRADO
    while True:  # Loop até encontrar uma posição válida
        comida_x = round(random.randrange(margem, LARGURA - margem, TAMANHO_QUADRADO) / float(TAMANHO_QUADRADO)) * float(TAMANHO_QUADRADO)
        comida_y = round(random.randrange(margem, ALTURA - margem, TAMANHO_QUADRADO) / float(TAMANHO_QUADRADO)) * float(TAMANHO_QUADRADO)
    
        ocupado = False
        for pixel in pixels:  # Verificar se a posição gerada já está ocupada pela cobrinha
            if pixel[0] == comida_x and pixel[1] == comida_y:
                ocupado = True
                break 

        if not ocupado:
            break  # Se a posição não estiver ocupada, sai do loop

    return comida_x, comida_y  # Retorna a posição gerada

def rodar_jogo() -> None:
    """Função principal que roda o jogo.
    Gerencia a lógica do jogo, incluindo movimentação da cobrinha, verificação de
    colisões e atualização da tela. Reinicia o jogo se necessário."""

    from interface import mostrar_mensagem_gameover, atualizar_jogo1, atualizar_jogo2, atualizar_jogo3, desenhar_cobra, desenhar_comida, desenhar_maior_pontuacao, desenhar_pontuacao, relogio

    global VELOCIDADE_COBRINHA
    fim_jogo, reiniciar_jogo = False, False           # Inicializa variáveis essenciais do jogo
    posicao_x, posicao_y = LARGURA / 2, ALTURA / 2
    velocidade_x, velocidade_y = 0, 0
    tamanho_cobra = 1
    pixels = []
    8
    comida1_x, comida1_y = gerar_comida(pixels)
    comida2_x, comida2_y = gerar_comida(pixels)
    maior_pontuacao = carregar_maior_pontuacao() 

    while not fim_jogo:
        while reiniciar_jogo:
            sair, reiniciar_jogo = mostrar_mensagem_gameover()
            if sair: fim_jogo = True
            elif reiniciar_jogo: return rodar_jogo()
        
        fim_jogo, reiniciar_jogo, velocidade_x, velocidade_y, posicao_x, posicao_y, pixels, tamanho_cobra, comida1_x, comida1_y, comida2_x, comida2_y, maior_pontuacao, VELOCIDADE_COBRINHA = rodar_eventos(fim_jogo, reiniciar_jogo, velocidade_x, velocidade_y, posicao_x, posicao_y, pixels, tamanho_cobra, comida1_x, comida1_y, comida2_x, comida2_y, maior_pontuacao, VELOCIDADE_COBRINHA)

        if tamanho_cobra - 1 >= 50: atualizar_jogo3(tamanho_cobra, tela) # Atualiza o nível com base no tamanho da cobra
        elif tamanho_cobra - 1 >= 30: atualizar_jogo2(tamanho_cobra, tela)
        elif tamanho_cobra - 1 >= 10: atualizar_jogo1(tamanho_cobra, tela)

        desenhar_cobra(pixels)    		        # Desenha os elementos na tela
        desenhar_pontuacao(tamanho_cobra - 1)
        desenhar_maior_pontuacao(maior_pontuacao)
        desenhar_comida(TAMANHO_QUADRADO, comida1_x, comida1_y)
        desenhar_comida(TAMANHO_QUADRADO, comida2_x, comida2_y)
        pygame.display.update()
        relogio.tick(VELOCIDADE_COBRINHA)