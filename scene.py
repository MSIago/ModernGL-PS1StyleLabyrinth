"""
Construcao da cena base: um labirinto simples gerado a partir de uma
grade 2D (0 = corredor, 1 = parede)..

O algoritmo de geracao do labirinto em si e propositalmente simples
(DFS de backtracking); o foco desta etapa e a estrutura de dados e o
pipeline de renderizacao, nao a geracao procedural.
"""

import random
from mesh import Vertex, MeshData

WALL_HEIGHT = 3.0
CELL_SIZE = 2.0


def generate_maze_grid(width: int, height: int, seed: int = None) -> list:
    """Gera um labirinto perfeito (sem loops) via DFS de backtracking.
    Retorna uma matriz width x height com 1 = parede, 0 = corredor."""
    if seed is not None:
        random.seed(seed)

    grid = [[1] * height for _ in range(width)]

    def carve(cx, cy):
        grid[cx][cy] = 0
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and grid[nx][ny] == 1:
                grid[cx + dx // 2][cy + dy // 2] = 0
                carve(nx, ny)

    carve(1, 1)
    return grid


def _add_quad(mesh: MeshData, p0, p1, p2, p3):
    """Adiciona um quad (2 triangulos) com UVs 0-1 padrao."""
    base = len(mesh.vertices)
    mesh.vertices.extend([
        Vertex(p0, (0.0, 0.0)),
        Vertex(p1, (1.0, 0.0)),
        Vertex(p2, (1.0, 1.0)),
        Vertex(p3, (0.0, 1.0)),
    ])
    mesh.indices.extend([base, base + 1, base + 2, base, base + 2, base + 3])


def build_maze_mesh(grid: list) -> MeshData:
    """Converte a grade do labirinto em geometria 3D: piso + paredes."""
    mesh = MeshData()
    width = len(grid)
    height = len(grid[0])

    # Piso (um unico quad grande cobrindo o labirinto).
    fx0, fz0 = 0.0, 0.0
    fx1, fz1 = width * CELL_SIZE, height * CELL_SIZE
    _add_quad(
        mesh,
        (fx0, 0.0, fz0), (fx1, 0.0, fz0),
        (fx1, 0.0, fz1), (fx0, 0.0, fz1),
    )

    # Paredes: para cada celula "parede", gera 4 faces verticais.
    for x in range(width):
        for z in range(height):
            if grid[x][z] != 1:
                continue
            x0, z0 = x * CELL_SIZE, z * CELL_SIZE
            x1, z1 = x0 + CELL_SIZE, z0 + CELL_SIZE
            y0, y1 = 0.0, WALL_HEIGHT

            # Norte, Sul, Leste, Oeste
            _add_quad(mesh, (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0))
            _add_quad(mesh, (x1, y0, z1), (x0, y0, z1), (x0, y1, z1), (x1, y1, z1))
            _add_quad(mesh, (x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0))
            _add_quad(mesh, (x0, y0, z1), (x0, y0, z0), (x0, y1, z0), (x0, y1, z1))

    return mesh


def find_spawn_point(grid: list) -> tuple:
    """Retorna uma posicao de mundo dentro de um corredor livre (1,1)."""
    return (1 * CELL_SIZE + CELL_SIZE / 2, 1.6, 1 * CELL_SIZE + CELL_SIZE / 2)
