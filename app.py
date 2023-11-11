from flask import Flask, request, jsonify, send_file
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
import uuid
import random

app = Flask(__name__)
ROOT_FOLDER="/home/arthurbmello/video-creation/videos/"
os.chdir(ROOT_FOLDER)

def criar_id_temporario():
    temp_id = str(uuid.uuid4())
    return temp_id

def salvar_arquivos_enviados(arquivos_enviados, caminho_pasta):
    caminho_pasta=ROOT_FOLDER+caminho_pasta
    # Criar a pasta de destino
    os.makedirs(caminho_pasta+'/saida', exist_ok=True)

    caminhos_arquivos = []
    for arquivo_enviado in arquivos_enviados:
        # Salva cada arquivo enviado na pasta de destino
        caminho_arquivo = os.path.join(caminho_pasta, arquivo_enviado.name)
        with open(caminho_arquivo, "wb") as arquivo:
            arquivo.write(arquivo_enviado.read())
        caminhos_arquivos.append(caminho_arquivo)

    return caminhos_arquivos

# Função para escolher aleatoriamente um arquivo de vídeo de uma pasta
def escolher_video_aleatorio(pasta):
    pasta=ROOT_FOLDER+'/'+pasta
    videos = [f for f in os.listdir(pasta) if f.endswith(".mp4")]
    if videos:
        return os.path.join(pasta, random.choice(videos))
    else:
        return None

def criar_sequencia_videos(recortes_clientes, pasta_cliente):

    vinheta_entrada = "vinheta_entrada.mp4"
    pastas_recortes = ["recorte3", "recorte4", "recorte6", "recorte7", "recorte9", "recorte10"]
    vinheta_fim = "vinheta_fim.mp4"

    # Caminhos para os arquivos de entrada e saída
    saida = f"{ROOT_FOLDER}/{pasta_cliente}/saida/filme_personalizado.mp4"

    # Inicializar a sequência com a vinheta de entrada
    sequencia = VideoFileClip(vinheta_entrada)

    # Adicionar os recortes dos clientes e recortes aleatórios
    for i in range(4):
        # Adicionar recorte do cliente
        recorte_cliente = recortes_clientes[i]
        sequencia = concatenate_videoclips([sequencia, VideoFileClip(recorte_cliente)])

        # Adicionar recorte aleatório
        if i * 2 < len(pastas_recortes):
            recorte_aleatorio1 = escolher_video_aleatorio(pastas_recortes[i * 2])
            if recorte_aleatorio1:
                sequencia = concatenate_videoclips([sequencia, VideoFileClip(recorte_aleatorio1)])

        if i * 2 + 1 < len(pastas_recortes):
            recorte_aleatorio2 = escolher_video_aleatorio(pastas_recortes[i * 2 + 1])
            if recorte_aleatorio2:
                sequencia = concatenate_videoclips([sequencia, VideoFileClip(recorte_aleatorio2)])

    # Adicionar a vinheta de fim
    sequencia = concatenate_videoclips([sequencia, VideoFileClip(vinheta_fim)])

    # ENVIAR MENSAGEM PARA O CLIENTE QUE O FILME FOI PRODUZIDO

    # Salvar o filme personalizado
    sequencia.write_videofile(saida, codec="libx264")
    return saida

@app.route('/', methods=['POST'])
def gerar_sequencia():
    if 'files[]' not in request.files:
        return jsonify({'error': 'Nenhum arquivo encontrado'}), 400

    arquivos = request.files.getlist('files[]')

    if not arquivos:
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    id_temporario = criar_id_temporario()
    pasta_cliente = f'cliente/{id_temporario}'
    arquivos_enviados = salvar_arquivos_enviados(arquivos, pasta_cliente)

    # Chama a função criar_sequencia_videos com a lista de caminhos dos arquivos enviados
    saida = criar_sequencia_videos(arquivos_enviados, pasta_cliente)

    #return jsonify({'message': 'Arquivos enviados e função criar_sequencia_videos executada com sucesso'}), 200
    return send_file(saida)

if __name__ == '__main__':
    app.run(debug=True)