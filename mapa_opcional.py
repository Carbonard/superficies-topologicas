import pygame
import math
import numpy as np
from random import random
from pathlib import Path

# -------------------------------------------------- AJUSTES INICIALES GENERALES --------------------------------------------------

pygame.init()

class InformacionGeneral():
    # Para guardar información relativa al tipo de partida
    def __init__(self, ancho, alto, n, m):
        self.ancho_mapa = ancho
        self.alto_mapa = alto
        
        self.n = n # para 2n+1 ventanas a lo ancho
        self.m = m # para 2m+1 ventanas a lo alto

general = InformacionGeneral(200,200,1,1)

pantalla = pygame.display.set_mode(
    (max(general.ancho_mapa,700),max(general.alto_mapa,700)),
    pygame.RESIZABLE)

pygame.display.set_caption("EL Multidejo de la Locura")

clock = pygame.time.Clock()

def imagen(nombre,ancho,alto):
    return pygame.transform.scale(pygame.image.load(Path("imagenes",nombre)).convert_alpha(),(ancho,alto))

class InformacionVentana():
    # Para guardar la información relativa a la ventana.
    def __init__(self):
        self.actualizar_posicion()

    def actualizar_posicion(self):
        self.ancho, self.alto = pantalla.get_size()
        self.x = (self.ancho-general.ancho_mapa)//2
        self.y = (self.alto-general.alto_mapa)//2

ventana = InformacionVentana()

# -------------------------------------------------- TIPOS DE UNIVERSO --------------------------------------------------

class UniversoToroidal():
    def __init__(self):
        pass
    @staticmethod
    def posiciones(i,j,x,y): # (i,j)*general.(ancho,alto)_mapa marca la esquina (superior izquierda) de la celda correspondiente
        # Para dibujar múltiples copias en cada celda del supermapa
        return (i*general.ancho_mapa + x,
                j*general.alto_mapa + y)

    def invertir(self,i,j):
        # Saber si la respectiva celda del supermapa está invertida en eje X o eje Y
        return False, False
        
    # Cuando un personaje sale por un lado del mapa, inv es si el paeronaje está invertido en algún eje o no.
    def salir_por_izquierda(self,x,y,inv):
        return x+general.ancho_mapa, y, inv
    def salir_por_derecha(self,x,y,inv):
        return x-general.ancho_mapa, y, inv
    def salir_por_arriba(self,x,y,inv):
        return x, y+general.alto_mapa, inv
    def salir_por_abajo(self,x,y,inv):
        return x, y-general.alto_mapa, inv

class UniversoKlein():
    def __init__(self):
        pass
    @staticmethod
    def posiciones(i,j,x,y): # (i,j)*general.(ancho,alto)_mapa marca la esquina (superior izquierda) de la celda correspondiente
        # Para dibujar múltiples copias en cada celda del supermapa
        if i%2==1:
            return (i*general.ancho_mapa + x,
                    j*general.alto_mapa + y)
        else:
            return (i*general.ancho_mapa + x,
                    j*general.alto_mapa + general.alto_mapa-y)

    def invertir(self,i,j):
        # Saber si la respectiva celda del supermapa está invertida en eje X o eje Y
        return False, i%2==0
        
    # Cuando un personaje sale por un lado del mapa, inv es si el paeronaje está invertido en algún eje o no.
    def salir_por_izquierda(self,x,y,inv):
        return x+general.ancho_mapa, general.alto_mapa-y, (False, not inv[1])
    def salir_por_derecha(self,x,y,inv):
        return x-general.ancho_mapa, general.alto_mapa-y, (False, not inv[1])
    def salir_por_arriba(self,x,y,inv):
        return x, y+general.alto_mapa, inv
    def salir_por_abajo(self,x,y,inv):
        return x, y-general.alto_mapa, inv

class UniversoProyectivo():
    def __init__(self):
        pass
    @staticmethod
    def posiciones(i,j,x,y): # (i,j)*general.(ancho,alto)_mapa marca la esquina (superior izquierda) de la celda correspondiente
        # Para dibujar múltiples copias en cada celda del supermapa
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
        # Saber si la respectiva celda del supermapa está invertida en eje X o eje Y
        return j%2==0, i%2==0
        
    # Cuando un personaje sale por un lado del mapa, actualizar información. "inv" es si el paeronaje está invertido en algún eje o no.
    def salir_por_izquierda(self,x,y,inv):
        return x+general.ancho_mapa, general.alto_mapa-y, (inv[0], not inv[1])
    def salir_por_derecha(self,x,y,inv):
        return x-general.ancho_mapa, general.alto_mapa-y, (inv[0], not inv[1])
    def salir_por_arriba(self,x,y,inv):
        return general.ancho_mapa-x, y+general.alto_mapa, (not inv[0],inv[1])
    def salir_por_abajo(self,x,y,inv):
        return general.ancho_mapa-x, y-general.alto_mapa, (not inv[0],inv[1])

# -------------------------------------------------- FONDOS --------------------------------------------------

class Fondos():
    def __init__(self):
        """2n+1 = cantidad de mapas a lo ancho
        2m+1 = cantidad de mapas a lo largo"""
        self.mapas = [[pygame.Surface((general.ancho_mapa,general.alto_mapa)) for j in range(-general.m,general.m+1)] for i in range(-general.n,general.n+1)]
        self.crear_fondo()

    # Si cambio el fondo esto se puede optimizar mucho
    def crear_fondo(self, color_superior=(0,0,250), color_inferior=(250,0,0)):
        fondo = pygame.Surface((general.ancho_mapa,general.alto_mapa))
        semi_diagonal = math.sqrt(general.ancho_mapa**2+general.alto_mapa**2)
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

# -------------------------------------------------- SUPER MAPA --------------------------------------------------

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
    # Los parametros hacen referencia a la posición en el supermapa y a si se tiene que invertir en la celda correspondiente
        if self.visible:
            if self.imagen!=None:
                # Si el personaje está invertido en la celda principal, invertir en la celda correspondiente
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
                self.mostrar_individual(*estado.universo.posiciones(i,j,self.x,self.y),*estado.universo.invertir(i,j))

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
            self.x , self.y, self.invertido = estado.universo.salir_por_izquierda(self.x, self.y, self.invertido)
        if self.x>general.ancho_mapa:
            self.x , self.y, self.invertido = estado.universo.salir_por_derecha(self.x, self.y, self.invertido)
        if self.y>general.alto_mapa:
            self.x , self.y, self.invertido = estado.universo.salir_por_abajo(self.x, self.y, self.invertido)
        if self.y<0:
            self.x , self.y, self.invertido = estado.universo.salir_por_arriba(self.x, self.y, self.invertido)

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

class EstadoJuego():
    def __init__(self):
        self.estado_de_juego = "menu inicial"
        self.activo = True
        self.raton_clicado = False
        self.universo=UniversoToroidal()
    
estado = EstadoJuego()

class Menu:
    def __init__(self, opciones):
        self.ancho = ventana.ancho*2//3
        self.alto = ventana.alto*2//3
        self.x = ventana.ancho//6
        self.y = ventana.alto//6
        self.margen_izquierdo = self.ancho//10
        self.margen_superior = self.alto//10

        self.tamaño_fuente = 25
        self.color_fuente = (250,250,250)
        self.color_fuente_resaltado = (0,200,250)
        self.color_fuente_clicado = (0,100,150)
        self.fuente = pygame.font.SysFont('Arial', self.tamaño_fuente)

        self.superficie = pygame.Surface((self.ancho, self.alto))

        # self.opciones = opciones
        self.opciones = []
        for i, (op,texto) in enumerate(opciones):
            opcion = {"estado": op,
                    "texto": self.fuente.render(texto, True, self.color_fuente),
                    "texto resaltado": self.fuente.render(texto, True, self.color_fuente_resaltado),
                    "texto clicado": self.fuente.render(texto, True, self.color_fuente_clicado),
                    "caja": None}
            opcion["caja"] = opcion["texto"].get_rect(topleft = (self.x + self.margen_izquierdo,
                                                                 self.y + self.margen_superior + i*self.tamaño_fuente*1.5))
            self.opciones.append(opcion)

        self.opcion_clicada = None
    
    def desplegar(self):

        pantalla.fill((0,0,0))
        self.superficie.fill((20,20,20))

        for i,opcion in enumerate(self.opciones):
            if opcion["caja"].collidepoint(pygame.mouse.get_pos()):
                if estado.raton_clicado:
                    self.opcion_clicada = i
                    self.superficie.blit(opcion["texto clicado"],(self.margen_izquierdo,
                                                                  self.margen_superior + i*self.tamaño_fuente*1.5))
                else:
                    self.superficie.blit(opcion["texto resaltado"],(self.margen_izquierdo,
                                                                    self.margen_superior + i*self.tamaño_fuente*1.5))
                if self.opcion_clicada==i and not estado.raton_clicado:
                    estado.estado_de_juego = opcion["estado"]
                    self.pulsar_boton(opcion)
                self.ilustrar_opcion_destacada(opcion)
            else:
                self.superficie.blit(opcion["texto"],(self.margen_izquierdo,
                                                      self.margen_superior + i*self.tamaño_fuente*1.5))
        if not estado.raton_clicado:
            self.opcion_clicada=None

        pantalla.blit(self.superficie,(self.x,self.y))
    
    def ilustrar_opcion_destacada(self, opcion):
        pass
    def pulsar_boton(self, opcion):
        pass

    def agregar_opciones(self,opciones: list):
        self.opciones.append(opciones)


"""
def dibujar_toro(surface):
    R, r = 150, 50  # Radio mayor y menor
    for theta in np.linspace(0, 2*np.pi, 30):  # Ángulo mayor
        for phi in np.linspace(0, 2*np.pi, 20):  # Ángulo menor
            # Coordenadas 3D
            x = (R + r * math.cos(phi)) * math.cos(theta)
            y = (R + r * math.cos(phi)) * math.sin(theta)
            z = r * math.sin(phi)
            
            # Proyección isométrica
            px = general.ancho_mapa//2 + (x - y) * 0.7
            py = general.alto_mapa//3 + (x + y)/2 * 0.7 - z * 0.7
            
            pygame.draw.circle(surface, (255, 100, 100), (int(px)+200, 250+int(py)), 3)
def dibujar_botella_klein(surface):
    for u in np.linspace(0, 2*np.pi, 40):
        for v in np.linspace(0, 2*np.pi, 20):
            # Ecuaciones paramétricas de la botella de Klein
            if u < np.pi:
                x = 6*math.cos(u)*(1 + math.sin(u)) + 4*(1 - math.cos(u)/2)*math.cos(u)*math.cos(v)
                y = 16*math.sin(u) + 4*(1 - math.cos(u)/2)*math.sin(u)*math.cos(v)
            else:
                x = 6*math.cos(u)*(1 + math.sin(u)) - 4*(1 - math.cos(u)/2)*math.cos(v)
                y = 16*math.sin(u)
            
            z = 4*(1 - math.cos(u)/2)*math.sin(v)
            
            # Proyección
            px = general.ancho_mapa//2 + (x - y) * 5
            py = general.alto_mapa//2 + (x + y)/2 * 3 - z * 5
            
            if 0 <= px < general.ancho_mapa and 0 <= py < general.alto_mapa:
                pygame.draw.circle(surface, (100, 255, 100), (200+int(px), 250+int(py)), 2)
def dibujar_banda_mobius(surface):
    for u in np.linspace(0, 2*np.pi, 50):
        for v in np.linspace(-1, 1, 20):
            # Ecuaciones paramétricas
            x = (1 + v/2 * math.cos(u/2)) * math.cos(u)
            y = (1 + v/2 * math.cos(u/2)) * math.sin(u)
            z = v/2 * math.sin(u/2)
            
            # Proyección
            px = general.ancho_mapa//2 + (x - y) * 100
            py = general.alto_mapa//2 + (x + y)/2 * 100 - z * 100
            
            pygame.draw.circle(surface, (100, 100, 255), (200+int(px), 250+int(py)), 2)
def dibujar_botella_klein_mejorada(surface):
    # Parámetros ajustables
    escala = 5
    desplazamiento_x, desplazamiento_y = general.ancho_mapa//2, general.alto_mapa//2
    rotacion = pygame.time.get_ticks() * 0.001  # Rotación animada
    
    for u in np.linspace(0, 2*np.pi, 40):
        for v in np.linspace(0, 2*np.pi, 20):
            # Ecuaciones paramétricas mejoradas
            r = 4 * (1 - math.cos(u)/2)
            
            if u < np.pi:
                x = 6 * math.cos(u) * (1 + math.sin(u)) + r * math.cos(u) * math.cos(v)
                y = 16 * math.sin(u) + r * math.sin(u) * math.cos(v)
                z = r * math.sin(v)
            else:
                x = 6 * math.cos(u) * (1 + math.sin(u)) - r * math.cos(v)
                y = 16 * math.sin(u)
                z = r * math.sin(v)
            
            # Rotación en 3D
            y_rot = y * math.cos(rotacion) - z * math.sin(rotacion)
            z_rot = y * math.sin(rotacion) + z * math.cos(rotacion)
            
            # Proyección isométrica con profundidad (z-buffering simple)
            px = desplazamiento_x + (x - y_rot) * escala * 0.7
            py = desplazamiento_y + (x + y_rot) * escala * 0.4 - z_rot * escala * 0.5
            
            # Color basado en profundidad
            profundidad = z_rot / 16 + 0.5  # Normalizado a [0,1]
            color = (
                int(100 + 155 * profundidad),
                int(255 - 100 * profundidad),
                int(100 + 155 * (1 - profundidad)))
            
            # if 0 <= px < general.ancho_mapa and 0 <= py < general.alto_mapa:
                # Dibujar con tamaño variable según profundidad
            radio = int(2 + 2 * (1 - profundidad))
            pygame.draw.circle(surface, (250,250,250), (200+int(px), 250+int(py)), radio)
def dibujar_plano_proyectivo(surface):
    # Parámetros para la superficie de Boy
    a, b, c = 0.5, 1.0, 0.3
    
    for u in np.linspace(0, np.pi, 30):
        for v in np.linspace(0, np.pi, 30):
            # Coordenadas paramétricas
            x = sqrt(2)*math.cos(u)*math.cos(v) / (math.sin(u)**2 + math.cos(v)**2)
            y = sqrt(2)*math.cos(u)*math.sin(v) / (math.sin(u)**2 + math.cos(v)**2)
            z = sqrt(2)*math.sin(u)*math.cos(v) / (math.sin(u)**2 + math.cos(v)**2)
            
            # Escalar y posicionar
            scale = 20
            px = general.ancho_mapa//2 + (x - y) * scale
            py = general.alto_mapa//2 + (x + y - z) * scale/2
            
            pygame.draw.circle(surface, (100, 100, 255), (200+int(px), 250+int(py)), 2)
def dibujar_plano_proyectivo_mejorado(surface):
    scale = 30
    points = []
    
    # Generar puntos
    for u in np.linspace(0, np.pi, 20):
        row = []
        for v in np.linspace(0, np.pi, 20):
            denominator = (math.sin(u)**2 + math.cos(v)**2)
            x = (math.sqrt(2)*math.cos(u)*math.cos(v)) / denominator
            y = (math.sqrt(2)*math.cos(u)*math.sin(v)) / denominator
            z = (math.sqrt(2)*math.sin(u)*math.cos(v)) / denominator
            
            px = 250 + (x - y) * scale
            py = 250 + (x + y - z) * scale/2
            row.append((px, py))
        points.append(row)
    
    # Dibujar triángulos
    for i in range(len(points)-1):
        for j in range(len(points[i])-1):
            pygame.draw.polygon(surface, (100, 100, 255, 100), [
                points[i][j],
                points[i+1][j],
                points[i][j+1]
            ], 1)
            pygame.draw.polygon(surface, (100, 100, 255, 100), [
                points[i+1][j],
                points[i+1][j+1],
                points[i][j+1]
            ], 1)
"""

def dibujar_toro_animado(surface):
    # Parámetros ajustados para que quepa bien
    R, r = 3.0, 1.0  # Radios normalizados
    escala = 30      # Factor de escala
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
            px = general.ancho_mapa//2 + (x - y_rot) * escala
            py = general.alto_mapa//2 + (x + y_rot - z_rot) * escala/2
            
            # Tamaño variable para efecto de profundidad
            radio = max(1, 3 - z_rot * 0.5)
            pygame.draw.circle(surface, (200,0,0), (200+int(px), 250+int(py)), int(radio))
def dibujar_botella_klein_con_lineas(surface):
    escala = 10
    desplazamiento = (menu_mapas.ancho//2,menu_mapas.alto//2+50)
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
    escala = 40  # Ajustado para visualización óptima
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
            px = general.ancho_mapa//2 + (x - y_rot) * escala
            py = general.alto_mapa//2 + (x + y_rot - z_rot*0.5) * escala * 0.6
            
            # Color con efecto de profundidad
            profundidad = (z_rot + 1.5) / 3.0  # Normalizado [0,1]
            azul = int(100 + 155 * profundidad)
            verde = int(200 - 100 * profundidad)
            color = (100, 0, 200)
            
            # if 0 <= px < general.ancho_mapa and 0 <= py < general.alto_mapa:  # Solo dibujar puntos visibles
            pygame.draw.circle(surface, color, (200+int(px), 250+int(py)), 2)

class MenuMapas(Menu):
    def __init__(self):
        super().__init__([("menu inicial", "Mundo Toroidal"),
                                   ("menu inicial", "Botella de Klein"),
                                   ("menu inicial", "Plano Proyectivo")])
        print(self.opciones)
        self.opciones[0]["universo"] = "toro"
        self.opciones[1]["universo"] = "Klein"
        self.opciones[2]["universo"] = "proyectivo"
    
    def ilustrar_opcion_destacada(self, opcion):
        if opcion["universo"]=="toro": dibujar_toro_animado(self.superficie)
        elif opcion["universo"]=="Klein": dibujar_botella_klein_con_lineas(self.superficie)
        elif opcion["universo"]=="proyectivo": dibujar_plano_proyectivo_animado(self.superficie)
        
    def pulsar_boton(self, opcion):
        if opcion["universo"]=="toro": estado.universo=UniversoToroidal()
        if opcion["universo"]=="Klein": estado.universo=UniversoKlein()
        if opcion["universo"]=="proyectivo": estado.universo=UniversoProyectivo()


menu_inicial = Menu(opciones = [("jugando", "Empezar a jugar"),
                                ("mapas", "Elegir mapa"),
                                ("cerrar", "Cerrar juego")])
menu_pausa = Menu(opciones = [("jugando", "Seguir jugando"),
                              ("menu inicial", "Volver al menú inicial"),
                              ("cerrar", "Cerrar juego")])
menu_mapas = MenuMapas()

def jugar():
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: movil.mover((-1,0))
    if keys[pygame.K_RIGHT]: movil.mover((1,0))
    if keys[pygame.K_UP]: movil.mover((0,-1))
    if keys[pygame.K_DOWN]: movil.mover((0,1))
    if keys[pygame.K_p]: estado.estado_de_juego="pausa"

    pantalla.fill((0, 0, 0))
    super_mapa.superficie.fill((0,200,0,0))
    mapas.mostrar()
    movil.mostrar()
    super_mapa.mostrar()


while estado.activo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            estado.activo = False
        if evento.type == pygame.VIDEORESIZE:
            ventana.actualizar_posicion()
            
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            estado.raton_clicado = True
        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            estado.raton_clicado = False
    
    if estado.estado_de_juego == "jugando":
        jugar()
    elif estado.estado_de_juego == "menu inicial":
        menu_inicial.desplegar()
    elif estado.estado_de_juego == "pausa":
        menu_pausa.desplegar()
    elif estado.estado_de_juego == "mapas":
        menu_mapas.desplegar()
    elif estado.estado_de_juego == "cerrar":
        estado.activo = False
    else:
        print("Esto no debería pasar")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
