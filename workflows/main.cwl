#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow
label: main

inputs:
- id: population
  type: File
  default:
    class: File
    location: ../assays/population/dataset/population.csv
- id: speakers
  type: File
  default:
    class: File
    location: ../assays/speakers/dataset/speakers_revised.csv

outputs:
- id: calculation_output
  type: File
  outputSource: calculation/output
- id: plot_output
  type: File
  outputSource: plot/output

steps:
- id: calculation
  in:
    population: population
    speakers: speakers
  run: calculation/calculation.cwl
  out:
  - id: output
- id: plot
  in:
    results: calculation/output
  run: plot/plot.cwl
  out:
  - id: output
