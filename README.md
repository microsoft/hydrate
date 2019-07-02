# Hydrate
Hydrate crawls a kubernetes cluster and generates a high level description of your deployments.

## Setup
Ensure you are using Python 3.6 or a newer version.
Include a "kubeconfig" file for your cluster in the same directory as hydrate.py,
or specify one with the -k argument.
Finally, install the dependencies.
```bash
pip install -r requirements.txt
```

## Basic Usage
```bash
python -m hydrate [-h] [-n NAME] [-k FILE] [-o PATH] [-v] [-d] run
```
The component.yaml file that is created is based on the specification detailed in the [Fabrikate](https://github.com/Microsoft/fabrikate "Fabrikate") repo.

[Fabrikate Component Definition](https://github.com/microsoft/fabrikate/blob/master/docs/component.md "Component Definition")

[Fabrikate Config Definition](https://github.com/microsoft/fabrikate/blob/master/docs/config.md "Config Definition")



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