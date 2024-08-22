# Experiment: Creating an ARC using renku and ARCitect
This repository contains a proof-of-concept ARC which was created using [`renku`](https://renkulab.io/) in combination with a [custom template](https://github.com/JensKrumsieck/renku-arc-template).

For the metadata annotation of the xlsx files the [ARCitect](https://github.com/nfdi4plants/ARCitect) was used. The detailed progress is documented in our [concept repo](https://github.com/fairagro/m4.4_concept/blob/main/test_existing_tools/renku_as_arc.md). The data and scripts are from our [Hello World Use Case](https://github.com/fairagro/m4.4_hello_world).

The workflow was recorded using `renku`s command, exported to its own [workflow format](https://github.com/fairagro/m4.4_renku-test-arc/blob/master/workflows/main.yml) which was then converted to CWL files by a [simple quick-and-dirty script](https://github.com/fairagro/m4.4_renku-test-arc/blob/master/workflows/convert.py).

## Usage
As this does not come with a Workflow using containers, yet, you need to install the python requirements.
```bash
pip install -r requirements.txt
```

To use the CWL Workflow, create a new run and execute `cwltool` from the `run`s folder. As the inputs have default values there is no need to specify inputs.

```bash
cd runs
mkdir my_run_folder
cd my_run_folder
cwltool ../../workflows/main.cwl
```

## Validation
The ARC validation pipeline by DataPLANT was used to [validate the ARC structure](https://github.com/fairagro/m4.4_renku-test-arc/actions/workflows/arc-validation.yml). Artifacts are built and attached to the pipeline's runs respectively.