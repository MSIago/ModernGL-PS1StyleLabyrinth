# PS1 Horror Renderer — Eixo 7 (Arquitetura de Consoles Antigos)

Projeto científico da disciplina de Computação Gráfica. Emula características
da pipeline de rasterização de 5ª geração (estilo PlayStation 1) aplicadas a
um labirinto de terror em tempo real.

## Como rodar

```bash
python -m venv venv
source venv/bin/activate  # (no Windows: venv\Scripts\activate)
pip install -r requirements.txt
python main.py
```

Requer uma GPU com suporte a OpenGL 3.3 core.

## Controles

| Tecla / Ação      | Efeito                                              |
|-------------------|------------------------------------------------------|
| W A S D           | Movimento (frente/trás/esquerda/direita)             |
| Espaço / Shift    | Sobe / desce                                         |
| Mouse             | Olhar em volta (mouse look)                          |
| T                 | Liga/desliga o efeito PS1 (vertex snapping)          |
| `+` / `-`         | Aumenta / diminui a resolução da grade de snapping   |
| Esc               | Fecha a aplicação                                    |

## Estrutura do projeto

```
ps1_horror_engine/
├── main.py            # janela, loop principal, input (Etapa 2)
├── camera.py           # câmera livre WASD + mouse (Etapa 2)
├── mesh.py             # estruturas de dados de vértice/malha + upload GPU (Etapa 2)
├── scene.py             # geração procedural do labirinto (Etapa 2)
├── shaders/
│   ├── vertex.glsl       # vertex snapping (efeito PS1)
│   └── fragment.glsl      # mapeamento afim (noperspective) + neblina
└── requirements.txt
```

## Relação com os artigos do Eixo 7

- **Everitt & Kilgard, "Practical and Robust Stenciled Shadow Volumes"**:
  o algoritmo de sombras via stencil buffer será implementado na Etapa 3,
  usando esta base de câmera/geometria como cenário de teste (labirinto
  de terror em vez do contexto genérico do artigo original).
- **"An online system which approved OpenGL 1.4 standard"**: fundamenta a
  escolha das limitações de pipeline fixa (sem correção de perspectiva por
  hardware, baixa precisão geométrica) que motivam o efeito de vertex
  snapping e o mapeamento afim já implementados nos shaders.

## Próximos passos (Etapa 3 e 4)

- Implementar shadow volumes com stencil buffer para as paredes do labirinto
- Adicionar dithering estilo PS1 (redução de profundidade de cor)
- Instrumentar tempo de frame / FPS e uso de memória para a Etapa 4
- Testar sob diferentes complexidades de labirinto (tamanho da grade)
