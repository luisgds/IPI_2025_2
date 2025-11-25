import cv2
import numpy as np
import matplotlib.pyplot as plt

def filtro_media_5x5(img):
    """Filtro de média simples 5x5 (domínio espacial)."""
    kernel = np.ones((5, 5), np.float32) / 25
    return cv2.filter2D(img, -1, kernel)

def filtro_gaussiano_freq(img, sigma):
    """Filtro gaussiano no domínio da frequência."""
    # Transformada de Fourier
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    # Criar filtro gaussiano passa-baixas
    linhas, colunas = img.shape
    cx, cy = colunas // 2, linhas // 2
    x = np.arange(colunas)
    y = np.arange(linhas)
    X, Y = np.meshgrid(x, y)
    gauss = np.exp(-((X - cx)**2 + (Y - cy)**2) / (2 * sigma**2))

    # Aplicar filtro
    filtrada = fshift * gauss
    # Inversa
    f_ishift = np.fft.ifftshift(filtrada)
    img_filtrada = np.fft.ifft2(f_ishift)
    return np.abs(img_filtrada)

# Carrega imagem em tons de cinza
img = cv2.imread("foto.ppm", cv2.IMREAD_GRAYSCALE)

# Filtro de média (espacial)
img_media = filtro_media_5x5(img)

# Filtro gaussiano (frequência)
sigma = 40
img_gauss = filtro_gaussiano_freq(img, sigma)

# Normaliza para visualização
img_media = cv2.normalize(img_media, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
img_gauss = cv2.normalize(img_gauss, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
img_media_bgr = cv2.cvtColor(img_media, cv2.COLOR_GRAY2BGR)
img_gauss_bgr = cv2.cvtColor(img_gauss, cv2.COLOR_GRAY2BGR)
cv2.imwrite("foto_media_5x5.ppm", img_media_bgr)
cv2.imwrite(f"foto_gauss_sigma_{sigma}.ppm", img_gauss_bgr)
# Mostra resultados
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.title("Original")
plt.imshow(img, cmap='gray')
plt.axis("off")

plt.subplot(1, 3, 2)
plt.title("Filtro Média 5x5 (Espacial)")
plt.imshow(img_media, cmap='gray')
plt.axis("off")

plt.subplot(1, 3, 3)
plt.title(f"Filtro Gaussiano (Freq) σ={sigma}")
plt.imshow(img_gauss, cmap='gray')
plt.axis("off")

plt.show()
