#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool
label: calculation

inputs:
- id: script
  type: File
  default:
    class: File
    location: calculation.py
  inputBinding:
    position: 0
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

baseCommand: python
