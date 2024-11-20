import customtkinter as ctk
import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import os

# Variables globales
mouse_x = 0
mouse_y = 0
button_left = False
model = None
data = None
scene = None
cam = None
context = None
opt = None
window = None
simulation_running = False  # Indicador de estado de simulación

# Función para generar el archivo XML dinámicamente
def generate_xml(sphere_radius, sphere_position, ramp_position, ramp_inclination):
    xml_content = f"""
    <mujoco model="dynamic_scene">
        <option timestep="0.01" gravity="0 0 -9.81"/>
        <worldbody>
            <!-- Suelo -->
            <geom name="floor" type="plane" size="10 10 0.1" rgba="0.8 0.8 0.8 1"/>
            <!-- Esfera -->
            <body name="ball" pos="{sphere_position[0]} {sphere_position[1]} {sphere_position[2]}">
                <geom type="sphere" size="{sphere_radius}" rgba="1 0 0 1"/>
                <joint type="free"/>
            </body>
            <!-- Rampa -->
            <body name="ramp" pos="{ramp_position[0]} {ramp_position[1]} {ramp_position[2]}">
                <geom name="inclined_ramp" type="box" size="1 0.5 0.1" rgba="0.7 0.7 0.7 1" euler="{ramp_inclination} 0 0"/>
            </body>
        </worldbody>
    </mujoco>
    """
    with open("dynamic_model.xml", "w") as file:
        file.write(xml_content)

# Clase Ball
class Ball:
    def __init__(self, data, name, radius=0.1, position=(0, 0, 1)):
        self.data = data
        self.name = name
        self.radius = radius
        self.position = np.array(position)

    def update_position(self, new_position):
        self.position = new_position
        self.data.qpos[:3] = new_position

# Callbacks para el ratón
def mouse_move(window, xpos, ypos):
    global mouse_x, mouse_y
    mouse_x = xpos
    mouse_y = ypos

def mouse_button(window, button, action, mods):
    global button_left
    if button == glfw.MOUSE_BUTTON_LEFT:
        button_left = (action == glfw.PRESS)

# Actualizar posición del objeto
def update_object_position(ball, window):
    if not button_left:
        return

    width, height = glfw.get_framebuffer_size(window)
    rel_x = (mouse_x / width) * 2 - 1
    rel_y = 1 - (mouse_y / height) * 2
    scale_x = 2.0
    scale_y = 2.0
    ball_pos = np.array([rel_x * scale_x, rel_y * scale_y, ball.position[2]])
    ball_pos[0] = max(-2.0, min(2.0, ball_pos[0]))
    ball_pos[1] = max(-2.0, min(2.0, ball_pos[1]))
    ball.update_position(ball_pos)
    print(f"Ball moved to: {ball_pos}")

# Inicialización de MuJoCo
def init_mujoco():
    global model, data, scene, cam, window, context, opt
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    window = glfw.create_window(1200, 900, "MuJoCo Simulation", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create GLFW window")

    glfw.make_context_current(window)
    glfw.swap_interval(1)
    model = mj.MjModel.from_xml_path('dynamic_model.xml')
    data = mj.MjData(model)
    cam = mj.MjvCamera()
    opt = mj.MjvOption()
    scene = mj.MjvScene(model, maxgeom=10000)
    context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)

    # Configurar cámara
    mj.mjv_defaultCamera(cam)
    mj.mjv_defaultOption(opt)
    cam.lookat[:] = [0, 0, 0.5]  # Centro del foco de la cámara
    cam.distance = 5.0           # Alejar la cámara
    cam.azimuth = 45             # Ángulo horizontal
    cam.elevation = -20          # Ángulo vertical

    glfw.set_cursor_pos_callback(window, mouse_move)
    glfw.set_mouse_button_callback(window, mouse_button)

# Interfaz gráfica
class SimulationGUI:
    def __init__(self):
        self.init_gui()

    def init_gui(self):
        self.root = ctk.CTk()
        self.root.title("Simulación de Esferas y Rampas")
        self.root.geometry("500x600")

        ctk.CTkLabel(self.root, text="Control de Simulación", font=("Arial", 20)).pack(pady=10)

        # Controles para la Esfera
        self.sphere_frame = ctk.CTkFrame(self.root)
        self.sphere_frame.pack(pady=10, fill="x", padx=10)

        ctk.CTkLabel(self.sphere_frame, text="Radio de la Esfera:").pack(anchor="w", padx=10)
        self.sphere_radius = ctk.CTkSlider(self.sphere_frame, from_=0.05, to=0.5, number_of_steps=50)
        self.sphere_radius.pack(fill="x", padx=10)

        ctk.CTkLabel(self.sphere_frame, text="Posición Inicial (X, Y, Z):").pack(anchor="w", padx=10)
        self.sphere_x = ctk.CTkSlider(self.sphere_frame, from_=-2.0, to=2.0, number_of_steps=100)
        self.sphere_x.pack(fill="x", padx=10)
        self.sphere_y = ctk.CTkSlider(self.sphere_frame, from_=-2.0, to=2.0, number_of_steps=100)
        self.sphere_y.pack(fill="x", padx=10)
        self.sphere_z = ctk.CTkSlider(self.sphere_frame, from_=0.5, to=3.0, number_of_steps=50)
        self.sphere_z.pack(fill="x", padx=10)

        # Controles para la Rampa
        self.ramp_frame = ctk.CTkFrame(self.root)
        self.ramp_frame.pack(pady=10, fill="x", padx=10)

        ctk.CTkLabel(self.ramp_frame, text="Posición de la Rampa (X, Y, Z):").pack(anchor="w", padx=10)
        self.ramp_x = ctk.CTkSlider(self.ramp_frame, from_=-2.0, to=2.0, number_of_steps=100)
        self.ramp_x.pack(fill="x", padx=10)
        self.ramp_y = ctk.CTkSlider(self.ramp_frame, from_=-2.0, to=2.0, number_of_steps=100)
        self.ramp_y.pack(fill="x", padx=10)
        self.ramp_z = ctk.CTkSlider(self.ramp_frame, from_=0.1, to=1.0, number_of_steps=50)
        self.ramp_z.pack(fill="x", padx=10)

        ctk.CTkLabel(self.ramp_frame, text="Inclinación de la Rampa:").pack(anchor="w", padx=10)
        self.ramp_angle = ctk.CTkSlider(self.ramp_frame, from_=0, to=45, number_of_steps=45)
        self.ramp_angle.pack(fill="x", padx=10)

        # Botón para iniciar simulación
        self.start_button = ctk.CTkButton(self.root, text="Iniciar Simulación", command=self.start_simulation)
        self.start_button.pack(pady=10)

        # Botón para reiniciar simulación
        self.reset_button = ctk.CTkButton(self.root, text="Reiniciar Simulación", command=self.reset_simulation)
        self.reset_button.pack(pady=10)

        self.root.mainloop()

    def start_simulation(self):
        global simulation_running

        if simulation_running:
            self.reset_simulation()

        sphere_radius = self.sphere_radius.get()
        sphere_position = (self.sphere_x.get(), self.sphere_y.get(), self.sphere_z.get())
        ramp_position = (self.ramp_x.get(), self.ramp_y.get(), self.ramp_z.get())
        ramp_inclination = self.ramp_angle.get()

        print(f"Esfera -> Radio: {sphere_radius}, Posición: {sphere_position}")
        print(f"Rampa -> Posición: {ramp_position}, Inclinación: {ramp_inclination}")

        generate_xml(sphere_radius, sphere_position, ramp_position, ramp_inclination)
        self.launch_simulation()

    def reset_simulation(self):
        global window, simulation_running

        if window:
            glfw.set_window_should_close(window, True)
            glfw.poll_events()
            glfw.terminate()

        simulation_running = False

    def launch_simulation(self):
        global simulation_running
        init_mujoco()
        ball = Ball(data=data, name="red_ball")
        simulation_running = True
        while not glfw.window_should_close(window):
            mj.mj_step(model, data)
            mj.mj_forward(model, data)
            update_object_position(ball, window)
            mj.mjv_updateScene(model, data, opt, None, cam, mj.mjtCatBit.mjCAT_ALL.value, scene)
            mj.mjr_render(mj.MjrRect(0, 0, 1200, 900), scene, context)
            glfw.swap_buffers(window)
            glfw.poll_events()

        glfw.terminate()
        simulation_running = False

if __name__ == "__main__":
    SimulationGUI()

