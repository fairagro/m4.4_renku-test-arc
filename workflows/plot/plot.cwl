#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool
label: plot

inputs:
- id: script
  type: File
  default:
    class: File
    location: plot.py
  inputBinding:
    position: 0
- id: results
  type: File
  default:
    class: File
    location: ../../results.csv
  inputBinding:
    prefix: -r
    position: 1

outputs:
- id: output
  type: File
  outputBinding:
    glob: results.svg

baseCommand: python
