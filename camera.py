"""
Camera de navegacao livre (estilo "noclip"), controlada por
WASD + mouse look.
"""

import numpy as np
from pyrr import Matrix44, Vector3


class Camera:
    def __init__(self, position=(0.0, 1.6, 5.0), yaw=-90.0, pitch=0.0,
                 speed=4.0, sensitivity=0.12, fov=70.0, aspect=16 / 9,
                 near=0.05, far=100.0):
        self.position = Vector3(position, dtype="f4")
        self.yaw = yaw
        self.pitch = pitch
        self.speed = speed
        self.sensitivity = sensitivity
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far

        self.front = Vector3([0.0, 0.0, -1.0], dtype="f4")
        self.up = Vector3([0.0, 1.0, 0.0], dtype="f4")
        self.right = Vector3([1.0, 0.0, 0.0], dtype="f4")
        self._update_vectors()

    def _update_vectors(self):
        yaw_r = np.radians(self.yaw)
        pitch_r = np.radians(self.pitch)

        front = Vector3([
            np.cos(yaw_r) * np.cos(pitch_r),
            np.sin(pitch_r),
            np.sin(yaw_r) * np.cos(pitch_r),
        ], dtype="f4")
        self.front = front.normalized

        world_up = Vector3([0.0, 1.0, 0.0], dtype="f4")
        self.right = self.front.cross(world_up).normalized
        self.up = self.right.cross(self.front).normalized

    def process_keyboard(self, keys, dt: float):
        """`keys` e um dict {"forward": bool, "backward": bool, ...}."""
        velocity = self.speed * dt
        if keys.get("forward"):
            self.position += self.front * velocity
        if keys.get("backward"):
            self.position -= self.front * velocity
        if keys.get("left"):
            self.position -= self.right * velocity
        if keys.get("right"):
            self.position += self.right * velocity
        if keys.get("up"):
            self.position += self.up * velocity
        if keys.get("down"):
            self.position -= self.up * velocity

    def process_mouse(self, dx: float, dy: float):
        self.yaw += dx * self.sensitivity
        self.pitch -= dy * self.sensitivity
        self.pitch = max(-89.0, min(89.0, self.pitch))
        self._update_vectors()

    def get_view_matrix(self) -> np.ndarray:
        return Matrix44.look_at(
            self.position,
            self.position + self.front,
            self.up,
        )

    def get_projection_matrix(self) -> np.ndarray:
        return Matrix44.perspective_projection(
            self.fov, self.aspect, self.near, self.far
        )
