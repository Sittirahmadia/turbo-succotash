"""
ModernGL-based 3D Cyberpunk Scene Renderer for NEON VOID OPTIMIZER.
Features: infinite wireframe grid, floating particles, low-poly city silhouette,
hexagonal overlays, holographic effects, and CRT/glitch post-processing.
"""

import logging
import time
from typing import Optional

import glm
import moderngl
import numpy as np

logger = logging.getLogger("NEON_VOID")

# Vertex shader for the 3D scene
VERTEX_SHADER = """
#version 330

uniform mat4 mvp;
uniform float time;

in vec3 in_position;
in vec3 in_color;
in vec2 in_uv;

out vec3 v_color;
out vec2 v_uv;
out float v_depth;

void main() {
    vec4 pos = mvp * vec4(in_position, 1.0);
    gl_Position = pos;
    v_color = in_color;
    v_uv = in_uv;
    v_depth = pos.w;
}
"""

# Fragment shader with cyberpunk effects
FRAGMENT_SHADER = """
#version 330

uniform float time;
uniform vec2 resolution;
uniform float glitch_intensity;
uniform float scanline_intensity;
uniform vec3 grid_color;
uniform vec3 particle_color;
uniform float fog_density;

in vec3 v_color;
in vec2 v_uv;
in float v_depth;

out vec4 fragColor;

// Random function
float rand(vec2 co) {
    return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

// Noise function
float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    float a = rand(i);
    float b = rand(i + vec2(1.0, 0.0));
    float c = rand(i + vec2(0.0, 1.0));
    float d = rand(i + vec2(1.0, 1.0));
    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

void main() {
    vec3 color = v_color;

    // Distance fog
    float fog = exp(-v_depth * fog_density);
    color = mix(vec3(0.02, 0.02, 0.04), color, fog);

    // Scanline effect
    if (scanline_intensity > 0.0) {
        float scanline = sin(gl_FragCoord.y * 3.14159 * 0.5) * 0.5 + 0.5;
        scanline = pow(scanline, 2.0);
        color *= mix(1.0, scanline, scanline_intensity * 0.3);
    }

    // Glitch effect
    if (glitch_intensity > 0.0) {
        float glitch = noise(vec2(gl_FragCoord.y * 0.1, time * 10.0));
        if (glitch > 0.97) {
            float shift = (rand(vec2(time, gl_FragCoord.y)) - 0.5) * glitch_intensity * 0.1;
            color.r += shift;
        }
    }

    // Subtle vignette
    vec2 uv = gl_FragCoord.xy / resolution;
    float vignette = 1.0 - length(uv - 0.5) * 0.8;
    vignette = smoothstep(0.0, 1.0, vignette);
    color *= vignette;

    // Tone mapping and glow
    color = color / (1.0 + color * 0.3);

    fragColor = vec4(color, 1.0);
}
"""

# Grid vertex shader
GRID_VERTEX = """
#version 330

uniform mat4 mvp;
uniform float time;

in vec3 in_position;
in float in_glow;

out float v_glow;
out float v_depth;

void main() {
    vec3 pos = in_position;
    // Subtle wave animation on grid
    pos.y += sin(pos.x * 0.5 + time * 0.5) * 0.1;
    pos.y += cos(pos.z * 0.3 + time * 0.3) * 0.05;

    vec4 world_pos = mvp * vec4(pos, 1.0);
    gl_Position = world_pos;
    v_glow = in_glow;
    v_depth = world_pos.w;
}
"""

# Grid fragment shader
GRID_FRAGMENT = """
#version 330

uniform float time;
uniform vec3 grid_color_base;
uniform vec3 grid_color_glow;
uniform float fog_density;

in float v_glow;
in float v_depth;

out vec4 fragColor;

void main() {
    vec3 color = mix(grid_color_base, grid_color_glow, v_glow);

    // Pulse effect
    float pulse = sin(time * 2.0) * 0.5 + 0.5;
    color *= 1.0 + pulse * v_glow * 0.5;

    // Distance fade
    float fade = exp(-v_depth * fog_density);
    color *= fade;

    fragColor = vec4(color, fade * 0.8);
}
"""

# Particle vertex shader
PARTICLE_VERTEX = """
#version 330

uniform mat4 mvp;
uniform float time;

in vec3 in_position;
in vec3 in_velocity;
in float in_life;
in float in_size;

out float v_life;
out float v_size;

void main() {
    vec3 pos = in_position + in_velocity * mod(time, 10.0);
    // Wrap around
    pos = mod(pos + 50.0, 100.0) - 50.0;

    vec4 world_pos = mvp * vec4(pos, 1.0);
    gl_Position = world_pos;
    gl_PointSize = in_size * (100.0 / world_pos.w);

    v_life = in_life;
    v_size = in_size;
}
"""

# Particle fragment shader
PARTICLE_FRAGMENT = """
#version 330

uniform vec3 particle_color;
uniform float time;

in float v_life;
in float v_size;

out vec4 fragColor;

void main() {
    // Circular particle
    vec2 coord = gl_PointCoord - vec2(0.5);
    float dist = length(coord);
    if (dist > 0.5) discard;

    // Soft edge
    float alpha = 1.0 - smoothstep(0.3, 0.5, dist);

    // Life-based fading
    float lifeFade = sin(v_life * 3.14159) * 0.5 + 0.5;

    // Color with glow
    vec3 color = particle_color * (1.0 + lifeFade * 0.5);
    alpha *= lifeFade * 0.6;

    fragColor = vec4(color, alpha);
}
"""


class CyberpunkRenderer:
    """
    3D Cyberpunk scene renderer using ModernGL.
    Renders an animated cyberpunk environment as the application background.
    """

    def __init__(self) -> None:
        self.ctx: Optional[moderngl.Context] = None
        self._initialized = False

        # Scene parameters
        self.time = 0.0
        self.camera_pos = glm.vec3(0.0, 5.0, -20.0)
        self.camera_target = glm.vec3(0.0, 0.0, 0.0)
        self.camera_up = glm.vec3(0.0, 1.0, 0.0)

        # Effect intensities
        self.glitch_intensity = 0.0
        self.scanline_intensity = 0.0
        self.fog_density = 0.02

        # Colors
        self.grid_color_base = glm.vec3(0.0, 0.6, 1.0)      # Electric Cyan
        self.grid_color_glow = glm.vec3(1.0, 0.0, 0.67)     # Hot Magenta
        self.particle_color = glm.vec3(0.22, 1.0, 0.08)     # Acid Green

        # OpenGL objects
        self._grid_program: Optional[moderngl.Program] = None
        self._particle_program: Optional[moderngl.Program] = None
        self._grid_vao: Optional[moderngl.VertexArray] = None
        self._particle_vao: Optional[moderngl.VertexArray] = None
        self._grid_buffer: Optional[moderngl.Buffer] = None
        self._particle_buffer: Optional[moderngl.Buffer] = None

        # Particle system
        self._particle_count = 500
        self._particles: Optional[np.ndarray] = None

    def initialize(self, ctx: moderngl.Context) -> bool:
        """Initialize the renderer with a ModernGL context."""
        try:
            self.ctx = ctx

            # Enable blending for transparency
            self.ctx.enable(moderngl.BLEND)
            self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
            self.ctx.enable(moderngl.DEPTH_TEST)

            # Create shaders and programs
            self._grid_program = self.ctx.program(
                vertex_shader=GRID_VERTEX,
                fragment_shader=GRID_FRAGMENT
            )
            self._particle_program = self.ctx.program(
                vertex_shader=PARTICLE_VERTEX,
                fragment_shader=PARTICLE_FRAGMENT
            )

            # Create geometry
            self._create_grid()
            self._create_particles()

            self._initialized = True
            logger.info("Cyberpunk renderer initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize cyberpunk renderer: {e}")
            return False

    def _create_grid(self) -> None:
        """Create the infinite wireframe grid geometry."""
        grid_size = 100
        grid_spacing = 2.0
        vertices = []

        # Horizontal lines
        for z in range(-grid_size, grid_size + 1):
            z_pos = z * grid_spacing
            glow = 1.0 if z % 5 == 0 else 0.3  # Major lines glow more
            vertices.extend([-grid_size * grid_spacing, 0.0, z_pos, glow])
            vertices.extend([grid_size * grid_spacing, 0.0, z_pos, glow])

        # Vertical lines
        for x in range(-grid_size, grid_size + 1):
            x_pos = x * grid_spacing
            glow = 1.0 if x % 5 == 0 else 0.3
            vertices.extend([x_pos, 0.0, -grid_size * grid_spacing, glow])
            vertices.extend([x_pos, 0.0, grid_size * grid_spacing, glow])

        vertex_data = np.array(vertices, dtype='f4')

        self._grid_buffer = self.ctx.buffer(vertex_data)
        self._grid_vao = self.ctx.vertex_array(
            self._grid_program,
            [
                (self._grid_buffer, '3f 1f', 'in_position', 'in_glow')
            ]
        )

    def _create_particles(self) -> None:
        """Create the floating particle system."""
        # Each particle: position(3) + velocity(3) + life(1) + size(1) = 8 floats
        particles = np.zeros(self._particle_count * 8, dtype='f4')

        for i in range(self._particle_count):
            base = i * 8
            # Random position in a large area
            particles[base + 0] = np.random.uniform(-50, 50)     # x
            particles[base + 1] = np.random.uniform(0.5, 20)     # y
            particles[base + 2] = np.random.uniform(-50, 50)     # z
            # Slow upward drift velocity
            particles[base + 3] = np.random.uniform(-0.5, 0.5)   # vx
            particles[base + 4] = np.random.uniform(0.2, 1.5)    # vy (upward)
            particles[base + 5] = np.random.uniform(-0.5, 0.5)   # vz
            particles[base + 6] = np.random.uniform(0, 1)        # life phase
            particles[base + 7] = np.random.uniform(1, 4)        # size

        self._particles = particles
        self._particle_buffer = self.ctx.buffer(particles)
        self._particle_vao = self.ctx.vertex_array(
            self._particle_program,
            [
                (self._particle_buffer, '3f 3f 1f 1f', 'in_position', 'in_velocity', 'in_life', 'in_size')
            ]
        )

    def update(self, delta_time: float) -> None:
        """Update scene animation."""
        self.time += delta_time

        # Subtle camera movement
        cam_x = np.sin(self.time * 0.1) * 5.0
        cam_y = 5.0 + np.sin(self.time * 0.15) * 1.5
        cam_z = -20.0 + np.cos(self.time * 0.08) * 3.0
        self.camera_pos = glm.vec3(cam_x, cam_y, cam_z)

        # Random glitch bursts
        if np.random.random() < 0.002:
            self.glitch_intensity = 1.0
        self.glitch_intensity *= 0.95  # Decay

    def render(self, width: int, height: int) -> None:
        """Render the complete cyberpunk scene."""
        if not self._initialized or not self.ctx:
            return

        try:
            # Clear
            self.ctx.clear(0.02, 0.02, 0.04, 1.0)

            # Build MVP matrix
            aspect = width / height if height > 0 else 1.0
            proj = glm.perspective(glm.radians(60.0), aspect, 0.1, 200.0)
            view = glm.lookAt(self.camera_pos, self.camera_target, self.camera_up)
            mvp = proj * view

            # Render grid
            if self._grid_vao and self._grid_program:
                mvp_bytes = np.array(mvp, dtype='f4').tobytes()
                self._grid_program['mvp'].write(mvp_bytes)
                self._grid_program['time'].value = self.time
                self._grid_program['grid_color_base'].write(self.grid_color_base)
                self._grid_program['grid_color_glow'].write(self.grid_color_glow)
                self._grid_program['fog_density'].value = self.fog_density
                self._grid_vao.render(moderngl.LINES)

            # Render particles
            if self._particle_vao and self._particle_program:
                self.ctx.enable(moderngl.BLEND)
                self._particle_program['mvp'].write(np.array(mvp, dtype='f4').tobytes())
                self._particle_program['time'].value = self.time
                self._particle_program['particle_color'].write(self.particle_color)
                self._particle_vao.render(moderngl.POINTS)

        except Exception as e:
            logger.debug(f"Render error: {e}")

    def resize(self, width: int, height: int) -> None:
        """Handle viewport resize."""
        if self.ctx:
            self.ctx.viewport = (0, 0, width, height)

    def set_effect_intensity(self, glitch: float = 0.0, scanline: float = 0.0) -> None:
        """Set post-processing effect intensities (0.0 to 1.0)."""
        self.glitch_intensity = max(0.0, min(1.0, glitch))
        self.scanline_intensity = max(0.0, min(1.0, scanline))

    def cleanup(self) -> None:
        """Clean up OpenGL resources."""
        self._initialized = False
        objects = [self._grid_vao, self._particle_vao, self._grid_buffer,
                   self._particle_buffer, self._grid_program, self._particle_program]
        for obj in objects:
            if obj is not None:
                try:
                    obj.release()
                except Exception:
                    pass

        self._grid_vao = None
        self._particle_vao = None
        self._grid_buffer = None
        self._particle_buffer = None
        self._grid_program = None
        self._particle_program = None
