from flask import Flask, render_template_string, request, redirect
import os

app = Flask(__name__)

STREAMLIT_DEFAULT = os.environ.get('STREAMLIT_URL', 'http://localhost:8501')

EMBED_HTML = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Embed · Predictor Salud Mental</title>
  <style>
    html,body{height:100%;margin:0}
    .frame{width:100%;height:100vh;border:none}
  </style>
</head>
<body>
  <iframe id="streamlit-embed" class="frame" src="{{ url }}" title="Predictor de Adicción — Streamlit" allow="clipboard-write" loading="lazy"></iframe>
</body>
</html>
"""

@app.route('/embed')
def embed():
    """Página embebible que carga la app Streamlit en un iframe.
    Puedes establecer la URL objetivo mediante la variable de entorno STREAMLIT_URL
    o añadiendo el query param ?url=... al request.
    """
    url = request.args.get('url') or STREAMLIT_DEFAULT
    return render_template_string(EMBED_HTML, url=url)

@app.route('/embed/redirect')
def embed_redirect():
    """Redirige directamente a la URL de Streamlit (útil si prefieres abrirla en nueva pestaña)."""
    url = request.args.get('url') or STREAMLIT_DEFAULT
    return redirect(url)

if __name__ == '__main__':
    port = int(os.environ.get('EMBED_PORT', 5000))
    app.run(host='0.0.0.0', port=port)
