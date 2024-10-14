import math

class Rampa:
    def __init__(self, inclinacion, longitud, friccion):
        self.inclinacion = inclinacion  # En grados
        self.longitud = longitud
        self.friccion = friccion

    def calcular_aceleracion(self, bola):
        gravedad = 9.81
        angulo_radianes = math.radians(self.inclinacion)
        aceleracion = gravedad * math.sin(angulo_radianes) - self.friccion * gravedad * math.cos(angulo_radianes)
        return max(aceleracion, 0)  
