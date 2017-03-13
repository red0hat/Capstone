Category Prediction Table: without lemmatization, ~4000 documents

|model|train|test|out of sample|params|Time to build model|Time to predict one page|
|:-----:|-----|----|:-------------:|-------|--- |---|
|Cosine Similarity| 94.5%|91.7%| 72.3% |	  | 18.0 sec| 4.1 ms|
|K Nearest Neighbors| 90.2%| 89.3% | 64.0% ||79 ms  | 1.45 ms	  |
|Multi Layer Perceptron| 97.7% | 94.8%| 70.8%  |activation= logistic, solver = 'adm', hidden\_layer\_size = (100,)| 26.3 sec|3.7 ms|
|Random Forest Classifier| 99.7% | 91.5%| 67.3%| estimators = 30|1.6 sec|120 μs|
|xgBoost | 99.7%| 92.7% | 66.8% | n\_estimators = 1000, max_depth = 5| 39 min | 6.6 ms|



For KNN, the recommended settings from a grid search did not improve perfomance over default settings.

