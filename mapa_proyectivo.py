import pygame
from math import sqrt
from random import random
from pathlib import Path

pygame.init()

class InformacionGeneral():
    def __init__(self, ancho, alto, n, m):
        self.ancho_mapa = ancho
        self.alto_mapa = alto
        
        self.n = n # para 2n+1 ventanas a lo ancho
        self.m = m # para 2m+1 ventanas a lo alto

general = InformacionGeneral(200,100,2,2)


pantalla = pygame.display.set_mode(
    (max(general.ancho_mapa,700),max(general.alto_mapa,500)),
    pygame.RESIZABLE)
pygame.display.set_caption("EL Multidejo de la Locura")
clock = pygame.time.Clock()

def imagen(nombre,ancho,alto):
    return pygame.transform.scale(pygame.image.load(Path("imagenes",nombre)).convert_alpha(),(ancho,alto))

class InformacionVentana():
    def __init__(self):
        self.actualizar_posicion()

    def actualizar_posicion(self):
        dim_pantalla_real = pantalla.get_size()
        self.x = (dim_pantalla_real[0]-general.ancho_mapa)//2
        self.y = (dim_pantalla_real[1]-general.alto_mapa)//2
ventana = InformacionVentana()

class Proyectivo():
    def __init__(self):
        self.mundo_correcto=True
    @staticmethod
    def posiciones(i,j,x,y): # ventana.x+i*general.ancho_mapa marca la esquina de la celda correspondiente
        if i%2==1:
            if j%2==1:
                return (i*general.ancho_mapa + x,
                        j*general.alto_mapa + y)
            else:
                return (i*general.ancho_mapa + general.ancho_mapa-x,
                        j*general.alto_mapa + y)
        else:
            if j%2==1:
                return (i*general.ancho_mapa + x,
                        j*general.alto_mapa + general.alto_mapa-y)
            else:
                return (i*general.ancho_mapa + general.ancho_mapa-x,
                        j*general.alto_mapa + general.alto_mapa-y)

    def invertir(self,i,j):
        return j%2==0, i%2==0
        
    def salir_por_izquierda(self,x,y,inv):
        return x+general.ancho_mapa, general.alto_mapa-y, (inv[0], not inv[1])
    def salir_por_derecha(self,x,y,inv):
        return x-general.ancho_mapa, general.alto_mapa-y, (inv[0], not inv[1])
    def salir_por_arriba(self,x,y,inv):
        return general.ancho_mapa-x, y+general.alto_mapa, (not inv[0],inv[1])
    def salir_por_abajo(self,x,y,inv):
        return general.ancho_mapa-x, y-general.alto_mapa, (not inv[0],inv[1])
universo=Proyectivo()

class Fondos():
    def __init__(self):
        """2n+1 = cantidad de mapas a lo ancho
        2m+1 = cantidad de mapas a lo largo"""
        self.mapas = [[pygame.Surface((general.ancho_mapa,general.alto_mapa)) for j in range(-general.m,general.m+1)] for i in range(-general.n,general.n+1)]
        self.crear_fondo()

    # Si cambio el fondo esto se puede optimizar mucho
    def crear_fondo(self, color_superior=(0,0,250), color_inferior=(250,0,0)):
        fondo = pygame.Surface((general.ancho_mapa,general.alto_mapa))
        semi_diagonal = sqrt(general.ancho_mapa**2+general.alto_mapa**2)
        resolucion = 30
        for _ in range(resolucion):
            ratio = _ / resolucion
            r = int(color_superior[0] * (1 - ratio) + color_inferior[0] * ratio)
            g = int(color_superior[1] * (1 - ratio) + color_inferior[1] * ratio)
            b = int(color_superior[2] * (1 - ratio) + color_inferior[2] * ratio)
            pygame.draw.circle(fondo, (r, g, b), (general.ancho_mapa//2, general.alto_mapa//2), (1-ratio)*semi_diagonal)
        for mapas in self.mapas:
            for mapa in mapas:
                mapa.blit(fondo,(0,0))

    def mostrar(self):# Tener en cuenta que los indices no se corresponden con lo aparente (-1 -> 2)
        for i in range(-general.n,general.n+1):
            for j in range(-general.m,general.m+1):
                pantalla.blit(self.mapas[i+general.n][j+general.m],(ventana.x+general.ancho_mapa*i,ventana.y+general.alto_mapa*j))

mapas = Fondos()

class SuperMapa():
    def __init__(self):
        self.superficie = pygame.Surface(((2*general.n+1)*general.ancho_mapa,(2*general.m+1)*general.alto_mapa),pygame.SRCALPHA)
    def mostrar(self):
        pantalla.blit(self.superficie,(ventana.x-general.n*general.ancho_mapa,ventana.y-general.m*general.alto_mapa))

super_mapa = SuperMapa()

# -------------------------------------------------- OBJETO --------------------------------------------------

def crear_robot(tamaño):
    superficie = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
    
    # Cuerpo (cuadrado principal)
    pygame.draw.rect(superficie, (100, 200, 100), (10, 10, tamaño-20, tamaño-20), border_radius=5)
    
    # Ojos (puntos brillantes)
    # pygame.draw.circle(superficie, (255, 255, 0), (tamaño//3, tamaño//3), 5)
    pygame.draw.circle(superficie, (255, 255, 0), (2*tamaño//3, tamaño//3), 5)
    
    # Boca (línea con efecto "píxel art")
    for x in range(tamaño//3, 2*tamaño//3, 5):
        pygame.draw.line(superficie, (255, 50, 50), (x, 2*tamaño//3), (x+3, 2*tamaño//3), 3)
    
    return superficie

class Objeto:
    def __init__(self, nombre="Objeto", x=general.ancho_mapa//2, y=general.alto_mapa//2, ancho=0, alto=0, img=None, visible=False):
        self.nombre=nombre
        self.x=x
        self.y=y
        self.ancho = ancho
        self.alto = alto
        self.invertido = (False,False)
        if img != None:
            self.imagen = imagen(img,ancho,alto)
        else:
            self.imagen = crear_robot((ancho+alto)//2)
        self.visible=visible

    def posicionar(self,x,y):# Para que la posición represente el centro del objeto
        return (x-self.ancho//2, y-self.alto//2)

    def mostrar_individual(self,x,y,invertir_x=False, invertir_y=False):
        if self.visible:
            if self.imagen!=None:
                if self.invertido[0]: invertir_x = not invertir_x
                if self.invertido[1]: invertir_y = not invertir_y
                super_mapa.superficie.blit(pygame.transform.flip(self.imagen,invertir_x,invertir_y),self.posicionar(x,y))
            else:
                pygame.draw.rect(
                    pygame.transform.flip(super_mapa.superficie,invertir_x,invertir_y),
                    (250,250,250),
                    (*self.posicionar(x,y),
                     self.ancho, self.alto
                    ))

    def mostrar(self):
        for i in range(-1,2*general.n+2):
            for j in range(-1,2*general.m+2):
                self.mostrar_individual(*universo.posiciones(i,j,self.x,self.y),*universo.invertir(i,j))

# # -------------------------------------------------- OBJETO RANDOM --------------------------------------------------
# class ObjetoRandom(Objeto):
#     def __init__(self, nombre="", x=False, y=False, ancho=0, alto=0, img=None, visible=False, colisionables=[]):
#         if not x:
#             x=random()*(general.ancho_mapa-ancho)
#         if not y:
#             y=random()*(general.alto_mapa-alto)
#         super().__init__(nombre, x, y, ancho, alto, img, visible)
#         self.colisionables = colisionables

#     def aparecer(self):
#         while any(self.colisiona_con(colisionable) for colisionable in self.colisionables):
#             self.x=random()*(general.ancho_mapa-self.ancho)
#             self.y=random()*(general.alto_mapa-self.alto)
#         self.visible=True
    
#     def desaparecer(self):
#         self.visible=False

# -------------------------------------------------- MOVIL --------------------------------------------------
class Movil(Objeto):
    def __init__(self, nombre="", x=general.ancho_mapa//2, y=general.alto_mapa//2, ancho=0, alto=0, img=None, visible=False, velocidad=10):
        super().__init__(nombre, x, y, ancho, alto, img, visible)
        self.velocidad = velocidad
        self.x_dinamico = x
        self.y_dinamico = y

    def mover(self,direccion):
        if self.invertido[0]:
            self.x -= direccion[0]*self.velocidad
        else:
            self.x += direccion[0]*self.velocidad
        if self.invertido[1]:
            self.y -= direccion[1]*self.velocidad
        else:
            self.y += direccion[1]*self.velocidad
        if self.x<0:
            self.x , self.y, self.invertido = universo.salir_por_izquierda(self.x, self.y, self.invertido)
        if self.x>general.ancho_mapa:
            self.x , self.y, self.invertido = universo.salir_por_derecha(self.x, self.y, self.invertido)
        if self.y>general.alto_mapa:
            self.x , self.y, self.invertido = universo.salir_por_abajo(self.x, self.y, self.invertido)
        if self.y<0:
            self.x , self.y, self.invertido = universo.salir_por_arriba(self.x, self.y, self.invertido)

# # -------------------------------------------------- PERSONAJE --------------------------------------------------

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

objeto = Objeto(ancho=100,alto=100,visible=True)
movil = Movil(ancho=60,alto=60,visible=True)

jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        if evento.type == pygame.VIDEORESIZE:
            ventana.actualizar_posicion()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: movil.mover((-1,0))
    if keys[pygame.K_RIGHT]: movil.mover((1,0))
    if keys[pygame.K_UP]: movil.mover((0,-1))
    if keys[pygame.K_DOWN]: movil.mover((0,1))

    pantalla.fill((0, 0, 0))
    super_mapa.superficie.fill((0,200,0,0))
    mapas.mostrar()
    movil.mostrar()
    super_mapa.mostrar()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
