import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Obtener la ruta absoluta del directorio donde se encuentra el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta completa a la imagen (desde 'res' dentro de la carpeta del proyecto)
image_path = os.path.join(script_dir, 'res', 'Imagen2.jpg')

# Verificar que la ruta de la imagen sea correcta
print(f"Ruta de la imagen: {image_path}")

# Cargar la imagen satelital
try:
    img = Image.open(image_path).convert('L')  # Convertir a escala de grises
except FileNotFoundError:
    print(f"Error: La imagen no se encontró en la ruta: {image_path}")
    exit()

img_array = np.array(img)

# Crear una malla de coordenadas para la imagen
x = np.linspace(0, img_array.shape[1], img_array.shape[1])
y = np.linspace(0, img_array.shape[0], img_array.shape[0])
x, y = np.meshgrid(x, y)

# Generar los valores de altura desde la imagen
z = img_array / 255.0  # Normalizar valores entre 0 y 1

# Crear la visualización 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plotear la superficie
ax.plot_surface(x, y, z, cmap='terrain')

# Etiquetas y mostrar
ax.set_title('Terreno 3D desde Imagen Satelital')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Altura (Z)')
plt.show()
