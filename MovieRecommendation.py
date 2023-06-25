from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.sql.functions import col

try:
    # Crear una sesión Spark
    spark = SparkSession.builder.appName("Movie Recommendation").config("spark.driver.bindAddress", "127.0.0.1").getOrCreate()

    # Cargar el conjunto de datos MovieLens
    data = spark.read.csv("ratings.csv", header=True, inferSchema=True)

    data = data.select("userId", "movieId", "rating")

    train, test = data.randomSplit([0.8, 0.2], seed=42)

    # Crear un modelo ALS
    als = ALS(userCol="userId", itemCol="movieId", ratingCol="rating", coldStartStrategy="drop")

    # Definir un evaluador RMSE
    evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")

    # Construir una cuadrícula de parámetros
    param_grid = ParamGridBuilder().addGrid(als.rank, [10, 15, 20]).addGrid(als.regParam, [0.01, 0.05, 0.1]).build()

    # Crear un validador cruzado con 5 pliegues
    cv = CrossValidator(estimator=als, estimatorParamMaps=param_grid, evaluator=evaluator, numFolds=5)

    # Ajustar el modelo en los datos de entrenamiento
    model = cv.fit(train)

    # Obtener el mejor modelo
    best_model = model.bestModel

    # Evaluar el modelo en los datos de prueba
    predictions = best_model.transform(test)
    rmse = evaluator.evaluate(predictions)

    # Imprimir las métricas
    print("RMSE: ", rmse)

    # Cargar el archivo movies.csv, que contiene información de las películas
    movies = spark.read.csv("movies.csv", header=True, inferSchema=True)

    # Generar una función para dar las películas recomendadas para el usuario
    def recommend_movie(user_id, num_rec):
        print("The", num_rec, "movies recommended for the user", user_id, "are:")

        # Generar número de recomendaciones de películas para cada usuario
        user_recs = best_model.recommendForAllUsers(num_rec)

        rec = user_recs.filter(user_recs.userId == user_id).select("recommendations").collect()[0][0]
        for row in rec:
            # Mostrar las recomendaciones para el usuario
            filtered_data = movies.filter(col("movieId") == row.movieId)
            movie_title = filtered_data.select("title").collect()[0][0]
            print("- ", movie_title)

    # Invocar a la función para generar la recomendación (usuario, num_recomendaciones)
    recommend_movie(3, 5)

except Exception as e:
    print("An error occurred:", str(e))

finally:
    if 'spark' in locals():
        # Detener la sesión Spark
        spark.stop()