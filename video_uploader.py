import streamlit as st
import requests
import time
# Define the API endpoint to which you want to send videos.
#api_endpoint = "http://127.0.0.1:5000/"
api_endpoint = "https://arthurbmello.eu.pythonanywhere.com/"
limite_arquivos = 4

def main():
    st.title("Uploader de videos")

    # Upload dos videos
    arquivos_enviados = st.file_uploader("Escolha até 4 videos", accept_multiple_files=True, type=["mp4", "avi"])
    if len(arquivos_enviados) > limite_arquivos:
        st.warning(f"Número máximo de arquivos atingido. Apenas os primeiros {limite_arquivos} serão processados.")
        arquivos_enviados = arquivos_enviados[:limite_arquivos]

    # Manda os videos para processamento via API
    if st.button("Processar Arquivos") and arquivos_enviados:
        start_time = time.time()
        arquivos = [('files[]', (file.name, file.getvalue())) for file in arquivos_enviados]
        with st.spinner('Processando...'):
            with requests.Session() as session:
                try:
                    saida = requests.post(api_endpoint, files=arquivos).content
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")

            #saida = requests.post(api_endpoint, files=arquivos).content
            #saida = requests.post(api_endpoint, files=arquivos).content
        st.video(saida)
        print("--- %.2f segundos ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()