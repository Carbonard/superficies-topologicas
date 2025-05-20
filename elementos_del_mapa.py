from dibujos import dibujar_robot
import pygame

class Objeto:
	def __init__(self, infomapa, juego, super_mapa, nombre="Objeto", x=0, y=0, ancho=0, alto=0, img=None, visible=False):
		self.super_mapa = super_mapa
		self.infomapa = infomapa
		self.juego = juego
		self.nombre=nombre
		self.x=x
		self.y=y
		self.ancho = ancho
		self.alto = alto
		self.invertido = (False,False)
		self.imagen = dibujar_robot((ancho+alto)//2)
		# if img != None:
		#     self.imagen = imagen(img,ancho,alto)
		# else:
		#     self.imagen = dibujar_robot((ancho+alto)//2)
		self.visible=visible

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
					pygame.transform.flip(self.super_mapa.superficie,invertir_x,invertir_y),
					(250,250,250),
					(*self.posicionar(x,y),
					 self.ancho, self.alto
					))

	def mostrar(self):
		for i in range(0,self.infomapa.n):
			for j in range(0,self.infomapa.m):
				self.mostrar_individual(*self.juego.universo.posiciones(i,j,self.x,self.y),*self.juego.universo.invertir(i,j))

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
	def __init__(self, infomapa, juego, super_mapa, nombre="", x=0, y=0, ancho=0, alto=0, img=None, visible=False, velocidad=10):
		super().__init__(infomapa, juego, super_mapa, nombre, x, y, ancho, alto, img, visible)
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
	def __init__(self, ventana, infomapa, juego, super_mapa, nombre="", x=0, y=0, ancho=0, alto=0, img=None, visible=True, velocidad=10):
		super().__init__(infomapa, juego, super_mapa, nombre, x, y, ancho, alto, img, visible, velocidad)
		self.ventana = ventana
		self.x_visible = self.x
		self.y_visible = self.y
		self.original = (x,y,velocidad)
	
	def reset(self):
		self.x, self.y, self.velocidad = self.original
		self.x_visible = self.x
		self.y_visible = self.y
		self.invertido = (False, False)

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
			
		self.x_visible += direccion[0]*self.velocidad

		self.y_visible += direccion[1]*self.velocidad
		# if juego.camara_subjetiva:
		#     if self.invertido[0]:
		#         ventana.x += direccion[0]*self.velocidad
		#     else:
		#         ventana.x -= direccion[0]*self.velocidad
		#     if self.invertido[1]:
		#         ventana.y += direccion[1]*self.velocidad
		#     else:
		#         ventana.y -= direccion[1]*self.velocidad
		# Comprobar si se sale del mapa principal
		if self.x<0:
			self.x , self.y, self.invertido = self.juego.universo.salir_por_izquierda(self.x, self.y, self.invertido)
			self.x_visible %= 2*self.infomapa.ancho_mapa
		if self.x>self.infomapa.ancho_mapa:
			self.x , self.y, self.invertido = self.juego.universo.salir_por_derecha(self.x, self.y, self.invertido)
			self.x_visible %= 2*self.infomapa.ancho_mapa
		if self.y>self.infomapa.alto_mapa:
			self.x , self.y, self.invertido = self.juego.universo.salir_por_abajo(self.x, self.y, self.invertido)
			self.y_visible %= 2*self.infomapa.alto_mapa
		if self.y<0:
			self.x , self.y, self.invertido = self.juego.universo.salir_por_arriba(self.x, self.y, self.invertido)
			self.y_visible %= 2*self.infomapa.alto_mapa
		if self.juego.camara_subjetiva:
			self.ventana.actualizar_posicion()


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