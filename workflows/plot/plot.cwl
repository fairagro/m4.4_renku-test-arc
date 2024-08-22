baseCommand: python
class: CommandLineTool
cwlVersion: v1.2
inputs:
- default:
    class: File
    location: plot.py
  id: script
  inputBinding:
    position: 0
  type: File
- default:
    class: File
    location: ../../results.csv
  id: results
  inputBinding:
    position: 1
    prefix: -r
  type: File
label: plot
outputs:
- id: output
  outputBinding:
    glob: results.svg
  type: File
