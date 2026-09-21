"""
Aplicacao interativa

Computacao Grafica - Arquitetura de Consoles Antigos.
Cenario adaptado: renderer estilo PS1 aplicado a um labirinto de terror.
"""

import sys
import os
import numpy as np
import glfw
import moderngl

from camera import Camera
from mesh import Mesh
from scene import generate_maze_grid, build_maze_mesh, find_spawn_point

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MAZE_WIDTH = 15   # deve ser impar
MAZE_HEIGHT = 15  # deve ser impar

# Diretorio onde este arquivo esta, independente de onde o "python" foi
# chamado (cwd). Assim "shaders/vertex.glsl" sempre resolve corretamente.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_shader_source(relative_path: str) -> str:
    full_path = os.path.join(BASE_DIR, relative_path)
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


class Application:
    def __init__(self):
        if hasattr(glfw, "PLATFORM") and hasattr(glfw, "PLATFORM_X11"):
            glfw.init_hint(glfw.PLATFORM, glfw.PLATFORM_X11)

        if not glfw.init():
            raise RuntimeError("Falha ao inicializar o GLFW")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

        self.window = glfw.create_window(
            WINDOW_WIDTH, WINDOW_HEIGHT,
            "Eixo 7 - PS1 Horror Renderer (Etapa 2)", None, None,
        )
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Falha ao criar a janela GLFW")

        glfw.make_context_current(self.window)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.program = self.ctx.program(
            vertex_shader=load_shader_source("vertex.glsl"),
            fragment_shader=load_shader_source("fragment.glsl"),
        )

        grid = generate_maze_grid(MAZE_WIDTH, MAZE_HEIGHT, seed=42)
        mesh_data = build_maze_mesh(grid)
        self.mesh = Mesh(self.ctx, self.program, mesh_data)

        spawn = find_spawn_point(grid)
        self.camera = Camera(position=spawn, aspect=WINDOW_WIDTH / WINDOW_HEIGHT)

        # Parametros controlaveis
        self.snap_enabled = True
        self.snap_resolution = (160.0, 120.0)  # resolucao "virtual" tipo PS1

        self._last_mouse = None
        self._keys_down = set()

        glfw.set_key_callback(self.window, self._on_key)
        glfw.set_cursor_pos_callback(self.window, self._on_mouse_move)

    def _on_key(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self._keys_down.add(key)
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True)
            if key == glfw.KEY_T:  # liga/desliga o efeito PS1
                self.snap_enabled = not self.snap_enabled
            if key == glfw.KEY_EQUAL:
                r = min(self.snap_resolution[0] * 1.25, 1920)
                self.snap_resolution = (r, r * 9 / 16)
            if key == glfw.KEY_MINUS:
                r = max(self.snap_resolution[0] / 1.25, 40)
                self.snap_resolution = (r, r * 9 / 16)
        elif action == glfw.RELEASE:
            self._keys_down.discard(key)

    def _on_mouse_move(self, window, xpos, ypos):
        if self._last_mouse is None:
            self._last_mouse = (xpos, ypos)
            return
        dx = xpos - self._last_mouse[0]
        dy = ypos - self._last_mouse[1]
        self._last_mouse = (xpos, ypos)
        self.camera.process_mouse(dx, dy)

    def _read_movement_keys(self) -> dict:
        return {
            "forward": glfw.KEY_W in self._keys_down,
            "backward": glfw.KEY_S in self._keys_down,
            "left": glfw.KEY_A in self._keys_down,
            "right": glfw.KEY_D in self._keys_down,
            "up": glfw.KEY_SPACE in self._keys_down,
            "down": glfw.KEY_LEFT_SHIFT in self._keys_down,
        }

    def run(self):
        last_time = glfw.get_time()
        while not glfw.window_should_close(self.window):
            now = glfw.get_time()
            dt = now - last_time
            last_time = now

            glfw.poll_events()
            self.camera.process_keyboard(self._read_movement_keys(), dt)

            self.ctx.clear(0.02, 0.02, 0.03)

            self.program["u_model"].write(np.identity(4, dtype="f4").tobytes())
            self.program["u_view"].write(self.camera.get_view_matrix().astype("f4").tobytes())
            self.program["u_projection"].write(self.camera.get_projection_matrix().astype("f4").tobytes())
            self.program["u_snap_enabled"].value = self.snap_enabled
            self.program["u_snap_resolution"].value = self.snap_resolution
            self.program["u_use_texture"].value = False
            self.program["u_base_color"].value = (0.55, 0.5, 0.55)
            self.program["u_fog_start"].value = 0.90
            self.program["u_fog_end"].value = 0.995
            self.program["u_fog_color"].value = (0.01, 0.01, 0.015)

            self.mesh.render()

            glfw.swap_buffers(self.window)

        self.mesh.release()
        glfw.terminate()


def main():
    try:
        app = Application()
    except RuntimeError as exc:
        print(f"Erro ao iniciar a aplicacao: {exc}", file=sys.stderr)
        sys.exit(1)
    app.run()


if __name__ == "__main__":
    main()
