import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import yt_dlp
import os
import subprocess
import threading

def find_ffmpeg():
    """ Tenta encontrar o caminho do ffmpeg utilizando o comando 'where' no Windows. """
    try:
        # Obter todos os caminhos do ffmpeg
        ffmpeg_paths = subprocess.check_output(['where', 'ffmpeg'], stderr=subprocess.STDOUT, universal_newlines=True).strip().split('\n')
        
        if ffmpeg_paths:
            return ffmpeg_paths[0]  # Retorna o primeiro caminho encontrado
    except subprocess.CalledProcessError:
        return None  # Caso o ffmpeg não seja encontrado

def list_formats(url):
    """Função para listar os formatos e resoluções do vídeo para fins de debug visual."""
    try:
        ydl_opts = {
            'format': 'bestaudio',  # Não baixar o vídeo, apenas pegar informações
            'noplaylist': True,     # Impedir o download de playlists
            'quiet': True,          # Silenciar a saída
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Obtendo informações do vídeo
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])

            if formats:
                debug_info = "Formatos disponíveis:\n"
                for f in formats:
                    # Adiciona as informações de formato e resolução
                    debug_info += f"ID: {f['format_id']}, Resolução: {f.get('height', 'N/A')}, Formato: {f['ext']}\n"
                debug_label.config(text=debug_info)  # Exibe no label de debug
            else:
                debug_label.config(text="Nenhum formato encontrado.")
    except Exception as e:
        debug_label.config(text=f"Erro ao listar formatos: {e}")

def download_video(url, path='.', audio_only=False, progress_callback=None):
    ffmpeg_path = find_ffmpeg()  # Encontrar o caminho do ffmpeg

    if ffmpeg_path:
        print(f"ffmpeg encontrado em: {ffmpeg_path}")
    else:
        print("ffmpeg não encontrado no sistema.")
        result_label.config(text="ffmpeg não encontrado no sistema.")
        return

    try:
        # Baixar o vídeo e o áudio
        ydl_opts = {
            'quiet': False,  # Exibir mais informações durante o download
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),  # Salvar com o nome do vídeo
            'noplaylist': True,  # Impedir o download de playlists
            'ffmpeg_location': ffmpeg_path,  # Caminho do ffmpeg se necessário
            'progress_hooks': [progress_callback],  # Definir o callback para progresso

            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extrair as informações do vídeo
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])

            # Exibe os formatos no console para depuração
            #list_formats(url)

            # Filtrar por resolução das fontes de vídeo
            if "www.twitch.tv" in url:
                RESOLUTION = 1080
                selected_format = next((f for f in formats if f.get('height') == RESOLUTION and f['ext'] == 'mp4'), None)
            elif "www.tiktok.com" in url:
                RESOLUTION = 1920
                selected_format = next((f for f in formats if f.get('height') == RESOLUTION and f['ext'] == 'webm' or f['ext'] == 'mp4'), None)
            else:
                RESOLUTION = 1080
                selected_format = next((f for f in formats if f.get('height') == RESOLUTION and f['ext'] == 'webm'), None)

            if selected_format:
                # Inicia o download com o formato selecionado
                if "www.youtube.com" in url or "www.instagram.com" in url or "https://youtu.be" in url:
                    ydl_opts['format'] = selected_format['format_id']+f"+bestaudio" if not audio_only else 'bestaudio'
                else:
                    ydl_opts['format'] = selected_format['format_id']
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            else:
                print(f"Formato {RESOLUTION} não encontrado. Usando o melhor formato disponível.")
                # Usar o melhor formato caso o resolução não esteja disponível
                ydl_opts['format'] = 'bestvideo+bestaudio'
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

        print(f"Download completo! O vídeo foi salvo em {path}")
        result_label.config(text="Download Concluído!")
        progress_bar.grid_forget()  # Esconde a barra de progresso quando o download terminar
        percentage_label.config(text="100%")  # Atualiza a porcentagem para 100%
        speed_label.config(text="Velocidade: 0 KB/s")  # Atualiza a velocidade para 0

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        result_label.config(text=f"Ocorreu um erro: {e}")


def progress_hook(d):
    """ Função de callback para atualizar a barra de progresso. """
    if d['status'] == 'downloading':
        # Verificar se 'total_bytes' existe no dicionário
        if 'total_bytes' in d:
            # Atualiza a barra de progresso com a porcentagem
            progress = d['downloaded_bytes'] / d['total_bytes'] * 100
            progress_bar['value'] = progress
            
            # Atualiza a porcentagem
            percentage_label.config(text=f"{int(progress)}%")
        else:
            # Para transmissões HLS, use o número de fragmentos como base para o progresso
            if 'fragment' in d:
                fragment_progress = d['fragment'] / d.get('fragment_count', 1) * 100
                progress_bar['value'] = fragment_progress
                percentage_label.config(text=f"{int(fragment_progress)}%")
        
        # Verifica se a velocidade foi retornada, senão, define como 0
        download_speed = d.get('speed', 0)  # Se 'speed' for None, usa 0
        
        if download_speed is not None:
            download_speed = download_speed / 1024  # Velocidade em KB/s
        else:
            download_speed = 0
        
        speed_label.config(text=f"Velocidade: {download_speed:.2f} KB/s")

        root.update_idletasks()  # Atualiza a interface gráfica
    elif d['status'] == 'finished':
        progress_bar['value'] = 100
        result_label.config(text="Download Concluído!")

def start_download():
    url = url_entry.get()
    download_path = path_entry.get() or '.'
    audio_only = audio_checkbox_var.get()  # Verifica se a checkbox de áudio foi marcada

    if not url:
        result_label.config(text="Por favor, insira a URL do vídeo.")
        return

    # Limpa a mensagem de resultado antes de iniciar um novo download
    result_label.config(text="")

    # Mostra a barra de progresso
    progress_bar.grid(row=5, column=0, columnspan=2, pady=5)
    percentage_label.grid(row=6, column=0, pady=5)  # Mostra a porcentagem
    speed_label.grid(row=6, column=1, pady=5)  # Mostra a velocidade

    # Inicia a thread para baixar o vídeo
    download_thread = threading.Thread(target=download_video, args=(url, download_path, audio_only, progress_hook))
    download_thread.start()

def browse_folder():
    folder_selected = filedialog.askdirectory(initialdir=os.path.dirname(__file__))
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Downloader de Vídeos")

# URL do vídeo
url_label = tk.Label(root, text="URL do Vídeo:")
url_label.grid(row=0, column=0, pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, pady=5)

# Checkbox para escolher se o áudio será baixado
audio_checkbox_var = tk.BooleanVar()
audio_checkbox = tk.Checkbutton(root, text="Baixar apenas o áudio", variable=audio_checkbox_var)
audio_checkbox.grid(row=1, column=0, columnspan=2, pady=5)

# Caminho do diretório
path_label = tk.Label(root, text="Caminho do diretório (opcional):")
path_label.grid(row=2, column=0, pady=5)

# Campo para mostrar o diretório selecionado
path_entry = tk.Entry(root, width=50)
path_entry.grid(row=3, column=0, columnspan=2, pady=5)
path_entry.insert(0, os.path.dirname(__file__))  # Define o diretório padrão para o diretório onde o script está localizado

# Botão para escolher o diretório
browse_button = tk.Button(root, text="Selecionar Diretório", command=browse_folder)
browse_button.grid(row=4, column=0, pady=5)

# Botão de download
download_button = tk.Button(root, text="Baixar Vídeo", command=start_download)
download_button.grid(row=4, column=1, pady=5)

# Barra de progresso (inicialmente oculta)
progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
progress_bar.grid_forget()  # Barra de progresso escondida no início

# Rótulo de porcentagem
percentage_label = tk.Label(root, text="0%", fg="blue")
percentage_label.grid_forget()  # Escondido inicialmente

# Rótulo de velocidade
speed_label = tk.Label(root, text="Velocidade: 0 KB/s", fg="blue")
speed_label.grid_forget()  # Escondido inicialmente

# Rótulo de resultado
result_label = tk.Label(root, text="", fg="green")
result_label.grid(row=7, column=0, columnspan=3, pady=5)

# Rótulo de debug (listagem de formatos e resoluções)
debug_label = tk.Label(root, text="", fg="red", justify="left")
debug_label.grid(row=8, column=0, columnspan=3, pady=5)

# Executar a interface
root.mainloop()
