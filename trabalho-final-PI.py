def criar_arquivo_ppm(largura, altura, pixels, nome_arquivo, tipo, tons=0):
    with open(nome_arquivo, 'w') as arquivo:
        # Escreve o cabeçalho do arquivo PBM
        arquivo.write(f"{tipo}\n")
        arquivo.write(f"{largura} {altura}\n")
        if(tipo=='P2' or tipo=='P3' ):
            # Valor máximo de cinza entre, sendo 0 preto e 20 branco
            arquivo.write(f"{tons}\n")
        # Escreve os pixels no arquivo
        if tipo == 'P3':
            for linha in pixels:
                linha_str = ''
                for pixel in linha:
                    pixel_str = ' '.join(map(str, pixel))
                    linha_str += ' ' + pixel_str
                arquivo.write(f"{linha_str}\n")
        else:
            for linha in pixels:
                linha_str = ' '.join(map(str, linha))
                arquivo.write(f"{linha_str}\n")

def ler_arquivo_pbm(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

        # Remove linhas em branco e comentários
        linhas = [linha.strip() for linha in linhas if linha.strip() and not linha.strip().startswith('#')]

        # Obtém largura e altura da imagem a partir do cabeçalho
        largura, altura = map(int, linhas[1].split())

        # Remove o cabeçalho e comentários
        dados_linhas = [linha for linha in linhas[2:] if not linha.startswith('#')]

        # Junta as linhas de dados em uma única string
        dados_str = ''.join(dados_linhas)

        # Divide a string de dados em linhas com a largura correta
        pixels = [[int(dados_str[i + j * largura]) for i in range(largura)] for j in range(altura)]

        return largura, altura, pixels
    

# dilatar pixels em uma mascara em forma de T
def dilatar(pixels):
    altura = len(pixels)
    largura = len(pixels[0])
    novos_pixels = [[0 for _ in range(largura)] for _ in range(altura)]
    for y in range(altura):
        for x in range(largura):
            if pixels[y][x] == 1:
                novos_pixels[y][x] = 1
                if x + 1 < largura:
                    novos_pixels[y][x + 1] = 1
                    novos_pixels[y][x + 2] = 1
                    novos_pixels[y][x + 3] = 1
                    novos_pixels[y][x + 4] = 1
                if x - 1 >= 0:
                    novos_pixels[y][x - 1] = 1
                    novos_pixels[y][x - 2] = 1
                    novos_pixels[y][x - 3] = 1
                    novos_pixels[y-1][x] = 1
                    novos_pixels[y-2][x] = 1
                    novos_pixels[y-3][x] = 1
    return novos_pixels


# busca por palavras na imagem utilizando BFS
from collections import deque

def bfs(matrix, start_i, start_j, visited):
    queue = deque([(start_i, start_j)])
    connected_pixels = []
    
    while queue:
        i, j = queue.popleft()
        if 0 <= i < len(matrix) and 0 <= j < len(matrix[0]) and not visited[i][j] and matrix[i][j] == 1:
            visited[i][j] = True
            connected_pixels.append((i, j))
            queue.extend([(i+1, j), (i-1, j), (i, j+1), (i, j-1)])
    
    return connected_pixels

def find_words(matrix):
    visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    words_count = 0
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1 and not visited[i][j]:
                connected_pixels = bfs(matrix, i, j, visited)
                # Count the connected pixels as one word
                words_count += 1
                
                # Check for distance between letters
                if words_count > 1:
                    last_word_end = connected_pixels[-1]
                    last_word_start = connected_pixels[0]
                    distance = ((last_word_end[0] - last_word_start[0]) ** 2 + 
                                (last_word_end[1] - last_word_start[1]) ** 2) ** 0.5
                    # If distance between words is greater than 9, consider them different words
                    if distance > 9:
                        words_count += 1
    
    return words_count

def remover_ruido_sal_pimenta(pixels, mascara=3):
    import copy
    
    # Cria uma cópia da matriz de pixels
    novos_pixels = copy.deepcopy(pixels)
    
    # Tamanho da imagem
    altura = len(pixels)
    largura = len(pixels[0])
    
    # Define o raio da mascara
    raio_mascara = mascara // 2
    
    # Verifica cada pixel na matriz
    for y in range(altura):
        for x in range(largura):
            pixel_central = pixels[y][x]
            
            # Cria uma lista para armazenar os valores dos pixels na mascara
            valores_mascara = []
            
            # Verifica os vizinhos dentro da mascara
            for j in range(-raio_mascara, raio_mascara + 1):
                for i in range(-raio_mascara, raio_mascara + 1):
                    if 0 <= y + j < altura and 0 <= x + i < largura:
                        valor_vizinho = pixels[y + j][x + i]
                        valores_mascara.append(valor_vizinho)
            
            # Calcula o valor da mediana na mascara
            valor_mediana = sorted(valores_mascara)[len(valores_mascara) // 2]
            
            # Se o pixel central for diferente da mediana, substitua-o pela mediana
            if pixel_central != valor_mediana:
                novos_pixels[y][x] = valor_mediana
                
    return novos_pixels

# Exemplo de uso 1
largura, altura, pixels = ler_arquivo_pbm("trabalho final/lorem_s12_c02_espacos_noise.pbm")

pixels = remover_ruido_sal_pimenta(pixels)

novos_pixels = dilatar(pixels)

num_palavras = find_words(novos_pixels)

criar_arquivo_ppm(largura, altura, novos_pixels, f"trabalho final/grupo_11_imagem_1_linhas_{'x'}_palavras_{num_palavras}.pbm", 'P1')




