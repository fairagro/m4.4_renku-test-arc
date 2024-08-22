import os
from typing import Union
import cwl_utils.parser.cwl_v1_2 as cwl
import yaml

wf_folder_absolute = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(wf_folder_absolute, ".."))

def extract_parameter(param_raw, output=False, index = 0, toolname = "") -> Union[cwl.CommandInputParameter, cwl.CommandOutputParameter]:
    name = next(iter(param_raw))
    path:str = param_raw[name]['path']
    if not output:
        path = os.path.relpath(path, wf_folder_absolute + "/" + toolname + "/")
        path = path.replace("workflows/" + toolname + "/", "")
    prefix = param_raw[name].get('prefix', None)

    if output:
        return cwl.CommandOutputParameter(
            type_='File',
            id=name,
            outputBinding=cwl.CommandOutputBinding(
                glob=path
            )
        )
    else:
        return cwl.CommandInputParameter(
            type_='File',
            id=name,
            inputBinding=cwl.CommandLineBinding(
                prefix=prefix,
                position=index
            ),
            default=cwl.File(
                location=path
            )
        )


def extract_step(step_raw) -> cwl.CommandLineTool:
    name = next(iter(step_raw))
    description = step_raw[name].get('description', '')
    command = step_raw[name]['command']
    inputs = step_raw[name].get('inputs', {})
    outputs = step_raw[name].get('outputs', {})

    cwl_inputs = [extract_parameter(input_raw, index = i, toolname=name) for i, input_raw in enumerate(inputs)]
    cwl_outputs = [extract_parameter(output_raw, output=True)
                   for output_raw in outputs]

    command = command.split(" ")[0]
    
    return cwl.CommandLineTool(
        cwlVersion='v1.2',
        label=name,
        doc=description,
        baseCommand=command,
        inputs=cwl_inputs,
        outputs=cwl_outputs
    )


with open(wf_folder_absolute + '/main.yml', 'r') as f:
    raw = yaml.safe_load(f)
for step in raw['steps']:
    tool = extract_step(step)
    with open("workflows/" + tool.label + "/" + tool.label + ".cwl", "w") as f:
        f.write(yaml.dump(tool.save()))
