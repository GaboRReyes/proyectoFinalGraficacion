import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cargar la imagen satelital
import os

# Ruta relativa a la imagen, desde donde se está ejecutando el script
image_path = os.path.join('pryectoFinalGraficacion', 'res', 'Imagen1.jpg')

# Continúa con tu procesamiento de la imagen
print(f"Ruta de la imagen: {image_path}")

img = Image.open(image_path).convert('L')  # Convertir a escala de grises
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
