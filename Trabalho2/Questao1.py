import cv2
import numpy as np
from skimage.filters import threshold_otsu
from skimage.morphology import opening, closing, disk
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt

import cv2
import numpy as np

img = cv2.imread("brain.png")
cv2.imwrite("brain_cortado.png", img[0:420, 0:430])

# Filtro passa-baixas (blur gaussiano) e mediana
# Leve borragem
GAUSSIAN_KERNEL = (5, 5)
GAUSSIAN_SIGMA = 1.0
MEDIAN_KERNEL = 5

# Apartir de 10 já começa a perder/inserir falsas informaçes
MORPH_RADIUS = 5            # aumentar ou diminuir para alterar o efeito dos quadrados
SELEM = disk(MORPH_RADIUS)

# 1. Ler imagem
img = cv2.imread("brain_cortado.png")

if img is None:
    raise FileNotFoundError("A imagem brain.png não foi encontrada no diretório!")

# 2. Converter para monocromática
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 3. Filtro passa-baixas + mediana
low_pass = cv2.GaussianBlur(gray, GAUSSIAN_KERNEL, GAUSSIAN_SIGMA)
denoised = cv2.medianBlur(low_pass, MEDIAN_KERNEL)

# 4. Limiar via histograma (Otsu)
# Esse valor depende dos filtros aplicados
# Para os valores atuais o threshold aceitaveis sao entr 140 e 190
threshold_value = 144
binary = denoised > threshold_value

# 5. Abertura + Fechamento
opened = opening(binary, SELEM)
closed = closing(opened, SELEM)

# 6. Conectividade e detecção do maior componente
labels = label(closed)
regions = regionprops(labels)

if len(regions) == 0:
    print("Nenhum elemento conexo encontrado!")
else:
    # Selecionar o maior componente
    largest_region = max(regions, key=lambda r: r.area)
    tumor_mask = labels == largest_region.label

# Resultados
plt.figure(figsize=(12, 8))

plt.subplot(231)
plt.title("Original")
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.subplot(232)
plt.title("Monocromática")
plt.imshow(gray, cmap="gray")
plt.axis("off")

plt.subplot(233)
plt.title("Após filtros")
plt.imshow(denoised, cmap="gray")
plt.axis("off")

plt.subplot(234)
plt.title("Binarização")
plt.imshow(binary, cmap="gray")
plt.axis("off")

plt.subplot(235)
plt.title("Abertura + Fechamento")
plt.imshow(closed, cmap="gray")
plt.axis("off")

plt.subplot(236)
plt.title("tumor")
plt.imshow(tumor_mask, cmap="gray")
plt.axis("off")

plt.tight_layout()
plt.show()
