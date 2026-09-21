"""
Estruturas de dados principais da engine.

Aqui definimos como a geometria fica organizada em memoria (arrays de
vertices/indices) e como ela e enviada para buffers na GPU via ModernGL.
"""

from dataclasses import dataclass, field
import numpy as np
import moderngl


@dataclass
class Vertex:
    position: tuple  # (x, y, z)
    uv: tuple         # (u, v)


@dataclass
class MeshData:
    """Representacao em memoria (CPU) de uma malha, antes de subir para a GPU."""
    vertices: list = field(default_factory=list)  # list[Vertex]
    indices: list = field(default_factory=list)   # list[int]

    def to_vertex_array(self) -> np.ndarray:
        """Achata a lista de Vertex em um array numpy intercalado
        (x, y, z, u, v) por vertice, formato esperado pelo VBO."""
        data = []
        for v in self.vertices:
            data.extend(v.position)
            data.extend(v.uv)
        return np.array(data, dtype="f4")

    def to_index_array(self) -> np.ndarray:
        return np.array(self.indices, dtype="i4")


class Mesh:
    """Malha ja carregada na GPU (VBO + IBO + VAO), pronta para desenho."""

    def __init__(self, ctx: moderngl.Context, program: moderngl.Program, mesh_data: MeshData):
        self.ctx = ctx
        self.vbo = ctx.buffer(mesh_data.to_vertex_array().tobytes())
        self.ibo = ctx.buffer(mesh_data.to_index_array().tobytes())

        self.vao = ctx.vertex_array(
            program,
            [(self.vbo, "3f 2f", "in_position", "in_uv")],
            self.ibo,
        )

    def render(self):
        self.vao.render(moderngl.TRIANGLES)

    def release(self):
        self.vao.release()
        self.vbo.release()
        self.ibo.release()
