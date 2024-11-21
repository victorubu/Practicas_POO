# Practicas_POO
En esta practica se han conseguido conocimiento clave a la ora de programar con objetos.
Tengo que reconocer que no ha sido sencillo y he creado muchas carpetas y archivos que no tienen funcionalidad alguna, pero gracias a la prueba y error he obtenido los objetivos propuestos.
Se han realizado varias funciones desde el comienzo de la practica pero solo me voy a centrar en las caracteristicas finales ya que son las funcionales.

**Características**
**Generación Dinámica del Modelo:

El proyecto genera dinámicamente un archivo XML para MuJoCo en base a los parámetros proporcionados por el usuario.
El modelo incluye:
Una esfera con radio y posición configurables.
Una rampa con posición e inclinación ajustables.
Un plano como base para el suelo. 

**Interfaz Gráfica de Usuario (GUI):
Permite configurar el radio y la posición inicial (X, Y, Z) de la esfera.
Permite ajustar la posición (X, Y, Z) y el ángulo de inclinación de la rampa.
Incluye botones para iniciar y reiniciar la simulación.

**Simulación en Tiempo Real:

Una simulación física basada en la interacción de la esfera con la rampa y el suelo.
Interacción con el mouse: el usuario puede mover la esfera en tiempo real arrastrándola.

**Configuración de Cámara:

La cámara está preconfigurada para centrarse en la esfera y la rampa.
Parámetros como distancia, ángulo azimutal y elevación garantizan una vista óptima de la escena.

**Descripción de Escena Basada en XML:

Genera un archivo XML (dynamic_model.xml) para la simulación en MuJoCo, basado en las configuraciones proporcionadas por el usuario. Esto garantiza flexibilidad y reproducibilidad.

**Componentes**
**Generador Dinámico de XML:

Genera el archivo dynamic_model.xml con los parámetros de la esfera y la rampa.
Ejemplo de estructura del XML generado:
<mujoco model="dynamic_scene">
    <option timestep="0.01" gravity="0 0 -9.81"/>
    <worldbody>
        <geom name="floor" type="plane" size="10 10 0.1" rgba="0.8 0.8 0.8 1"/>
        <body name="ball" pos="0 0 1">
            <geom type="sphere" size="0.1" rgba="1 0 0 1"/>
            <joint type="free"/>
        </body>
        <body name="ramp" pos="0.5 0 0.1">
            <geom name="inclined_ramp" type="box" size="1 0.5 0.1" rgba="0.7 0.7 0.7 1" euler="0.3 0 0"/>
        </body>
    </worldbody>
</mujoco>

**Interfaz Gráfica (GUI):
  Construida con customtkinter, permite:
  Ajustar el radio y la posición (X, Y, Z) de la esfera mediante deslizadores. 
  Ajustar la posición (X, Y, Z) y el ángulo de inclinación de la rampa.
  Botones para iniciar y reiniciar la simulación.

**Simulación Física:
  Utiliza el motor de física de MuJoCo para simular dinámicas reales, como gravedad y colisiones.
  La esfera puede rodar o caer dependiendo de la configuración de la rampa y el suelo.

**Interacción con el Mouse:
  Permite al usuario arrastrar la esfera en tiempo real durante la simulación, actualizando su posición dinámicamente.

**Cómo Funciona**
**Interacción con la GUI:
  El usuario ajusta los deslizadores en la GUI para configurar el radio y la posición inicial de la esfera, así como la posición e inclinación de la rampa.

**Generación del XML:
  Al hacer clic en "Iniciar Simulación", se genera un archivo XML (dynamic_model.xml) con los parámetros especificados.

**Inicio de la Simulación:
  MuJoCo carga el archivo XML y comienza la simulación física.
  La escena incluye el suelo, la esfera y la rampa, con la esfera reaccionando a la gravedad y las interacciones definidas.

**Actualizaciones en Tiempo Real:
  La posición de la esfera puede actualizarse dinámicamente con la interacción del mouse.
  La cámara se actualiza continuamente para renderizar la escena.

**Requisitos**

**Librerías de Python:
  mujoco: Motor de física para la simulación.
  mujoco.glfw: Administrador de contexto OpenGL para renderizar la escena.
  customtkinter: Librería para la creación de interfaces gráficas modernas.
  numpy: Cálculos numéricos para las actualizaciones de posición y geometría.

**Principales Funcionalidades**

**Geometría Dinámica:
  Genera una escena completamente configurable de forma dinámica.

**Interfaz Interactiva:
  Controles intuitivos mediante deslizadores y botones.

**Actualizaciones en Tiempo Real:
  Simulación interactiva con actualizaciones en vivo mediante entrada del mouse.

