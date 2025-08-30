#crcastro 2025-08-29
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime, timedelta
import calendar # Importa el módulo calendar
import os # Importa el módulo 'os' para verificar la existencia del archivo
import requests # Para hacer peticiones HTTP
from bs4 import BeautifulSoup # Para parsear HTML



# Función para realizar web scraping de las tasas de cambio
def get_exchange_rates():
    """
    Extrae las tasas de cambio del Dólar y el Euro desde la página oficial del BCV.
    """
    url = "https://www.bcv.org.ve/glosario/cambio-oficial"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        # Se añade `verify=False` para ignorar la verificación del certificado SSL
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()  # Lanza un error si la solicitud no fue exitosa
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscar los elementos que contienen las tasas
        # Se asume una estructura donde las tasas están en un h6
        # Si la estructura cambia, este selector debe ser ajustado
        dolar_text = soup.find('div', id='dolar').find('strong').text.strip().replace(',', '.')
        euro_text = soup.find('div', id='euro').find('strong').text.strip().replace(',', '.')
        
        dolar_rate = float(dolar_text)
        euro_rate = float(euro_text)
        
        return dolar_rate, euro_rate
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la página del BCV: {e}")
        return None, None
    except AttributeError:
        st.error("Error al encontrar las tasas en la página del BCV. La estructura HTML puede haber cambiado.")
        return None, None
    except ValueError:
        st.error("Error al convertir la tasa de cambio. El formato en la página no es el esperado.")
        return None, None


# --- Configuración de la Página ---
def principal():
    """Página principal de la aplicación."""
    
    # Creamos dos columnas con una relación de 0.5:4 para forzar la imagen a la izquierda
    col1, col2 = st.columns([1.0, 4]) 
    
    image_path = "./assets/imagen1.jpg"
    
    with col1:
        # Verifica si el archivo de imagen existe antes de intentar mostrarlo
        if os.path.exists(image_path):
            st.image(image_path)
        else:
            st.warning(f"Advertencia: No se encontró la imagen en la ruta '{image_path}'. Asegúrate de que el archivo exista.")
    
    with col2:
        st.title("Te gusto el Aumento ? 😢")

    st.markdown("""
    ¡Bienvenido a tu herramienta para visualizar tus ingresos!
    
    Esta aplicación te permite de manera sencilla:
    
    * Calcular tus nuevos salarios después de un aumento.
    * Visualizar el impacto de tus aumentos con gráficos interactivos.
    * Analizar tu historial salarial de forma clara.
    """)
    
    st.header("¿Cómo empezar?")
    st.markdown("""
    Simplemente sigue estos 3 pasos:
    
    1.  **Navega a la página de "Gráficos Interactivos"** usando el menú de la izquierda.
    2.  **Ingresa tu información** de salario y aumento en el formulario. Los gráficos se actualizarán automáticamente.
    3.  **Opcional: Si tienes muchos datos,** ve a la página de "Visualización" y carga un archivo CSV para un análisis más completo.
    
    ¡Y listo! Podrás ver cómo tus aumentos afectan tus ingresos de manera visual e interactiva.

    """)
    st.warning("No olvides que puedes usar el menú lateral en cualquier momento para ir a las diferentes secciones.")
    st.warning("No olvides darles las gracias a tu VP por este maravilloso aumento. 😂", icon="⚠️")


def Visualizacion():
    """Página para cargar y visualizar datos desde un archivo CSV."""
    st.title("Visualización de Datos")
    st.write("Carga un archivo CSV para la visualización de tu Aumento.")
    st.warning("El archivo CSV debe contener las columnas 'Empleado', 'Salario_Actual', 'Aumento_(%)' o 'Monto_Aumento' y 'Fecha_Aumento', separadas por coma.")
    file_csv = st.file_uploader("Carga tu archivo CSV", type=["csv"])

    if file_csv is not None:
        df = pd.read_csv(file_csv)
        st.write("Datos Cargados:")
        st.dataframe(df)

        # Validar columnas necesarias
        if 'Empleado' in df.columns and 'Salario_Actual' in df.columns and ('Aumento_(%)' in df.columns or 'Monto_Aumento' in df.columns):
            # Obtener las tasas de cambio
            dolar_rate, euro_rate = get_exchange_rates()
            if not dolar_rate or not euro_rate:
                st.error("No se pudieron obtener las tasas de cambio. Los valores en USD/EUR no se mostrarán.")
                dolar_rate = 1
                euro_rate = 1

            # Calcular el nuevo salario
            if 'Monto_Aumento' in df.columns:
                df['Nuevo Salario'] = df['Salario_Actual'] + df['Monto_Aumento']
                df['Monto_Aumento_USD'] = df['Monto_Aumento'] / dolar_rate
                df['Monto_Aumento_EUR'] = df['Monto_Aumento'] / euro_rate
            else:
                df['Nuevo Salario'] = df['Salario_Actual'] * (1 + df['Aumento_(%)'] / 100)

            # Convertir la columna de fechas a formato datetime si existe
            if 'Fecha_Aumento' in df.columns:
                df['Fecha_Aumento'] = pd.to_datetime(df['Fecha_Aumento'])

            # Calcular las conversiones de salario
            df['Salario_Actual_USD'] = df['Salario_Actual'] / dolar_rate
            df['Salario_Actual_EUR'] = df['Salario_Actual'] / euro_rate
            df['Nuevo_Salario_USD'] = df['Nuevo Salario'] / dolar_rate
            df['Nuevo_Salario_EUR'] = df['Nuevo Salario'] / euro_rate


            st.write("Datos con Nuevo Salario Calculado:")
            st.dataframe(df.round(2)) # Redondeamos para mejor visualización
            st.write("Resumen Estadístico:")

            # GRÁFICO 1: Comparación de salarios
            fig = px.bar(df, x='Empleado', y=['Salario_Actual', 'Nuevo Salario'], barmode='group',
                         title="Comparación de Salarios Antes y Después del Aumento")
            st.plotly_chart(fig)

            # GRÁFICO 2: Evolución de salarios en el tiempo
            if 'Fecha_Aumento' in df.columns:
                # Crear un DataFrame para el Salario Actual en la fecha de hoy
                df_salario_actual = df[['Empleado', 'Salario_Actual']].copy()
                df_salario_actual['Fecha'] = pd.to_datetime('today').normalize()
                df_salario_actual.rename(columns={'Salario_Actual': 'Salario'}, inplace=True)

                # Crear un DataFrame para el Nuevo Salario en la fecha de aumento
                df_nuevo_salario = df[['Empleado', 'Fecha_Aumento', 'Nuevo Salario']].copy()
                df_nuevo_salario.rename(columns={'Nuevo Salario': 'Salario', 'Fecha_Aumento': 'Fecha'}, inplace=True)

                # Unir los dos DataFrames
                df_evolucion = pd.concat([df_salario_actual, df_nuevo_salario], ignore_index=True)
                df_evolucion.sort_values(by=['Empleado', 'Fecha'], inplace=True)

                # Generar el gráfico de línea
                fig2 = px.line(df_evolucion, x='Fecha', y='Salario', color='Empleado',
                               title="Evolución del Salario en el Tiempo")
                st.plotly_chart(fig2)
            else:
                st.error("Para el gráfico de evolución, el archivo debe contener la columna 'Fecha_Aumento'.")

            # Botones de descarga
            download_grafic = st.download_button(
                label="Descargar Gráficos Comparación",
                data=fig.to_html(),
                file_name="Grafico_comparacion_salarios_Antes_Despues.html",
                mime="text/html"
            )
            if 'Fecha_Aumento' in df.columns:
                download_evolucion = st.download_button(
                    label="Descargar Gráficos Evolución de Salario",
                    data=fig2.to_html(),
                    file_name="Grafico_evolucion_salarios.html",
                    mime="text/html"
                )
        else:
            st.error("El archivo CSV no contiene las columnas necesarias.")
            st.write("Asegúrate de que tu archivo CSV tenga las siguientes columnas:")
            st.write("- Empleado")
            st.write("- Salario_Actual")
            st.write("- Aumento_(%) o Monto_Aumento")
            st.write("- Fecha_Aumento")

def Graficos_Interactivos():
    """Página para ingresar datos manualmente y generar gráficos."""
    st.title("Carga tu Sueldo y Bonos sin llorar")
    st.write("Ingresa tus datos de salario y aumento. Los datos de la tabla y los gráficos se actualizarán a continuación.")

    # Inicializar una lista en el estado de la sesión si aún no existe
    if 'data_records' not in st.session_state:
        st.session_state.data_records = []

    # Crear un formulario para recolectar los datos.
    with st.form(key='salary_form'):
        st.subheader("Ingresar nuevo registro de salario")
        nombre = st.text_input("Nombre del Empleado", key="form_nombre")
        salario = st.number_input("Salario Anual", min_value=0.0, format="%f", key="form_salario")
        bono = st.number_input("Bono Actual", min_value=0.0, format="%f", key="form_bono")
        aumento_porcentaje = st.number_input("% de Aumento", min_value=0.0, format="%f", key="form_aumento")
        fecha_aumento = st.date_input("Fecha de Aumento", date.today(), key="form_fecha")
        
        # Botón para enviar el formulario
        submit_button = st.form_submit_button(label='Guardar Datos')

    # Si el formulario fue enviado
    if submit_button:
        # Crea un diccionario con los datos
        record = {
            "Empleado": nombre,
            "Salario_Actual": salario,
            "Bono": bono,
            "Aumento_(%)": aumento_porcentaje,
            "Fecha_Aumento": fecha_aumento.strftime("%Y-%m-%d") # Formato para compatibilidad
        }
        # Agrega el nuevo registro a la lista en el estado de la sesión
        st.session_state.data_records.append(record)
        st.success("¡Datos guardados con éxito!")
    
    # Mostrar la tabla de datos y los gráficos solo si hay registros
    if st.session_state.data_records:
        st.subheader("Datos Ingresados")
        # Convertir la lista de diccionarios a un DataFrame de Pandas
        df = pd.DataFrame(st.session_state.data_records)
        df['Nuevo Salario'] = df['Salario_Actual'] * (1 + df['Aumento_(%)'] / 100)
        
        # Obtener las tasas de cambio
        dolar_rate, euro_rate = get_exchange_rates()
        if not dolar_rate or not euro_rate:
            st.error("No se pudieron obtener las tasas de cambio. Los valores en USD/EUR no se mostrarán.")
            dolar_rate = 1
            euro_rate = 1

        # Agregar columnas con la conversión de salario y bono a USD y EUR
        df['Salario_Actual_USD'] = df['Salario_Actual'] / dolar_rate
        df['Salario_Actual_EUR'] = df['Salario_Actual'] / euro_rate
        df['Bono_USD'] = df['Bono'] / dolar_rate
        df['Bono_EUR'] = df['Bono'] / euro_rate

        # Mostrar la tabla
        st.dataframe(df.round(2)) # Redondeamos para mejor visualización

        # Gráfico de barras
        fig_bar = px.bar(df, x='Empleado', y=['Salario_Actual', 'Nuevo Salario'], barmode='group',
                         title="Comparación de Salarios (Interactivos)")
        st.plotly_chart(fig_bar)

        # Gráfico de línea
        fig_line = px.line(df, x='Fecha_Aumento', y=['Salario_Actual', 'Nuevo Salario'],
                           title="Evolución de Salarios (Interactivos)")
        st.plotly_chart(fig_line)

        # Botón para limpiar los datos
        st.button("Limpiar Datos", on_click=lambda: st.session_state.data_records.clear())
        
        # Botón de descarga de la información como CSV
        st.download_button(
            label="Descargar Datos",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="datos_salarios.csv",
            mime="text/csv"
        )
        # Boton de descarga de Graficos
        st.download_button(
            label="Descargar Gráfico de Barras",
            data=fig_bar.to_html(),
            file_name="Grafico_barras_salarios.html",
            mime="text/html"
        )
        st.download_button(
            label="Descargar Gráfico de Líneas",
            data=fig_line.to_html(),
            file_name="Grafico_lineas_salarios.html",
            mime="text/html"
        )


# Función para calcular el pago de vacaciones
def calcular_vacaciones_pago(salario_mensual, fecha_ingreso):
    """
    Calcula el pago de vacaciones y el bono vacacional.
    Regla: 15 días base + 1 día por cada año de antigüedad a partir del segundo año.
    Bono Vacacional: 15 días de salario.
    """
    hoy = date.today()
    antiguedad_timedelta = hoy - fecha_ingreso
    antiguedad_anos = antiguedad_timedelta.days // 365

    # Cálculo de los días de vacaciones legales según la antigüedad
    dias_vacaciones_legales = 15
    # La regla legal establece 15 días base para el primer año y 1 día adicional por cada año subsiguiente
    # Por lo tanto, se suma un día por cada año de antigüedad completo
    if antiguedad_anos >= 1:
        dias_vacaciones_legales += antiguedad_anos

    # Cálculo del monto del salario diario
    salario_diario = salario_mensual / 30

    # Monto de las vacaciones
    monto_vacaciones = salario_diario * dias_vacaciones_legales
    
    # Monto del bono vacacional (15 días)
    monto_bono = salario_diario * 15

    # Pago total por vacaciones
    pago_total_vacaciones = monto_vacaciones + monto_bono

    return antiguedad_anos, dias_vacaciones_legales, monto_bono, pago_total_vacaciones


def Vacaciones():
    """Página para calculo de Vacaciones."""
    st.title("Cálculo de Vacaciones")
    st.markdown("""
    Aquí puedes calcular el monto de tu pago de vacaciones y bono vacacional.
    
    Ingresa los siguientes datos:
    """)

    with st.form(key='vacaciones_form'):
        col1, col2 = st.columns(2)
        with col1:
            fecha_ingreso = st.date_input("Fecha de Ingreso", date.today(), key="fecha_ingreso")
        with col2:
            salario_mensual = st.number_input("Salario Mensual (VES)", min_value=0.0, format="%f", key="salario_mensual")

        st.markdown("---")
        st.subheader("Fechas de Disfrute (Opcional)")
        st.markdown("Estas fechas son solo para referencia y no se usan en el cálculo actual.")
        col3, col4 = st.columns(2)
        with col3:
            fecha_inicio = st.date_input("Fecha de Inicio de Vacaciones", date.today(), key="fecha_inicio_vacaciones")
        with col4:
            fecha_fin = st.date_input("Fecha de Fin de Vacaciones", date.today(), key="fecha_fin_vacaciones")

        calcular_button = st.form_submit_button(label="Calcular Vacaciones")

    if calcular_button and salario_mensual > 0:
        # Realizar los cálculos
        antiguedad_anos, dias_vacaciones, monto_bono, pago_total_ves = calcular_vacaciones_pago(salario_mensual, fecha_ingreso)

        # Obtener las tasas de cambio para la conversión
        dolar_rate, euro_rate = get_exchange_rates()
        
        # Mostrar el resultado del cálculo en VES
        st.subheader("Resultados del Cálculo")
        st.markdown(f"**Antigüedad:** {antiguedad_anos} años")
        st.markdown(f"**Días de Vacaciones:** {dias_vacaciones} días")
        st.markdown(f"**Días de Bono Vacacional:** 15 días")
        st.metric(label="Monto Total a Pagar (VES)", value=f"Bs. {pago_total_ves:,.2f}")

        # Si las tasas de cambio se obtuvieron correctamente, mostrar las conversiones
        if dolar_rate and euro_rate:
            pago_total_usd = pago_total_ves / dolar_rate
            pago_total_eur = pago_total_ves / euro_rate
            
            # Mostrar los montos con el nuevo formato
            st.metric(label="Monto Total a Pagar (USD)", value=f"$ {pago_total_usd:,.2f}")
            st.metric(label="Monto Total a Pagar (EUR)", value=f"€ {pago_total_eur:,.2f}")
        else:
            st.error("No se pudieron obtener las tasas de cambio. Por favor, inténtalo de nuevo más tarde.")

        # --- Nuevo Calendario Visual de Vacaciones ---
        st.subheader("Calendario de Vacaciones")
        if fecha_fin < fecha_inicio:
            st.error("La fecha de fin de vacaciones no puede ser anterior a la fecha de inicio.")
        else:
            # Lista para almacenar los dataframes de cada mes
            calendarios_df = []
            current_date = fecha_inicio
            
            while current_date <= fecha_fin:
                # Días de la semana en español
                dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
                
                # Creamos un objeto de calendario en español
                cal = calendar.Calendar(firstweekday=calendar.MONDAY)
                
                # Obtener las fechas del mes actual
                fechas_mes = list(cal.itermonthdates(current_date.year, current_date.month))
                fechas_vacaciones = set([fecha_inicio + timedelta(days=x) for x in range((fecha_fin - fecha_inicio).days + 1)])
                
                # Rellenar con los días del mes y marcar los días de vacaciones
                dias_calendario = []
                for fecha in fechas_mes:
                    if fecha.month == current_date.month:
                        if fecha in fechas_vacaciones:
                            dias_calendario.append(f"**{fecha.day}**") # Resaltar con negritas
                        else:
                            dias_calendario.append(str(fecha.day))
                    else:
                        dias_calendario.append('')
                
                # Convertir la lista plana en una lista de listas para el DataFrame
                semanas = [dias_calendario[i:i+7] for i in range(0, len(dias_calendario), 7)]
                
                # Convertir la lista en un DataFrame para mostrar el calendario
                calendario_df = pd.DataFrame(semanas, columns=dias_semana)
                calendarios_df.append((f"{current_date.strftime('%B %Y')}", calendario_df))
                
                # Avanzar al siguiente mes
                current_date = current_date.replace(day=28) + timedelta(days=4)
                current_date = current_date.replace(day=1)

            # Mostrar cada calendario
            for month_name, df in calendarios_df:
                st.subheader(f"Calendario de Vacaciones - {month_name}")
                st.dataframe(df, hide_index=True)

            st.markdown(f"**Número de Días de Vacaciones:** {len(fechas_vacaciones)} días.")
        
        # --- Botón de descarga para el reporte de vacaciones en formato HTML ---
        # Crear el contenido del archivo HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Vacaciones</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; padding: 20px; color: #333; }}
        .container {{ max-width: 800px; margin: auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h1, h2, h3 {{ color: #004d99; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: center; }}
        th {{ background-color: #f2f2f2; }}
        .vacation-day {{ font-weight: bold; background-color: #e6f7ff; color: #004d99; }}
        .metric {{ border-left: 5px solid #004d99; padding-left: 10px; margin-top: 15px; }}
        .metric-value {{ font-size: 1.5em; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Reporte de Cálculo de Vacaciones</h1>
        <p>Este reporte detalla el cálculo de tu pago de vacaciones y el calendario correspondiente.</p>
        <hr>
        <h2>Resumen del Cálculo</h2>
        <p><strong>Antigüedad:</strong> {antiguedad_anos} años</p>
        <p><strong>Días de Vacaciones:</strong> {dias_vacaciones} días</p>
        <p><strong>Bono Vacacional:</strong> 15 días</p>

        <div class="metric">
            <h3>Monto Total a Pagar (VES)</h3>
            <p class="metric-value">Bs. {pago_total_ves:,.2f}</p>
        </div>
"""
        # Agregar la conversión a USD y EUR si las tasas están disponibles
        if dolar_rate and euro_rate:
            pago_total_usd = pago_total_ves / dolar_rate
            pago_total_eur = pago_total_ves / euro_rate
            html_content += f"""
        <div class="metric">
            <h3>Monto Total a Pagar (USD)</h3>
            <p class="metric-value">$ {pago_total_usd:,.2f}</p>
        </div>
        <div class="metric">
            <h3>Monto Total a Pagar (EUR)</h3>
            <p class="metric-value">€ {pago_total_eur:,.2f}</p>
        </div>
"""

        # Agregar los calendarios al contenido HTML
        if 'calendarios_df' in locals():
            html_content += """
        <hr>
        <h2>Calendario de Vacaciones</h2>
"""
            for month_name, df in calendarios_df:
                html_content += f"""
        <h3>{month_name}</h3>
        {df.to_html(index=False, classes='calendario-table')}
"""
        html_content += """
    </div>
</body>
</html>
"""

        st.download_button(
            label="Descargar Reporte de Vacaciones",
            data=html_content.encode('utf-8'),
            file_name="reporte_vacaciones.html",
            mime="text/html"
        )


def Liquidacion():
    """Página para calculo de Liquidacion."""
    st.title("Calculadora de Liquidación")
    st.markdown("Ingresa los datos para calcular tu liquidación de acuerdo con la Ley Orgánica del Trabajo.")
    
    with st.form(key='liquidacion_form'):
        st.subheader("Datos del Empleado")
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_ingreso = st.date_input("Fecha de Ingreso", date.today(), key="liq_fecha_ingreso")
        with col2:
            fecha_egreso = st.date_input("Fecha de Egreso", date.today(), key="liq_fecha_egreso")

        st.markdown("---")
        st.subheader("Información Salarial")
        salario_base_mensual = st.number_input("Salario Base Mensual (VES)", min_value=0.0, format="%f", key="liq_salario_base")
        bono_promedio_mensual = st.number_input("Promedio de Bonos/Comisiones Mensuales (VES)", min_value=0.0, format="%f", key="liq_bono_promedio")
        
        st.markdown("---")
        st.subheader("Beneficios Pendientes y Deducciones")
        dias_vacaciones_pendientes = st.number_input("Días de vacaciones pendientes", min_value=0, key="liq_vacaciones_pendientes")
        adelanto_prestaciones = st.number_input("Adelanto de Prestaciones Sociales (VES)", min_value=0.0, format="%f", key="liq_adelanto")
        
        calcular_button = st.form_submit_button(label="Calcular Liquidación")

    if calcular_button:
        if fecha_egreso < fecha_ingreso:
            st.error("La fecha de egreso no puede ser anterior a la fecha de ingreso.")
        else:
            # Calcular la antigüedad en días, meses y años
            diferencia_dias = (fecha_egreso - fecha_ingreso).days
            antiguedad_anos = diferencia_dias // 365
            dias_restantes = diferencia_dias % 365
            
            # Cálculo del salario integral
            salario_integral = (salario_base_mensual + bono_promedio_mensual) * 1.15
            
            # Componentes de la liquidación
            # Prestaciones sociales (30 días por año de servicio, más fracción)
            prestaciones_sociales = (salario_integral / 30) * (antiguedad_anos * 30 + dias_restantes)
            
            # Vacaciones fraccionadas (15 días por año)
            vacaciones_fraccionadas = (salario_base_mensual / 30) * dias_vacaciones_pendientes
            
            # Bono Vacacional Fraccionado (15 días por año)
            bono_vacacional_fraccionado = (salario_base_mensual / 360) * diferencia_dias * 15
            
            # Salario del último mes
            dias_ultimo_mes = fecha_egreso.day
            salario_ultimo_mes = (salario_base_mensual / 30) * dias_ultimo_mes
            
            # Total de la liquidación
            total_bruto = prestaciones_sociales + vacaciones_fraccionadas + bono_vacacional_fraccionado + salario_ultimo_mes
            total_neto = total_bruto - adelanto_prestaciones
            
            # Obtener las tasas de cambio para la conversión
            dolar_rate, euro_rate = get_exchange_rates()

            # Mostrar los resultados
            st.subheader("Resultados del Cálculo de Liquidación")
            
            # Tabla de desglose
            data = {
                "Concepto": ["Salario Último Mes", "Prestaciones Sociales", "Vacaciones Fraccionadas", "Bono Vacacional Fraccionado", "TOTAL BRUTO", "Adelantos/Deducciones", "TOTAL NETO"],
                "Monto (VES)": [salario_ultimo_mes, prestaciones_sociales, vacaciones_fraccionadas, bono_vacacional_fraccionado, total_bruto, adelanto_prestaciones, total_neto]
            }
            df_resumen = pd.DataFrame(data).round(2)
            st.dataframe(df_resumen, hide_index=True)
            
            # Metricas finales
            st.metric(label="Monto Neto a Pagar (VES)", value=f"Bs. {total_neto:,.2f}")
            if dolar_rate and euro_rate:
                total_neto_usd = total_neto / dolar_rate
                total_neto_eur = total_neto / euro_rate
                st.metric(label="Monto Neto a Pagar (USD)", value=f"$ {total_neto_usd:,.2f}")
                st.metric(label="Monto Neto a Pagar (EUR)", value=f"€ {total_neto_eur:,.2f}")
            
            # Botón de descarga del reporte HTML
            html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Liquidación</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; padding: 20px; color: #333; }}
        .container {{ max-width: 800px; margin: auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h1, h2, h3 {{ color: #004d99; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .metric {{ border-left: 5px solid #004d99; padding-left: 10px; margin-top: 15px; }}
        .metric-value {{ font-size: 1.5em; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Reporte de Liquidación</h1>
        <p>Este reporte detalla el cálculo de tu liquidación de acuerdo con la información suministrada.</p>
        <hr>
        <h2>Resumen de Datos</h2>
        <p><strong>Fecha de Ingreso:</strong> {fecha_ingreso}</p>
        <p><strong>Fecha de Egreso:</strong> {fecha_egreso}</p>
        <p><strong>Antigüedad:</strong> {antiguedad_anos} años y {dias_restantes} días</p>
        <p><strong>Salario Base Mensual:</strong> Bs. {salario_base_mensual:,.2f}</p>
        <p><strong>Salario Integral:</strong> Bs. {salario_integral:,.2f}</p>
        <hr>
        <h2>Cálculo Detallado</h2>
        {df_resumen.to_html(index=False)}
        
        <div class="metric">
            <h3>Monto Neto a Pagar (VES)</h3>
            <p class="metric-value">Bs. {total_neto:,.2f}</p>
        </div>
"""
            if dolar_rate and euro_rate:
                total_neto_usd = total_neto / dolar_rate
                total_neto_eur = total_neto / euro_rate
                html_content += f"""
        <div class="metric">
            <h3>Monto Neto a Pagar (USD)</h3>
            <p class="metric-value">$ {total_neto_usd:,.2f}</p>
        </div>
        <div class="metric">
            <h3>Monto Neto a Pagar (EUR)</h3>
            <p class="metric-value">€ {total_neto_eur:,.2f}</p>
        </div>
"""
            html_content += """
    </div>
</body>
</html>
"""
            st.download_button(
                label="Descargar Reporte de Liquidación",
                data=html_content.encode('utf-8'),
                file_name="reporte_liquidacion.html",
                mime="text/html"
            )


# --- Configuración del Menú de Navegación ---
st.sidebar.title("Menú")
pagina = st.sidebar.selectbox("Selecciona una página", ["Principal", "Visualización", "Gráficos Interactivos",
                                                     "Vacaciones","Liquidacion"])

if pagina == "Principal":
    principal()
elif pagina == "Visualización":
    Visualizacion()
elif pagina == "Gráficos Interactivos":  # CORREGIDO: coincide con el texto de la opción
    Graficos_Interactivos()
elif pagina == "Vacaciones":
    Vacaciones()
elif pagina == "Liquidacion":
    Liquidacion()
