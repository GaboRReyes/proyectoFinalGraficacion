import numpy as np
from PIL import Image
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import os
from scipy.ndimage import gaussian_filter

def init_pygame_opengl(window_width, window_height):
    pygame.init()
    pygame.display.set_mode((window_width, window_height), pygame.DOUBLEBUF | pygame.OPENGL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    gluPerspective(45, (window_width / window_height), 0.1, 2000.0)  # Aumento del plano de recorte lejano

def load_texture_and_height_map(image_path):
    image = Image.open(image_path).convert("RGB")
    texture_data = image.tobytes("raw", "RGB", 0, -1)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    height_map = np.array(image.convert("L")) / 255.0
    height_map = gaussian_filter(height_map, sigma=2)
    border_size = 10
    height_map[:border_size, :] = 0
    height_map[-border_size:, :] = 0
    height_map[:, :border_size] = 0
    height_map[:, -border_size:] = 0

    return texture_id, height_map, image.width, image.height  # Ahora retornamos también las dimensiones de la imagen

def calculate_terrain_metrics(height_map, height_scale):
    grad_x, grad_y = np.gradient(height_map)
    avg_slope = np.mean(np.sqrt(grad_x ** 2 + grad_y ** 2)) * height_scale
    return avg_slope

def draw_terrain(height_map, texture_id, scale_factor=1.0, height_scale=30.0):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    rows, cols = height_map.shape
    half_width = (cols - 1) * scale_factor / 2
    half_height = (rows - 1) * scale_factor / 2
    for i in range(rows - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(cols):
            for k in (i, i + 1):
                x, y = j * scale_factor - half_width, k * scale_factor - half_height
                z = height_map[k, j] * height_scale
                glTexCoord2f(j / cols, k / rows)
                glVertex3f(x, y, z)
        glEnd()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, 'res', 'Imagen5.jpg')  # Cambiar el nombre según la imagen
    window_width, window_height = 900, 800
    init_pygame_opengl(window_width, window_height)

    texture_id, height_map, image_width, image_height = load_texture_and_height_map(image_path)

    # Escala basada en las dimensiones de la imagen
    scale_factor_x = 1.0  # Puedes ajustar esto si es necesario para obtener el tamaño del terreno en unidades reales
    scale_factor_y = 1.0  # Lo mismo para la dimensión Y

    terrain_length = image_height * scale_factor_y  # Usamos la altura de la imagen para determinar el largo
    terrain_width = image_width * scale_factor_x  # Usamos el ancho de la imagen para determinar el ancho

    # Cálculos de métricas
    avg_slope = calculate_terrain_metrics(height_map, height_scale=30.0)

    print(f"Dimensiones del terreno:")
    print(f"- Largo: {terrain_length:.2f} metros (basado en la altura de la imagen)")
    print(f"- Ancho: {terrain_width:.2f} metros (basado en el ancho de la imagen)")
    print(f"Inclinación promedio: {avg_slope:.2f} m/m")

    rows, cols = height_map.shape
    # Alejar la cámara más aún
    glTranslatef(0, 0, -terrain_length * 1.5)  # Alejamos la cámara aún más

    rotation_x = 0.0
    rotation_y = 0.0
    rotation_speed = 60.0

    clock = pygame.time.Clock()
    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            rotation_x -= rotation_speed * delta_time
        if keys[pygame.K_DOWN]:
            rotation_x += rotation_speed * delta_time
        if keys[pygame.K_LEFT]:
            rotation_y -= rotation_speed * delta_time
        if keys[pygame.K_RIGHT]:
            rotation_y += rotation_speed * delta_time
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(rotation_x, 1, 0, 0)
        glRotatef(rotation_y, 0, 1, 0)
        draw_terrain(height_map, texture_id)
        glPopMatrix()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
