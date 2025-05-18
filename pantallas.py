import pygame
import numpy as np
from universos import posiciones

class SuperMapa():
	def __init__(self, ctx):
		self.pantalla = ctx.pantalla
		self.infomapa = ctx.infomapa
		self.ventana = ctx.ventana
		self.superficie = pygame.Surface((ctx.infomapa.n * ctx.infomapa.ancho_mapa, ctx.infomapa.m * ctx.infomapa.alto_mapa),pygame.SRCALPHA)
		
	def mostrar(self):
		self.pantalla.blit(self.superficie,(self.ventana.x - self.infomapa.ancho_mapa, self.ventana.y - self.infomapa.alto_mapa))
	
class Fondos(SuperMapa):
	def __init__(self, ctx):
		super().__init__(ctx)
		self.juego = ctx.juego
		"""2n+1 = cantidad de mapas a lo ancho
		2m+1 = cantidad de mapas a lo largo"""
		self.crear_fondo()

	# Si cambio el fondo esto se puede optimizar mucho
	def crear_fondo(self):#, color_superior=(0,0,250), color_inferior=(250,0,0)):
		NEGRO = (0, 0, 0)               # Contornos
		BLANCO = (255, 255, 255)
		# --- Cuerpo del atún ---
		escala=1
		superancho = self.infomapa.ancho_mapa
		superalto = self.infomapa.alto_mapa
		surface = pygame.Surface((superancho,superalto))
		ancho = int(superancho*0.7)
		alto = int(superalto*0.5)
		cuerpo_rect = pygame.Rect((superancho-ancho)//2-superancho*0.1, (superalto-alto)//2, ancho, alto)
		pygame.draw.ellipse(surface, BLANCO, cuerpo_rect)  # Cuerpo principal
		colas_width = int(superancho*escala*0.2)
		colas_height = int(superalto*escala*0.15)
		cola1_rect = pygame.Rect(superancho*0.65, superalto//2-alto*0.3, colas_width, colas_height)
		cola2_rect = pygame.Rect(superancho*0.65, superalto//2+alto*0.3-colas_height, colas_width, colas_height)
		pygame.draw.ellipse(surface, BLANCO, cola1_rect)  # Cuerpo principal
		pygame.draw.ellipse(surface, BLANCO, cola2_rect)  # Cuerpo principal
		
		radio = superalto*0.01
		pygame.draw.circle(surface, NEGRO, (superancho//2-ancho//4-superancho*0.1, superalto//2-alto//4), radio)
		pygame.draw.circle(surface, NEGRO, (superancho//2+ancho//4-superancho*0.1, superalto//2-alto//4), radio)
		c=(superancho*0.4, superalto*0.4)
		r=10
		pygame.draw.lines(surface, NEGRO, False, [(int(c[0]+r*np.cos(np.pi*t/10)),int(c[1]+r*np.sin(np.pi*t/10))) for t in range(0,11,2)], width=5)   

		for i in range(0,self.infomapa.n):
			for j in range(0,self.infomapa.m):
				self.superficie.blit(pygame.transform.flip(surface, *self.juego.universo.invertir(i,j)), posiciones(self.infomapa,i,j,0,0))
		# fondo = pygame.Surface((infomapa.ancho_mapa,infomapa.alto_mapa))
		# semi_diagonal = math.sqrt(infomapa.ancho_mapa**2+infomapa.alto_mapa**2)
		# resolucion = 30
		# for _ in range(resolucion):
		#     ratio = _ / resolucion
		#     r = int(color_superior[0] * (1 - ratio) + color_inferior[0] * ratio)
		#     g = int(color_superior[1] * (1 - ratio) + color_inferior[1] * ratio)
		#     b = int(color_superior[2] * (1 - ratio) + color_inferior[2] * ratio)
		#     pygame.draw.circle(fondo, (r, g, b), (infomapa.ancho_mapa//2, infomapa.alto_mapa//2), (1-ratio)*semi_diagonal)
		# for mapas in self.mapas:
		#     for mapa in mapas:
		#         mapa.blit(fondo,(0,0))

	# def mostrar(self):# Tener en cuenta que los indices no se corresponden con lo aparente (-1 -> 2)
	#     for i in range(0,infomapa.n):
	#         for j in range(0,infomapa.m):
	#             pantalla.blit(self.mapas[i][j],(ventana.x+infomapa.ancho_mapa*(i-1),ventana.y+infomapa.alto_mapa*(j-1)))

	# def mostrar(self):# Tener en cuenta que los indices no se corresponden con lo aparente (-1 -> 2)
	#     for i in range(0,infomapa.n):
	#         for j in range(0,infomapa.m):
	#             pantalla.blit(self.mapas[i][j],(ventana.x+infomapa.ancho_mapa*(i-1),ventana.y+infomapa.alto_mapa*(j-1)))
