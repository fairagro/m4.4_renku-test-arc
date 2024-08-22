#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool
label: plot

requirements:
- class: InitialWorkDirRequirement
  listing:
  - entryname: plot.py
    entry:
      $include: plot.py

inputs:
- id: results
  type: File
  default:
    class: File
    location: ../../results.csv
  inputBinding:
    prefix: -r

outputs:
- id: output
  type: File
  outputBinding:
    glob: results.svg

baseCommand:
- python
- plot.py
