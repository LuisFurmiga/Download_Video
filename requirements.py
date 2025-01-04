import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def install_ffmpeg():
    """Função para instalar o ffmpeg via winget."""
    try:
        subprocess.check_call(["winget", "install", "ffmpeg"])
        print("FFmpeg foi instalado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Ocorreu um erro ao tentar instalar o FFmpeg: {e}")

required_packages = [
    "yt-dlp"
]

# Instalar pacotes Python
for package in required_packages:
    install(package)

# Instalar FFmpeg
install_ffmpeg()

print("Todos os pacotes necessários foram instalados com sucesso!")
