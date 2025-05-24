import pygame

from dibujos import *
from informaciones import *
from universos import *
from pantallas import *
from elementos_del_mapa import *
from menus import *

pygame.init()

ctx = Contexto()

infomapa = InformacionMapa(800,600,4,4)
ctx.infomapa = infomapa

juego = InformacionJuego()
ctx.juego = juego

pantalla = pygame.display.set_mode(
	(infomapa.ancho_mapa,infomapa.alto_mapa),
	pygame.RESIZABLE)
ctx.pantalla = pantalla

pygame.display.set_caption("Superficies Topológicas")

clock = pygame.time.Clock()

# def imagen(nombre,ancho,alto):
# 	return pygame.transform.scale(pygame.image.load(Path("imagenes",nombre)).convert_alpha(),(ancho,alto))

ventana = InformacionVentana(ctx)
ctx.ventana = ventana

super_mapa = SuperMapa(ctx)
ctx.super_mapa = super_mapa

juego.jugador = Jugador(ctx, ancho=40, alto=40, x=infomapa.ancho_mapa//2, y=infomapa.alto_mapa//2, velocidad = 10)
juego.universo = UniversoToroidal(infomapa)

fondo = Fondos(ctx)
ctx.fondo = fondo

menu_inicial = MenuInicio(ctx, opciones = [("jugando", "Empezar a jugar"),
								("mapas", "Elegir mapa"),
								("configuracion", "Configuración"),
								("cerrar", "Cerrar juego")])
menu_pausa = Menu(ctx, opciones = [("jugando", "Seguir jugando"),
							  ("menu inicial", "Volver al menú inicial"),
							  ("cerrar", "Cerrar juego")])
menu_mapas = MenuMapas(ctx)
menu_configuracion = MenuConfig(ctx)

pared1 = ParedHorizontal(ctx, 0, infomapa.ancho_mapa/3, 0, color=(250,0,0))
pared2 = ParedVertical(ctx, infomapa.ancho_mapa/3, 0, infomapa.alto_mapa*2/3, color=(250,0,0))
pared3 = ParedHorizontal(ctx, infomapa.ancho_mapa/3, infomapa.ancho_mapa, infomapa.alto_mapa*2/3, color=(250,0,0))
pared4 = ParedVertical(ctx, infomapa.ancho_mapa, infomapa.alto_mapa*2/3, infomapa.alto_mapa, color=(250,0,0))



def jugar():
	
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT]: juego.jugador.mover((-1,0))
	if keys[pygame.K_RIGHT]: juego.jugador.mover((1,0))
	if keys[pygame.K_UP]: juego.jugador.mover((0,-1))
	if keys[pygame.K_DOWN]: juego.jugador.mover((0,1))
	if keys[pygame.K_p]: juego.estado_de_juego="pausa"
	if keys[pygame.K_i]: juego.estado_de_juego="menu inicial"
	if keys[pygame.K_m]: juego.estado_de_juego="mapas"

	pantalla.fill((0, 0, 0))
	super_mapa.superficie.fill((0,200,0,0))
	fondo.mostrar()
	for paredd in paredes:
		paredd.mostrar()
	juego.jugador.mostrar()
	# for rect in obstaculos:
	# 	pygame.draw.rect(pantalla, (0, 250, 0), rect)
	super_mapa.mostrar()


while juego.activo:
	for evento in pygame.event.get():
		if evento.type == pygame.QUIT:
			juego.activo = False
		if evento.type == pygame.VIDEORESIZE:
			ventana.actualizar_posicion()
			
		if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
			juego.raton_clicado = True
		if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
			juego.raton_clicado = False

	if juego.estado_de_juego == "jugando":
		jugar()
	elif juego.estado_de_juego == "menu inicial":
		menu_inicial.desplegar()
	elif juego.estado_de_juego == "pausa":
		menu_pausa.desplegar()
	elif juego.estado_de_juego == "mapas":
		menu_mapas.desplegar()
	elif juego.estado_de_juego == "configuracion":
		menu_configuracion.desplegar()
	elif juego.estado_de_juego == "cerrar":
		juego.activo = False
	else:
		print("Esto no debería pasar")

	pygame.display.flip()
	clock.tick(60)

pygame.quit()
