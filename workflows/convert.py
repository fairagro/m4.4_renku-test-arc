import os
from typing import Union
import cwl_utils.parser.cwl_v1_2 as cwl
from cwlformat.formatter import cwl_format
import yaml

arc_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
arc_folders = {
    "workflows": os.path.join(arc_root, "workflows"),
    "assays": os.path.join(arc_root, "assays"),
    "studies": os.path.join(arc_root, "studies"),
    "runs": os.path.join(arc_root, "runs"),
}

def is_in(path: str, foldername: str) -> bool:
    return not os.path.relpath(path, arc_folders[foldername]).startswith("..")

def locate_file(path: str) -> Union[str, None]:
    for folder in arc_folders.values():
        if os.path.exists(os.path.join(folder, path)):
            return os.path.join(folder, path)
    return None

def get_name(obj: object) -> str:
    return list(obj.keys())[0]

def get_tool(renku_step: str) -> cwl.CommandLineTool:
    label = get_name(renku_step)
    doc = renku_step[label].get('description', '')
    baseCommand = renku_step[label]['command'].split(" ")[0]
    requirements = []
    inputs = []
    outputs = []
    for input in renku_step[label].get('inputs', {}):
        id = get_name(input)
        if is_in(input[id]['path'], "workflows"):
            base_name =  os.path.basename(input[id]['path'])
            requirements.append(cwl.InitialWorkDirRequirement(listing=[{"entryname": base_name, "entry": {"$include": base_name}}]))
            baseCommand += " " + base_name
        else: 
            inputs.append(cwl.CommandInputParameter(
                type_='File',
                id=id,
                inputBinding=cwl.CommandLineBinding(
                    prefix=input[id].get('prefix', None)
                ),
                default=cwl.File(
                    location=os.path.relpath(input[id]['path'], os.path.join(arc_folders["workflows"], label))
                )
            ))
    for output in renku_step[label].get('outputs', {}):
        id = get_name(output)
        outputs.append(cwl.CommandOutputParameter(
            type_='File',
            id=id,
            outputBinding=cwl.CommandOutputBinding(
                glob=output[id]['path']
            )
        ))
        
            
    return cwl.CommandLineTool(
        cwlVersion='v1.2',
        label=label,
        doc=doc,
        baseCommand=baseCommand.split(" "),
        inputs=inputs,
        outputs=outputs,
        requirements=requirements
    )
with open(locate_file("main.yml"), 'r') as f:
    raw = yaml.safe_load(f)
tools = [get_tool(step) for step in raw['steps']]

for tool in tools:
    with open("workflows/" + tool.label + "/" + tool.label + ".cwl", "w") as f:
        f.write(cwl_format(yaml.dump(tool.save())))

inputFiles = []
outputFiles = {}
steps =[]
for tool in tools:
    step_inputs= {}
    for input in tool.inputs:
        if os.path.basename(input.default.location) not in outputFiles.values():
            defaultFile = input.default
            defaultFile.location = defaultFile.location[3:]
            inputFiles.append(cwl.WorkflowInputParameter(id=input.id, type_="File", default=defaultFile))
            step_inputs[input.id] = input.id
        else:
            for key, output in outputFiles.items():
                if os.path.basename(input.default.location) == output:
                    step_inputs[input.id] = key
                    break
    steps.append(cwl.WorkflowStep(id=tool.label, run=tool.label + "/" + tool.label + ".cwl", in_ = step_inputs, out=[cwl.WorkflowStepOutput(id=output.id) for output in tool.outputs]))
    for output in tool.outputs:
        outputFiles[tool.label + "/" + output.id] = output.outputBinding.glob

label = raw["name"]        
doc = raw["description"]
outputs = []
for key in outputFiles.keys():
    outputs.append(cwl.WorkflowOutputParameter(id=key.replace("/", "_"), type_="File", outputSource=key))
workflow = cwl.Workflow(cwlVersion='v1.2', label=label, doc=doc, steps=steps, inputs=inputFiles, outputs=outputs)
with open("workflows/"+label+".cwl", "w") as f:
    f.write(cwl_format(yaml.dump(workflow.save()))
)
# not beautiful but it works