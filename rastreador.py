import pygame
import serial
import math
import sys

# --- CONFIGURAÇÕES ---
PORTA_COM = 'COM3'
RAIO_MAXIMO_CM = 40 
LARGURA_TELA = 800
ALTURA_TELA = 400

try:
    arduino = serial.Serial(PORTA_COM, 9600, timeout=0.05)
except:
    print(f"Erro: Conecte o Arduino ou mude a porta {PORTA_COM}")
    sys.exit()

pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Radar Ultrassônico")
fonte = pygame.font.SysFont("consolas", 20, bold=True)

x_centro = LARGURA_TELA // 2
y_centro = ALTURA_TELA

# Lista para guardar: [angulo, distancia, opacidade, cor_rgb]
pontos_detectados = []

angulo_atual = 0
distancia_atual = 0
cor_alerta_atual = (0, 255, 0) # Começa verde

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 1. LÊ OS DADOS DA SERIAL
    try:
        if arduino.in_waiting > 0:
            linha = arduino.readline().decode('utf-8').strip()
            if "," in linha:
                ang_str, dist_str = linha.split(",")
                angulo_atual = int(ang_str)
                distancia_atual = int(dist_str)
                
                # Só registra se for uma distância real
                if 2 < distancia_atual < RAIO_MAXIMO_CM:
                    # LÓGICA DE CORES
                    if distancia_atual > 30:
                        cor_alvo = (0, 255, 0)    # Verde
                    elif distancia_atual > 15:
                        cor_alvo = (255, 255, 0)  # Amarelo
                    else:
                        cor_alvo = (255, 0, 0)    # Vermelho
                        
                    cor_alerta_atual = cor_alvo # Atualiza a cor dos textos
                    pontos_detectados.append([angulo_atual, distancia_atual, 255, cor_alvo])
                else:
                    cor_alerta_atual = (0, 255, 0) # Se não tem nada perto, fica verde
    except:
        pass

    # 2. DESENHA O FUNDO E O GRID
    tela.fill((10, 15, 10)) # Fundo escuro
    for raio in range(100, LARGURA_TELA // 2, 100):
        pygame.draw.arc(tela, (0, 80, 0), (x_centro - raio, y_centro - raio, raio*2, raio*2), 0, math.pi, 1)

    # 3. A LINHA DE VARREDURA
    rad_linha = math.radians(180 - angulo_atual)
    x_linha = x_centro + int(math.cos(rad_linha) * (LARGURA_TELA // 2))
    y_linha = y_centro - int(math.sin(rad_linha) * (LARGURA_TELA // 2))
    pygame.draw.line(tela, (0, 200, 0), (x_centro, y_centro), (x_linha, y_linha), 3)

    # 4. DESENHA OS PONTOS (ALVOS)
    for p in pontos_detectados[:]:
        ang_p, dist_p, opacidade, cor_p = p
        
        raio_pixel = (dist_p / RAIO_MAXIMO_CM) * (LARGURA_TELA // 2)
        rad_p = math.radians(180 - ang_p)
        x_p = x_centro + int(math.cos(rad_p) * raio_pixel)
        y_p = y_centro - int(math.sin(rad_p) * raio_pixel)
        
        # Efeito de brilho que vai apagando (Fade out)
        fator_fade = opacidade / 255.0
        cor_fade = (int(cor_p[0] * fator_fade), int(cor_p[1] * fator_fade), int(cor_p[2] * fator_fade))
        
        pygame.draw.circle(tela, cor_fade, (x_p, y_p), 8)
        
        # O ponto vai sumindo com o tempo
        p[2] -= 4 
        if p[2] <= 0:
            pontos_detectados.remove(p)

    # 5. TEXTO DINÂMICO (Muda de cor conforme o perigo)
    texto_ang = fonte.render(f"ANGULO: {angulo_atual} graus", True, (0, 255, 0))
    texto_dist = fonte.render(f"ALVO MAIS PROXIMO: {distancia_atual} cm", True, cor_alerta_atual)
    tela.blit(texto_ang, (10, 10))
    tela.blit(texto_dist, (10, 40))

    pygame.display.flip()
    clock.tick(60)