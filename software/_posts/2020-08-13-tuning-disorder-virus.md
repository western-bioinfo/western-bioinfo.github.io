---
layout: software
title: tuning-disorder-virus
year: 2020
authors: ArtPoon, galmog, Abayomi-Olabode
github: https://github.com/PoonLab/tuning-disorder-virus
license: License(name="MIT License")
description: "Ensemble classifier of intrinsic protein disorder for viruses"
forks: 0
stars: 0
image: https://www.ncbi.nlm.nih.gov/pmc/articles/instance/7882063/bin/veaa106f4.jpg
---

This is a repository for sharing Python scripts and data associated with our manuscript "Tuning Intrinsic Disorder Predictors for Virus Proteins".

## Prerequisites
* [pandas](https://pandas.pydata.org/)
* [BioPython](https://biopython.org/)
* [joblib](https://joblib.readthedocs.io/en/latest/)
* [selenium](https://pypi.org/project/selenium/)

## Disclaimer
We wrote most of these scripts to automate the form submission process for analyzing virus and non-virus protein sequences using intrinsic protein disorder predictors that can only be accessed online (through third-party web servers).
Although we had considered releasing these scripts as a properly packaged Python module, we determined that access to the third-party servers hosting various intrinsic disorder prediction algorithms was too irregular.
Hence, we cannot guarantee that every one of these servers will be online.
