📊 Aplicación de Gráficos de Salarios
¡Bienvenido a tu herramienta personal para visualizar y calcular tus ingresos y beneficios laborales! Esta aplicación, construida con Streamlit, te ayuda a entender el impacto de los aumentos salariales, calcular tu pago de vacaciones y estimar tu liquidación de manera sencilla e interactiva.

🚀 Características Principales
La aplicación está organizada en varias páginas, accesibles desde el menú lateral:

🏠 Principal
Una introducción a la aplicación y una breve guía de cómo empezar.

📈 Visualización de Datos
Carga un archivo CSV con tu historial salarial para obtener un análisis detallado y gráficos comparativos.

Formato del Archivo CSV:
El archivo debe contener las siguientes columnas (separadas por comas) para que la visualización funcione correctamente:

Empleado (Nombre del empleado)

Salario_Actual (Salario actual en bolívares)

Aumento_(%) o Monto_Aumento (Porcentaje de aumento o monto fijo en bolívares)

Fecha_Aumento (Fecha del aumento, en formato AAAA-MM-DD)

📊 Gráficos Interactivos
Ideal para cálculos rápidos. Ingresa tu salario y porcentaje de aumento manualmente y observa los cambios en tiempo real en los gráficos.

🏖️ Cálculo de Vacaciones
Calcula tu pago por vacaciones y bono vacacional, basándose en tu salario y años de antigüedad.

💰 Calculadora de Liquidación
Estima tu liquidación de acuerdo con la Ley Orgánica del Trabajo. Ingresa tu fecha de ingreso, fecha de egreso y tu salario para obtener un desglose detallado de los montos a recibir.

⚙️ Despliegue de la Aplicación (Docker y Kubernetes)
Esta aplicación está diseñada para ser desplegada en un entorno contenerizado, lo que facilita su instalación y escalabilidad. Sigue estos pasos para ponerla en marcha:

1. Dockerización
Construye la imagen de Docker en tu máquina local. Asegúrate de estar en el directorio de tu proyecto y que tu Dockerfile esté ahí.

docker build -t calculadora-salarial .

Etiqueta la imagen con tu nombre de usuario de Docker Hub.

docker tag calculadora-salarial tu_usuario_docker/calculadora-salarial:latest

Sube la imagen a Docker Hub para que sea accesible desde tu servidor.

docker push tu_usuario_docker/calculadora-salarial:latest

2. Despliegue con Kubernetes
Conéctate a tu servidor Debian y asegúrate de que kubectl esté configurado y conectado a tu clúster de Kubernetes.

Edita el archivo kubernetes.yaml y reemplaza tu_usuario_docker con tu usuario de Docker Hub.

Aplica el manifiesto de Kubernetes para desplegar la aplicación.

kubectl apply -f kubernetes.yaml

Verifica el estado de los pods y servicios para asegurarte de que todo esté corriendo.

kubectl get pods
kubectl get services

💻 Ejecución Local
Si prefieres ejecutar la aplicación en tu computadora sin usar Docker, sigue estos pasos.

1. Requisitos
Asegúrate de tener Python 3.9 o superior y las dependencias instaladas. Si aún no lo has hecho, puedes instalar las librerías con este comando:

pip install -r requirements.txt

2. Ejecutar la Aplicación
Navega hasta el directorio de tu proyecto en la terminal y usa el siguiente comando para iniciar la aplicación:

streamlit run app.py

La aplicación se abrirá automáticamente en tu navegador predeterminado en http://localhost:8501. Si no se abre, puedes copiar y pegar esa dirección en la barra de direcciones del navegador.

¡Listo! Con estos pasos, tu aplicación estará corriendo en un clúster de Kubernetes, gestionando la escalabilidad y la disponibilidad de forma automática.