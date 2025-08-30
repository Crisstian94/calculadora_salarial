#crcastro 2025-08-29
import pandas as pd
import numpy as np

# Definimos el número de empleados para los datos de prueba
num_empleados = 10

# Nombres ficticios para los empleados
empleados = [f'Empleado_{i+1}' for i in range(num_empleados)]

# Generamos salarios aleatorios con decimales entre 30000.00 y 120000.00
salarios_actuales = np.random.uniform(30000.00, 120000.00, size=num_empleados).round(2)

# Generamos un porcentaje de aumento aleatorio con decimales entre 2% y 50%
aumento_porcentaje = np.random.uniform(2, 50, size=num_empleados).round(2)

# Calculamos el monto de aumento
monto_aumento = salarios_actuales * (aumento_porcentaje / 100)

# Generamos fechas de aumento aleatorias en el período especificado
fechas_aumento = pd.to_datetime(np.random.choice(pd.date_range('2024-03-01', '2025-08-29'), size=num_empleados))

# Creamos el diccionario de datos
data = {
    'Empleado': empleados,
    'Salario_Actual': salarios_actuales,
    'Aumento_(%)': aumento_porcentaje,
    'Monto_Aumento': monto_aumento.round(2),
    'Fecha_Aumento': fechas_aumento
}

# Creamos el DataFrame de prueba
df_aumento = pd.DataFrame(data)

# Guardamos el DataFrame en un archivo CSV
df_aumento.to_csv('aumentos.csv', index=False)

print("Archivo 'aumentos.csv' generado con éxito. Puedes usarlo para probar tu aplicación.")