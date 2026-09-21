#version 330

// Vertex shader "estilo PS1":
// - transforma o vertice normalmente (model -> view -> projecao)
// - em seguida faz o "vertex snapping": arredonda a posicao em espaco de
//   clip para uma grade de baixa resolucao, imitando a falta de precisao
//   (fixed-point) dos transformadores de geometria de 5a geracao.

uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;

// Resolucao "virtual" da grade de snapping. Valores baixos (ex: 160x120)
// deixam o efeito mais forte/perceptivel; valores altos suavizam.
uniform vec2 u_snap_resolution;
uniform bool u_snap_enabled;

in vec3 in_position;
in vec2 in_uv;

// 'noperspective' desativa a correcao de perspectiva na interpolacao,
// reproduzindo o mapeamento de textura afim classico do PS1.
noperspective out vec2 v_uv;

void main() {
    vec4 world_pos = u_model * vec4(in_position, 1.0);
    vec4 view_pos = u_view * world_pos;
    vec4 clip_pos = u_projection * view_pos;

    if (u_snap_enabled && clip_pos.w > 0.0001) {
        // Converte para NDC, aplica o snapping na grade e volta para clip
        // space multiplicando por w novamente.
        vec3 ndc = clip_pos.xyz / clip_pos.w;
        vec2 grid = u_snap_resolution;
        ndc.xy = floor(ndc.xy * grid) / grid;
        clip_pos.xyz = ndc * clip_pos.w;
    }

    v_uv = in_uv;
    gl_Position = clip_pos;
}
