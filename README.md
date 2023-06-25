# Recomendador de películas con Spark
  
Este proyecto usa el algoritmo ALS (Alternating Least Squares) para aprender los factores latentes de los usuarios y las películas a partir de los datos de calificación o rating, que son el número de veces que un usuario ha visto una película. El proyecto hace lo siguiente:

- Carga los datos de calificación desde un archivo csv, que contiene el id del usuario, el id de la película y el número de veces que la ha visto.
- Divide los datos en conjuntos de entrenamiento y prueba, usando la ley de Pareto en proporción de 80/20.
- Construye y ajusta el modelo ALS en los datos de entrenamiento, usando una validación cruzada con 5 pliegues y una cuadrícula de parámetros para encontrar el mejor modelo.
- Evalúa el modelo en los datos de prueba, usando la métrica RMSE (Root Mean Squared Error).
- Muestra las recomendaciones para un usuario específico, y de acuerdo al número de recomendaciones que se desee.

Cabe resaltar que los pasos detallados, mejor documentados y comentados se lo puede revisar directamente desde Google colab: [Movie Recommendation](https://colab.research.google.com/drive/1rZeTbitXChyC4WGYxqjCVYKCvh6q_1bI)

## Desafíos

Algunos de los desafíos que se enfrentan al usar este enfoque son:

- El problema de la escalabilidad, que ocurre cuando hay muchos usuarios y películas y el modelo se vuelve muy grande y complejo. El código usa Spark para distribuir el cómputo y aprovechar los recursos del clúster, pero se podrían optimizar algunos parámetros como el número de iteraciones, el rango o la regularización.
- Los datos del entrenamiento se encuentran codificados, por lo que se tuvo que hacer un mapeo de acuerdo a los id's de las películas para encontrar sus respectivso nombres en el otro archivo csv.
- Ejecutar el programa sin errores algunos, y que las primeras veces daba errores de configuración del "driven", puesto que faltaba especificar en la crecion de la sesión de spark.

## Hallazgos

Algunos hallazgos o perspectivas interesantes que se pueden obtener al usar este enfoque son:

- El modelo ALS puede capturar las preferencias implícitas o explícitas de los usuarios y las películas, y generar recomendaciones personalizadas basadas en los factores latentes.
- El modelo ALS puede mejorar su rendimiento al usar una validación cruzada y una búsqueda de cuadrícula para encontrar los mejores parámetros, pero también hay que tener en cuenta el costo computacional y el riesgo de sobreajuste.
- El modelo ALS puede generar recomendaciones para todos los usuarios o para un solo usuario, lo que permite explorar las similitudes o diferencias entre los perfiles de los usuarios y las películas.

## Ejecución

Para ejecutar este proyecto, se necesita tener instalado Spark y Python en su máquina. También necesita descargar los archivos ratings.csv y movies.csv desde el repositorio: [ml-latest-small](https://github.com/rafaelgsantoss/ml-latest-small) o también desde los archivos de este repositorio. 
Luego puedes ejecutar el código con el siguiente comando:

```bash
./spark-submit --master spark://<ip nodo master>:7077 --deploy-mode client --py-files ratings.csv,movies.csv MovieRecommendation.py
```

La siguiente imágen pertenece a la ejecución del programa:

![image](https://github.com/BradlhyMachado/Recomendador-de-peliculas-con-spark/assets/89551198/ec7bb7eb-a520-4018-92c1-0f92a26419d4)
