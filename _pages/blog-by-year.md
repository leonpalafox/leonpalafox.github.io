---
layout: archive
title: "Blog"
permalink: blog-by-year
excerpt: "Year-by-year archive of Leon Palafox's articles on AI, data strategy, and innovation."
lang: en
image: "/assets/images/header.jpg"
classes: wide
author_profile: true
---

Browse every article by publication year, or jump to topic hubs:
[Categories](/categories/) · [Tags](/tags/)

{% assign postsByYear = site.posts | group_by_exp:"post", "post.date | date: '%Y'"  %}
{% for year in postsByYear %}
  <h2 id="{{ year.name | slugify }}" class="archive__subtitle">{{ year.name }}</h2>
  {% for post in year.items %}
    {% include archive-single.html %}
  {% endfor %}
{% endfor %}
