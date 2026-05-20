---
title: "Machine Learning 2"
excerpt: "Universidad Panamericana — ensembles, dimensionality reduction & explainability for tabular/financial data."
header:
  overlay_color: "#000"
  overlay_filter: "0.5"
---

**Universidad Panamericana** · *Maestría en Ciencia de Datos* · ML2 2026
**Instructor:** Dr. León Palafox

## Course description

The second course in the machine learning track. The semester is organized around three blocks:

1. **Ensembles for tabular data** — bagging, boosting and stacking, building up from Random Forests through XGBoost and into stacked meta-learners. Closes with a serious treatment of hyperparameter tuning and the kind of cross-validation that doesn't lie when the data is a time series.
2. **Unsupervised structure & visualization** — PCA as the linear backbone, then t-SNE and UMAP for the cases where linear projections aren't enough. A decision framework for choosing among the three.
3. **Explainability (XAI) & capstone** — global and local explanations of complex tabular models, and a final project that ties the semester together.

Throughout, examples lean on financial use cases relevant to the Mexican context (credit scoring, yield-curve analysis, factor models).

## Course at a glance

| # | Sesión | Slides |
| -- | ------ | ------ |
| 1 | Bagging y Random Forests | *Próximamente* |
| 2 | De Gradiente Descendente a XGBoost | [PDF]({{ site.baseurl }}/assets/slides/ml2/class-02.pdf) |
| 3 | Stacking, Tuning y Validación Cruzada en Series de Tiempo | [PDF]({{ site.baseurl }}/assets/slides/ml2/class-03-stacking-tuning-cv.pdf) |
| 4 | Análisis de Componentes Principales (PCA) | [PPTX]({{ site.baseurl }}/assets/slides/ml2/class-04-pca.pptx) |
| 5 | Reducción No-Lineal — t-SNE y UMAP | [PPTX]({{ site.baseurl }}/assets/slides/ml2/class-05-tsne-umap.pptx) |
| 6 | XAI Global | *Próximamente* |
| 7 | XAI Local + Capstone | *Próximamente* |

---

## Detailed syllabus

### Clase 1 — Bagging y Random Forests

*Próximamente — slides not yet posted.*

Bias/variance review, bootstrap aggregating, out-of-bag error, feature subsampling, why Random Forest is the safe default on tabular data.

---

### Clase 2 — De Gradiente Descendente a XGBoost

*Boosting como descenso por gradiente en el espacio de funciones.*

**Plan de la sesión (~100 min)**

1. **Repaso de gradiente descendente (25 min)** — qué problema resuelve, regla de actualización, learning rate, convexidad vs no-convexidad. Puente conceptual: GD en parámetros vs GD en funciones.
2. **AdaBoost (20 min)** — la pregunta original de Kearns & Valiant (1988), el algoritmo de Freund & Schapire, decision stumps, reweighting, ensemble por voto ponderado.
3. **Gradient Boosting (40 min)** — la generalización de Friedman: cada árbol predice los residuales del anterior. Por qué se llama *gradient* boosting. Hiperparámetros que importan: `learning_rate`, `n_estimators`, `max_depth`, `subsample`, `colsample_bytree`. Cualquier pérdida diferenciable.
4. **XGBoost (15 min)** — aproximación de Taylor de segundo orden, regularización en el objetivo, sparsity-aware split finding, histogram-based splitting. Comparación con LightGBM y CatBoost.

**Hands-on:** Colab donde se implementa gradient boosting desde cero (~30 líneas) y se compara contra XGBoost en el dataset de crédito de la Clase 1.

**Referencias:**

- Kearns, M., & Valiant, L. (1988). *Learning Boolean formulae or finite automata is as hard as factoring.* — la pregunta original sobre weak learners.
- Schapire, R. E. (1990). *The strength of weak learnability.* Machine Learning.
- Freund, Y., & Schapire, R. E. (1996). *Experiments with a new boosting algorithm* — el algoritmo AdaBoost.
- Schapire, R. E., Freund, Y., Bartlett, P., & Lee, W. S. (1998). *Boosting the margin: A new explanation for the effectiveness of voting methods.* Annals of Statistics.
- Friedman, J. H. (1999). *Greedy function approximation: A gradient boosting machine.* Annals of Statistics.
- Chen, T., & Guestrin, C. (2016). [*XGBoost: A scalable tree boosting system.*](https://arxiv.org/abs/1603.02754) KDD '16.
- Ke, G., et al. (2017). *LightGBM: A highly efficient gradient boosting decision tree.* NeurIPS.
- Prokhorenkova, L., et al. (2018). *CatBoost: unbiased boosting with categorical features.* NeurIPS.

---

### Clase 3 — Stacking, Tuning y Validación Cruzada en Series de Tiempo

*Cerrando el bloque de ensembles antes de pivotear a métodos no supervisados.*

**Plan de la sesión (~85 min)**

1. **Stacking y blending (30 min)** — combinar modelos heterogéneos (RF + XGBoost + LogReg) con un meta-learner. La trampa: leakage cuando el meta-learner ve predicciones sobreajustadas. La solución: **out-of-fold (OOF) predictions** vía K-fold CV. Stacking vs blending. Cuándo NO usar stacking (modelos base muy correlacionados, dataset pequeño, requisitos de interpretabilidad).
2. **Hyperparameter tuning (30 min)** — el problema fundamental (5¹⁰ ≈ 9.7M combinaciones). Grid search, random search, **Bayesian optimization con Optuna** (TPE + median pruner). Errores comunes: tunear sobre el test set, no fijar la seed, ignorar la varianza del estimador.
3. **Validación cruzada en series de tiempo (25 min)** *— sección crítica para datos financieros.* Por qué K-fold estándar miente cuando hay estructura temporal. **Walk-forward validation** (expanding window y sliding window). **Purged K-fold con embargo** para targets con horizonte temporal. **Group K-fold** cuando hay múltiples observaciones por entidad.

**Hands-on:** Colab `03_stacking_cv.ipynb` — implementar stacking incorrecto y correcto, comparar K-fold estándar vs walk-forward sobre el dataset de crédito con índice temporal.

**Referencias:**

- Wolpert, D. H. (1992). *Stacked generalization.* Neural Networks. — formulación original.
- Bergstra, J., & Bengio, Y. (2012). [*Random search for hyper-parameter optimization.*](https://www.jmlr.org/papers/v13/bergstra12a.html) JMLR 13.
- Akiba, T., et al. (2019). *Optuna: A next-generation hyperparameter optimization framework.* KDD.
- **López de Prado, M. (2018).** *Advances in Financial Machine Learning*, Capítulo 7 — purged K-fold con embargo. **Lectura muy recomendada para todos los que trabajen con datos financieros.**

---

### Clase 4 — Análisis de Componentes Principales (PCA)

*Reducción de dimensión, intuición geométrica, y por qué los factores de la curva de tasas son level, slope y curvature.*

**Plan de la sesión (~80 min)**

1. **La maldición de la dimensionalidad (10 min)** — concentración geométrica en alta dimensión; por qué más features no siempre ayuda.
2. **Refresco de álgebra lineal (10 min)** — eigenvalores, eigenvectores, descomposición espectral, SVD como la implementación numéricamente estable.
3. **PCA: las dos derivaciones (40 min)** — como maximización de varianza y como minimización del error de reconstrucción (son el mismo problema). Conexión con eigendecomposición de la matriz de covarianza y con la SVD de la matriz de datos centrada.
4. **Interpretación y aplicación (20 min)** — scree plot, loadings, cuándo estandarizar, fallas típicas de PCA. **Caso de uso central:** la curva de tasas mexicanas — los primeros 3 componentes explican ~99% de la varianza y son interpretables como **nivel, pendiente y curvatura** (Litterman & Scheinkman, 1991). PCA en otros contextos: factores de equity (Fama–French rediscovered), preprocesamiento para clustering, detección de anomalías.

**Hands-on:** Colab `04_pca.ipynb` — PCA desde cero con NumPy (covarianza → eigendecomposition), verificación contra sklearn, scree plot, loadings, aplicación al dataset de tasas mexicanas 2010–2024.

**Referencias:**

- Pearson, K. (1901). *On lines and planes of closest fit to systems of points in space.* Philosophical Magazine. — la formulación original de PCA como minimización de reconstrucción.
- Hotelling, H. (1933). *Analysis of a complex of statistical variables into principal components.* Journal of Educational Psychology.
- **Litterman, R., & Scheinkman, J. (1991).** *Common factors affecting bond returns.* Journal of Fixed Income. — el paper que estableció level/slope/curvature como los tres factores de la curva de tasas.
- Fama, E., & French, K. (1993). *Common risk factors in the returns on stocks and bonds.* Journal of Financial Economics. — los factores que PCA redescubre automáticamente sobre retornos de acciones.
- Jolliffe, I. T. (2002). *Principal Component Analysis* (2nd ed.). Springer. — la referencia de libro.

---

### Clase 5 — Reducción No-Lineal: t-SNE y UMAP

*Cuando PCA no es suficiente: visualización de variedades complejas.*

**Plan de la sesión (~80 min)**

1. **La hipótesis de la variedad (10 min)** — los datos reales, aunque vivan en alta dimensión, suelen concentrarse sobre variedades de mucho menor dimensión. PCA captura esto cuando la variedad es lineal; t-SNE y UMAP la capturan cuando es curva.
2. **t-SNE (35 min)** — el método dominante 2008–2018. Similaridad en alta dimensión con Gaussianas, en baja dimensión con Student-t (resuelve el *crowding problem*). KL divergence como pérdida. **Perplexity** como el hiperparámetro que cambia todo: siempre ejecutar con varios valores (5, 30, 100) y mirar los tres. Cómo leer una visualización: distancias entre clústeres NO son interpretables; t-SNE es un microscopio, no un mapa.
3. **UMAP (20 min)** — el sucesor de t-SNE. Más rápido, mejor estructura global, fundamento teórico más sólido (aunque opaco — fuzzy simplicial sets, topología algebraica). Hiperparámetros: `n_neighbors`, `min_dist`. Diferencias operacionales con t-SNE (vecindades, distancias, distribución en baja dim, inicialización spectral).
4. **Marco de decisión PCA / t-SNE / UMAP (15 min)** — flowchart por objetivo (preprocesamiento vs EDA visual vs detección de anomalías) y por estructura de datos (lineal vs no-lineal, tamaño de n). Errores comunes en visualizaciones t-SNE/UMAP.

**Hands-on:** Colab — PCA vs t-SNE vs UMAP sobre el mismo dataset (Swiss roll, subset de MNIST, dataset de crédito). Sweep de `perplexity` y `n_neighbors`. Discusión sobre qué hacer con los resultados.

**Referencias:**

- **van der Maaten, L., & Hinton, G. (2008).** [*Visualizing data using t-SNE.*](https://www.jmlr.org/papers/v9/vandermaaten08a.html) JMLR — el paper original de t-SNE.
- **Wattenberg, M., Viégas, F., & Johnson, I. (2016).** [*How to Use t-SNE Effectively.*](https://distill.pub/2016/misread-tsne/) Distill. — **lectura obligatoria.** Interactivo, corto, y cambia cómo lees visualizaciones de t-SNE para siempre.
- **McInnes, L., Healy, J., & Melville, J. (2018).** [*UMAP: Uniform manifold approximation and projection for dimension reduction.*](https://arxiv.org/abs/1802.03426) arXiv:1802.03426.
- McInnes, L. — [*Understanding UMAP*](https://pair-code.github.io/understanding-umap/) (pair-code) y la documentación de [`umap-learn`](https://umap-learn.readthedocs.io/). Más accesible que el paper original.
- Fefferman, C., Mitter, S., & Narayanan, H. (2016). *Testing the manifold hypothesis.* Journal of the AMS. — condiciones formales bajo las cuales la manifold hypothesis es testeable.

---

### Clase 6 — XAI Global

*Próximamente.* Permutation importance, feature importance de ensembles, partial dependence plots (PDP), ICE plots, SHAP global summaries.

### Clase 7 — XAI Local + Capstone

*Próximamente.* SHAP values, LIME, counterfactual explanations. Discusión del capstone y rúbrica.

---

## Reading list (consolidated)

**Libros**

- Hastie, T., Tibshirani, R., & Friedman, J. *The Elements of Statistical Learning* (2nd ed.). Capítulos 9–10, 14–15. [Free PDF](https://hastie.su.domains/ElemStatLearn/).
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction* (2022). MIT Press.
- López de Prado, M. *Advances in Financial Machine Learning* (2018). Wiley. — **lectura recomendada para datos financieros**, en particular el Capítulo 7.
- Molnar, C. [*Interpretable Machine Learning*](https://christophm.github.io/interpretable-ml-book/). Texto abierto, referencia para el bloque de XAI.

**Papers fundacionales (en orden temático)**

- Schapire (1990); Freund & Schapire (1996) — AdaBoost.
- Friedman (1999) — Gradient Boosting Machines.
- Chen & Guestrin (2016) — XGBoost.
- Wolpert (1992) — Stacked Generalization.
- Bergstra & Bengio (2012) — Random Search.
- Pearson (1901); Hotelling (1933) — PCA.
- Litterman & Scheinkman (1991) — PCA sobre la curva de tasas.
- van der Maaten & Hinton (2008) — t-SNE.
- McInnes, Healy & Melville (2018) — UMAP.
- Wattenberg, Viégas & Johnson (2016) — *How to Use t-SNE Effectively*.

## Tools

- Python 3.10+, `numpy`, `pandas`, `scikit-learn`
- `xgboost`, `lightgbm`, `catboost`
- `optuna` para hyperparameter tuning
- `umap-learn`, `openTSNE` para reducción no-lineal
- `shap`, `lime` para el bloque de XAI

## Assessment

- Homework:
- Project:
- Final exam:

## Schedule & Office Hours

- **Lectures:**
- **Office hours:**
- **Contact:**
