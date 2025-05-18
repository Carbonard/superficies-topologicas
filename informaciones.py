class Contexto():
	def __init__(self):
		self.infomapa = None
		self.juego = None
		self.super_mapa = None
		self.fondo = None
		self.ventana = None
		self.pantalla = None

class InformacionMapa():
	# Para guardar información relativa al tipo de partida
	def __init__(self, ancho, alto, n, m):
		self.ancho_mapa = ancho
		self.alto_mapa = alto
		
		self.n = n # n filas de celdas
		self.m = m # m columnas de celdas


class InformacionJuego():
	# Para guardar información relativa al tipo de partida
	def __init__(self):

		self.jugador = None
		self.estado_de_juego = "menu inicial"
		self.camara_subjetiva = True
		self.celda_visible_i=1
		self.celda_visible_j=1

		self.activo = True
		self.raton_clicado = False
		self.universo=None

class InformacionVentana():
	# Para guardar la información relativa a la ventana.
	def __init__(self, ctx):
		self.pantalla = ctx.pantalla
		self.infomapa = ctx.infomapa
		self.juego = ctx.juego
		self.actualizar_posicion()

	def actualizar_posicion(self):
		self.ancho, self.alto = self.pantalla.get_size()
		self.x = (self.ancho-self.infomapa.ancho_mapa)//2
		self.y = (self.alto-self.infomapa.alto_mapa)//2
		if self.juego.estado_de_juego == "jugando" and self.juego.camara_subjetiva:
			self.x -= (self.juego.jugador.x_visible - self.infomapa.ancho_mapa//2)
			self.y -= (self.juego.jugador.y_visible - self.infomapa.alto_mapa//2)

