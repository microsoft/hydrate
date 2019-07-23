"""Use to construct the High-Level Deployment."""
from .comments import TOP_LEVEL_COMMENT
from .cluster import Cluster
from .component import TopComponent
from .scrape import Scraper
from .manifest import generate_manifests
from .match import Matcher

from sys import stdout
import os.path
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml import YAML
yaml = YAML()

MAPPING = 2
SEQUENCE = 4
OFFSET = 2
verbose_print = None


class HLD_Generator():
    """Creates HLD from Cluster and Fabrikate Components."""

    def __init__(self, args):
        """Construct HLD_Generator object."""
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
        """Generate the component.yaml."""
        # Step 1a. Get cluster components
        cluster_components = self._get_cluster_components()
        # Step 1b. Get repo components, instantiate matcher
        repo_components = self._get_component_definitions()
        self.matcher = Matcher(repo_components)
        # Step 2. Find the matches between the cluster and repo
        match_categories = self._get_matches(cluster_components)
        # Step 3. Generate the HLD
        self._generate_HLD(match_categories)
        # Step 4. Generate the manifests directory
        self._generate_manifests()

    def _get_cluster_components(self):
        """Get objects living on the cluster."""
        print("Connecting to cluster...")
        self.cluster.connect_to_cluster()
        print("Connected!")
        print("Collecting information from the cluster...")
        return self.cluster.get_components()

    def _get_component_definitions(self):
        """Get component definitions from the Fabrikate-Definitions repository."""
        print("Collecting Fabrikate Component Definitions from GitHub...")
        scraper = Scraper()
        return scraper.get_repo_components()

    def _get_matches(self, cluster_components):
        """Get MatchCategories from the Matcher."""
        print("Comparing Cluster Deployments to Fabrikate Definitions...")
        return self.matcher.match_components(cluster_components)

    def _generate_HLD(self, match_categories):
        """Manipulate the MatchCategories into yaml."""
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

    def _matches_to_components(self, matches):
        """Get the components from the matches."""
        subcomponents = []
        for match in matches:
            subcomponents.append(match.get_component())
        return subcomponents

    def _set_subcomponents(self, match_categories):
        """Set subcomponents for the top component from the match categories."""
        data = CommentedMap(self.top_component.as_yaml())
        data.yaml_set_start_comment(TOP_LEVEL_COMMENT)
        temp_list = CommentedSeq()

        # Set the subcomponents and comments
        for top_comment, start_index, matches in match_categories:
            components = self._matches_to_components(matches)

            for subcomponent in components:
                try:  # Extract inline comment before it's removed
                    inline_comment = subcomponent.inline_comment
                except AttributeError:
                    inline_comment = None

                d2 = CommentedMap(subcomponent.as_yaml())

                if inline_comment:  # Apply inline comment to data
                    d2.yaml_add_eol_comment(comment=inline_comment,
                                            key='name')
                temp_list.append(d2)

            temp_list.yaml_set_comment_before_after_key(key=start_index,
                                                        before=top_comment,
                                                        indent=OFFSET)
        data['subcomponents'] = temp_list
        return data

    def _generate_manifests(self):
        """Generate the manifests."""
        namespaces = self.cluster.get_namespaces()
        generate_manifests(namespaces)

    def dump_yaml(self, data, output):
        """Dump yaml to output."""
        yaml.indent(mapping=MAPPING, sequence=SEQUENCE, offset=OFFSET)
        yaml.dump(data, output)
