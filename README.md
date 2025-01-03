
# **Downloader de Vídeos do Instagram, YouTube e TikTok**

Este projeto é um **Downloader de Vídeos** desenvolvido em Python, utilizando o `yt-dlp` para baixar vídeos de plataformas como instagram, YouTube e TikTok. O script possui uma interface gráfica (GUI) simples construída com o módulo `tkinter`, permitindo ao usuário selecionar a URL do vídeo, escolher se deseja baixar áudio, selecionar o diretório de destino e acompanhar o progresso do download.

## **Requisitos**

Antes de usar o script, você precisará garantir que todos os pacotes necessários estejam instalados em seu sistema. O script usa os seguintes pacotes:

- **yt-dlp**: Biblioteca para download de vídeos de várias plataformas.
- **tkinter**: Biblioteca para criação da interface gráfica.
- **subprocess**: Para executar comandos do sistema (como verificar a instalação do FFmpeg).
- **threading**: Para rodar o download em segundo plano sem bloquear a interface.

### **Instalação dos Pacotes Necessários**

1. **Instalar `yt-dlp` e `tkinter`**:

   Você pode usar o seguinte script para instalar os pacotes necessários:

   ```bash
   pip install yt-dlp
   ```

   **Nota**: `tkinter` já deve estar pré-instalado com o Python, mas em alguns sistemas, você pode precisar instalá-lo manualmente.

2. **Instalar o FFmpeg**:

   Para baixar vídeos com o melhor formato de vídeo e áudio, o script usa o **FFmpeg**. Se você não tem o FFmpeg instalado, o script tenta localizá-lo automaticamente. Caso não consiga, você pode instalar o FFmpeg manualmente:

   - No Windows, use o **winget**:
   
     ```bash
     winget install ffmpeg
     ```

   Ou baixe a versão mais recente do FFmpeg em [ffmpeg.org](https://ffmpeg.org/download.html) e adicione o caminho para o executável do FFmpeg no código.

## **Como Usar o Script**

1. **Execute o Script**:
   
   Abra o terminal e execute o arquivo Python:

   ```bash
   python seu_arquivo.py
   ```

2. **Interface Gráfica**:
   
   - **URL do Vídeo**: Insira a URL do vídeo do YouTube ou TikTok no campo de entrada.
   - **Baixar apenas o áudio**: Marque esta caixa de seleção se você quiser baixar apenas o áudio do vídeo.
   - **Caminho do diretório**: Você pode selecionar o diretório onde o vídeo será salvo. Caso contrário, o script salvará o vídeo no diretório padrão.
   - **Botão "Selecionar Diretório"**: Clique para escolher o diretório onde os vídeos serão salvos.
   - **Botão "Baixar Vídeo"**: Clique para iniciar o download do vídeo.

## **Estrutura do Código**

### **Funções principais**:

1. **`find_ffmpeg()`**: 
   - Procura o executável `ffmpeg` no seu sistema usando o comando `where` no Windows.
   - Retorna o caminho do FFmpeg, ou `None` caso não seja encontrado.

2. **`list_formats(url)`**:
   - Exibe a lista de formatos disponíveis para o vídeo fornecido (apenas para fins de depuração).

3. **`download_video(url, path, audio_only, progress_callback)`**:
   - Baixa o vídeo ou áudio usando `yt-dlp`.
   - Se o vídeo de uma plataforma específica (como YouTube ou TikTok) não tiver a resolução especificada, o script seleciona o melhor formato disponível.

4. **`progress_hook(d)`**:
   - Função de callback para atualizar a barra de progresso durante o download.

5. **`start_download()`**:
   - Inicia o download do vídeo em uma nova thread para que a interface gráfica não trave.

6. **`browse_folder()`**:
   - Abre uma janela de seleção de diretório para que o usuário possa escolher onde salvar o vídeo.

### **Componentes da Interface Gráfica**:

- **Campos de Entrada**: Para a URL do vídeo e o diretório onde o vídeo será salvo.
- **Checkbox**: Para escolher se o áudio deve ser baixado.
- **Botões**: Para iniciar o download e selecionar o diretório.
- **Barra de Progresso**: Exibe o progresso do download.
- **Rótulos**: Para mostrar informações sobre o progresso, velocidade e resultados do download.
- **Debug**: Exibe informações sobre os formatos de vídeo disponíveis para fins de diagnóstico.

## **Exemplo de Uso**:

1. Insira a URL do vídeo desejado no campo de entrada (exemplo: `https://www.youtube.com/watch?v=0G7HX16YTLU`).
2. Marque a opção "Baixar apenas o áudio" se desejar baixar apenas o áudio.
3. Clique em "Selecionar Diretório" para escolher onde salvar o vídeo.
4. Clique em "Baixar Vídeo" para iniciar o download.
5. A barra de progresso será atualizada conforme o download avança. Quando o download for concluído, a mensagem "Download Concluído!" será exibida.

## **Problemas Comuns e Soluções**:

1. **FFmpeg não encontrado**:
   - Certifique-se de que o FFmpeg está corretamente instalado e acessível no sistema. Se o script não encontrar o FFmpeg, ele exibirá uma mensagem de erro.

2. **Erro ao baixar formatos**:
   - Se a resolução selecionada não estiver disponível, o script automaticamente usará o melhor formato disponível. Certifique-se de que o vídeo não está protegido por DRM ou em um formato não suportado.

3. **Dependências ausentes**:
   - Se você não tiver o `yt-dlp` ou outros pacotes, o script mostrará um erro. Execute o comando de instalação para garantir que todas as dependências estejam presentes:
   
   ```bash
   pip install yt-dlp
   ```

---

# **Conclusão**

Este projeto oferece uma maneira simples e eficiente de baixar vídeos de plataformas populares como YouTube e TikTok. Com a interface gráfica fácil de usar e suporte para múltiplos formatos, ele torna o processo de download mais acessível.
