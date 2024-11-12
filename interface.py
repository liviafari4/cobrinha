"""JOGO DA COBRINHA SNACK"""

from logica import rodar_jogo
import pygame
from typing import List, Tuple

# Inicializa o pygame
pygame.init() 
pygame.display.set_caption("Cobrinha Snake") # Define o título da janela do jogo
LARGURA, ALTURA = 1200, 800 # Define a largura e altura da tela
tela = pygame.display.set_mode((LARGURA, ALTURA)) # Cria a tela com as dimensões definidas 
relogio = pygame.time.Clock() # Cria um relógio para controlar a taxa de atualização do jogo

# CONSTANTES GLOBAIS (CORES USADAS NO JOGO)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0) 
BRANCO = (255, 255, 255)
AZUL = (0, 0, 64)
ROXO = (64, 0, 64)
ROSA = (255, 0, 255)

# CONSTANTES GLOBAIS
TAMANHO_QUADRADO = 20  # Tamanho de cada segmento da cobra
VELOCIDADE_COBRINHA = 8 # Velocidade inicial da cobrinha

def atualizar_jogo1(tamanho_cobra: int, tela) -> None:
    """
    Atualiza o fundo do jogo com base no tamanho da cobra, mudando para uma cor específica.
    """
    if (tamanho_cobra - 1) >= 10:
        tela.fill(ROXO)

def atualizar_jogo2(tamanho_cobra: int, tela) -> None:
    """
    Atualiza o fundo do jogo com base no tamanho da cobra, mudando para uma cor específica.
    """
    if (tamanho_cobra - 1) >= 30:
        tela.fill(AZUL)

def atualizar_jogo3(tamanho_cobra: int, tela) -> None:
    """
    Atualiza o fundo do jogo com base no tamanho da cobra, mudando para uma cor específica.
    """
    if (tamanho_cobra - 1) >= 50:
        tela.fill(ROSA)

def desenhar_comida(tamanho: int, comida_x: float, comida_y: float) -> None:
    """
    Desenha a comida na tela.
    """
    pygame.draw.rect(tela, VERMELHO, [comida_x, comida_y, tamanho, tamanho]) # Desenha a comida como um quadrado vermelho

def desenhar_cobra(pixels: List[Tuple[int, int]]) -> None:
    """
    Desenha a cobrinha na tela, representando cada segmento como um retângulo verde.
    """
    for pixel in pixels:
        pygame.draw.rect(tela, VERDE, [pixel[0], pixel[1], TAMANHO_QUADRADO, TAMANHO_QUADRADO]) #Desenha cada segmento da cobra

def desenhar_pontuacao(pontuacao: int) -> None:
    """
    Desenha a pontuação atual do jogador no canto superior esquerdo da tela.
    """
    fonte = pygame.font.SysFont("Helvetica", 25) # Define a fonte da pontuação
    texto = fonte.render(f"Pontos: {pontuacao}", True, AMARELO) # Renderiza o texto com a pontuação
    tela.blit(texto, [1, 1]) # Desenha a pontuação na tela

def mostrar_mensagem(mensagem: str, cor: Tuple[int, int, int]) -> None:
    """
    Exibe uma mensagem na tela.
    """
    fonte_game_over = pygame.font.SysFont(None, 50) # Define a fonte da mensagem
    texto = fonte_game_over.render(mensagem, True, cor) # Renderiza a mensagem
    texto_rect = texto.get_rect(center=(LARGURA / 2, ALTURA / 2)) # Centraliza a mensagem na tela
    tela.blit(texto, texto_rect) # Desenha a mensagem na tela
    pygame.display.update() # Atualizar a tela 

def mostrar_mensagem_gameover() -> Tuple[bool, bool]:
    """
    Exibe a mensagem de Game Over e retorna as escolhas do jogador.
    Retorna se o jogador deseja sair ou reiniciar o jogo.
    """
    tela.fill(BRANCO) # Preenche a tela com a cor branca
    mostrar_mensagem("Game Over! Pressione S para Sair ou J para Jogar Novamente", VERMELHO)
    sair = False # Variável para verificar se o jogador deseja sair
    reiniciar = False # Variável para verificar se o jogador deseja reiniciar o jogo

	# Loop que espera uma escolha do jogador 
    while not sair and not reiniciar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: # Se o jogador fechar a janela
                sair = True
            elif evento.type == pygame.KEYDOWN: # Se uma tecla for pressionada
                if evento.key == pygame.K_s: # Tecla"S" para sair
                    sair = True
                elif evento.key == pygame.K_j: # Tecla"J" para reiniciar
                    reiniciar = True
        
    return sair, reiniciar # Retorna as escolhas do jogador

def desenhar_maior_pontuacao(maior_pontuacao: int) -> None:
    """Desenha a maior pontuação na tela."""
    fonte = pygame.font.SysFont("Helvetica", 25)
    texto = fonte.render(f"Maior Pontuação: {maior_pontuacao}", True, AMARELO)
    tela.blit(texto, [LARGURA - texto.get_width() - 10, 1]) # Desenha a maior pontuação no canto superior direito da tela 

def mostrar_mensagem_gameover() -> Tuple[bool, bool]:
    """
    Exibe a mensagem de Game Over e retorna as escolhas do jogador.
    Retorna se o jogador deseja sair ou reiniciar o jogo.
    """
    tela.fill(BRANCO) # Preenche a tela com a cor branca
    mostrar_mensagem("Game Over! Pressione S para Sair ou J para Jogar Novamente", VERMELHO)
    sair = False # Variável para verificar se o jogador deseja sair
    reiniciar = False # Variável para verificar se o jogador deseja reiniciar o jogo

	# Loop que espera uma escolha do jogador 
    while not sair and not reiniciar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: # Se o jogador fechar a janela
                sair = True
            elif evento.type == pygame.KEYDOWN: # Se uma tecla for pressionada
                if evento.key == pygame.K_s: # Tecla"S" para sair
                    sair = True
                elif evento.key == pygame.K_j: # Tecla"J" para reiniciar
                    reiniciar = True
        
    return sair, reiniciar # Retorna as escolhas do jogador

# Função principal que roda o jogo
if __name__ == "__main__":
    rodar_jogo()
