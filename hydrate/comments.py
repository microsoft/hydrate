"""Home of component.yaml comment constants."""


TOP_LEVEL_COMMENT = '''Automatically generated using hydrate.
Repository link: https://github.com/microsoft/hydrate
Fabrikate Docs: https://github.com/Microsoft/fabrikate
For private repositories, check the following:
Authentication: https://github.com/microsoft/fabrikate/blob/master/docs/auth.md
For more information on how components are structured, check the following:
Component Model: https://github.com/microsoft/fabrikate/blob/master/docs/component.md'''


FULL_MATCH_COMMENT = '''Full Match Components'''


PARTIAL_MATCH_COMMENT = '''Partial Match Components'''


NO_MATCH_COMMENT = '''No Match Deployments
In order to use these deployments with Fabrikate, follow the steps below.
1. Populate the source (git repository link)
2. Add a path field (path within the git repository) ex: "path: stable/"
3. Specify helm for applications generated using a Helm chart ex: "type: helm"
Otherwise, comment them out to prevent errors with Fabrikate generation.'''
