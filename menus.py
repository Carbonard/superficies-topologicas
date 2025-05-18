from dibujos import dibujar_toro_animado, dibujar_botella_klein_con_lineas, dibujar_plano_proyectivo_animado
from universos import *
import pygame

class Menu:
	def __init__(self, ctx, opciones):
		self.pantalla = ctx.pantalla
		self.ventana = ctx.ventana
		self.juego = ctx.juego
		
		self.ancho = self.ventana.ancho*2//3
		self.alto = self.ventana.alto*2//3
		self.x = self.ventana.ancho//6
		self.y = self.ventana.alto//6
		self.margen_izquierdo = self.ancho//10
		self.margen_superior = self.alto//10

		self.tamaño_fuente = 25
		self.color_fuente = (250,250,250)
		self.color_fuente_resaltado = (0,200,250)
		self.color_fuente_clicado = (0,100,150)
		self.fuente = pygame.font.SysFont('Arial', self.tamaño_fuente)

		# self.opciones = opciones
		self.opciones = []
		for i, (op,texto) in enumerate(opciones):
			opcion = self.crear_opcion(i,op,texto)
			self.opciones.append(opcion)

		self.opcion_clicada = None

	def crear_opcion(self,i,op,texto):
		opcion = {"juego": op,
				 "texto": self.fuente.render(texto, True, self.color_fuente),
				 "texto resaltado": self.fuente.render(texto, True, self.color_fuente_resaltado),
				 "texto clicado": self.fuente.render(texto, True, self.color_fuente_clicado),
				 "caja": None}
		opcion["caja"] = opcion["texto"].get_rect(topleft = (self.x + self.margen_izquierdo,
															 self.y + self.margen_superior + i*self.tamaño_fuente*1.5))
		return opcion

	def ajustar_tamaño(self):

		self.ancho = self.ventana.ancho*2//3
		self.alto = self.ventana.alto*2//3
		self.x = self.ventana.ancho//6
		self.y = self.ventana.alto//6
		self.margen_izquierdo = self.ancho//10
		self.margen_superior = self.alto//10

		self.superficie = pygame.Surface((self.ancho, self.alto))
		for i, opcion in enumerate(self.opciones):
			opcion["caja"] = opcion["texto"].get_rect(topleft = (self.x + self.margen_izquierdo,
																 self.y + self.margen_superior + i*self.tamaño_fuente*1.5))
	
	def desplegar(self):

		self.ajustar_tamaño()
		self.pantalla.fill((0,0,0))
		self.superficie.fill((20,20,20))

		for i,opcion in enumerate(self.opciones):
			if opcion["caja"].collidepoint(pygame.mouse.get_pos()):
				if self.juego.raton_clicado:
					self.opcion_clicada = i
					self.superficie.blit(opcion["texto clicado"],(self.margen_izquierdo,
																  self.margen_superior + i*self.tamaño_fuente*1.5))
				else:
					self.superficie.blit(opcion["texto resaltado"],(self.margen_izquierdo,
																	self.margen_superior + i*self.tamaño_fuente*1.5))
				if self.opcion_clicada==i and not self.juego.raton_clicado:
					self.juego.estado_de_juego = opcion["juego"]
					self.pulsar_boton(opcion)
				self.ilustrar_opcion_destacada(opcion)
			else:
				self.superficie.blit(opcion["texto"],(self.margen_izquierdo,
													  self.margen_superior + i*self.tamaño_fuente*1.5))
		if not self.juego.raton_clicado:
			self.opcion_clicada=None

		self.pantalla.blit(self.superficie,(self.x,self.y))
	
	def ilustrar_opcion_destacada(self, opcion):
		pass
	def pulsar_boton(self, opcion):
		pass

	def agregar_opciones(self,opciones: list):
		self.opciones.append(opciones)

class MenuInicio(Menu):
	def __init__(self, ctx, opciones):
		super().__init__(ctx, opciones)
	
	def pulsar_boton(self, opcion):
		self.juego.jugador.reset()
		self.juego.celda_visible_i=1
		self.juego.celda_visible_j=1
		self.ventana.actualizar_posicion()

class MenuMapas(Menu):
	def __init__(self, ctx):
		self.fondo = ctx.fondo
		self.infomapa = ctx.infomapa
		super().__init__(ctx, [("menu inicial", "Mundo Toroidal"),
						  ("menu inicial", "Botella de Klein"),
						  ("menu inicial", "Plano Proyectivo")])
		self.opciones[0]["universo"] = "toro"
		self.opciones[1]["universo"] = "Klein"
		self.opciones[2]["universo"] = "proyectivo"
	
	def ilustrar_opcion_destacada(self, opcion):
		if opcion["universo"]=="toro": dibujar_toro_animado(self.superficie)
		elif opcion["universo"]=="Klein": dibujar_botella_klein_con_lineas(self.superficie)
		elif opcion["universo"]=="proyectivo": dibujar_plano_proyectivo_animado(self.superficie)
		
	def pulsar_boton(self, opcion):
		if opcion["universo"]=="toro": self.juego.universo=UniversoToroidal(self.infomapa)
		if opcion["universo"]=="Klein": self.juego.universo=UniversoKlein(self.infomapa)
		if opcion["universo"]=="proyectivo": self.juego.universo=UniversoProyectivo(self.infomapa)
		
		self.fondo.crear_fondo()

class MenuConfig(Menu):
	def __init__(self, ctx):
		super().__init__(ctx, [("configuracion", "Cambiar a cámara fija" if ctx.juego.camara_subjetiva else "Cambiar a cámara subjetiva"),
						  ("menu inicial", "Volver a menú")])
		self.opciones[0]["nombre"] = "camara"
		self.opciones[1]["nombre"] = "volver"
	
	def pulsar_boton(self, opcion):
		if opcion["nombre"] == "camara":
			self.juego.camara_subjetiva = not self.juego.camara_subjetiva
			self.opciones[0] = self.crear_opcion(0, opcion["juego"], "Cambiar a cámara fija" if self.juego.camara_subjetiva else "Cambiar a cámara subjetiva")
			self.opciones[0]["nombre"] = "camara"