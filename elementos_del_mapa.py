from dibujos import dibujar_robot
import pygame

class Objeto:
	def __init__(self, ctx, nombre="Objeto", x=0, y=0, ancho=0, alto=0, img=None, visible=False, color = (250,0,0)):
		self.super_mapa = ctx.super_mapa
		self.infomapa = ctx.infomapa
		self.juego = ctx.juego
		self.nombre=nombre
		self.x=x
		self.y=y
		self.ancho = ancho
		self.alto = alto
		self.invertido = (False,False)
		self.imagen = img
		# if img != None:
		#     self.imagen = imagen(img,ancho,alto)
		# else:
		#     self.imagen = dibujar_robot((ancho+alto)//2)
		self.visible=visible
		self.color = color

	def posicionar(self,x,y):# Para que la posición represente el centro del objeto
		return (x-self.ancho//2, y-self.alto//2)

	def mostrar_individual(self,x,y,invertir_x=False, invertir_y=False):
	# Los parametros hacen referencia a la posición en el supermapa y a si se tiene que invertir en la celda correspondiente
		if self.visible:
			if self.imagen!=None:
				# Si el personaje está invertido en la celda principal, invertir en la celda correspondiente
				if self.invertido[0]: invertir_x = not invertir_x
				if self.invertido[1]: invertir_y = not invertir_y
				self.super_mapa.superficie.blit(pygame.transform.flip(self.imagen,invertir_x,invertir_y),self.posicionar(x,y))
			else:
				pygame.draw.rect(
					self.super_mapa.superficie,
					self.color,
					(*self.posicionar(x,y),
					 self.ancho, self.alto
					))

	def mostrar(self):
		for i in range(0,self.infomapa.n):
			for j in range(0,self.infomapa.m):
				self.mostrar_individual(*self.juego.universo.posiciones(i,j,self.x,self.y),*self.juego.universo.invertir(i,j))

paredes = []

class ParedHorizontal(Objeto):
	def __init__(self, ctx, x1, x2, y, grosor=5, color = (250,0,0)):
		"""x1 < x2"""
		self.x1 = x1
		self.x2 = x2
		self.grosor = grosor
		super().__init__(ctx,
				   		nombre="Pared " + str(len(paredes)),
						x=(x1+x2)/2,
						y=y,
						ancho=x2-x1,
						alto=2*grosor,
						img=None,
						visible=True,
						color = color)
		paredes.append(self)

class ParedVertical(Objeto):
	def __init__(self, ctx, x, y1, y2, grosor=5, color = (250,0,0)):
		"""x1 < x2"""
		self.y1 = y1
		self.y2 = y2
		self.grosor = grosor
		super().__init__(ctx,
				   		nombre="Pared " + str(len(paredes)),
						x=x,
						y=(y2+y1)/2,
						alto=y2-y1,
						ancho=2*grosor,
						img=None,
						visible=True,
						color = color)
		paredes.append(self)

obstaculos = []

def calcular_obstaculos(juego):
	obstaculos.clear()
	for pared in paredes:
		obstaculos.append(pygame.Rect(*pared.posicionar(pared.x,pared.y),pared.ancho, pared.alto))
		if pared.y - pared.alto/2 < juego.jugador.alto:
			nx, ny, _ = pared.juego.universo.salir_por_arriba(pared.x,pared.y, (True,True))
			obstaculos.append(pygame.Rect(*pared.posicionar(nx,ny),pared.ancho, pared.alto))
		if pared.y + pared.alto/2 > pared.infomapa.alto_mapa - juego.jugador.alto:
			nx, ny, _ = pared.juego.universo.salir_por_abajo(pared.x,pared.y, (True,True))
			obstaculos.append(pygame.Rect(*pared.posicionar(nx,ny),pared.ancho, pared.alto))
		if pared.x - pared.ancho/2 < juego.jugador.ancho:
			nx, ny, _ = pared.juego.universo.salir_por_izquierda(pared.x,pared.y, (True,True))
			obstaculos.append(pygame.Rect(*pared.posicionar(nx,ny),pared.ancho, pared.alto))
		if pared.x + pared.ancho/2 > pared.infomapa.ancho_mapa - juego.jugador.alto:
			nx, ny, _ = pared.juego.universo.salir_por_derecha(pared.x,pared.y, (True,True))
			obstaculos.append(pygame.Rect(*pared.posicionar(nx,ny),pared.ancho, pared.alto))


# # -------------------------------------------------- OBJETO RANDOM --------------------------------------------------
# class ObjetoRandom(Objeto):
#     def __init__(self, nombre="", x=False, y=False, ancho=0, alto=0, img=None, visible=False, colisionables=[]):
#         if not x:
#             x=random()*(infomapa.ancho_mapa-ancho)
#         if not y:
#             y=random()*(infomapa.alto_mapa-alto)
#         super().__init__(nombre, x, y, ancho, alto, img, visible)
#         self.colisionables = colisionables

#     def aparecer(self):
#         while any(self.colisiona_con(colisionable) for colisionable in self.colisionables):
#             self.x=random()*(infomapa.ancho_mapa-self.ancho)
#             self.y=random()*(infomapa.alto_mapa-self.alto)
#         self.visible=True
	
#     def desaparecer(self):
#         self.visible=False

# -------------------------------------------------- MOVIL --------------------------------------------------
class Movil(Objeto):
	def __init__(self, ctx, nombre="", x=0, y=0, ancho=0, alto=0, img=None, visible=False, velocidad=10):
		super().__init__(ctx, nombre, x, y, ancho, alto, img, visible)
		self.velocidad = velocidad

	def mover(self,direccion):
		# Moverse según si está invertido o no
		if self.invertido[0]:
			self.x -= direccion[0]*self.velocidad
		else:
			self.x += direccion[0]*self.velocidad
		if self.invertido[1]:
			self.y -= direccion[1]*self.velocidad
		else:
			self.y += direccion[1]*self.velocidad
		# Comprobar si se sale del mapa principal
		if self.x<0:
			self.x , self.y, self.invertido = self.juego.universo.salir_por_izquierda(self.x, self.y, self.invertido)
		if self.x>self.infomapa.ancho_mapa:
			self.x , self.y, self.invertido = self.juego.universo.salir_por_derecha(self.x, self.y, self.invertido)
		if self.y>self.infomapa.alto_mapa:
			self.x , self.y, self.invertido = self.juego.universo.salir_por_abajo(self.x, self.y, self.invertido)
		if self.y<0:
			self.x , self.y, self.invertido = self.juego.universo.salir_por_arriba(self.x, self.y, self.invertido)

# # -------------------------------------------------- PERSONAJE --------------------------------------------------

class Jugador(Movil):
	def __init__(self, ctx, nombre="", x=0, y=0, ancho=0, alto=0, img=None, visible=True, velocidad=10):
		super().__init__(ctx, nombre, x, y, ancho, alto, dibujar_robot((ancho+alto)//2), visible, velocidad)
		self.ventana = ctx.ventana
		self.x_visible = self.x
		self.y_visible = self.y
		self.original = (x,y,velocidad)
	
	def reset(self):
		self.x, self.y, self.velocidad = self.original
		self.x_visible = self.x
		self.y_visible = self.y
		self.invertido = (False, False)
	
	def calcular_nuevas_coordenadas(self, direccion):
		# Moverse según si está invertido o no
		if self.invertido[0]:
			x = self.x - direccion[0]*self.velocidad
		else:
			x = self.x + direccion[0]*self.velocidad
		if self.invertido[1]:
			y = self.y - direccion[1]*self.velocidad
		else:
			y = self.y + direccion[1]*self.velocidad

		invertido = self.invertido

		if x<0:
			x , y, invertido = self.juego.universo.salir_por_izquierda(x, y, self.invertido)
		if x>self.infomapa.ancho_mapa:
			x , y, invertido = self.juego.universo.salir_por_derecha(x, y, self.invertido)
		if y>self.infomapa.alto_mapa:
			x , y, invertido = self.juego.universo.salir_por_abajo(x, y, self.invertido)
		if y<0:
			x , y, invertido = self.juego.universo.salir_por_arriba(x, y, self.invertido)
		return x, y, invertido

	def puede_moverse(self, x, y):
		# print(pygame.Rect(*self.posicionar(x,y),self.ancho,self.alto).collidelist(obstaculos))
		return -1 == pygame.Rect(*self.posicionar(x,y),self.ancho,self.alto).collidelist(obstaculos)
	
	def mover(self, direccion, choque=False):
		# # Moverse según si está invertido o no
		# if self.invertido[0]:
		# 	self.nueva_x = self.x - direccion[0]*self.velocidad
		# else:
		# 	self.nueva_x = self.x + direccion[0]*self.velocidad
		# if self.invertido[1]:
		# 	self.nueva_y = self.y - direccion[1]*self.velocidad
		# else:
		# 	self.nueva_y = self.y + direccion[1]*self.velocidad
		x, y, invertido = self.calcular_nuevas_coordenadas(direccion)

		if self.puede_moverse(x, y):
			self.x = x
			self.y = y
			self.invertido = invertido
			
			self.x_visible = (self.x_visible + direccion[0]*self.velocidad)%(2*self.infomapa.ancho_mapa)

			self.y_visible = (self.y_visible + direccion[1]*self.velocidad)%(2*self.infomapa.alto_mapa)

			# if self.x<0:
			# 	self.x , self.y, self.invertido = self.juego.universo.salir_por_izquierda(self.x, self.y, self.invertido)
			# 	self.x_visible %= 2*self.infomapa.ancho_mapa
			# if self.x>self.infomapa.ancho_mapa:
			# 	self.x , self.y, self.invertido = self.juego.universo.salir_por_derecha(self.x, self.y, self.invertido)
			# 	self.x_visible %= 2*self.infomapa.ancho_mapa
			# if self.y>self.infomapa.alto_mapa:
			# 	self.x , self.y, self.invertido = self.juego.universo.salir_por_abajo(self.x, self.y, self.invertido)
			# 	self.y_visible %= 2*self.infomapa.alto_mapa
			# if self.y<0:
			# 	self.x , self.y, self.invertido = self.juego.universo.salir_por_arriba(self.x, self.y, self.invertido)
			# 	self.y_visible %= 2*self.infomapa.alto_mapa
			if self.juego.camara_subjetiva:
				self.ventana.actualizar_posicion()
			return True
		else:
			if not choque: # Para que no se quede a cierta distancia de la pared
				print("No puede :(", self.x, self.y)
				dir = (direccion[0]/self.velocidad, direccion[1]/self.velocidad)
				while self.mover(dir, choque = True):
					pass
			return False
			


# class Personaje(Movil):
	
#     def __init__(self, nombre="", x=0, y=0, ancho=0, alto=0, img=None, visible=False, velocidad=5, img_mov=None):
#         super().__init__(nombre, x, y, ancho, alto, img, visible)
#         self.imagen = imagen(img, ancho, alto)
#         self.imagen_normal = imagen(img, ancho, alto)
#         self.imagen_movimiento = imagen(img_mov, ancho, alto)
#         self.contador_keys_mov = 0

#     def manejar_eventos(self,evento):
#         if evento.type == pygame.KEYDOWN:
#             if evento.key in (pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN):
#                 self.cambiar_imagen(self.imagen_movimiento)
#                 self.contador_keys_mov +=1
#         if evento.type == pygame.KEYUP:
#             if evento.key in (pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN):
#                 self.contador_keys_mov -= 1
#                 if self.contador_keys_mov == 0:
#                     self.cambiar_imagen(self.imagen_normal)
	
#     def cambiar_imagen(self, img):
#         self.imagen = img