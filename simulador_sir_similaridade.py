import pygame
import numpy as np
import random
import sys

# =====================================================================
# CONFIGURAÇÕES DO SIMULADOR E DA GRADE ESPACIAL
# =====================================================================
GRID_SIZE = 120       # Tamanho da matriz (120x120 células)
CELL_SIZE = 6         # Tamanho em pixels de cada célula
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 15              # Velocidade de evolução do autômato (frames por segundo)

# Paleta de Cores (R, G, B)
COLOR_BG = (20, 20, 20)           # Fundo escuro (bordas)
COLOR_S = (220, 220, 220)         # Suscetível (Cinza/Branco)
COLOR_I = (255, 50, 50)           # Infectado (Vermelho - Influenza ativa)
COLOR_R = (50, 150, 255)          # Recuperado (Azul - Imune)

# Constantes de Estado do Modelo SIR
S = 0
I = 1
R = 2

# =====================================================================
# PARÂMETROS EPIDEMIOLÓGICOS DO MODELO DA INFLUENZA
# =====================================================================
BETA = 0.25   # Probabilidade de transmissão (contágio) por contato validado
GAMMA = 0.08  # Probabilidade de recuperação (saída do compartimento I para R)
I0 = 3        # Pacientes zero (focos de infecção iniciais)

# =====================================================================
# FUNÇÕES DO AUTÔMATO CELULAR
# =====================================================================

def init_grid():
    """
    Inicializa o espaço bidimensional. 
    A população começa totalmente Suscetível, com I0 pacientes Infectados distribuídos aleatoriamente.
    """
    grid = np.full((GRID_SIZE, GRID_SIZE), S, dtype=int)
    
    # Inserção estocástica dos casos iniciais
    for _ in range(I0):
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        grid[x, y] = I
        
    return grid

def calcular_dimensao_similaridade(grid, x, y):
    """
    Calcula a influência da vizinhança de Moore (8 vizinhos).
    Retorna o número de vizinhos que possuem o estado Infectado (I).
    """
    contagem_infectados = 0
    
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue # Ignora a própria célula central
            
            nx, ny = x + dx, y + dy
            
            # Garante que a verificação não ultrapasse os limites da matriz espacial
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[nx, ny] == I:
                    contagem_infectados += 1
                    
    return contagem_infectados

def update_grid(grid_atual):
    """
    Varre a matriz aplicando as equações diferenciais/probabilísticas do modelo SIR,
    retornando a grade espacial para o instante t+1.
    """
    # Cria uma cópia para garantir que a atualização seja síncrona (celulas evoluem juntas)
    nova_grid = grid_atual.copy()
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            estado_atual = grid_atual[x, y]
            
            # --- REGRA 1: Transição S -> I (Baseado na Similaridade Local) ---
            if estado_atual == S:
                ni = calcular_dimensao_similaridade(grid_atual, x, y)
                if ni > 0:
                    # Aplicação da probabilidade cumulativa de infecção
                    prob_infeccao = 1 - (1 - BETA) ** ni
                    if random.random() < prob_infeccao:
                        nova_grid[x, y] = I
                        
            # --- REGRA 2: Transição I -> R (Recuperação Espontânea) ---
            elif estado_atual == I:
                if random.random() < GAMMA:
                    nova_grid[x, y] = R
                    
            # O estado R é terminal neste modelo (imunidade mantida), não há regras.
                    
    return nova_grid

def desenhar_graficos(screen, grid):
    """
    Renderiza o estado matemático da matriz como pixels visuais na interface Pygame.
    """
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            estado = grid[x, y]
            
            if estado == S:
                cor = COLOR_S
            elif estado == I:
                cor = COLOR_I
            elif estado == R:
                cor = COLOR_R
            else:
                cor = COLOR_BG
                
            pygame.draw.rect(
                screen, 
                cor, 
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

# =====================================================================
# LOOP PRINCIPAL DA SIMULAÇÃO (MOTOR GRÁFICO)
# =====================================================================

def executar_simulador():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Autômato Celular: Modelo SIR Espacial (Influenza)")
    clock = pygame.time.Clock()
    
    grid = init_grid()
    rodando = True
    pausado = False

    while rodando:
        # 1. Processamento de Eventos (Teclado/Mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pausado = not pausado # Pausa para observar clusters e frentes de onda
                if event.key == pygame.K_r:
                    grid = init_grid()    # Reinicia a dinâmica do zero
                if event.key == pygame.K_ESCAPE:
                    rodando = False

        # 2. Atualização Matemática
        if not pausado:
            grid = update_grid(grid)
            
        # 3. Renderização Visual
        screen.fill(COLOR_BG)
        desenhar_graficos(screen, grid)
        pygame.display.flip()
        
        # 4. Controle temporal (FPS)
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    executar_simulador()