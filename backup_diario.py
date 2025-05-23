import os
import shutil
from datetime import datetime
from pathlib import Path

def limpiar_ruta(ruta):
    # Convierte a str y elimina comillas al inicio y fin si las tiene
    return str(ruta).strip('"')

# Rutas base
base_dir = Path(limpiar_ruta(Path(__file__).parent.resolve()))  # Directorio del script
db_filename = "base_datos_inventario.db"
carpetas_datos = ["fotos", "pdf_especificaciones", "pdf_documentaciones"]

# Ruta de respaldo en el escritorio
escritorio = Path(limpiar_ruta(os.path.join(os.environ["USERPROFILE"], "Desktop")))
carpeta_respaldo_base = escritorio / "copias_seguridad"
fecha_hoy = datetime.now().strftime("%Y-%m-%d")
carpeta_destino = carpeta_respaldo_base / f"copia_{fecha_hoy}"

# Crear carpeta de respaldo del día si no existe
os.makedirs(carpeta_destino, exist_ok=True)

# Copiar base de datos
ruta_db_origen = base_dir / limpiar_ruta(db_filename)
ruta_db_destino = carpeta_destino / limpiar_ruta(db_filename)
shutil.copy2(ruta_db_origen, ruta_db_destino)

# Copiar carpetas
for carpeta in carpetas_datos:
    carpeta_limpia = limpiar_ruta(carpeta)
    origen = base_dir / carpeta_limpia
    destino = carpeta_destino / carpeta_limpia
    if origen.exists():
        shutil.copytree(origen, destino)
    else:
        print(f"⚠️ La carpeta {carpeta_limpia} no existe y no se ha copiado.")

print(f"✅ Copia de seguridad completada en: {carpeta_destino}")
