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
-h, --help | Show the help message and exit
-n NAME, --name NAME | Name of the main component (default:hydrated-cluster)
-k FILE, --kubeconfig FILE | Kubeconfig file for the cluster (default:kubeconfig)
-o PATH, --output PATH | Output path for the generated component.yaml.
-v, --verbose | Verbose output logs.
-d, --dry-run | Print component.yaml to the terminal.