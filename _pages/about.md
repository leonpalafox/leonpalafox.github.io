---
layout: single
title: "About"
permalink: about
excerpt: "Professional bio, research background, and career timeline of Leon Palafox."
lang: en
image: "/assets/images/header.jpg"
toc: true
author_profile: true
---

I’m the **Director of the AI Innovation Lab at [GBM](https://www.gbm.com/)**, where I lead large-scale **personalization, recommender systems, embeddings, and experimentation platforms** for retail investing.  
I’m also a **Lecturer at [Universidad Panamericana](https://www.up.edu.mx/en/mexico){:target='_blank'}** and a regular **columnist at *El Financiero*** on AI, data strategy, and innovation.

---

## 🧠 Research

My research interests lie in **applied Machine Learning**, especially in domains where data meets complex systems.  
I’ve worked on projects across:

- Neuroscience  
- Astrophysics  
- Planetary Sciences  
- Financial Sciences  

I’m currently exploring how **Machine Learning can support decision-making in social and financial systems**, from investment analytics to recommender systems for retail platforms.

---

## 🎓 Academia

I earned my **Bachelor’s Degree in Engineering from the _National Autonomous University of Mexico (UNAM)_**, graduating *Magna Cum Laude* and receiving the **Medalla Gabino Barreda** as the top student in my class.  
I was a Research Intern at the _Institute of Applied Mathematics (Mexico)_, and earned both my **Master’s and PhD in Machine Learning and AI applied to Bioinformatics from the _University of Tokyo_ (Japan)**, funded by the prestigious **Monbukagakusho (MEXT) Scholarship** from the Japanese Ministry of Education.

I later worked as a **postdoctoral researcher at the _University of California, Los Angeles (UCLA) School of Medicine_**, applying ML to neuroscience, and at the **_University of Arizona_**, where I applied ML to planetary sciences.  
Afterward, I became a **Staff Scientist at the University of Arizona**.

---

## 💼 Industry

I’ve worked at the intersection of AI, data strategy, and business for over a decade.  
Currently I’m **Director of the AI Innovation Lab at GBM**, building internal AI capabilities and launching large-scale recommender systems and personalization engines.

Previously, I served as:

- **AI Innovation Lab Director at Novartis**
- **AI Head at Algorithia (Grupo Salinas)**
- **Director of Machine Learning at Banorte Financial Group**
- **Machine Learning and Data Science Professor at Universidad Panamericana**
- **Senior Data Science Consultant at Rich IT**
- Data and Business Analyst at **San Luis Rassini**

---

## 📅 Timeline

<style type="text/css">
  .timeline-logo { float:left; vertical-align: middle; margin-right: 10px; }
  .timeline-text { vertical-align: middle; display: table-cell; }
</style>

<div>
    {% assign events = site.events | sort: 'date' | reverse %}
    {% for event in events %}
    <big>{{ event.date | date: '%Y/%m' }}
    {% if event.enddate != blank %}
         - {{ event.enddate | date: '%Y/%m' }}
    {% else %} - Present
    {% endif %}
    </big>
    <div>
        <img class="timeline-logo" src="{{site.baseurl}}{{ event.image }}" width="80" height="80" alt="{{ event.content | strip_html | strip_newlines | normalize_whitespace }}">
        <span class="timeline-text"><small>{{ event.content }}</small></span>
    </div>
    <br><br>
    {% endfor %}
</div>
