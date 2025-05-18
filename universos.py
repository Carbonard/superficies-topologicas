def posiciones(infomapa,i,j,x,y): # (i,j)*juego.(ancho,alto)_mapa marca la esquina (superior izquierda) de la celda correspondiente
		# Para posicionar los fondos.
		return (i*infomapa.ancho_mapa + x,
				j*infomapa.alto_mapa + y)

class UniversoToroidal():
	def __init__(self, infomapa):
		self.infomapa = infomapa
	
	def posiciones(self,i,j,x,y): # (i,j)*juego.(ancho,alto)_mapa marca la esquina (superior izquierda) de la celda correspondiente
		# Para dibujar múltiples copias en cada celda del supermapa
		return (i*self.infomapa.ancho_mapa + x,
				j*self.infomapa.alto_mapa + y)

	def invertir(self,i,j):
		# Saber si la respectiva celda del supermapa está invertida en eje X o eje Y
		return False, False
		
	# Cuando un personaje sale por un lado del mapa, inv es si el paeronaje está invertido en algún eje o no.
	def salir_por_izquierda(self,x,y,inv):
		return x+self.infomapa.ancho_mapa, y, inv
	def salir_por_derecha(self,x,y,inv):
		return x-self.infomapa.ancho_mapa, y, inv
	def salir_por_arriba(self,x,y,inv):
		return x, y+self.infomapa.alto_mapa, inv
	def salir_por_abajo(self,x,y,inv):
		return x, y-self.infomapa.alto_mapa, inv

class UniversoKlein():
	def __init__(self, infomapa):
		self.infomapa = infomapa
	# @staticmethod
	def posiciones(self,i,j,x,y): # (i,j)*juego.(ancho,alto)_mapa marca la esquina (superior izquierda) de la celda correspondiente
		# Para dibujar múltiples copias en cada celda del supermapa
		if i%2==1:
			return (i*self.infomapa.ancho_mapa + x,
					j*self.infomapa.alto_mapa + y)
		else:
			return (i*self.infomapa.ancho_mapa + x,
					j*self.infomapa.alto_mapa + self.infomapa.alto_mapa-y)

	def invertir(self,i,j):
		# Saber si la respectiva celda del supermapa está invertida en eje X o eje Y
		return False, i%2==0
		
	# Cuando un personaje sale por un lado del mapa, inv es si el paeronaje está invertido en algún eje o no.
	def salir_por_izquierda(self,x,y,inv):
		return x+self.infomapa.ancho_mapa, self.infomapa.alto_mapa-y, (False, not inv[1])
	def salir_por_derecha(self,x,y,inv):
		return x-self.infomapa.ancho_mapa, self.infomapa.alto_mapa-y, (False, not inv[1])
	def salir_por_arriba(self,x,y,inv):
		return x, y+self.infomapa.alto_mapa, inv
	def salir_por_abajo(self,x,y,inv):
		return x, y-self.infomapa.alto_mapa, inv

class UniversoProyectivo():
	def __init__(self, infomapa):
		self.infomapa = infomapa
	# @staticmethod
	def posiciones(self,i,j,x,y): # (i,j)*juego.(ancho,alto)_mapa marca la esquina (superior izquierda) de la celda correspondiente
		# Para dibujar múltiples copias en cada celda del supermapa
		if i%2==1:
			if j%2==1:
				return (i*self.infomapa.ancho_mapa + x,
						j*self.infomapa.alto_mapa + y)
			else:
				return (i*self.infomapa.ancho_mapa + self.infomapa.ancho_mapa-x,
						j*self.infomapa.alto_mapa + y)
		else:
			if j%2==1:
				return (i*self.infomapa.ancho_mapa + x,
						j*self.infomapa.alto_mapa + self.infomapa.alto_mapa-y)
			else:
				return (i*self.infomapa.ancho_mapa + self.infomapa.ancho_mapa-x,
						j*self.infomapa.alto_mapa + self.infomapa.alto_mapa-y)

	def invertir(self,i,j):
		# Saber si la respectiva celda del supermapa está invertida en eje X o eje Y
		return j%2==0, i%2==0
		
	# Cuando un personaje sale por un lado del mapa, actualizar información. "inv" es si el paeronaje está invertido en algún eje o no.
	def salir_por_izquierda(self,x,y,inv):
		return x+self.infomapa.ancho_mapa, self.infomapa.alto_mapa-y, (inv[0], not inv[1])
	def salir_por_derecha(self,x,y,inv):
		return x-self.infomapa.ancho_mapa, self.infomapa.alto_mapa-y, (inv[0], not inv[1])
	def salir_por_arriba(self,x,y,inv):
		return self.infomapa.ancho_mapa-x, y+self.infomapa.alto_mapa, (not inv[0],inv[1])
	def salir_por_abajo(self,x,y,inv):
		return self.infomapa.ancho_mapa-x, y-self.infomapa.alto_mapa, (not inv[0],inv[1])