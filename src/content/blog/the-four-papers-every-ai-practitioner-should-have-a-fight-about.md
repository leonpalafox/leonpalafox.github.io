---
title: "The Four Papers Every AI Practitioner Should Have a Fight About"
description: "Four papers that explain why scaling keeps beating cleverness, and why every AI practitioner should argue about them."
pubDate: 2026-03-18
lang: en
tags: ["ia", "tecnologia", "investigacion"]
cover: the-four-papers-every-ai-practitioner-should-have-a-fight-about
source: "https://medium.com/@leonpalafox/the-four-papers-every-ai-practitioner-should-have-a-fight-about-5f21a491ed93"
sourceName: "Medium"
---

Most people follow AI through product launches and benchmark announcements. That works if you want to know what shipped. It won’t tell you why the field moves the way it does.

In my seminar at Universidad Panamericana, I give students four papers. Not a survey. An argument. And every semester, the argument gets ugly in exactly the right way.

### Paper 1: The Bitter Lesson, Richard Sutton (2019)

Sutton’s essay is two pages and has embarrassed a lot of smart people.

The claim: every time researchers encoded human knowledge into AI — chess heuristics, grammar rules, vision priors — they eventually lost to systems that just scaled compute. Search and learning, scaled up, beat cleverness. Every time, across sixty years.

I open here because this sets the prior you need before anything else makes sense. If you believe domain expertise is the lasting competitive advantage in AI, Sutton is the first paper that will make you uncomfortable.

He’s not saying human knowledge is worthless. He’s saying encoding it into the architecture is the mistake. That distinction matters more as the papers go on.

### Paper 2: Training Compute-Optimal Large Language Models, Hoffmann et al., DeepMind (2022)

The Chinchilla paper. Scale wins, but the field had been scaling wrong.

For a given compute budget, you get better results training a smaller model on more tokens than a larger model on fewer. DeepMind trained Chinchilla on roughly four times more data than Gopher at the same cost. It outperformed Gopher on almost every benchmark. The industry had been leaving performance on the table.

This constrains Sutton’s prior in ways that actually matter for practice. Scale isn’t a blank check. There’s an optimal point, it’s further toward data than most labs were going, and once you know that, the interesting questions shift: what happens to the ratio as you push into training regimes nobody has explored? How much data does the internet actually have? For anyone building AI outside the handful of labs with unlimited budgets, this is where scaling laws become engineering decisions.

### Paper 3: DeepSeek-R1, DeepSeek AI (2025)

This is where class gets loud.

DeepSeek-R1 matched OpenAI’s o1 on reasoning benchmarks at a fraction of the reported training cost. Not a bigger model. Reinforcement learning on chain-of-thought reasoning, applied to an architecture that wasn’t dramatically larger than what already existed.

The paper hit hard because it challenged something the field had quietly started assuming: that frontier performance is downstream of capital. Know the scaling recipe, fund the run, win. DeepSeek-R1 showed algorithmic efficiency can move faster than spending, which changes the picture considerably for anyone not named Google or Microsoft.

For Mexico, this matters in ways that haven’t been fully worked out. The story where AI is an infrastructure race — you either have the data centers or you’re an observer — may be less settled than it looked a year ago.

### Paper 4: The Platonic Representation Hypothesis, Huh et al., MIT (2024)

This one took me a week to sit with.

The hypothesis: as models scale across modalities (vision, language, code, audio), they appear to converge toward the same underlying representations of reality. Different architectures, different training pipelines, different labs. Same structure emerging at the bottom.

If that holds, models aren’t just compressing statistical patterns. They’re converging on something like a shared model of how the world actually works, and the representations reflect structure that’s really there.

I put this last because it refuses to close. The Bitter Lesson says compute wins. Chinchilla says compute has shape. DeepSeek says the shape can be gamed. The Platonic Representation Hypothesis says underneath all of it there may be a floor, a structure every sufficiently capable system will eventually find regardless of how it was built. We don’t know if that’s true. That’s why it ends the list.

### The fight the list is designed to start

Sutton is almost aggressively anti-knowledge-engineering. The Platonic Representation Hypothesis suggests models are converging on something deeply structured — which sounds a lot like what Sutton warned against encoding by hand, except nobody planned it.

DeepSeek undercuts the capital narrative that Chinchilla quietly enabled. If you know the optimal scaling recipe, the only variable left is budget. DeepSeek-R1 broke that logic, at least partially, and the “at least partially” is where most of the arguing happens.

My students go at this for two hours every semester. So far, nobody has won.
