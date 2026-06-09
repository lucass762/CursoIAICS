import cv2

def detectar_rostos():
    # Carregar o classificador pré-treinado de faces
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Ler a imagem
    img = cv2.imread('multidao.png')
    
    if img is None:
        print("Erro: Não foi possível carregar a imagem 'pessoas.png'. Verifique se o arquivo existe.")
        return

    # Converter para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detectar rostos
    # scaleFactor: compensa o fato de alguns rostos estarem mais perto da câmera do que outros
    # minNeighbors: quantos vizinhos cada retângulo candidato deve ter para ser mantido
    rostos = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=0, minSize=(10, 10))

    print(f"Foram detectados {len(rostos)} rostos.")

    # Desenhar o quadrado verde em volta de cada rosto
    # Cor BGR: (0, 255, 0) é verde, espessura: 2
    for (x, y, w, h) in rostos:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Salvar o resultado
    cv2.imwrite('multidao_com_rostos.png', img)
    print("Imagem salva com sucesso como 'multidao_com_rostos.png'.")

    # Tentar mostrar a imagem (pode não funcionar em ambientes sem interface gráfica)
    try:
        cv2.imshow('Detecção de Rostos', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception:
        print("Aviso: Não foi possível exibir a janela da imagem (ambiente sem GUI).")

if __name__ == "__main__":
    detectar_rostos()