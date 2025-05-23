import os
import shutil
from datetime import datetime
from pathlib import Path

# Rutas base
base_dir = Path(__file__).parent.resolve()  # Directorio del script
db_filename = "base_datos_inventario.db"
carpetas_datos = ["fotos", "pdf_especificaciones", "pdf_documentaciones"]

# Ruta de respaldo en el escritorio
escritorio = Path.home() / "Escritorio"
carpeta_respaldo_base = escritorio / "copias_seguridad"
fecha_hoy = datetime.now().strftime("%Y-%m-%d")
carpeta_destino = carpeta_respaldo_base / f"copia_{fecha_hoy}"

# Crear carpeta de respaldo del día si no existe
os.makedirs(carpeta_destino, exist_ok=True)

# Copiar base de datos
ruta_db_origen = base_dir / db_filename
ruta_db_destino = carpeta_destino / db_filename
shutil.copy2(ruta_db_origen, ruta_db_destino)

# Copiar carpetas
for carpeta in carpetas_datos:
    origen = base_dir / carpeta
    destino = carpeta_destino / carpeta
    if origen.exists():
        shutil.copytree(origen, destino)
    else:
        print(f"⚠️ La carpeta {carpeta} no existe y no se ha copiado.")

print(f"✅ Copia de seguridad completada en: {carpeta_destino}")
