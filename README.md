# Hydrate
[![Build Status](https://dev.azure.com/epicstuff/hydrate/_apis/build/status/microsoft.hydrate?branchName=master)](https://dev.azure.com/epicstuff/hydrate/_build/latest?definitionId=98&branchName=master)

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

## Running in Docker
### Step 1. Build The Image
Run the following command from the Hydrate project directory.
```bash
docker build --tag=[image-name] .
```
### Step 2. Run The Image
```bash
docker run [image-name] [args]
```

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.