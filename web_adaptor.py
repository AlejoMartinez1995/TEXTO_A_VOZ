'''
Adaptador Web Real para el Conversor de Artículo a Audio.
Conecta la interfaz web directamente con tu clase textToAudio.
'''
from flask import Flask, render_template_string, request, send_file, jsonify
import importlib
import io

app = Flask(__name__)

NOMBRE_ARCHIVO_ORIGINAL = 'texto_a_voz'

try:
    modulo_original = importlib.import_module(NOMBRE_ARCHIVO_ORIGINAL)
    textToAudio = getattr(modulo_original, 'textToAudio')
except Exception as e:
    textToAudio = None

HTML_CONVERSOR = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conversor de Artículo a MP3</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; text-align: center; margin-top: 50px; background-color: #f4f7f6; color: #333; }
        .contenedor { background: white; padding: 30px; display: inline-block; border-radius: 8px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); max-width: 500px; width: 90%; }
        h2 { color: #028090; margin-bottom: 20px; }
        p { color: #666; font-size: 0.95rem; margin-bottom: 20px; }
        input[type="text"] { width: 100%; padding: 12px; margin-bottom: 20px; border: 2px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 1rem; }
        input[type="text"]:focus { border-color: #00a896; outline: none; }
        button { padding: 12px 25px; background-color: #00a896; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; font-weight: bold; width: 100%; }
        button:hover { background-color: #028090; }
        .status { margin-top: 20px; font-weight: bold; color: #028090; min-height: 20px; }
        .error { color: #e63946; }
    </style>
</head>
<body>
    <div class="contenedor">
        <h2>Conversor de Artículo a Audio</h2>
        <p>Introduce la URL de un artículo web para extraer su texto y generar un archivo MP3 reproducible.</p>
        <input type="text" id="url-input" placeholder="https://ejemplo.com/articulo" autocomplete="off">
        <button id="btn-submit" onclick="convertirArticulo()">Convertir a MP3</button>
        <div id="status-msg" class="status"></div>
    </div>

    <script>
        function convertirArticulo() {
            const urlInput = document.getElementById('url-input').value.trim();
            const statusDiv = document.getElementById('status-msg');
            const btn = document.getElementById('btn-submit');

            if (!urlInput) {
                statusDiv.className = "status error";
                statusDiv.innerText = "Por favor, ingresa una URL antes de continuar.";
                return;
            }

            statusDiv.className = "status";
            statusDiv.innerText = "Procesando artículo y generando MP3...";
            btn.disabled = true;

            fetch('/api/convertir', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: urlInput })
            })
            .then(res => {
                if (!res.ok) return res.json().then(err => { throw new Error(err.error || "Error en el servidor"); });
                return res.blob();
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'audio_articulo.mp3';
                document.body.appendChild(a);
                a.click();
                a.remove();
                
                statusDiv.innerText = "¡Audio MP3 descargado con éxito!";
                document.getElementById('url-input').value = "";
                btn.disabled = false;
            })
            .catch(err => {
                statusDiv.className = "status error";
                statusDiv.innerText = err.message;
                btn.disabled = false;
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_CONVERSOR)

@app.route('/api/convertir', methods=['POST'])
def convertir_api():
    data = request.get_json()
    url = data.get('url')

    if not textToAudio:
        return jsonify({"error": "No se pudo cargar el módulo lógico original."}), 500

    try:
        conversor = textToAudio(url)
        # Ejecutamos la descarga usando BeautifulSoup
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        import requests
        from bs4 import BeautifulSoup
        from gtts import gTTS
        
        res = requests.get(conversor.url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        texto_extraido = "\n".join([p.get_text() for p in soup.find_all('p')])
        
        if not texto_extraido.strip():
            return jsonify({"error": "No se pudo extraer suficiente texto de esta URL."}), 400
        
        tts = gTTS(texto_extraido, lang='es')
        
        buffer_audio = io.BytesIO()
        tts.write_to_fp(buffer_audio)
        buffer_audio.seek(0)
        
        return send_file(
            buffer_audio,
            mimetype='audio/mp3',
            as_attachment=True,
            download_name='audio_articulo.mp3'
        )

    except Exception as e:
        return jsonify({"error": f"Error al procesar: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)