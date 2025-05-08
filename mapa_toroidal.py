import pygame
from math import sqrt
from random import random
from pathlib import Path

pygame.init()

# __________________________________________________ AJUSTES INICIALES __________________________________________________

ancho_mapa = 1100
alto_mapa = 700

pantalla = pygame.display.set_mode(
    (ancho_mapa,alto_mapa),
    pygame.RESIZABLE)
pygame.display.set_caption("EL Multidejo de la Locura")
clock = pygame.time.Clock()

def imagen(nombre,ancho,alto):
    return pygame.transform.scale(pygame.image.load(Path("imagenes",nombre)).convert_alpha(),(ancho,alto))

# __________________________________________________ DEFINICIÓN DE CLASES __________________________________________________

# Decorador
def en_mapas_adyacentes(func):
    """Añadir para recorrer todos los mapas siendo:  
        # i=self.x + k1*ancho_mapa  
        # j=self.y + k2*alto_mapa
        con k1,k2 in [-1,0,1]"""
    def wrapper(self, *args, **kwargs):
        for k1 in [-1, 0, 1]:
            for k2 in [-1, 0, 1]:
                res= func(self, *args, i=self.x + k1*ancho_mapa, j=self.y + k2*alto_mapa, **kwargs)
                if res == True:
                    return True
    return wrapper

def parametros_hitbox(x,y,ancho,alto):
    return (x,y,ancho,alto)

# -------------------------------------------------- MAPA --------------------------------------------------
class Mapa:
    def __init__(self, x, y, ancho=ancho_mapa, alto=alto_mapa):
        self.posicion = (x, y)
        self.ancho = ancho
        self.alto = alto
        self.area = pygame.Surface((ancho,alto))

    def crear_fondo(self, color_superior=(0,0,250), color_inferior=(250,0,0)):
        semi_diagonal = sqrt(self.alto**2+self.ancho**2)
        resolucion = 30
        for r in range(resolucion):
            ratio = r / resolucion
            r = int(color_superior[0] * (1 - ratio) + color_inferior[0] * ratio)
            g = int(color_superior[1] * (1 - ratio) + color_inferior[1] * ratio)
            b = int(color_superior[2] * (1 - ratio) + color_inferior[2] * ratio)
            pygame.draw.circle(self.area, (r, g, b), (self.ancho//2, self.alto//2), (1-ratio)*semi_diagonal)

    def mostrar(self):
        pantalla.blit(self.area,self.posicion)

# -------------------------------------------------- SUPERMAPA --------------------------------------------------
class SuperMapa:
    def __init__(self):
        dim_pantalla_real = pantalla.get_size()
        posicion_mapa_central = (
            (dim_pantalla_real[0]-ancho_mapa)/2,
            (dim_pantalla_real[1]-alto_mapa)/2
        )
        self.mapas = [[Mapa(posicion_mapa_central[0]+i*ancho_mapa,posicion_mapa_central[1]+j*alto_mapa) for j in [-1,0,1]] for i in [-1,0,1]]
        
    def actualizar_posicion(self):
        dim_pantalla_real = pantalla.get_size()
        posicion_mapa_central = (
            (dim_pantalla_real[0]-ancho_mapa)/2,
            (dim_pantalla_real[1]-alto_mapa)/2
        )
        self.mapas = [[Mapa(posicion_mapa_central[0]+i*ancho_mapa,posicion_mapa_central[1]+j*alto_mapa) for j in [-1,0,1]] for i in [-1,0,1]]

    def crear_fondo(self):
        for mapas in self.mapas:
            for mapa in mapas:
                mapa.crear_fondo()

    def mostrar(self):
        for mapas in self.mapas:
            for mapa in mapas:
                mapa.mostrar()

super_mapa_fijo = SuperMapa()

# -------------------------------------------------- OBJETO --------------------------------------------------
class Objeto:
    def __init__(self, nombre="", x=0, y=0, ancho=0, alto=0, img=None, visible=False):
        self.nombre=nombre
        self.x=x
        self.y=y
        self.ancho = ancho
        self.alto = alto
        self.imagen=imagen(img,ancho,alto)
        self.visible=visible

    def mostrar_local(self,mapa):
        if self.visible and self.imagen!=None:
            mapa.area.blit(self.imagen,(self.x,self.y))


    def mostrar(self):
        for mapas in super_mapa_fijo.mapas:
            for mapa in mapas:
                self.mostrar_local(mapa)
    @property
    def hitbox(self):
        return pygame.Rect(parametros_hitbox(self.x,self.y,self.ancho,self.alto))
    
    def colisiona_con(self, cosa):
        return cosa.hitbox.colliderect(self.hitbox)

# -------------------------------------------------- OBJETO RANDOM --------------------------------------------------
class ObjetoRandom(Objeto):
    def __init__(self, nombre="", x=False, y=False, ancho=0, alto=0, img=None, visible=False, colisionables=[]):
        if not x:
            x=random()*(ancho_mapa-ancho)
        if not y:
            y=random()*(alto_mapa-alto)
        super().__init__(nombre, x, y, ancho, alto, img, visible)
        self.colisionables = colisionables

    def aparecer(self):
        while any(self.colisiona_con(colisionable) for colisionable in self.colisionables):
            self.x=random()*(ancho_mapa-self.ancho)
            self.y=random()*(alto_mapa-self.alto)
        self.visible=True
    
    def desaparecer(self):
        self.visible=False

# -------------------------------------------------- MOVIL --------------------------------------------------
class Movil(Objeto):
    def __init__(self, nombre="", x=0, y=0, ancho=0, alto=0, img=None, visible=False, velocidad=10):
        super().__init__(nombre, x, y, ancho, alto, img, visible)
        self.velocidad = velocidad
        self.x_dinamico = x
        self.y_dinamico = y
    @property
    def hitbox_dinamico(self):
        return pygame.Rect(self.x_dinamico, self.y_dinamico, self.ancho, self.alto)
    def mover_arriba(self,v=1):
        """v = modificación de velocidad"""
        self.y -= self.velocidad*v
        self.y_dinamico -= self.velocidad*v
        self.y %= alto_mapa
    def mover_abajo(self,v=1):
        """v = modificación de velocidad"""
        self.y += self.velocidad*v
        self.y_dinamico += self.velocidad*v
        self.y %= alto_mapa
    def mover_izquierda(self,v=1):
        """v = modificación de velocidad"""
        self.x -= self.velocidad*v
        self.x_dinamico -= self.velocidad*v
        self.x %= ancho_mapa
    def mover_derecha(self,v=1):
        """v = modificación de velocidad"""
        self.x += self.velocidad*v
        self.x_dinamico += self.velocidad*v
        self.x %= ancho_mapa
    
    @en_mapas_adyacentes
    def mostrar_local(self, mapa: Mapa, i, j):
        mapa.area.blit(self.imagen,(i,j))
        
        # transparent_surface = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        # pygame.draw.rect(transparent_surface, (0, 200, 0, 100),transparent_surface.get_rect())
        # mapa.area.blit(transparent_surface,(i,j))
    
    @en_mapas_adyacentes
    def colisiona_con(self, cosa: Objeto, i=0, j=0):
        return pygame.Rect(parametros_hitbox(i,j, self.ancho, self.alto)).colliderect(cosa.hitbox)

# -------------------------------------------------- PERSONAJE --------------------------------------------------

class Personaje(Movil):
    
    def __init__(self, nombre="", x=0, y=0, ancho=0, alto=0, img=None, visible=False, velocidad=5, img_mov=None):
        super().__init__(nombre, x, y, ancho, alto, img, visible)
        self.imagen = imagen(img, ancho, alto)
        self.imagen_normal = imagen(img, ancho, alto)
        self.imagen_movimiento = imagen(img_mov, ancho, alto)
        self.contador_keys_mov = 0

    def manejar_eventos(self,evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN):
                self.cambiar_imagen(self.imagen_movimiento)
                self.contador_keys_mov +=1
        if evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN):
                self.contador_keys_mov -= 1
                if self.contador_keys_mov == 0:
                    self.cambiar_imagen(self.imagen_normal)
    
    def cambiar_imagen(self, img):
        self.imagen = img

class Cuadrado(Movil):
    def __init__(self, nombre="", x=0, y=0, ancho=50, alto=50, velocidad=5, color=(250,250,250), visible=False):
        super().__init__(nombre, x=x, y=y, ancho=ancho, alto=alto, velocidad=velocidad, visible=visible)
        self.color=color
    def mostrar_local(self, mapa: Mapa):
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                pygame.draw.rect(
                    mapa.area,
                    self.color,
                    (self.x + i*ancho_mapa,
                     self.y + j*alto_mapa,
                     self.ancho, self.alto
                    ))

#__________________________________________________ CREACION PERSONAJE __________________________________________________

# cuby = Cuadrado()

el_dejo = Personaje(nombre="El Dejo", x=50, y=50, ancho=150, alto=150,
                    img = "dejo_cara.png",
                    img_mov = "dejo_caminando.png")

oso = Movil(nombre="Oso goloso",
            x=ancho_mapa//2, y=alto_mapa//2,
            ancho=200, alto=200,
            img="oso.png", visible=True, velocidad=5)

manzana = ObjetoRandom(
                        nombre="Manzana",
                        ancho = 50, alto = 50,
                        img = "manzana.png",
                        visible = True,
                        colisionables = [el_dejo, oso]
                        )
zapatillas = ObjetoRandom(
                        nombre="Zapatillas",
                        ancho = 100, alto = 100,
                        img = "zapatillas.png",
                        visible = False,
                        colisionables = [el_dejo]
                        )


#__________________________________________________ BUCLE PRINCIPAL __________________________________________________

racha_perdidas=0
total_manzanas_jugador=0

jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        if evento.type == pygame.VIDEORESIZE:
            super_mapa_fijo.actualizar_posicion()
        el_dejo.manejar_eventos(evento)

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]: el_dejo.mover_izquierda()
    if keys[pygame.K_RIGHT]: el_dejo.mover_derecha()
    if keys[pygame.K_UP]: el_dejo.mover_arriba()
    if keys[pygame.K_DOWN]: el_dejo.mover_abajo()
    
    if oso.colisiona_con(manzana):
        racha_perdidas += 1
        oso.velocidad += 0.3
        manzana.aparecer()
        if racha_perdidas==5:
            zapatillas.aparecer()
    if el_dejo.colisiona_con(manzana):
        total_manzanas_jugador +=1
        racha_perdidas = 0
        zapatillas.desaparecer()
        manzana.aparecer()
        # if random()*100//1%5==0:
        #     zapatillas.aparecer()
    if zapatillas.visible and el_dejo.colisiona_con(zapatillas):
        racha_perdidas = 0
        zapatillas.desaparecer()
        el_dejo.velocidad += 10
    
    if oso.x+oso.ancho<manzana.x+5:
        oso.mover_derecha()
    elif oso.x>manzana.x-5:
        oso.mover_izquierda()
    if oso.y+oso.alto<manzana.y+5:
        oso.mover_abajo()
    elif oso.y>manzana.y-5:
        oso.mover_arriba()

    pantalla.fill((0, 0, 0))
    super_mapa_fijo.crear_fondo()
    manzana.mostrar()
    if zapatillas.visible:
        zapatillas.mostrar()
    oso.mostrar()
    el_dejo.mostrar()
    super_mapa_fijo.mostrar()
    pygame.display.flip()
    clock.tick(60)
    if oso.velocidad>200:
        jugando = False

print("Has obtenido",total_manzanas_jugador,"manzanas.")

pygame.quit()

# Para el ejecutable:
# input("Pulsa enter para cerrar.")