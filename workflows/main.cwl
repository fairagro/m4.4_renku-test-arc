#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow
label: main

inputs:
- id: population
  type: File
  default:
    class: File
    location: ../../assays/population/dataset/population.csv
  inputBinding:
    prefix: -p
    position: 1
- id: speakers
  type: File
  default:
    class: File
    location: ../../assays/speakers/dataset/speakers_revised.csv
  inputBinding:
    prefix: -s
    position: 2

outputs:
- id: output
  type: File
  outputBinding:
    glob: results.csv
- id: output
  type: File
  outputBinding:
    glob: results.svg

steps: []
