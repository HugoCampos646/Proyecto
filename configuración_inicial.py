import os
import streamlit as st
import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

def buscarBaseDatos():
    # Verificar si la base de datos existe
    db_path = "base_datos_inventario.db"
    if os.path.exists(db_path):
        conexion = sqlite3.connect(db_path)
        cursor = conexion.cursor()

        # Crear tabla atributos si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS atributos (
            nombre TEXT,
            es_principal INTEGER DEFAULT 0,
            tipo TEXT DEFAULT 'text',
            orden INTEGER,
            borrable INTEGER
        )
        """)

        # Crear tabla productos si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            nombre TEXT NOT NULL,
            ubicacion TEXT NOT NULL,
            descripcion TEXT,
            palabras_clave TEXT,
            ruta_fotos TEXT,
            ruta_pdf_especificaciones TEXT,
            ruta_pdf_documentacion TEXT,
            persona_responsable TEXT,
            numero_inventario TEXT,
            fecha_compra DATE,
            numero_serie TEXT,
            proyecto TEXT,
            numero_factura TEXT
        )
        """)

        # Crear tabla usuarios si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            usuario TEXT NOT NULL UNIQUE,
            contraseña TEXT NOT NULL,
            es_admin BOOLEAN NOT NULL
        )
        """)

        # Verificar si existe el usuario admin. Si no, lo crea.
        cursor.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO usuarios (usuario, contraseña, es_admin) VALUES (?, ?, ?)",
                        ('admin', 'admin', 1))

        conexion.commit()
        conexion.close()
    else:
        st.error("⚠️ No se encuentra la base de datos 'base_datos_inventario.db' en la carpeta del proyecto, porfavor recarga esta pagina.")


def hacer_backup_diario():
    base_dir = Path(__file__).parent.resolve()
    db_filename = "base_datos_inventario.db"
    carpetas_datos = ["fotos", "pdf_especificaciones", "pdf_documentaciones"]

    escritorio = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
    carpeta_respaldo_base = escritorio / "copias_seguridad"
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    carpeta_destino = carpeta_respaldo_base / f"copia_{fecha_hoy}"

    if carpeta_destino.exists():
        return  # Ya existe copia de hoy

    try:
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

    except Exception:
        pass  # Silenciar cualquier error


def configurarPantallaLogo():
    # Configuración de la pantalla y nombre de la aplicación
    st.set_page_config(layout="wide", page_title='Inventario')
    st.logo("logo.png", size="large")
