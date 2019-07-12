"""Use to construct the High-Level Deployment."""
from sys import stdout
import os.path
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml import YAML
yaml = YAML()

from .cluster import Cluster
from .component import TopComponent
from .component import CommentedComponent
from .scrape import Scraper
from .match import Matcher

MAPPING = 2
SEQUENCE = 4
OFFSET = 2
verbose_print = None

class HLD_Generator():
    '''Creates HLD from Cluster and Fabrikate Components.'''

    def __init__(self, args):
        '''Construct HLD_Generator Object'''
        self.top_component = TopComponent(name=args.name)
        self.cluster = Cluster(args.kubeconfig)
        self.dry_run = args.dry_run
        self.output = args.output

        self.matcher = None

        # Define verbose_print as print if -v, o.w. do nothing
        global verbose_print
        verbose_print = print if args.verbose else lambda *a, **k: None
        verbose_print("Printing verbosely...")

    def generate(self):
        '''Generate the component.yaml.
        '''
        # Step 1a. Get cluster components
        cluster_components = self._get_cluster_components()
        # Step 1b. Get repo components, instantiate matcher
        repo_components = self._get_component_definitions()
        self.matcher = Matcher(repo_components)
        # Step 2. Find the matches between the cluster and repo
        match_categories = self._get_matches(cluster_components)
        # Step 3. Generate the HLD
        self._generate_HLD(match_categories)

    def _get_cluster_components(self):
        '''Get objects living on the cluster.'''
        print("Connecting to cluster...")
        self.cluster.connect_to_cluster()
        print("Connected!")
        print("Collecting information from the cluster...")
        return self.cluster.get_components()

    def _get_component_definitions(self):
        '''Get component definitions from the Fabrikate-Definitions repository.'''
        print("Collecting Fabrikate Component Definitions from GitHub...")
        scraper = Scraper()
        return scraper.get_repo_components()

    def _get_matches(self, cluster_components):
        '''Get MatchCategories from the Matcher.'''
        print("Comparing Cluster Deployments to Fabrikate Definitions...")
        return self.matcher.match_components(cluster_components)

    def _generate_HLD(self, match_categories):
        '''Manipulate the MatchCategories into yaml.'''
        verbose_print("Appending subcomponents to the main component...")
        data = self._set_subcomponents(match_categories)
        print("Creating component.yaml...")
        if self.dry_run:
            verbose_print("Writing component.yaml to terminal...")
            output = stdout
            self.dump_yaml(data, output)
        else:
            if self.output:
                verbose_print("Writing component.yaml to {}".format(self.output))
                output_file = os.path.join(self.output, "component.yaml")
            else:
                # File Written just outside the hydrate directory?
                path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
                verbose_print("Writing component.yaml to {}".format(path))
                output_file = "component.yaml"
            with open(output_file, 'w') as of:
                self.dump_yaml(data, of)

    def _set_subcomponents(self, match_categories):
        '''Set subcomponents for the top component from the match categories.'''
        from .comments import TOP_LEVEL_COMMENT
        from .comments import FULL_MATCH_COMMENT
        from .comments import PARTIAL_MATCH_COMMENT
        from .comments import NO_MATCH_COMMENT

        data = CommentedMap(self.top_component.as_yaml())
        data.yaml_set_start_comment(TOP_LEVEL_COMMENT)
        tmp_lst = CommentedSeq()

        # Set the subcomponents and comments
        for category, start_index, subcomponents in match_categories:
            for subcomponent in subcomponents:
                comment = None
                if isinstance(subcomponent, CommentedComponent):
                    comment = subcomponent.inline_comment
                tmp_lst.append(subcomponent.as_yaml(), comment=comment)
            tmp_lst.yaml_set_comment_before_after_key(start_index, category, OFFSET)
        data['subcomponents'] = tmp_lst

        return data

    def dump_yaml(self, data, output):
        '''Dump yaml to output.'''
        yaml.indent(mapping=MAPPING, sequence=SEQUENCE, offset=OFFSET)
        yaml.dump(data, output)
