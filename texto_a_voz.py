'''Este proyecto es convertir un artículo existente en un archivo de audio reproducible
en formato mp3. '''

import tkinter as tk
from tkinter import messagebox
from gtts import gTTS
from newspaper import Article

class textToAudio:
    '''Clase que convierte un artículo de una URL a un archivo de audio mp3.'''
    def __init__(self, url):
        '''Inicializa la clase con la URL del artículo a convertir.'''
        self.url = url
        self.article = Article(self.url)

    def convert(self):
        '''Convierte el artículo a un archivo de audio mp3.'''
        self.article.download()
        self.article.parse()
        text = self.article.text
        if not text.strip():
            print("Error: No se pudo extraer texto de esta URL. Asegúrate de que sea un artículo válido.")
            return
        tts = gTTS(text, lang='es')
        tts.save('audio.mp3')

class ConversorApp:
    '''Clase que maneja la parte visual del programa y la interaccion con el usuario.'''
    def __init__(self, root):
        '''Inicializa la clase y configura la ventana.'''
        self.root = root
        self.root.title("Conversor de Artículo a Audio")
        self.root.geometry("450x200")
        self.root.resizable(False, False)

        # Componentes visuales (Etiqueta, Entrada de texto y Botón)
        self.label = tk.Label(root, text="Introduce la URL del artículo:", font=("Arial", 11))
        self.label.pack(pady=15)

        self.url_entry = tk.Entry(root, width=50, font=("Arial", 10))
        self.url_entry.pack(pady=5)
        self.url_entry.focus() # Enfoca el cursor automáticamente aquí

        self.btn_convertir = tk.Button(
            root, 
            text="Convertir a MP3", 
            command=self.ejecutar_conversion,
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 10, "bold"),
            padx=10, 
            pady=5
        )
        self.btn_convertir.pack(pady=20)

    def ejecutar_conversion(self):
        '''Lee la URL, invoca a textToAudio y maneja las alertas al usuario.'''
        url_ingresada = self.url_entry.get().strip()

        # Validación si el campo está vacío
        if not url_ingresada:
            messagebox.showwarning("Falta URL", "Por favor, ingresa una URL antes de continuar.")
            return

        try:
            # Usamos tu clase textToAudio para procesar la lógica
            procesador = textToAudio(url_ingresada)
            procesador.convert()
            
            # Si todo sale bien, mostramos mensaje de éxito
            messagebox.showinfo("¡Éxito!", "El artículo ha sido convertido a audio y guardado como 'audio.mp3'")
            self.url_entry.delete(0, tk.END) # Limpia el campo para la próxima

        except Exception as e:
            # Si algo falla (el error que pusimos arriba o problemas de red), avisa al usuario
            messagebox.showerror("Error", f"Ocurrió un problema:\n{str(e)}")
        

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import messagebox
    
    root_ventana = tk.Tk()
    app = ConversorApp(root_ventana)
    root_ventana.mainloop()