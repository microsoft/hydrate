# Hydrate
Hydrate crawls a kubernetes cluster and generates a high level description of your deployments.

## Setup
Include a "kubeconfig" file for your cluster in the same directory as hydrate.py

## Basic Usage
```bash
python hydrate.py [-h] [-n NAME] [-o path] [-v] [-d] run
```

### Positional arguments:

Arg | Usage
--- | ---
run | Generate component.yaml for current configuration

### Optional arguments:

Arg | Usage
--- | ---
-h, --help | show this help message and exit
-n NAME, --name NAME | Specify the name of the main component.
-o path, --output path | Specify path of the generated component.yaml.
-v, --verbose | Print more output.
-d, --dry-run | Print component.yaml to the terminal.