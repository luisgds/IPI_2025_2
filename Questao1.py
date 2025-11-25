from PIL import Image
import os
import math

class ManipularImage():
    """ 
    Inicia uma instância recebendo o arquivo que deseja que
    seja alterado: nome_entrada; e nome_saida para o nome que
    será salvo a nova imagem transformando a imagem no formato
    PPM e salva ela com o nome que estiver no nome_saida e 
    pega essa imagem ppm para as futuras manipulações.
    """
    def __init__(self, nome_entrada: str, nome_saida: str, l:int = 720, a:int = 1280):
        extensao = os.path.splitext(nome_entrada)[1].lower()
        self.nome_saida = nome_saida
        if extensao in [".jpg", ".jpeg", ".png", ".bmp"]:
            # Redimencionando a imagem para 720p por padrão
            self.aux = Image.open(nome_entrada)
            nova_res = (a, l)
            img_redimensionada = self.aux.resize(nova_res, Image.LANCZOS)
            img_redimensionada.save(nome_saida + extensao)
            print("Imagem redimensionada para 720p com sucesso!")
            # Transforma a imagem em .ppm
            self.img = Image.open(nome_saida + extensao)
            self.img.save(nome_saida + ".ppm")
            print(f"Convertido '{nome_entrada}' → '{nome_saida}.ppm'")
        else:
            print("Formato não suportado para conversão!")

        # Guarda o nome do arquivo PPM para uso posterior
        self.img = nome_saida + ".ppm"


    def reduzir_ppm(self, nome_entrada):
        """
        Lê arquivo .ppm do tipo P6 e salva um novo arquivo
        tirando os pixels das linhas impares e colunas impares.
        """

        with open(nome_entrada, "rb") as f:
            tipo = f.readline().strip() 
            while True:
                linha = f.readline()
                if not linha.startswith(b'#'):  
                    largura, altura = map(int, linha.split())
                    break
            max_valor = int(f.readline().strip())
            dados = f.read()

        pixels = [list(dados[i:i+3]) for i in range(0, len(dados), 3)]
        matriz = [pixels[i * largura:(i + 1) * largura] for i in range(altura)]
        matriz = [linha for i, linha in enumerate(matriz) if i % 2 == 0]
        nova_matriz = []
        for linha in matriz:
            nova_matriz.append([px for j, px in enumerate(linha) if j % 2 == 0])

        nova_altura = len(nova_matriz)
        nova_largura = len(nova_matriz[0])
        self.nome = self.nome_saida + "reduzida.ppm"
        with open(self.nome, "wb") as f:
            cabecalho = f"P6\n{nova_largura} {nova_altura}\n{max_valor}\n"
            f.write(cabecalho.encode())

            for linha in nova_matriz:
                for pixel in linha:
                    f.write(bytes(pixel))

        print(f"Imagem reduzida salva como '{self.nome}' ({nova_largura}x{nova_altura})")

    def aumentar_ppm(self, nome_entrada):
        with open(nome_entrada, "rb") as f:
            tipo = f.readline().strip()  
            while True:
                linha = f.readline()
                if not linha.startswith(b'#'):
                    largura, altura = map(int, linha.split())
                    break
            max_valor = int(f.readline().strip())
            dados = f.read()

        pixels = [list(dados[i:i+3]) for i in range(0, len(dados), 3)]
        matriz = [pixels[i * largura:(i + 1) * largura] for i in range(altura)]

        matriz_largura = []
        for linha in matriz:
            nova_linha = []
            for j in range(largura - 1):
                p1 = linha[j]
                p2 = linha[j + 1]
                nova_linha.append(p1)
                novo_px = [
                    (p1[0] + p2[0]) // 2,
                    (p1[1] + p2[1]) // 2,
                    (p1[2] + p2[2]) // 2
                ]
                nova_linha.append(novo_px)
            nova_linha.append(linha[-1])  
            nova_linha.append(linha[-1])  
            matriz_largura.append(nova_linha)

        nova_largura = len(matriz_largura[0])

        matriz_final = []
        for i in range(len(matriz_largura) - 1):
            linha1 = matriz_largura[i]
            linha2 = matriz_largura[i + 1]
            matriz_final.append(linha1)
            nova_linha = []
            for j in range(nova_largura):
                p1 = linha1[j]
                p2 = linha2[j]
                novo_px = [
                    (p1[0] + p2[0]) // 2,
                    (p1[1] + p2[1]) // 2,
                    (p1[2] + p2[2]) // 2
                ]
                nova_linha.append(novo_px)
            matriz_final.append(nova_linha)
        matriz_final.append(matriz_largura[-1]) 
        matriz_final.append(matriz_largura[-1])

        nova_altura = len(matriz_final)
        self.nome = self.nome_saida + "aumentado.ppm"
        with open(self.nome, "wb") as f:
            cabecalho = f"P6\n{nova_largura} {nova_altura}\n{max_valor}\n"
            f.write(cabecalho.encode())

            for linha in matriz_final:
                for pixel in linha:
                    f.write(bytes(pixel))

        print(f"Imagem aumentada salva como '{self.nome}' ({nova_largura}x{nova_altura})")


    def calcular_erro(self, nome_original, nome_processada):
        def ler_ppm(nome):
            with open(nome, "rb") as f:
                tipo = f.readline().strip()
                while True:
                    linha = f.readline()
                    if not linha.startswith(b'#'):
                        largura, altura = map(int, linha.split())
                        break
                max_valor = int(f.readline().strip())
                dados = f.read()
            pixels = [list(dados[i:i+3]) for i in range(0, len(dados), 3)]
            return largura, altura, pixels

        largura1, altura1, pixels1 = ler_ppm(nome_original)
        largura2, altura2, pixels2 = ler_ppm(nome_processada)

        if largura1 != largura2 or altura1 != altura2:
            raise ValueError("As imagens devem ter o mesmo tamanho para comparar!")

        # Calcula soma dos erros quadráticos
        soma_erro = 0
        for p1, p2 in zip(pixels1, pixels2):
            for c1, c2 in zip(p1, p2):
                soma_erro += (c1 - c2) ** 2

        n = largura1 * altura1 * 3  # total de canais
        rmse = math.sqrt(soma_erro / n)
        print(f"RMSE entre as imagens: {rmse}")
        return rmse


imagem = ManipularImage("eu.jpg", "foto")
imagem.reduzir_ppm("foto.ppm")
imagem.aumentar_ppm("fotoreduzida.ppm")
imagem.calcular_erro("foto.ppm", "fotoaumentado.ppm") # Questão 1
imagem.calcular_erro("foto.ppm", "foto_media_5x5.ppm") # Questão 2 5x5
imagem.calcular_erro("foto.ppm", "foto_gauss_sigma_40.ppm") # Questão 2 gauss

