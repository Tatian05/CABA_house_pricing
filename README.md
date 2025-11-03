# Análisis del Mercado Inmobiliario CABA (2024-2025)

## Objetivo del proyecto
Este proyecto se enfoca en el análisis de precios y expensas de departamentos en venta y alquiler en la Ciudad Autónoma de Buenos Aires (CABA), Argentina.
El objetivo es construir un **pipeline de datos** desde la ingesta y limpieza hasta la visualización,
permitiendo a los usuarios identificar tendencias de precios y comparar la rentabilidad entre barrios y tipos de operación.

---

## 🛠️ Stack Tecnológico

| Componente | Herramienta |
| :--- | :--- |
| **Ingeniería de Datos (ETL)** | Python (Pandas) |
| **Almacenamiento** | PostgreSQL |
| **Visualización** | Power BI |
| **Control de Versiones** | Git / GitHub |

---

## Proceso de Ingeniería de Datos (ETL)
El proceso se dividió en tres etapas utilizando scripts de Python.

1. **Ingesta(Extraction)**:
   Se utiliza Python junto a la librería *requests* para obtener los datos crudos del dataset de propiedades inmobiliarias y se carga en un DataFrame para su manipulación.
2. **Limpieza y modelado(Transformation)**:
   Esta etapa es crucial para pasar de los datos crudos a un **Modelo Dimensional (Esquema Estrella)**
   - Pequeñas transformaciones: Cambios en la nomenclatura y asignación del tipo de dato correspondiente a las columnas, eliminación de filas con datos críticos nulos y outliers.
   - Parseo de características: Se aplicarion **expresiones regulares(Regex)** para extrear características clave del campo de texto descriptivo *features*, creando columnas numéricas para:
     - m² (metros cuadrados)
     - n_rooms (Ambientes)
     - n_bed (Dormitorios)
     - n_bath (Baños)
     - has_park (Cocheras)
   - Creación del modelo: Los datos se separaron en las siguientes tablas optimizadas
     - Hecho (fact_prices): Contiene métricas como *price*, *expenses* y fecha de obtención *fetch_date*.
     - Dimensiones(dim_operation, dim_neighborhood, dim_departments): Contienen atributos descriptivos como dirección, características y nombre del barrio.
4. **Almacenamiento(Load)**:
   Las tablas del modelo dimensional se almacenan en una base de datos PostgreSQL para luegos ser leídos en Power BI.

---

## Análisis de Datos y Dashboard (Power BI)
1. **Modelado en Power BI**
   Se establecieron relaciones de **Uno a Varios (1:*)** entre las dimensiones y la tabla de hechos.Se creó la tabla 'calendar' como tabla de fechas principal para permitir el análisis temporal.
2. **Medidas DAX Clave**
   Se crearon medidas explícitas para garantizar la presición de los cálculos y controla el contexto de filto:
     - **Precio, expensas y m² promedio **: Métricas bases para comparaciones justas entre barrios.
     - **Tendencia de Expensas/Precio**: Análisis de la evolución de ambos costos a lo largo del tiempo.
     - **Composición del departamento promedio**: Se utiliza la función *switch* para mostrar y filtar el promedio de las características en un solo gráfico.
3. **Visualización**
   El *dashboard* interactivo permite:
     - **Filtar**: Segmentar el mercado por **Tipo de Operaración** y **Barrio**.
     - **Ranking**: Identificar los barrios más caros y accesibles.
     - **Evolución**: Analizar la evolución de precios y expensas a través de los años.

---

## Contact:
- **Name:** Sebastián Esnaola
- **LinkedIn:** [www.linkedin.com/in/sebastian-esnaola]
- **Email:** isp2014asje@gmail.com


