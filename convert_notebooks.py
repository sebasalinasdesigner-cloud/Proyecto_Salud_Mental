"""
convert_notebooks.py

Script sencillo para convertir todos los archivos .ipynb en la carpeta actual
a archivos .html usando `jupyter nbconvert`. No elimina los archivos .ipynb.

Uso:
    python convert_notebooks.py        # convierte todos los notebooks en la carpeta
    python convert_notebooks.py file.ipynb  # convierte un notebook específico

Requiere: `jupyter` (o al menos `nbconvert`) instalado. Puedes instalarlo con:
    pip install nbconvert

El script se limita a ejecutar `jupyter nbconvert --to html <notebook>` para
preservar el contenido original del .ipynb y generar un .html en la misma carpeta.
"""

import subprocess
from pathlib import Path
import sys


def convert_notebook(nb_path: Path) -> int:
    """Convierte un notebook a HTML usando jupyter nbconvert.
    Retorna 0 si fue exitoso, distinto de 0 en caso de error."""
    try:
        print(f"Convirtiendo: {nb_path} → {nb_path.with_suffix('.html')}")
        # Intentar usar el entrypoint 'jupyter' si está disponible
        try:
            subprocess.run(["jupyter", "nbconvert", "--to", "html", str(nb_path)], check=True)
            return 0
        except FileNotFoundError:
            # Si 'jupyter' no está en PATH, usar el intérprete actual con -m nbconvert
            subprocess.run([sys.executable, "-m", "nbconvert", "--to", "html", str(nb_path)], check=True)
            return 0
    except subprocess.CalledProcessError as e:
        print(f"Error al convertir {nb_path}: {e}", file=sys.stderr)
        return e.returncode


if __name__ == '__main__':
    p = Path('.').resolve()
    args = sys.argv[1:]

    if args:
        # Convertir archivos específicos pasados por argumento
        exit_codes = []
        for a in args:
            nb = Path(a)
            if not nb.exists():
                print(f"No se encontró el archivo: {nb}", file=sys.stderr)
                exit_codes.append(3)
                continue
            exit_codes.append(convert_notebook(nb))
        sys.exit(0 if all(c == 0 for c in exit_codes) else 1)

    # Si no hay args, convertir todos los .ipynb en la carpeta actual
    notebooks = sorted(p.glob('*.ipynb'))
    if not notebooks:
        print("No se encontraron archivos .ipynb en la carpeta actual.")
        sys.exit(0)

    any_error = False
    for nb in notebooks:
        code = convert_notebook(nb)
        if code != 0:
            any_error = True

    if any_error:
        print("Algunas conversiones fallaron. Revisa la salida anterior.")
        sys.exit(1)
    else:
        print("Conversión completada correctamente.")
        sys.exit(0)
