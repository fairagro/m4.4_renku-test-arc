baseCommand: python
class: CommandLineTool
cwlVersion: v1.2
inputs:
- default:
    class: File
    location: calculation.py
  id: script
  inputBinding:
    position: 0
  type: File
- default:
    class: File
    location: ../../assays/population/dataset/population.csv
  id: population
  inputBinding:
    position: 1
    prefix: -p
  type: File
- default:
    class: File
    location: ../../assays/speakers/dataset/speakers_revised.csv
  id: speakers
  inputBinding:
    position: 2
    prefix: -s
  type: File
label: calculation
outputs:
- id: output
  outputBinding:
    glob: results.csv
  type: File
