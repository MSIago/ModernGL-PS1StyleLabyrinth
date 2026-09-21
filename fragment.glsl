#version 330

noperspective in vec2 v_uv;
out vec4 f_color;

uniform sampler2D u_texture;
uniform bool u_use_texture;
uniform vec3 u_base_color;

// Neblina simples (comum em jogos de terror de 5a geracao para esconder
// o clipping de distancia curto do hardware original).
uniform float u_fog_start;
uniform float u_fog_end;
uniform vec3 u_fog_color;

void main() {
    vec3 color = u_use_texture ? texture(u_texture, v_uv).rgb : u_base_color;

    float depth = gl_FragCoord.z / gl_FragCoord.w;
    float fog_factor = clamp((depth - u_fog_start) / (u_fog_end - u_fog_start), 0.0, 1.0);
    color = mix(color, u_fog_color, fog_factor);

    f_color = vec4(color, 1.0);
}
