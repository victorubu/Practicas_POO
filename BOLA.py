class Ball:
    def __init__(self, radio, masa, color, posicion_inicial=(0, 0)):
        self.radio = radio
        self.masa = masa
        self.color = color
        self.posicion = posicion_inicial
        self.velocidad = 0

    def actualizar_posicion(self, tiempo, aceleracion):
        # Calcula la nueva posición según la fórmula física: s = ut + (1/2)at^2
        self.posicion = (
            self.posicion[0] + self.velocidad * tiempo + 0.5 * aceleracion * (tiempo ** 2),
            self.posicion[1]
        )
        self.velocidad += aceleracion * tiempo
