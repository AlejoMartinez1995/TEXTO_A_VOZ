'''Este proyecto convierte un artículo existente en un archivo de audio reproducible en formato mp3.'''

from gtts import gTTS
import requests
from bs4 import BeautifulSoup

class textToAudio:
    '''Clase que convierte un artículo de una URL a un archivo de audio mp3.'''
    def __init__(self, url):
        '''Inicializa la clase con la URL del artículo a convertir.'''
        self.url = url
        # Creamos un objeto simulado para mantener compatibilidad con tu estructura original
        self.article = type('MockArticle', (object,), {'text': ''})()

    def convert(self):
        '''Convierte el artículo a un archivo de audio mp3.'''
        # Hacemos la descarga de forma directa
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(self.url, headers=headers, timeout=10)
        
        # Parseamos el HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos los párrafos típicos de un artículo
        parrafos = soup.find_all('p')
        texto_extraido = "\n".join([p.get_text() for p in parrafos])
        
        self.article.text = texto_extraido

        if not texto_extraido.strip():
            print("Error: No se pudo extraer texto de esta URL. Asegúrate de que sea un artículo válido.")
            return
            
        tts = gTTS(texto_extraido, lang='es')
        tts.save('audio.mp3')

class ConversorApp:
    '''Clase que maneja la parte visual del programa y la interacción con el usuario.'''
    def __init__(self, root):
        self.root = root
        # El resto de tu configuración de Tkinter queda idéntica si usás la app local...

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import messagebox
    root_ventana = tk.Tk()
    app = ConversorApp(root_ventana)
    root_ventana.mainloop()