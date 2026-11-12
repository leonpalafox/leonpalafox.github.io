---
title: "De listas estáticas a recomendaciones dinámicas: el nuevo recomendador de Fondos y SMAs en GBM"
description: "Cómo GBM pasó de carruseles estáticos a un recomendador colaborativo para Fondos y SMAs, y qué aprendió en el camino."
pubDate: 2026-04-13
lang: es
tags: ["ia", "financiero", "personalizacion"]
cover: de-listas-estaticas-a-recomendaciones-dinamicas-gbm
source: "https://medium.com/gbm-tech/de-listas-est%C3%A1ticas-a-recomendaciones-din%C3%A1micas-el-nuevo-recomendador-de-fondos-y-smas-en-gbm-284e2744a371"
sourceName: "GBM Tech"
---

En GBM, la personalización siempre ha sido un objetivo central. Sin embargo, hasta hace poco, los carruseles en la app eran *estáticos*, mostrando los mismos Productos Financieros en la sección de **Oportunidades de Inversión** para todos los clientes, sin importar sus perfiles, comportamientos o necesidades. Esto generaba una experiencia limitada, poco adaptada a la diversidad de inversionistas que tenemos.

Conscientes de esta limitación, decidimos dar un primer paso hacia un sistema más inteligente. El resultado fue la implementación de un *recomendador colaborativo*, que representa un cambio importante en nuestra manera de acercar productos a los clientes. En su estado actual, este recomendador no utiliza aún información de mercado ni señales externas; es únicamente un *filtro basado en colaboración*, que aprende de las interacciones de los usuarios y busca patrones en el comportamiento colectivo para ofrecer sugerencias más relevantes.

Este enfoque, aunque sencillo, nos permitió avanzar rápido y validar el concepto. Lo más destacable es que, gracias a nuestra infraestructura de despliegue, logramos pasar de la idea a un experimento funcional en menos de *tres semanas*. Este ritmo acelerado es reflejo de una plataforma tecnológica madura que nos permite iterar con velocidad, mantener estándares de calidad y probar hipótesis en un entorno real sin fricciones innecesarias.

## De lo estático a lo dinámico

- *Antes*: una lista fija de productos que no se adaptaba ni aprendía.

- *Hoy*: un sistema colaborativo que recomienda productos en función de lo que clientes con perfiles e intereses similares han explorado o contratado. Aunque no incorpora aún información del mercado ni variables externas, este simple ajuste representa una mejora significativa respecto a la experiencia anterior, abriendo la puerta a una interacción más personalizada y viva.

## Lo que viene

Este experimento con filtrado colaborativo es solo el inicio. El aprendizaje obtenido y la velocidad de despliegue alcanzada nos permiten pensar en los siguientes pasos con confianza. Nuestra hoja de ruta contempla evolucionar hacia modelos híbridos que combinen el filtrado colaborativo con más señales, como *información del portafolio*, *historial de interacción*, o *indicadores de riesgo*. También exploraremos cómo integrar nuevos enfoques, como técnicas de *machine learning supervisado* y eventualmente *refuerzo* para capturar mejor las dinámicas cambiantes de los inversionistas.

## *En conclusión…*

Gracias a una infraestructura de despliegue ágil y al poder del filtrado colaborativo, hemos demostrado que en GBM podemos transformar un concepto en una prueba real en cuestión de semanas. Este primer paso nos da la base para seguir iterando y construir un sistema de recomendación de Fondos y Cuentas Temáticas (SMAs) cada vez más sofisticado, flexible y cercano a las necesidades de cada cliente.

## *AVISO LEGAL*

El contenido de este blog tiene fines informativos y refleja únicamente la perspectiva del autor. No constituye asesoría profesional, financiera, legal ni de inversión. GBM no garantiza la exactitud, integridad ni actualidad de la información publicada. Cualquier mención a productos, servicios o tecnologías no implica recomendación por parte de GBM. El acceso y uso de este contenido es responsabilidad exclusiva del lector. Para información oficial, consulte los canales institucionales de GBM.
