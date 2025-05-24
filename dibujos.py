import pygame
import math
import numpy as np

def dibujar_toro_animado(surface: pygame.SurfaceType):
	# Parámetros ajustados para que quepa bien
	R, r = 3.0, 1.0  # Radios normalizados
	escala = surface.get_width()*2//3 * 0.1      # Factor de escala
	ancho = surface.get_width()
	alto = surface.get_height()
	tiempo=pygame.time.get_ticks()*0.0005
	for theta in np.linspace(0, 2*np.pi, 30):
		for phi in np.linspace(0, 2*np.pi, 20):
			# Coordenadas 3D con rotación
			x = (R + r * math.cos(phi)) * math.cos(theta)
			y = (R + r * math.cos(phi)) * math.sin(theta)
			z = r * math.sin(phi)
			
			# Rotación en 3D (animada con el tiempo)
			y_rot = y * math.cos(tiempo) - z * math.sin(tiempo)
			z_rot = y * math.sin(tiempo) + z * math.cos(tiempo)
			
			# Proyección isométrica ajustada
			px = ancho//2 + (x - y_rot) * escala
			py = alto//2 + (x + y_rot - z_rot) * escala/2
			
			# Tamaño variable para efecto de profundidad
			radio = max(1, 3 - z_rot * 0.5)
			pygame.draw.circle(surface, (200,0,0), (int(px), int(py)), int(radio))

def dibujar_botella_klein_con_lineas(surface):
	escala = surface.get_height()*2//3 * 0.05
	desplazamiento = (surface.get_width()//2, surface.get_height()//2)
	rotacion = pygame.time.get_ticks() * 0.0005
	
	# Generar malla de puntos
	puntos = []
	for u in np.linspace(0, 2*np.pi, 40):
		fila = []
		for v in np.linspace(0, 2*np.pi, 20):
			r = 4 * (1 - math.cos(u)/2)
			
			if u < np.pi:
				x = 6 * math.cos(u) * (1 + math.sin(u)) + r * math.cos(u) * math.cos(v)
				y = 16 * math.sin(u) + r * math.sin(u) * math.cos(v)
				z = r * math.sin(v)
			else:
				x = 6 * math.cos(u) * (1 + math.sin(u)) - r * math.cos(v)
				y = 16 * math.sin(u)
				z = r * math.sin(v)
			
			# Rotación 3D
			y_rot = y * math.cos(rotacion) - z * math.sin(rotacion)
			z_rot = y * math.sin(rotacion) + z * math.cos(rotacion)
			
			px = desplazamiento[0] + (x - y_rot) * escala * 0.7
			py = desplazamiento[1] + (x + y_rot) * escala * 0.4 - z_rot * escala * 0.5
			
			fila.append((px, py, z_rot))
		puntos.append(fila)
	
	# Dibujar líneas horizontales
	for i in range(len(puntos)):
		for j in range(len(puntos[i])-1):
			z_avg = (puntos[i][j][2] + puntos[i][j+1][2]) / 2
			intensidad = 0#max(0, min(255, int(255 * (1 - z_avg/20))))#int(255 * (1 - z_avg/20))
			pygame.draw.line(surface, (intensidad, 255, intensidad), 
						   (puntos[i][j][0], puntos[i][j][1]),
						   (puntos[i][j+1][0], puntos[i][j+1][1]), 1)
	
	# Dibujar líneas verticales
	for i in range(len(puntos)-1):
		for j in range(len(puntos[i])):
			z_avg = (puntos[i][j][2] + puntos[i+1][j][2]) / 2
			intensidad = 0#max(0, min(255, int(255 * (1 - z_avg/20))))
			pygame.draw.line(surface, (intensidad, 255, intensidad),
						   (puntos[i][j][0], puntos[i][j][1]),
						   (puntos[i+1][j][0], puntos[i+1][j][1]), 1)
			
def dibujar_plano_proyectivo_animado(surface):
	escala = surface.get_height()*2//3 * 0.1  # Ajustado para visualización óptima
	ancho = surface.get_width()
	alto = surface.get_height()
	tiempo=pygame.time.get_ticks()*0.001
	for u in np.linspace(0, np.pi, 25):  # Menos puntos para mejor rendimiento
		for v in np.linspace(0, np.pi, 25):
			# Ecuaciones paramétricas optimizadas
			denom = max(0.1, (math.sin(u)**2 + math.cos(v)**2))  # Evitar división por cero
			x = math.sqrt(2) * math.cos(u) * math.cos(v) / denom
			y = math.sqrt(2) * math.cos(u) * math.sin(v) / denom
			z = math.sqrt(2) * math.sin(u) * math.cos(v) / denom
			
			# Rotación 3D
			y_rot = y * math.cos(tiempo*0.7) - z * math.sin(tiempo*0.7)
			z_rot = y * math.sin(tiempo*0.7) + z * math.cos(tiempo*0.7)
			
			# Proyección ajustada al centro de la pantalla
			px = ancho//2 + (x - y_rot) * escala
			py = alto//2 + (x + y_rot - z_rot*0.5) * escala * 0.6
			
			# Color con efecto de profundidad
			profundidad = (z_rot + 1.5) / 3.0  # Normalizado [0,1]
			azul = int(100 + 155 * profundidad)
			verde = int(200 - 100 * profundidad)
			color = (100, 0, 200)
			
			# if 0 <= px < juego.ancho_mapa and 0 <= py < juego.alto_mapa:  # Solo dibujar puntos visibles
			pygame.draw.circle(surface, color, (int(px), int(py)), 2)

def dibujar_robot(tamaño):
    superficie = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
    
    # Cuerpo (cuadrado principal)
    pygame.draw.rect(superficie, (100, 200, 100), (0, 0, tamaño, tamaño), border_radius=5)
    
    # Ojos (puntos brillantes)
    pygame.draw.circle(superficie, (255, 255, 0), (tamaño//3, tamaño//3), 4)
    pygame.draw.circle(superficie, (255, 255, 0), (2*tamaño//3, tamaño//3), 4)
    
    # Boca (línea con efecto "píxel art")
    for x in range(tamaño//4, 3*tamaño//4, 5):
        pygame.draw.line(superficie, (255, 50, 50), (x, 2*tamaño//3), (x+3, 2*tamaño//3), 3)
    
    return superficie