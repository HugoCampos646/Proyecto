import streamlit as st
import sqlite3
import pandas as pd
import os
import shutil
from configuración_inicial import hacer_backup_diario, configurarPantallaLogo, buscarBaseDatos


#     ██████╗  ██████╗  ███╗   ██╗ ███████╗ ██╗  ██████╗ 
#    ██╔════╝ ██╔═══██╗ ████╗  ██║ ██╔════╝ ██║ ██╔════╝ 
#    ██║      ██║   ██║ ██╔██╗ ██║ █████╗   ██║ ██║  ███╗
#    ██║      ██║   ██║ ██║╚██╗██║ ██╔══╝   ██║ ██║   ██║ 
#    ╚██████╗ ╚██████╔╝ ██║ ╚████║ ██║      ██║ ╚██████╔╝
#     ╚═════╝  ╚═════╝  ╚═╝  ╚═══╝ ╚═╝      ╚═╝  ╚═════╝  
                                                                                                      

configurarPantallaLogo()
buscarBaseDatos()
hacer_backup_diario()


#    ██╗ ███╗   ██╗  ██████╗ ██╗  ██████╗      ███████╗ ███████╗ ███████╗ ██╗  ██████╗  ███╗   ██╗
#    ██║ ████╗  ██║ ██╔════╝ ██║ ██╔═══██╗     ██╔════╝ ██╔════╝ ██╔════╝ ██║ ██╔═══██╗ ████╗  ██║
#    ██║ ██╔██╗ ██║ ██║      ██║ ██║   ██║     ███████╗ █████╗   ███████╗ ██║ ██║   ██║ ██╔██╗ ██║
#    ██║ ██║╚██╗██║ ██║      ██║ ██║   ██║     ╚════██║ ██╔══╝   ╚════██║ ██║ ██║   ██║ ██║╚██╗██║
#    ██║ ██║ ╚████║ ╚██████╗ ██║ ╚██████╔╝     ███████║ ███████╗ ███████║ ██║ ╚██████╔╝ ██║ ╚████║
#    ╚═╝ ╚═╝  ╚═══╝  ╚═════╝ ╚═╝  ╚═════╝      ╚══════╝ ╚══════╝ ╚══════╝ ╚═╝  ╚═════╝  ╚═╝  ╚═══╝


# Inicializar la sesión si no existe
# Inicializar todos los estados de sesión necesarios
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Ver productos"  # Página predeterminada después del inicio de sesión
    
# Inicializar username y password solo si no existen
if "username" not in st.session_state:
    st.session_state.username = ""  # Inicializar username solo si no existe
if "password" not in st.session_state:
    st.session_state.password = ""  # Inicializar password solo si no existe

# Inicializar explícitamente es_admin
if "es_admin" not in st.session_state:
    st.session_state.es_admin = False

# Función para conectar a la base de datos y verificar usuario y contraseña
def verificar_usuario(usuario, contrasena):
    conexion = sqlite3.connect("base_datos_inventario.db")
    cursor = conexion.cursor()
    query = "SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?"
    cursor.execute(query, (usuario, contrasena))
    resultado = cursor.fetchone()
    
    # Verificar si el usuario es administrador
    es_admin = False
    if resultado:
        # IMPORTANTE: Ajusta esta consulta según tu estructura de base de datos
        # Esto asume que tienes una columna 'es_admin' en tu tabla de usuarios
        try:
            query_admin = "SELECT es_admin FROM usuarios WHERE usuario = ? AND contraseña = ?"
            cursor.execute(query_admin, (usuario, contrasena))
            admin_result = cursor.fetchone()
            es_admin = bool(admin_result[0]) if admin_result else False
        except Exception as e:
            print(f"Error al verificar admin: {e}")
            es_admin = False
    
    conexion.close()
    return resultado, es_admin

# Función para iniciar sesión
def iniciar_sesion():
    usuario, es_admin = verificar_usuario(st.session_state.username, st.session_state.password)
    if usuario:
        st.session_state.logged_in = True
        st.session_state.error_message = ""  # Limpiar mensajes de error
        st.session_state.usuarioActivo = st.session_state.username
        st.session_state.contraseñaActiva = st.session_state.password
        st.session_state.es_admin = es_admin
    else:
        st.session_state.error_message = "⚠️ Usuario o contraseña incorrectos. Inténtalo nuevamente."
        st.session_state.es_admin = False

# Función para cerrar sesión
def cerrar_sesion():
    # Reiniciar todos los estados de sesión relacionados con la autenticación
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.password = ""
    st.session_state.usuarioActivo = ""
    st.session_state.contraseñaActiva = ""
    st.session_state.current_page = "Ver productos"  # Restablecer a página predeterminada
    st.session_state.es_admin = False  # Reiniciar estado de administrador

# Si el usuario no ha iniciado sesión
if not st.session_state.logged_in:
    st.title("Inicio de Sesión")
    st.divider()

    # Campos de entrada para el usuario y contraseña
    username = st.text_input("Usuario", placeholder="Ingresa tu nombre de usuario", key="username")
    password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="password")

    # Botón para iniciar sesión
    if st.button("Iniciar sesión", on_click=iniciar_sesion):
        if "error_message" in st.session_state and st.session_state.error_message:
            st.error(st.session_state.error_message)



#    ██╗ ███╗   ██╗ ██╗   ██╗ ███████╗ ███╗   ██╗ ████████╗  █████╗  ██████╗  ██╗  ██████╗ 
#    ██║ ████╗  ██║ ██║   ██║ ██╔════╝ ████╗  ██║ ╚══██╔══╝ ██╔══██╗ ██╔══██╗ ██║ ██╔═══██╗
#    ██║ ██╔██╗ ██║ ██║   ██║ █████╗   ██╔██╗ ██║    ██║    ███████║ ██████╔╝ ██║ ██║   ██║
#    ██║ ██║╚██╗██║ ╚██╗ ██╔╝ ██╔══╝   ██║╚██╗██║    ██║    ██╔══██║ ██╔══██╗ ██║ ██║   ██║
#    ██║ ██║ ╚████║  ╚████╔╝  ███████╗ ██║ ╚████║    ██║    ██║  ██║ ██║  ██║ ██║ ╚██████╔╝
#    ╚═╝ ╚═╝  ╚═══╝   ╚═══╝   ╚══════╝ ╚═╝  ╚═══╝    ╚═╝    ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝  ╚═════╝


# Si el usuario ha iniciado sesión
else:
    # Barra de navegación con botones
    st.sidebar.title("Navegación")
    if st.sidebar.button("Ver productos"):
        st.session_state.current_page = "Ver productos"
    if st.sidebar.button("Añadir productos"):
        st.session_state.current_page = "Añadir productos"
    if st.session_state.get('es_admin', False):
        if st.sidebar.button("Usuarios"):
            st.session_state.current_page = "Usuarios"
        if st.sidebar.button("Opciones base de datos"):
            st.session_state.current_page = "Opciones base de datos"
    if st.sidebar.button("Cerrar sesión", on_click=cerrar_sesion):
        st.rerun()  # Recargar la aplicación para mostrar la pantalla de inicio de sesión

    # Mostrar el nombre de usuario activo y si es administrador o no
    st.sidebar.write(f"👤 Usuario: {st.session_state.usuarioActivo}")
    st.sidebar.write(f"🏷️ Rol: {'Administrador' if st.session_state.get('es_admin', False) else 'Usuario'}")

    # Página de Productos
    if st.session_state.current_page == "Ver productos":
        
        # Conectar a la base de datos SQLite
        db_path = "base_datos_inventario.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Función para obtener los atributos de productos
        def obtener_atributos():
            cursor.execute("""
                SELECT nombre, es_principal, tipo, orden, borrable 
                FROM atributos 
                WHERE borrable = 1
                ORDER BY orden
            """)
            return cursor.fetchall()

        # Obtener los atributos
        atributos = obtener_atributos()

        # Separar atributos principales y secundarios
        atributos_principales = [attr[0] for attr in atributos if attr[1] == 1]
        todos_atributos = [attr[0] for attr in atributos]
        tipos_atributos = {attr[0]: attr[2] for attr in atributos}
        
        # Verificar si hay atributos principales, si no, usar algunos predeterminados
        if not atributos_principales:
            atributos_principales = ['nombre', 'ubicacion', 'descripcion', 'persona_responsable']
        
        # Construir la consulta SQL dinámicamente
        columnas_select = ", ".join(todos_atributos)
        if not columnas_select:
            columnas_select = "nombre, ubicacion, descripcion, persona_responsable, numero_inventario, fecha_compra, numero_serie, proyecto, numero_factura, ruta_pdf_especificaciones, ruta_pdf_documentacion, ruta_fotos"
        
        # Recuperar los datos de la tabla 'productos'
        query = f"""
        SELECT {columnas_select}
        FROM productos
        """
        df = pd.read_sql_query(query, conn)
        
        # Asegurar que el DataFrame tenga las columnas necesarias
        for col in ['ruta_pdf_especificaciones', 'ruta_pdf_documentacion', 'ruta_fotos']:
            if col not in df.columns:
                df[col] = None

        st.write("### Lista de productos")
        st.divider()
        
        # Barra de filtrado
        filtro = st.text_input("🔍 Filtrar productos:", placeholder="Ingresa palabras de filtrado separadas por comas")
        
        # Aplicar filtro si hay texto
        df_filtrado = df
        if filtro:
            # Convertir columnas a tipo string para buscar
            columnas_busqueda = atributos_principales
            
            # Inicializar la máscara como falso para todas las filas
            mascara = pd.Series([False] * len(df))
            
            # Dividir el filtro en términos separados por comas y eliminar espacios en blanco
            terminos_busqueda = [termino.strip() for termino in filtro.split(',') if termino.strip()]
            
            # Para cada término de búsqueda
            for termino in terminos_busqueda:
                mascara_termino = pd.Series([False] * len(df))
                
                # Buscar el término en cada columna
                for col in columnas_busqueda:
                    if col in df.columns:
                        mascara_termino = mascara_termino | df[col].astype(str).str.contains(termino, case=False, na=False)
                
                # Agregar este término a la máscara general (OR entre términos)
                mascara = mascara | mascara_termino
            
            # Aplicar la máscara al dataframe
            df_filtrado = df[mascara]
        
        # Crear un dataframe solo con las columnas que queremos mostrar en la tabla principal
        columnas_tabla = [col for col in atributos_principales if col in df.columns]
        if not columnas_tabla:
            columnas_tabla = ['nombre', 'ubicacion', 'descripcion', 'persona_responsable']
        
        df_tabla = df_filtrado[columnas_tabla]

        # Calcular altura dinámica basada en el número de filas filtradas
        # Definimos una altura mínima y una altura por fila
        altura_minima = 100  # Altura mínima en píxeles
        altura_por_fila = 35  # Altura aproximada por fila en píxeles
        num_filas = len(df_tabla)
        altura_tabla = max(altura_minima, min(600, num_filas * altura_por_fila + 40))  # +40 para el encabezado
        
        # Mostrar la tabla filtrada con altura dinámica (solo con las columnas seleccionadas)
        st.dataframe(df_tabla, use_container_width=True, height=altura_tabla, hide_index=True)
        
        # Inicializar estados en session_state
        if "editable" not in st.session_state:
            st.session_state.editable = False
        if "selected_product" not in st.session_state:
            st.session_state.selected_product = None  # Inicializamos el producto seleccionado previamente
        if "confirmar_eliminacion" not in st.session_state:
            st.session_state.confirmar_eliminacion = False

        # Verificar si hay productos disponibles
        if len(df_filtrado) > 0:
            # Selectbox para seleccionar un producto
            producto_seleccionado = st.selectbox(
                "Selecciona un producto para más información:",
                options=[""] + df_filtrado["nombre"].tolist(),
                format_func=lambda x: "" if x == "" else x
            )
        else:
            producto_seleccionado = ""

        # Verificar si se ha cambiado de producto seleccionado
        if producto_seleccionado != st.session_state.selected_product:
            st.session_state.editable = False  # Reiniciar el estado de edición si cambia el producto
            st.session_state.selected_product = producto_seleccionado  # Actualizar el producto seleccionado

        # Mostrar información del producto seleccionado en pestañas
        if producto_seleccionado:
            producto_info = df[df["nombre"] == producto_seleccionado].iloc[0]  # Obtener datos del producto seleccionado

            tabs = st.tabs(["Datos y Editar", "PDFs Descargables", "Imágenes"])

            # Pestaña 1: Datos y Editar
            # Pestaña 1: Datos y Editar
            with tabs[0]:
                # Crear dos columnas para la vista dividida
                col_datos, col_imagenes = st.columns([1.5, 1])
                
                # Columna de datos y edición
                with col_datos:
                    st.write("### Datos del Producto")
                    
                    # Generar campos de datos dinámicamente según los atributos
                    campos_editados = {}
                    
                    # Diccionario para guardar los valores de campo editados
                    for attr_name in todos_atributos:
                        if attr_name in df.columns:
                            attr_tipo = tipos_atributos.get(attr_name, 'text')
                            
                            # Obtener el valor actual
                            valor_actual = producto_info[attr_name]
                            
                            # Crear el campo de entrada apropiado según el tipo
                            if attr_tipo == 'date':
                                # Para fechas
                                fecha_valor = pd.to_datetime(valor_actual) if valor_actual and pd.notna(valor_actual) else None
                                campos_editados[attr_name] = st.date_input(
                                    attr_name.replace('_', ' ').capitalize(),
                                    value=fecha_valor,
                                    disabled=not st.session_state.editable
                                )
                            elif attr_tipo == 'integer':
                                # Para números enteros
                                try:
                                    valor_int = int(valor_actual) if valor_actual and pd.notna(valor_actual) else 0
                                except (ValueError, TypeError):
                                    valor_int = 0
                                campos_editados[attr_name] = st.number_input(
                                    attr_name.replace('_', ' ').capitalize(), 
                                    value=valor_int,
                                    disabled=not st.session_state.editable
                                )
                            else:
                                # Para texto y otros tipos
                                campos_editados[attr_name] = st.text_input(
                                    attr_name.replace('_', ' ').capitalize(),
                                    value="" if valor_actual is None else str(valor_actual),
                                    disabled=not st.session_state.editable
                                )

                    # Botones de acción (editar, guardar, eliminar)
                    if not st.session_state.confirmar_eliminacion:
                        col_editar, col_guardar, col_eliminar = st.columns(3)

                        with col_editar:
                            if not st.session_state.editable:
                                if st.button("✏️ Editar"):
                                    st.session_state.editable = True
                                    st.rerun()

                        with col_guardar:
                            if st.session_state.editable:
                                if st.button("✅ Aceptar"):
                                    conn = sqlite3.connect(db_path)
                                    cursor = conn.cursor()
                                    
                                    # Preparar la consulta de actualización dinámicamente
                                    set_clause = ", ".join([f"{attr} = ?" for attr in campos_editados.keys()])
                                    query_update = f"""
                                    UPDATE productos
                                    SET {set_clause}
                                    WHERE nombre = ?
                                    """
                                    
                                    # Preparar los valores para la consulta
                                    valores = []
                                    for attr, valor in campos_editados.items():
                                        if attr in tipos_atributos and tipos_atributos[attr] == 'date' and valor:
                                            valores.append(valor.strftime('%Y-%m-%d'))
                                        else:
                                            valores.append(valor)
                                    
                                    # Añadir el nombre original como último parámetro para WHERE
                                    valores.append(producto_info["nombre"])
                                    
                                    cursor.execute(query_update, valores)
                                    conn.commit()
                                    conn.close()
                                    st.success("Cambios guardados correctamente.")
                                    st.session_state.editable = False
                                    st.rerun()

                        with col_eliminar:
                            if "confirmar_eliminacion" not in st.session_state:
                                st.session_state.confirmar_eliminacion = False

                            if st.button("🗑️ Eliminar producto"):
                                st.session_state.confirmar_eliminacion = True
                                st.rerun()
                    else:
                        # Mostrar confirmación de eliminación en una sección separada (no dentro de columnas)
                        st.warning("⚠️ ¿Estás seguro de que deseas eliminar este producto? Esta acción no se puede deshacer.")
                        # Usar nuevas columnas directamente bajo col_datos (no anidadas)
                        col_si, col_no = st.columns(2)

                        with col_si:
                            if st.button("✅ Sí, eliminar"):
                                conn = sqlite3.connect(db_path)
                                cursor = conn.cursor()

                                # Obtener rutas antes de eliminar el producto
                                cursor.execute("""
                                    SELECT ruta_fotos, ruta_pdf_documentacion, ruta_pdf_especificaciones
                                    FROM productos
                                    WHERE nombre = ?
                                """, (producto_info["nombre"],))
                                rutas = cursor.fetchone()

                                # Eliminar producto de la base de datos
                                cursor.execute("DELETE FROM productos WHERE nombre = ?", (producto_info["nombre"],))
                                conn.commit()
                                conn.close()

                                # Eliminar carpeta de fotos (si existe)
                                ruta_fotos = rutas[0]
                                if ruta_fotos and os.path.exists(ruta_fotos) and os.path.basename(os.path.dirname(ruta_fotos)) == "fotos":
                                    try:
                                        shutil.rmtree(ruta_fotos)
                                    except Exception as e:
                                        st.warning(f"No se pudo eliminar la carpeta de fotos: {e}")

                                # Eliminar carpeta de documentación
                                ruta_doc = rutas[1]
                                if ruta_doc:
                                    try:
                                        if os.path.isfile(ruta_doc):
                                            carpeta = os.path.dirname(ruta_doc)
                                        else:
                                            carpeta = ruta_doc
                                        if os.path.basename(os.path.dirname(carpeta)) == "pdf_documentaciones":
                                            shutil.rmtree(carpeta)
                                    except Exception as e:
                                        st.warning(f"No se pudo eliminar la carpeta de documentación: {e}")

                                # Eliminar carpeta de especificaciones
                                ruta_spec = rutas[2]
                                if ruta_spec:
                                    try:
                                        if os.path.isfile(ruta_spec):
                                            carpeta = os.path.dirname(ruta_spec)
                                        else:
                                            carpeta = ruta_spec
                                        if os.path.basename(os.path.dirname(carpeta)) == "pdf_especificaciones":
                                            shutil.rmtree(carpeta)
                                    except Exception as e:
                                        st.warning(f"No se pudo eliminar la carpeta de especificaciones: {e}")

                                st.success("Producto eliminado correctamente.")
                                st.session_state.confirmar_eliminacion = False
                                st.rerun()

                        with col_no:
                            if st.button("❌ Cancelar"):
                                st.session_state.confirmar_eliminacion = False
                                st.rerun()

                # Columna de imágenes (solo visualización)
                with col_imagenes:
                    st.write("### Imágenes del Producto")
                    
                    # Definir la ruta para las fotos basada en el nombre del producto
                    if not producto_info["ruta_fotos"] or not os.path.exists(producto_info["ruta_fotos"]):
                        ruta_fotos = f"fotos/{producto_info['nombre']}"
                    else:
                        ruta_fotos = producto_info["ruta_fotos"]
                    
                    # Verificar si hay imágenes existentes
                    hay_imagenes = False
                    if os.path.exists(ruta_fotos):
                        fotos = [f for f in os.listdir(ruta_fotos) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
                        hay_imagenes = len(fotos) > 0
                    
                    # Crear un contenedor con altura fija para las imágenes
                    imagen_container = st.container()
                    
                    if hay_imagenes:
                        # Inicializar o corregir índice de imagen
                        if "imagen_actual_datos" not in st.session_state or st.session_state.imagen_actual_datos >= len(fotos):
                            st.session_state.imagen_actual_datos = 0

                        # Mostrar imagen actual dentro de un contenedor de altura fija
                        with imagen_container:
                            # Crear un espacio fijo para la imagen
                            imagen_height = 300  # Altura fija en píxeles
                            st.markdown(f"""
                                <div style="display: flex; justify-content: center; align-items: center; height: {imagen_height}px; overflow: hidden;">
                                </div>
                            """, unsafe_allow_html=True)
                            
                            foto_actual = os.path.join(ruta_fotos, fotos[st.session_state.imagen_actual_datos])
                            st.image(
                                foto_actual,
                                caption=None,  # Sin caption
                                use_container_width=True
                            )
                        
                        # Controles de navegación
                        col_anterior, col_siguiente = st.columns(2)
                        with col_anterior:
                            if st.button("🡄", key="anterior_datos"):
                                st.session_state.imagen_actual_datos = (st.session_state.imagen_actual_datos - 1) % len(fotos)
                                st.rerun()
                        with col_siguiente:
                            if st.button("🡆", key="siguiente_datos"):
                                st.session_state.imagen_actual_datos = (st.session_state.imagen_actual_datos + 1) % len(fotos)
                                st.rerun()
                    else:
                        # Mostrar mensaje en el contenedor de tamaño fijo
                        with imagen_container:
                            st.warning("No hay imágenes disponibles para este producto.")


            # Pestaña 2: PDFs Descargables
            with tabs[1]:
                st.write("### PDFs del Producto")
                
                # Obtener rutas actualizadas directamente desde la base de datos
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT ruta_pdf_especificaciones, ruta_pdf_documentacion
                    FROM productos
                    WHERE nombre = ?
                """, (producto_info["nombre"],))
                resultado = cursor.fetchone()
                conn.close()

                ruta_especificaciones = resultado[0] if resultado else None
                ruta_documentacion = resultado[1] if resultado else None
                col1, col2 = st.columns(2)

                with col1:
                    if ruta_especificaciones and os.path.exists(ruta_especificaciones):
                        try:
                            with open(ruta_especificaciones, "rb") as file:
                                st.download_button(
                                    label="⬇️ Descargar PDF Especificaciones",
                                    data=file.read(),
                                    file_name=os.path.basename(ruta_especificaciones),
                                    mime="application/pdf"
                                )
                        except IsADirectoryError:
                            # Si es un directorio, buscar el primer PDF
                            pdf_files = [f for f in os.listdir(ruta_especificaciones) if f.lower().endswith('.pdf')]
                            if pdf_files:
                                pdf_path = os.path.join(ruta_especificaciones, pdf_files[0])
                                with open(pdf_path, "rb") as file:
                                    st.download_button(
                                        label="⬇️ Descargar PDF Especificaciones",
                                        data=file.read(),
                                        file_name=pdf_files[0],
                                        mime="application/pdf"
                                    )
                            else:
                                st.warning("No existe PDF de especificaciones para este producto.")
                        except FileNotFoundError:
                            st.warning("El archivo PDF de especificaciones no se encuentra.")
                    else:
                        st.warning("No existe PDF de especificaciones para este producto.")

                with col2:
                    if ruta_documentacion and os.path.exists(ruta_documentacion):
                        try:
                            with open(ruta_documentacion, "rb") as file:
                                st.download_button(
                                    label="⬇️ Descargar PDF Documentación",
                                    data=file.read(),
                                    file_name=os.path.basename(ruta_documentacion),
                                    mime="application/pdf"
                                )
                        except IsADirectoryError:
                            # Si es un directorio, buscar el primer PDF
                            pdf_files = [f for f in os.listdir(ruta_documentacion) if f.lower().endswith('.pdf')]
                            if pdf_files:
                                pdf_path = os.path.join(ruta_documentacion, pdf_files[0])
                                with open(pdf_path, "rb") as file:
                                    st.download_button(
                                        label="⬇️ Descargar PDF Documentación",
                                        data=file.read(),
                                        file_name=pdf_files[0],
                                        mime="application/pdf"
                                    )
                            else:
                                st.warning("No existe PDF de documentación para este producto.")
                        except FileNotFoundError:
                            st.warning("El archivo PDF de documentación no se encuentra.")
                    else:
                        st.warning("No existe PDF de documentación para este producto.")
                
                # Inicializar variables de estado para los formularios
                if "edit_especificaciones" not in st.session_state:
                    st.session_state.edit_especificaciones = False
                if "edit_documentacion" not in st.session_state:
                    st.session_state.edit_documentacion = False
                if "confirm_delete_spec" not in st.session_state:
                    st.session_state.confirm_delete_spec = False
                if "confirm_delete_doc" not in st.session_state:
                    st.session_state.confirm_delete_doc = False
                
                col3, col4 = st.columns(2)

                # Botón para editar especificaciones
                with col3:
                    if not st.session_state.edit_especificaciones and not st.session_state.confirm_delete_spec:
                        if st.button("📝 Gestionar PDF Especificaciones", key="edit_spec_btn"):
                            st.session_state.edit_especificaciones = True
                            st.rerun()
                
                # Botón para editar documentación
                with col4:
                    if not st.session_state.edit_documentacion and not st.session_state.confirm_delete_doc:
                        if st.button("📝 Gestionar PDF Documentación", key="edit_doc_btn"):
                            st.session_state.edit_documentacion = True
                            st.rerun()
                
                # Formulario para editar PDF de especificaciones
                if st.session_state.edit_especificaciones:
                    st.divider()
                    #st.write("#### Gestión de PDF de especificaciones")
                    
                    # Opción para subir nuevo PDF
                    st.write("##### Subir nuevo PDF")
                    pdf_especificaciones = st.file_uploader("Seleccionar archivo PDF", type=["pdf"], key="especificaciones_uploader")
                    
                    col_guardar, col_empty = st.columns(2)
                    
                    with col_guardar:
                        if st.button("💾 Guardar nuevo PDF", key="save_specs") and pdf_especificaciones is not None:
                            # Crear estructura de directorios si no existe
                            base_dir = "pdf_especificaciones"
                            if not os.path.exists(base_dir):
                                os.makedirs(base_dir)
                            
                            # Crear directorio para el producto si no existe
                            producto_dir = os.path.join(base_dir, producto_info["nombre"])
                            if not os.path.exists(producto_dir):
                                os.makedirs(producto_dir)
                            
                            # Guardar el nuevo PDF
                            file_path = os.path.join(producto_dir, pdf_especificaciones.name)
                            with open(file_path, "wb") as f:
                                f.write(pdf_especificaciones.getbuffer())
                            
                            # Actualizar la base de datos con la nueva ruta
                            conn = sqlite3.connect(db_path)
                            cursor = conn.cursor()
                            query_update = """
                            UPDATE productos
                            SET ruta_pdf_especificaciones = ?
                            WHERE nombre = ?
                            """
                            cursor.execute(query_update, (file_path, producto_info["nombre"]))
                            conn.commit()
                            conn.close()
                            
                            st.success(f"PDF de especificaciones actualizado correctamente.")
                            st.session_state.edit_especificaciones = False
                            st.rerun()
                    
                    # Opción para eliminar PDF existente
                    if ruta_especificaciones and os.path.exists(ruta_especificaciones):
                        st.divider()
                        st.write("##### Eliminar PDF existente")
                        
                        if not st.session_state.confirm_delete_spec:
                            if st.button("🗑️ Eliminar PDF actual", key="delete_spec_btn"):
                                st.session_state.confirm_delete_spec = True
                                st.rerun()
                        else:
                            st.warning("⚠️ ¿Estás seguro de que deseas eliminar el PDF de especificaciones? Esta acción no se puede deshacer.")
                            col_si_spec, col_no_spec = st.columns(2)
                            
                            with col_si_spec:
                                if st.button("✅ Sí, eliminar", key="confirm_delete_spec_yes"):
                                    # Identificar la ruta del archivo
                                    ruta_archivo = None
                                    try:
                                        if os.path.isfile(ruta_especificaciones):
                                            ruta_archivo = ruta_especificaciones
                                        elif os.path.isdir(ruta_especificaciones):
                                            pdf_files = [f for f in os.listdir(ruta_especificaciones) if f.lower().endswith('.pdf')]
                                            if pdf_files:
                                                ruta_archivo = os.path.join(ruta_especificaciones, pdf_files[0])
                                    except Exception:
                                        pass
                                    
                                    # Eliminar el archivo si existe
                                    if ruta_archivo and os.path.isfile(ruta_archivo):
                                        try:
                                            os.remove(ruta_archivo)
                                            
                                            # Actualizar la base de datos para eliminar la ruta
                                            conn = sqlite3.connect(db_path)
                                            cursor = conn.cursor()
                                            query_update = """
                                            UPDATE productos
                                            SET ruta_pdf_especificaciones = NULL
                                            WHERE nombre = ?
                                            """
                                            cursor.execute(query_update, (producto_info["nombre"],))
                                            conn.commit()
                                            conn.close()
                                            
                                            st.success("PDF de especificaciones eliminado correctamente.")
                                        except Exception as e:
                                            st.error(f"Error al eliminar el archivo: {e}")
                                    
                                    st.session_state.confirm_delete_spec = False
                                    st.session_state.edit_especificaciones = False
                                    st.rerun()
                                    
                            with col_no_spec:
                                if st.button("❌ Cancelar eliminación", key="confirm_delete_spec_no"):
                                    st.session_state.confirm_delete_spec = False
                                    st.rerun()
                    
                    st.divider()
                    if st.button("↩️ Volver", key="cancel_specs"):
                        st.session_state.edit_especificaciones = False
                        st.session_state.confirm_delete_spec = False
                        st.rerun()
                
                # Formulario para editar PDF de documentación
                if st.session_state.edit_documentacion:
                    #st.write("#### Gestión de PDF de documentación")
                    
                    # Opción para subir nuevo PDF
                    st.divider()
                    st.write("##### Subir nuevo PDF")
                    pdf_documentacion = st.file_uploader("Seleccionar archivo PDF", type=["pdf"], key="documentacion_uploader")
                    
                    col_guardar, col_empty = st.columns(2)
                    
                    with col_guardar:
                        if st.button("💾 Guardar nuevo PDF", key="save_docs") and pdf_documentacion is not None:
                            # Crear estructura de directorios si no existe
                            base_dir = "pdf_documentaciones"
                            if not os.path.exists(base_dir):
                                os.makedirs(base_dir)
                            
                            # Crear directorio para el producto si no existe
                            producto_dir = os.path.join(base_dir, producto_info["nombre"])
                            if not os.path.exists(producto_dir):
                                os.makedirs(producto_dir)
                            
                            # Guardar el nuevo PDF
                            file_path = os.path.join(producto_dir, pdf_documentacion.name)
                            with open(file_path, "wb") as f:
                                f.write(pdf_documentacion.getbuffer())
                            
                            # Actualizar la base de datos con la nueva ruta
                            conn = sqlite3.connect(db_path)
                            cursor = conn.cursor()
                            query_update = """
                            UPDATE productos
                            SET ruta_pdf_documentacion = ?
                            WHERE nombre = ?
                            """
                            cursor.execute(query_update, (file_path, producto_info["nombre"]))
                            conn.commit()
                            conn.close()
                            
                            st.success(f"PDF de documentación actualizado correctamente.")
                            st.session_state.edit_documentacion = False
                            st.rerun()
                    
                    # Opción para eliminar PDF existente
                    if ruta_documentacion and os.path.exists(ruta_documentacion):
                        st.divider()
                        st.write("##### Eliminar PDF existente")
                        
                        if not st.session_state.confirm_delete_doc:
                            if st.button("🗑️ Eliminar PDF actual", key="delete_doc_btn"):
                                st.session_state.confirm_delete_doc = True
                                st.rerun()
                        else:
                            st.warning("⚠️ ¿Estás seguro de que deseas eliminar el PDF de documentación? Esta acción no se puede deshacer.")
                            col_si_doc, col_no_doc = st.columns(2)
                            
                            with col_si_doc:
                                if st.button("✅ Sí, eliminar", key="confirm_delete_doc_yes"):
                                    # Identificar la ruta del archivo
                                    ruta_archivo = None
                                    try:
                                        if os.path.isfile(ruta_documentacion):
                                            ruta_archivo = ruta_documentacion
                                        elif os.path.isdir(ruta_documentacion):
                                            pdf_files = [f for f in os.listdir(ruta_documentacion) if f.lower().endswith('.pdf')]
                                            if pdf_files:
                                                ruta_archivo = os.path.join(ruta_documentacion, pdf_files[0])
                                    except Exception:
                                        pass
                                    
                                    # Eliminar el archivo si existe
                                    if ruta_archivo and os.path.isfile(ruta_archivo):
                                        try:
                                            os.remove(ruta_archivo)
                                            
                                            # Actualizar la base de datos para eliminar la ruta
                                            conn = sqlite3.connect(db_path)
                                            cursor = conn.cursor()
                                            query_update = """
                                            UPDATE productos
                                            SET ruta_pdf_documentacion = NULL
                                            WHERE nombre = ?
                                            """
                                            cursor.execute(query_update, (producto_info["nombre"],))
                                            conn.commit()
                                            conn.close()
                                            
                                            st.success("PDF de documentación eliminado correctamente.")
                                        except Exception as e:
                                            st.error(f"Error al eliminar el archivo: {e}")
                                    
                                    st.session_state.confirm_delete_doc = False
                                    st.session_state.edit_documentacion = False
                                    st.rerun()
                                    
                            with col_no_doc:
                                if st.button("❌ Cancelar eliminación", key="confirm_delete_doc_no"):
                                    st.session_state.confirm_delete_doc = False
                                    st.rerun()
                    
                    st.divider()
                    if st.button("↩️ Volver", key="cancel_docs"):
                        st.session_state.edit_documentacion = False
                        st.session_state.confirm_delete_doc = False
                        st.rerun()
                    
                

            # Pestaña 3: Imágenes
            with tabs[2]:
                st.write("### Imágenes del Producto")

                # Definir la ruta para las fotos basada en el nombre del producto
                # Si no existe, la creamos al momento de agregar imágenes
                if not producto_info["ruta_fotos"] or not os.path.exists(producto_info["ruta_fotos"]):
                    ruta_fotos = f"fotos/{producto_info['nombre']}"
                else:
                    ruta_fotos = producto_info["ruta_fotos"]
                
                
                # Estado para controlar el modo de edición
                if "modo_edicion_imagenes" not in st.session_state:
                    st.session_state.modo_edicion_imagenes = False
                
                # Verificar si hay imágenes existentes
                hay_imagenes = False
                if os.path.exists(ruta_fotos):
                    fotos = [f for f in os.listdir(ruta_fotos) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
                    hay_imagenes = len(fotos) > 0
                
                # Modo de visualización normal
                if not st.session_state.modo_edicion_imagenes:
                    if hay_imagenes:
                        # Inicializar o corregir índice de imagen
                        if "imagen_actual" not in st.session_state or st.session_state.imagen_actual >= len(fotos):
                            st.session_state.imagen_actual = 0

                        # Controles de navegación
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            if st.button("🡄", key="anterior"):
                                st.session_state.imagen_actual = (st.session_state.imagen_actual - 1) % len(fotos)
                        with col2:
                            if st.button("🡆", key="siguiente"):
                                st.session_state.imagen_actual = (st.session_state.imagen_actual + 1) % len(fotos)
                        
                        # Mostrar imagen actual
                        foto_actual = os.path.join(ruta_fotos, fotos[st.session_state.imagen_actual])
                        st.image(
                            foto_actual,
                            caption=fotos[st.session_state.imagen_actual],
                        )
                    else:
                        st.warning("No hay imágenes disponibles para este producto.")
                        st.session_state.imagen_actual = 0  # Reiniciar índice si no hay fotos
                
                # Modo de edición
                else:
                    # En modo edición, mostramos diferente contenido según si hay imágenes o no
                    # Subir nuevas imágenes
                    st.divider()
                    st.write("##### Subir nueva imagen")
                    uploaded_files = st.file_uploader("Seleccionar un archivo png, jpg, jpeg", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
                    
                    if uploaded_files:
                        # Crear la carpeta si no existe
                        os.makedirs(ruta_fotos, exist_ok=True)
                        
                        # Si la ruta de fotos es diferente a la almacenada, actualizamos en la BD
                        if ruta_fotos != producto_info["ruta_fotos"]:
                            conn = sqlite3.connect(db_path)
                            cursor = conn.cursor()
                            cursor.execute("UPDATE productos SET ruta_fotos = ? WHERE nombre = ?", (ruta_fotos, producto_info["nombre"]))
                            conn.commit()
                            conn.close()
                        
                        # Procesamos cada archivo subido
                        for uploaded_file in uploaded_files:
                            file_path = os.path.join(ruta_fotos, uploaded_file.name)
                            
                            # Guardar archivo subido
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            st.success(f"Imagen guardada: {uploaded_file.name}")
                    
                    # Verificar si hay imágenes después de subir (puede haber cambiado)
                    if os.path.exists(ruta_fotos):
                        fotos = [f for f in os.listdir(ruta_fotos) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
                        hay_imagenes = len(fotos) > 0
                    
                    # Mostrar y permitir eliminar imágenes existentes
                    if hay_imagenes:
                        st.divider()
                        st.write("##### Eliminar imágenes existentes")
                        
                        # Mostrar imágenes en una cuadrícula para eliminar
                        cols = st.columns(3)
                        for i, foto in enumerate(fotos):
                            with cols[i % 3]:
                                foto_path = os.path.join(ruta_fotos, foto)
                                st.image(foto_path, caption=foto, width=150)
                                if st.button(f"Eliminar", key=f"del_{i}"):
                                    os.remove(foto_path)
                                    st.rerun()
                
                # Botón para alternar entre modo normal y modo edición
                    st.divider()
                if st.button("🖼️ Editar imagenes" if not st.session_state.modo_edicion_imagenes else "↩️ Volver a visualización"):
                    st.session_state.modo_edicion_imagenes = not st.session_state.modo_edicion_imagenes
                    st.rerun()




#    ██╗   ██╗ ███████╗ ██╗   ██╗  █████╗  ██████╗  ██╗  ██████╗  ███████╗
#    ██║   ██║ ██╔════╝ ██║   ██║ ██╔══██╗ ██╔══██╗ ██║ ██╔═══██╗ ██╔════╝
#    ██║   ██║ ███████╗ ██║   ██║ ███████║ ██████╔╝ ██║ ██║   ██║ ███████╗
#    ██║   ██║ ╚════██║ ██║   ██║ ██╔══██║ ██╔══██╗ ██║ ██║   ██║ ╚════██║
#    ╚██████╔╝ ███████║ ╚██████╔╝ ██║  ██║ ██║  ██║ ██║ ╚██████╔╝ ███████║
#     ╚═════╝  ╚══════╝  ╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝  ╚═════╝  ╚══════╝
                                                              

    # Página de Usuarios
    # Página de Usuarios
    elif st.session_state.current_page == "Usuarios":

        # Inicialización de estados comunes
        init_defaults = {
            'usuarioNuevo': "",
            'contraseñaNueva': "",
            'contraseñaRepetida': "",
            'admin': False,
            'usuario_agregado': "",
            'usuarioEliminar': "",
            'nombre_eliminado': "",
            'mostrar_exito_agregar': False,
            'mostrar_exito_eliminar': False,
            'limpiar_despues_agregar': False,
            'limpiar_despues_eliminar': False
        }
        for key, default in init_defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default
        
        # Limpieza de campos si es necesario (antes de instanciar widgets)
        if st.session_state.limpiar_despues_agregar:
            st.session_state.usuarioNuevo = ""
            st.session_state.contraseñaNueva = ""
            st.session_state.contraseñaRepetida = ""
            st.session_state.admin = False
            st.session_state.limpiar_despues_agregar = False
            st.session_state.mostrar_exito_agregar = True
        
        if st.session_state.limpiar_despues_eliminar:
            st.session_state.usuarioEliminar = ""
            st.session_state.limpiar_despues_eliminar = False
            st.session_state.mostrar_exito_eliminar = True

        # FORMULARIO PARA AGREGAR USUARIO
        st.write("### Dar de alta usuario:")
        with st.form(key="form_agregar_usuario"):
            st.text_input("Nombre de usuario", key="usuarioNuevo", placeholder="Ingresa nuevo nombre de usuario")
            st.text_input("Contraseña:", type="password", key="contraseñaNueva", placeholder="Ingresa nueva contraseña")
            st.text_input("Confirmar contraseña", type="password", key="contraseñaRepetida", placeholder="Confirma la contraseña")
            st.checkbox("Es administrador", value=False, key="admin")
            agregar = st.form_submit_button("👤➕ Agregar usuario")
        
        # Mostrar mensaje de éxito si corresponde
        if st.session_state.mostrar_exito_agregar:
            st.success(f"Usuario '{st.session_state.usuario_agregado}' agregado con éxito.")
            st.session_state.mostrar_exito_agregar = False
        
        # Procesar envío del formulario
        if agregar:
            usuarioNuevo = st.session_state.usuarioNuevo.strip()
            contrasena = st.session_state.contraseñaNueva.strip()
            repetir = st.session_state.contraseñaRepetida.strip()
            admin = st.session_state.admin

            # Validaciones
            if not usuarioNuevo or not contrasena or not repetir:
                st.warning("Todos los campos deben estar completos y no pueden contener solo espacios.", icon="⚠️")
            elif contrasena != repetir:
                st.warning("Las contraseñas deben ser idénticas.", icon="⚠️")
            else:
                conn = sqlite3.connect("base_datos_inventario.db")
                cursor = conn.cursor()
                cursor.execute("SELECT es_admin FROM usuarios WHERE usuario = ? AND contraseña = ?", 
                            (st.session_state.usuarioActivo, st.session_state.contraseñaActiva))
                result = cursor.fetchone()

                if result and result[0] == 1:
                    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = ?", (usuarioNuevo,))
                    if cursor.fetchone()[0]:
                        st.warning(f"El usuario '{usuarioNuevo}' ya existe.", icon="⚠️")
                    else:
                        cursor.execute("INSERT INTO usuarios (usuario, contraseña, es_admin) VALUES (?, ?, ?)",
                                    (usuarioNuevo, contrasena, 1 if admin else 0))
                        conn.commit()
                        st.session_state.usuario_agregado = usuarioNuevo
                        st.session_state.limpiar_despues_agregar = True
                        # Ocultar el otro mensaje si existe
                        st.session_state.mostrar_exito_eliminar = False
                        st.rerun()
                else:
                    st.warning("Solo los administradores pueden agregar usuarios.", icon="⚠️")
                conn.close()

        st.divider()

        # FORMULARIO PARA ELIMINAR USUARIO
        st.write("### Dar de baja usuario:")
        with st.form(key="form_eliminar_usuario"):
            st.text_input("Nombre de usuario a eliminar", key="usuarioEliminar", placeholder="Ingresa el nombre de usuario a eliminar")
            eliminar = st.form_submit_button("👤❌ Eliminar usuario")
        
        # Mostrar mensaje de éxito si corresponde
        if st.session_state.mostrar_exito_eliminar:
            st.success(f"Usuario '{st.session_state.nombre_eliminado}' eliminado con éxito.")
            st.session_state.mostrar_exito_eliminar = False
        
        # Procesar envío del formulario
        if eliminar:
            usuarioEliminar = st.session_state.usuarioEliminar.strip()

            # Validaciones
            if not usuarioEliminar:
                st.warning("El nombre de usuario no puede estar vacío ni contener solo espacios.", icon="⚠️")
            else:
                conn = sqlite3.connect("base_datos_inventario.db")
                cursor = conn.cursor()
                cursor.execute("SELECT es_admin FROM usuarios WHERE usuario = ? AND contraseña = ?", 
                            (st.session_state.usuarioActivo, st.session_state.contraseñaActiva))
                result = cursor.fetchone()

                if result and result[0] == 1:
                    if usuarioEliminar == st.session_state.usuarioActivo:
                        st.warning("No puedes eliminar tu propio usuario.", icon="⚠️")
                    else:
                        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = ?", (usuarioEliminar,))
                        if cursor.fetchone()[0]:
                            cursor.execute("DELETE FROM usuarios WHERE usuario = ?", (usuarioEliminar,))
                            conn.commit()
                            st.session_state.nombre_eliminado = usuarioEliminar
                            st.session_state.limpiar_despues_eliminar = True
                            # Ocultar el otro mensaje si existe
                            st.session_state.mostrar_exito_agregar = False
                            st.rerun()
                        else:
                            st.warning(f"El usuario '{usuarioEliminar}' no existe.", icon="⚠️")
                else:
                    st.warning("Solo los administradores pueden eliminar usuarios.", icon="⚠️")
                conn.close()



#     █████╗  ███╗   ██╗  █████╗  ██████╗  ██╗ ██████╗ 
#    ██╔══██╗ ████╗  ██║ ██╔══██╗ ██╔══██╗ ██║ ██╔══██╗
#    ███████║ ██╔██╗ ██║ ███████║ ██║  ██║ ██║ ██████╔╝
#    ██╔══██║ ██║╚██╗██║ ██╔══██║ ██║  ██║ ██║ ██╔══██╗
#    ██║  ██║ ██║ ╚████║ ██║  ██║ ██████╔╝ ██║ ██║  ██║
#    ╚═╝  ╚═╝ ╚═╝  ╚═══╝ ╚═╝  ╚═╝ ╚═════╝  ╚═╝ ╚═╝  ╚═╝
                                             

    # Página de añadir producto
    # Página de añadir producto
    elif st.session_state.current_page == "Añadir productos":
        st.write("### Añadir producto")
        
        # Inicializar el mensaje de éxito
        if 'producto_agregado' not in st.session_state:
            st.session_state.producto_agregado = False
            st.session_state.nombre_producto = ""
        
        # Conectar a la base de datos para obtener los atributos
        conn = sqlite3.connect("base_datos_inventario.db")
        cursor = conn.cursor()
        
        # Obtener todos los atributos borrables (borrable = 1)
        cursor.execute("""
            SELECT nombre, tipo, es_principal
            FROM atributos
            WHERE borrable = 1
            ORDER BY orden
        """)
        atributos_borrables = cursor.fetchall()
        
        # Campos de rutas que siempre estarán presentes
        campos_fijos = ["ruta_pdf_especificaciones", "ruta_pdf_documentacion", "ruta_fotos"]
        
        # Función para manejar el envío del formulario
        def submit_form():
            # Validar que los campos obligatorios no estén vacíos y no contengan solo espacios
            # Solo son obligatorios: nombre, ubicacion y persona_responsable
            campos_obligatorios = ["nombre", "ubicacion", "persona_responsable"]
            
            # Todos los valores deben ser válidos
            valores_formulario = {}
            campos_invalidos = []
            
            # Verificar todos los campos obligatorios
            for campo in campos_obligatorios:
                valor = st.session_state.get(f"input_{campo}")
                if isinstance(valor, str):
                    if not valor or not valor.strip():
                        campos_invalidos.append(campo)
                    else:
                        valores_formulario[campo] = valor.strip()
                else:
                    valores_formulario[campo] = valor
                    
            if campos_invalidos:
                st.warning(f"Por favor, completa correctamente los siguientes campos obligatorios: {', '.join(campos_invalidos)}", icon="⚠️")
                return False
            
            # Recopilar los valores de todos los campos (obligatorios y opcionales)
            for attr in atributos_borrables:
                campo = attr[0]
                if campo not in valores_formulario:  # Si no es un campo principal ya procesado
                    valor = st.session_state.get(f"input_{campo}")
                    # Manejar fechas y otros tipos de datos
                    if attr[1] == 'date' and valor:
                        valores_formulario[campo] = valor.strftime('%Y-%m-%d')
                    else:
                        valores_formulario[campo] = valor
            
            # Manejar archivos y carpetas
            pdf_documentacion = st.session_state.input_pdf_documentacion
            pdf_especificaciones = st.session_state.input_pdf_especificaciones
            imagenes = st.session_state.input_imagenes
            
            # Crear nombre único de carpeta
            base_nombre = valores_formulario.get('nombre', '').strip().replace(" ", "_")
            nombre_final = base_nombre
            contador = 1
            
            # Comprobar si ya existen carpetas con ese nombre y evitar sobrescribir
            rutas = {}
            for carpeta in ["fotos"]:  # Siempre creamos la carpeta de fotos
                ruta_base = os.path.join(carpeta, nombre_final)
                while os.path.exists(ruta_base):
                    nombre_final = f"{base_nombre}_{contador}"
                    ruta_base = os.path.join(carpeta, nombre_final)
                    contador += 1
                rutas[carpeta] = ruta_base
                os.makedirs(ruta_base, exist_ok=True)

            # Estas carpetas solo se crean si hay archivos correspondientes
            if pdf_documentacion:
                carpeta = "pdf_documentaciones"
                ruta_base = os.path.join(carpeta, nombre_final)
                rutas[carpeta] = ruta_base
                os.makedirs(ruta_base, exist_ok=True)

            if pdf_especificaciones:
                carpeta = "pdf_especificaciones"
                ruta_base = os.path.join(carpeta, nombre_final)
                rutas[carpeta] = ruta_base
                os.makedirs(ruta_base, exist_ok=True)

            # Guardar imágenes
            if imagenes:
                for imagen in imagenes:
                    try:
                        with open(os.path.join(rutas["fotos"], imagen.name), "wb") as f:
                            f.write(imagen.getvalue())
                    except Exception as e:
                        st.error(f"Error al guardar la imagen {imagen.name}: {e}")

            # Guardar PDF de documentación
            ruta_doc = None
            if pdf_documentacion and "pdf_documentaciones" in rutas:
                try:
                    ruta_archivo_doc = os.path.join(rutas["pdf_documentaciones"], pdf_documentacion.name)
                    with open(ruta_archivo_doc, "wb") as f:
                        f.write(pdf_documentacion.getvalue())
                    ruta_doc = ruta_archivo_doc
                except Exception as e:
                    st.error(f"Error al guardar el PDF de Documentación: {e}")

            # Guardar PDF de especificaciones
            ruta_esp = None
            if pdf_especificaciones and "pdf_especificaciones" in rutas:
                try:
                    ruta_archivo_esp = os.path.join(rutas["pdf_especificaciones"], pdf_especificaciones.name)
                    with open(ruta_archivo_esp, "wb") as f:
                        f.write(pdf_especificaciones.getvalue())
                    ruta_esp = ruta_archivo_esp
                except Exception as e:
                    st.error(f"Error al guardar el PDF de Especificaciones: {e}")

            # Agregar las rutas a los valores del formulario
            valores_formulario['ruta_pdf_especificaciones'] = ruta_esp
            valores_formulario['ruta_pdf_documentacion'] = ruta_doc
            valores_formulario['ruta_fotos'] = rutas["fotos"]
            valores_formulario['nombre'] = nombre_final  # Actualizar el nombre con el nombre final

            try:
                # Construir la consulta de inserción dinámicamente
                columnas = list(valores_formulario.keys())
                placeholders = ", ".join(["?"] * len(columnas))
                columnas_str = ", ".join(columnas)
                
                query = f"""
                    INSERT INTO productos (
                        {columnas_str}
                    )
                    VALUES ({placeholders})
                """
                
                # Ejecutar la inserción
                cursor.execute(query, list(valores_formulario.values()))
                conn.commit()
                
                # Guardar información para el mensaje de éxito
                st.session_state.producto_agregado = True
                st.session_state.nombre_producto = nombre_final
                
                return True
                    
            except Exception as e:
                st.error(f"Error al guardar en la base de datos: {e}")
                return False
            finally:
                conn.close()
        
        # Crear formulario
        with st.form("formulario_producto", clear_on_submit=True):
            # Crear dinámicamente los campos del formulario según los atributos borrables
            for attr in atributos_borrables:
                nombre_atributo = attr[0]
                tipo_atributo = attr[1]
                es_principal = attr[2]
                
                # Determinar si es campo obligatorio
                etiqueta = f"{nombre_atributo.replace('_', ' ').capitalize()}"
                if nombre_atributo in ["nombre", "ubicacion", "persona_responsable"]:
                    etiqueta += " *"
                    
                # Crear el campo adecuado según el tipo
                if tipo_atributo == 'date':
                    st.date_input(etiqueta, value=None, key=f"input_{nombre_atributo}")
                elif tipo_atributo == 'integer':
                    st.number_input(etiqueta, key=f"input_{nombre_atributo}", step=1)
                else:  # text
                    st.text_input(etiqueta, key=f"input_{nombre_atributo}")

            # Cargar archivo PDF de documentación
            st.file_uploader(
                "Subir PDF de Documentación",
                type=["pdf"],
                help="Selecciona un archivo en formato PDF",
                key="input_pdf_documentacion"
            )

            # Cargar archivo PDF de especificaciones
            st.file_uploader(
                "Subir PDF de Especificaciones",
                type=["pdf"],
                help="Selecciona un archivo en formato PDF",
                key="input_pdf_especificaciones"
            )

            # Cargar imágenes
            st.file_uploader(
                "Subir imágenes del producto",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=True,
                help="Selecciona imágenes en formato PNG, JPG o JPEG",
                key="input_imagenes"
            )

            # Botón de envío
            submitted = st.form_submit_button("Guardar producto", icon="➕")
            
            if submitted:
                success = submit_form()
                if success:
                    st.rerun()

            # Mostrar mensaje de éxito si corresponde
            if st.session_state.producto_agregado:
                st.success(f"Producto '{st.session_state.nombre_producto}' añadido exitosamente.")
                st.session_state.producto_agregado = False
                
        # Cerrar la conexión a la base de datos
        conn.close()


#     ██████╗  ███████╗ ███████╗ ████████╗ ██╗  ██████╗  ███╗   ██╗     ██████╗  ██████╗ 
#    ██╔════╝  ██╔════╝ ██╔════╝ ╚══██╔══╝ ██║ ██╔═══██╗ ████╗  ██║     ██╔══██╗ ██╔══██╗
#    ██║  ███╗ █████╗   ███████╗    ██║    ██║ ██║   ██║ ██╔██╗ ██║     ██║  ██║ ██████╔╝
#    ██║   ██║ ██╔══╝   ╚════██║    ██║    ██║ ██║   ██║ ██║╚██╗██║     ██║  ██║ ██╔══██╗
#    ╚██████╔╝ ███████╗ ███████║    ██║    ██║ ╚██████╔╝ ██║ ╚████║     ██████╔╝ ██████╔╝
#     ╚═════╝  ╚══════╝ ╚══════╝    ╚═╝    ╚═╝  ╚═════╝  ╚═╝  ╚═══╝     ╚═════╝  ╚═════╝ 


# Página de Opciones Base de Datos
    elif st.session_state.current_page == "Opciones base de datos":
        # Verificar si el usuario es administrador
        conn = sqlite3.connect("base_datos_inventario.db")
        cursor = conn.cursor()

        query_admin = "SELECT es_admin FROM usuarios WHERE usuario = ? AND contraseña = ?"
        cursor.execute(query_admin, (st.session_state.usuarioActivo, st.session_state.contraseñaActiva))
        result = cursor.fetchone()

        if not result or result[0] != 1:
            st.warning("Esta sección es solo para administradores.")
            st.session_state.current_page = "Ver productos"
            st.rerun()

        st.title("Opciones de Base de Datos")

        if 'limpiar_input_atributo' not in st.session_state:
            st.session_state.limpiar_input_atributo = False
        if 'mensaje_agregar' not in st.session_state:
            st.session_state.mensaje_agregar = None
        if 'mensaje_eliminar' not in st.session_state:
            st.session_state.mensaje_eliminar = None

        tab_gestionar, tab_mostrar, tab_borrar = st.tabs(["Gestionar Atributos", "Configurar Visualización", "Borrar datos"])

        with tab_gestionar:
            st.subheader("Agregar Nuevo Atributo")

            def reset_input():
                st.session_state.limpiar_input_atributo = True
                return ""

            with st.form("agregar_atributo", clear_on_submit=True):
                valor_inicial = "" if st.session_state.limpiar_input_atributo else st.session_state.get('valor_actual_input', "")
                if st.session_state.limpiar_input_atributo:
                    st.session_state.limpiar_input_atributo = False

                nuevo_atributo = st.text_input("Nombre del atributo:",
                                            key="input_nuevo_atributo",
                                            placeholder="Ingresa nombre del nuevo atributo",
                                            value=valor_inicial)

                tipo_atributo = st.selectbox(
                    "Tipo de dato:",
                    options=["text", "date"],
                    format_func=lambda x: {
                        "text": "Texto",
                        "date": "Fecha"
                    }.get(x)
                )
                mostrar_principal = st.checkbox("Mostrar en tabla principal", value=False)
                submitted = st.form_submit_button("Agregar atributo")

                if st.session_state.mensaje_agregar:
                    if "error" in st.session_state.mensaje_agregar:
                        st.error(st.session_state.mensaje_agregar["error"])
                    elif "success" in st.session_state.mensaje_agregar:
                        st.success(st.session_state.mensaje_agregar["success"])
                    st.session_state.mensaje_agregar = None

                if submitted:
                    if not nuevo_atributo or not nuevo_atributo.strip():
                        st.session_state.mensaje_agregar = {"error": "El nombre del atributo no puede estar vacío."}
                        st.session_state.valor_actual_input = nuevo_atributo  # Guardar input en error
                        st.rerun()
                    else:
                        nuevo_atributo = nuevo_atributo.strip().lower().replace(" ", "_")
                        cursor.execute("SELECT COUNT(*) FROM atributos WHERE nombre = ?", (nuevo_atributo,))
                        exists = cursor.fetchone()[0]

                        if exists:
                            st.session_state.mensaje_agregar = {"error": f"El atributo '{nuevo_atributo}' ya existe."}
                            st.session_state.valor_actual_input = nuevo_atributo  # Guardar input en error
                            st.rerun()
                        else:
                            try:
                                cursor.execute("SELECT MAX(orden) FROM atributos")
                                max_orden = cursor.fetchone()[0] or 0

                                cursor.execute("""
                                    INSERT INTO atributos (nombre, es_principal, tipo, orden, borrable)
                                    VALUES (?, ?, ?, ?, ?)
                                """, (nuevo_atributo, 1 if mostrar_principal else 0, tipo_atributo, max_orden + 1, 1))

                                cursor.execute("PRAGMA table_info(productos)")
                                columnas = [col[1] for col in cursor.fetchall()]

                                if nuevo_atributo not in columnas:
                                    cursor.execute(f"ALTER TABLE productos ADD COLUMN {nuevo_atributo} {tipo_atributo}")

                                conn.commit()
                                st.session_state.mensaje_agregar = {"success": f"Atributo '{nuevo_atributo}' agregado correctamente."}
                                st.session_state.limpiar_input_atributo = True
                                st.session_state.valor_actual_input = ""
                                if "input_nuevo_atributo" in st.session_state:
                                    del st.session_state["input_nuevo_atributo"]
                                st.rerun()
                            except sqlite3.Error as e:
                                st.session_state.mensaje_agregar = {"error": f"Error al agregar el atributo: {e}"}
                                st.session_state.valor_actual_input = nuevo_atributo
                                st.rerun()
            st.subheader("Eliminar Atributo")

            cursor.execute("""
                SELECT nombre FROM atributos 
                WHERE borrable = 1
                ORDER BY orden
            """)
            atributos = [a[0] for a in cursor.fetchall()]

            if atributos:
                with st.form("eliminar_atributo"):
                    atributo_seleccionado = st.selectbox("Seleccionar atributo a eliminar:", options=[""] + atributos)
                    st.warning("⚠️ ADVERTENCIA: Al eliminar un atributo se perderán todos los datos asociados a él en todos los productos.")
                    submit_eliminar = st.form_submit_button("Eliminar atributo")

                    if st.session_state.mensaje_eliminar:
                        if "error" in st.session_state.mensaje_eliminar:
                            st.error(st.session_state.mensaje_eliminar["error"])
                        elif "success" in st.session_state.mensaje_eliminar:
                            st.success(st.session_state.mensaje_eliminar["success"])
                        st.session_state.mensaje_eliminar = None

                    if submit_eliminar:
                        if not atributo_seleccionado:
                            st.session_state.mensaje_eliminar = {"error": "Por favor, selecciona un atributo para eliminar."}
                            st.rerun()
                        try:
                            nombre_eliminado = atributo_seleccionado

                            cursor.execute("DELETE FROM atributos WHERE nombre = ?", (atributo_seleccionado,))

                            cursor.execute("PRAGMA table_info(productos)")
                            columnas_actuales_info = cursor.fetchall()
                            columnas_filtradas = [col for col in columnas_actuales_info if col[1] != atributo_seleccionado]

                            orden_fijo = [
                                "nombre", "ubicacion", "descripcion", "palabras_clave",
                                "ruta_fotos", "ruta_pdf_especificaciones", "ruta_pdf_documentacion",
                                "persona_responsable", "numero_inventario", "fecha_compra",
                                "numero_serie", "proyecto", "numero_factura"
                            ]

                            columnas_filtradas_ordenadas = sorted(
                                columnas_filtradas,
                                key=lambda c: orden_fijo.index(c[1]) if c[1] in orden_fijo else 999
                            )

                            columnas_definiciones = []
                            for col in columnas_filtradas_ordenadas:
                                columna_def = f"{col[1]} {col[2]}"
                                if col[3]:
                                    columna_def += " NOT NULL"
                                columnas_definiciones.append(columna_def)

                            create_table_script = "CREATE TABLE productos (\n"
                            create_table_script += ",\n".join([f"  {col_def}" for col_def in columnas_definiciones])
                            create_table_script += "\n);"

                            columnas_nombres = [col[1] for col in columnas_filtradas_ordenadas]
                            columnas_str = ", ".join(columnas_nombres)

                            cursor.execute("ALTER TABLE productos RENAME TO productos_backup")
                            cursor.execute(create_table_script)
                            cursor.execute(f"INSERT INTO productos ({columnas_str}) SELECT {columnas_str} FROM productos_backup")
                            cursor.execute("DROP TABLE productos_backup")

                            conn.commit()
                            st.session_state.mensaje_eliminar = {"success": f"Atributo '{nombre_eliminado}' eliminado correctamente de la base de datos y de los productos."}
                            st.session_state.valor_actual_input = ""
                            if "input_nuevo_atributo" in st.session_state:
                                del st.session_state["input_nuevo_atributo"]
                            st.rerun()

                        except Exception as e:
                            st.session_state.mensaje_eliminar = {"error": f"Error al eliminar el atributo: {e}"}
                            st.rerun()
            else:
                st.info("No hay atributos que se puedan eliminar.")
                


        with tab_mostrar:
            st.subheader("Configurar Visualización de Atributos")
            # 🧹 CAMBIO: solo atributos donde borrable = 1
            cursor.execute("SELECT nombre, es_principal, orden FROM atributos WHERE borrable = 1 ORDER BY orden")
            atributos = cursor.fetchall()

            st.write("Selecciona los atributos que quieres mostrar en la tabla principal:")

            with st.form("configurar_atributos"):
                atributos_estados = {}
                atributos_ordenados = []

                for atributo in atributos:
                    nombre_atributo, es_principal, orden = atributo
                    mostrar = st.checkbox(f"{nombre_atributo}", value=bool(es_principal))
                    atributos_estados[nombre_atributo] = mostrar
                    atributos_ordenados.append((nombre_atributo, mostrar, orden))

                submitted = st.form_submit_button("Guardar configuración")
                if submitted:
                    try:
                        for nombre_atributo, mostrar in atributos_estados.items():
                            cursor.execute("""
                            UPDATE atributos SET es_principal = ? WHERE nombre = ?
                            """, (1 if mostrar else 0, nombre_atributo))
                        conn.commit()
                        st.success("Configuración guardada correctamente.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al actualizar la configuración: {e}")

            st.subheader("Reordenar Atributos en la Tabla Principal")
            atributos_principales = [a for a in atributos_ordenados if a[1]]

            if atributos_principales:
                opciones_reordenar = [nombre for nombre, _, _ in atributos_principales]

                nuevas_posiciones = st.multiselect(
                    "Selecciona el orden de los atributos principales:",
                    options=opciones_reordenar,
                    default=opciones_reordenar
                )

                if st.button("Guardar orden"):
                    try:
                        for i, nombre in enumerate(nuevas_posiciones):
                            cursor.execute("UPDATE atributos SET orden = ? WHERE nombre = ?", (i + 1, nombre))
                        conn.commit()
                        st.success("Orden de atributos actualizado correctamente.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al actualizar el orden: {e}")
            else:
                st.info("No hay atributos seleccionados para mostrar en la tabla principal.")

        conn.close()

        with tab_borrar:
            st.subheader("Eliminar productos masivamente")

            db_path = "base_datos_inventario.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT nombre FROM productos")
            productos = [row[0] for row in cursor.fetchall()]

            if "todos_seleccionados" not in st.session_state:
                st.session_state.todos_seleccionados = False

            seleccionados = st.multiselect(
                "Selecciona los productos a eliminar",
                productos,
                default=productos if st.session_state.todos_seleccionados else []
            )

            col_sel_all, col_clear_sel = st.columns([1, 1])
            with col_sel_all:
                if st.button("Seleccionar todos"):
                    st.session_state.todos_seleccionados = True
                    st.rerun()
            with col_clear_sel:
                if st.button("Limpiar selección"):
                    st.session_state.todos_seleccionados = False
                    st.rerun()

            if seleccionados:
                if "confirmacion_eliminar" not in st.session_state:
                    st.session_state.confirmacion_eliminar = False

                if not st.session_state.confirmacion_eliminar:
                    if st.button("🗑️ Eliminar productos seleccionados"):
                        st.session_state.confirmacion_eliminar = True
                        st.rerun()
                else:
                    st.warning(f"⚠️ ¿Estás seguro de que deseas eliminar {len(seleccionados)} productos? Esta acción no se puede deshacer.")
                    col_yes, col_no = st.columns(2)

                    with col_yes:
                        if st.button("✅ Sí, eliminar"):
                            for nombre in seleccionados:
                                cursor.execute("""
                                    SELECT ruta_fotos, ruta_pdf_documentacion, ruta_pdf_especificaciones
                                    FROM productos
                                    WHERE nombre = ?
                                """, (nombre,))
                                rutas = cursor.fetchone()

                                cursor.execute("DELETE FROM productos WHERE nombre = ?", (nombre,))
                                conn.commit()

                                ruta_fotos = rutas[0]
                                if ruta_fotos and os.path.exists(ruta_fotos):
                                    try:
                                        shutil.rmtree(ruta_fotos)
                                    except Exception as e:
                                        st.warning(f"No se pudo eliminar la carpeta de fotos para {nombre}: {e}")

                                ruta_doc = rutas[1]
                                if ruta_doc:
                                    try:
                                        carpeta = os.path.dirname(ruta_doc) if os.path.isfile(ruta_doc) else ruta_doc
                                        shutil.rmtree(carpeta)
                                    except Exception as e:
                                        st.warning(f"No se pudo eliminar la carpeta de documentación para {nombre}: {e}")

                                ruta_spec = rutas[2]
                                if ruta_spec:
                                    try:
                                        carpeta = os.path.dirname(ruta_spec) if os.path.isfile(ruta_spec) else ruta_spec
                                        shutil.rmtree(carpeta)
                                    except Exception as e:
                                        st.warning(f"No se pudo eliminar la carpeta de especificaciones para {nombre}: {e}")

                            st.success(f"Se eliminaron {len(seleccionados)} productos correctamente.")
                            st.session_state.confirmacion_eliminar = False
                            st.session_state.todos_seleccionados = False
                            st.rerun()

                    with col_no:
                        if st.button("❌ Cancelar"):
                            st.session_state.confirmacion_eliminar = False
                            st.rerun()