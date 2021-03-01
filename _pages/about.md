---
layout: single
title: "About"
permalink: about
excerpt: "Bio."
toc: True
author_profile: True
---

I'm Machine Learning Director at Banorte Financial Group, leading all the initiatives that use AI at the core of the business. I'm a Lecturer at [Universidad Panamericana](http://www.up.edu.mx/en/mexico){:target='_blank'}.
## Research
My research interests are in the field of applied Machine Learning, some of my projects have involved :
- Neuroscience
- Astrophysics
- Planetary Sciences
- Financial Sciences

I'm currently interested in the applications of Machine Learning toward social groups and financial applications.

## Academia

I got my Bachelor's Degree from _Mexico's National Autonomous University_ (Mexico). I was a Research Intern at the _Institue of Applied Mathematics_ (Mexico). I obtained my Master’s Degree in Information Technologies from the _University of Tokyo_ (Japan), as fellow of the _Monbukagakusho Scholarship_ (Embassy Recommendation) from the Japanese Ministry of Education, Culture, Sports, Science and Technology. And my Phd from the same institution. I was a postdoctoral fellow at _The University of California, Los Angeles_ (USA) and at _The University of Arizona_. Then I was a Staff Scientist also at _The University of Arizona_

## Industry
 I'm currently head of Machine Learning at Banorte FInancial Group. I worked at _San Luis Rassini_ as a data analys and strategy analyst. I also worked in _Rich IT_ as a Data Science Senior Consultant.

## Timeline

<style type="text/css">
  .timeline-logo   { float:left;
             vertical-align: middle;
             margin-right: 10px; }

  .timeline-text { vertical-align: middle;
            display: table-cell; }
</style>

<div>
    {% assign events = site.events | sort: 'date' %}
    {% for event in site.events reversed %}
    {% assign date = event.date | date: '%Y/%m' %}
    {% assign enddate = event.enddate | date: '%Y/%m' %}
    <big>{{ event.date | date: '%Y/%m' }}
    {% if event.enddate != blank %}
        {% if date < enddate %} - {{ event.enddate | date: '%Y/%m' }}
        {% endif %}
    {% else %} - 
    {% endif %}
    </big>
    <div>
        <img class="timeline-logo" src="{{site.baseurl}}{{ event.image }}" width="80" height="80">
        <span class="timleline-text"><small>{{ event.content }}</small></span>
    </div>
    <br><br>
    {% endfor %}
</div>