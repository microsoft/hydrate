"""Provide class to match cluster objects with Fabrikate component definitions."""
from enum import Enum
from collections import namedtuple
from .component import CommentedComponent
from .comments import FULL_MATCH_COMMENT
from .comments import PARTIAL_MATCH_COMMENT
from .comments import NO_MATCH_COMMENT
from .telemetry import Telemetry


class Matcher():
    """Match the deployments found on a cluster with the Fabrikate Definitions."""

    def __init__(self, repo_components):
        """Instantiate a Matcher object.

        Args:
            repo_components: list of Component objects

        """
        self.repo_components = repo_components
        self.match_categories = []

    def match_components(self, cluster_components):
        """Generate cluster and repo component matches.

        Overwrites existing match_categories attribute.

        Args:
            repo_components: list of Components from the definitions repository
            cluster_components: list of Components from the cluster

        Returns:
            match_categories: list of MatchCategory namedtuples

        """
        MatchCategory = namedtuple('MatchCategory',
                                   ['top_comment', 'start_index', 'matches'])
        self.match_categories = []

        FullMatchResults = self.get_full_matches(cluster_components)

        if FullMatchResults.full_matches:
            self.match_categories.append(
                MatchCategory(top_comment=FULL_MATCH_COMMENT,
                              start_index=self.get_start_index(),
                              matches=FullMatchResults.full_matches))

            send_match_name_telemetry(FullMatchResults.full_matches, "Full Matches")
            send_match_number_telemetry(FullMatchResults.full_matches, "Full Matches")

        if FullMatchResults.leftovers:
            PartialMatchResults = self.get_partial_matches(FullMatchResults.leftovers)

            if PartialMatchResults.partial_matches:
                self.match_categories.append(
                    MatchCategory(top_comment=PARTIAL_MATCH_COMMENT,
                                  start_index=self.get_start_index(),
                                  matches=PartialMatchResults.partial_matches))

                send_match_name_telemetry(PartialMatchResults.partial_matches,
                                          "Partial Matches")
                send_match_number_telemetry(PartialMatchResults.partial_matches,
                                            "Partial Matches")

            if PartialMatchResults.no_matches:
                NoMatchResults = self.get_no_matches(PartialMatchResults.no_matches)

                self.match_categories.append(
                    MatchCategory(top_comment=NO_MATCH_COMMENT,
                                  start_index=self.get_start_index(),
                                  matches=NoMatchResults))

                send_match_number_telemetry(NoMatchResults, "No Matches")

        return self.match_categories

    def get_start_index(self):
        """Calculate start_index based on the last MatchCategory in the list."""
        start_idx = 0
        if self.match_categories:
            start_idx = len(self.match_categories[-1].matches) \
                        + self.match_categories[-1].start_index
        return start_idx

    def get_full_matches(self, cluster_components):
        """Determine which components fully match the cluster.

        Returns:
            FullMatchResults: namedtuple
                full_matches: list of components or []
                leftovers: list of components or None

        """
        FullMatchResults = namedtuple('FullMatchResults', ['full_matches', 'leftovers'])
        full_matches = []
        leftovers = None
        cluster_map = {cc.name: cc for cc in cluster_components}
        cluster_set = set(cluster_map.keys())

        for rc in self.repo_components:
            repo_set = set(rc.name.split('-'))
            if repo_set.issubset(cluster_set):
                cc_names = cluster_set.intersection(repo_set)
                cluster_matches = [cluster_map[component_name] for component_name in cc_names]
                cluster_set.difference_update(repo_set)

                full_matches.append(
                    Match(category=MatchCategory.FULL_MATCH,
                          cluster_matches=cluster_matches,
                          repo_match=rc))

        if cluster_set:
            leftovers = [cc for cc in cluster_components if cc.name in cluster_set]

        return FullMatchResults(full_matches, leftovers)

    def get_partial_matches(self, full_match_leftovers):
        """Determine which components partially match the cluster.

        Args:
            repo_components: list of Components from the definitions repository
            full_match_leftovers: list of leftover deployments after get_full_matches

        Returns:
            PartialMatchResults: namedtuple
                partial_matches: dict(key: component.name, value: list of components)
                leftovers: list of components

        """
        PartialMatchResults = namedtuple('PartialMatchResults', ['partial_matches', 'no_matches'])

        partial_matches = []
        no_matches = None
        cluster_map = {cc.name: cc for cc in full_match_leftovers}
        cluster_name_set = set(cluster_map.keys())

        for repo_component in self.repo_components:
            repo_component_name_set = set(repo_component.name.split('-'))
            common_names = repo_component_name_set.intersection(cluster_name_set)

            if common_names:
                cluster_name_set.difference_update(common_names)
                cluster_matches = [cluster_map[c_name] for c_name in common_names]

                partial_matches.append(
                    Match(category=MatchCategory.PARTIAL_MATCH,
                          cluster_matches=cluster_matches,
                          repo_match=repo_component))

        if cluster_name_set:
            no_matches = [cc for cc in full_match_leftovers if cc.name in cluster_name_set]

        return PartialMatchResults(partial_matches, no_matches)

    def get_no_matches(self, partial_match_leftovers):
        """Process the components that don't match existing definitions."""
        NoMatchResults = []

        if partial_match_leftovers:
            for component in partial_match_leftovers:
                NoMatchResults.append(
                    Match(category=MatchCategory.NO_MATCH,
                          cluster_matches=component))

        return NoMatchResults


class MatchCategory(Enum):
    """Flags for different kinds of matches."""

    FULL_MATCH = 1
    PARTIAL_MATCH = 2
    NO_MATCH = 3


class Match():
    """Match base class.

    Args:
        category: MatchCategory enum
        cluster_matches: list of Components
        repo_match: Component or None

    """

    def __init__(self, category=None, cluster_matches=[], repo_match=None):
        """See help(Match)."""
        self.category = category
        self.cluster_matches = cluster_matches
        self.repo_match = repo_match

    def get_component(self):
        """Return the component from the Match."""
        if self.category == MatchCategory.FULL_MATCH:
            return self.repo_match
        if self.category == MatchCategory.PARTIAL_MATCH:
            inline_comment = "Cluster Components: "
            inline_comment += ", ".join([cc.name for cc in self.cluster_matches])
            return CommentedComponent(inline_comment=inline_comment,
                                      component=self.repo_match)
        if self.category == MatchCategory.NO_MATCH:
            return self.cluster_matches


def send_match_name_telemetry(matches, match_type):
    """Send telemetry of the names of matches found."""
    TELEMETRY = Telemetry(None)

    match_string = namedtuple("match_string", ["cluster_matches", "repo_match"])
    match_strings = []
    for m in matches:
        cluster_match_names = []
        for cc in m.cluster_matches:
            cluster_match_names.append(cc.name)
        repo_match_name = m.repo_match.name
        match_strings.append(match_string(cluster_match_names, repo_match_name))

    for match in match_strings:
        TELEMETRY.track_event(match_type, {"cluster_match_names": match.cluster_matches,
                                           "repo_match_name": match.repo_match})


def send_match_number_telemetry(matches, match_type):
    """Send telemetry of the number of matches found."""
    TELEMETRY = Telemetry(None)
    TELEMETRY.track_metric(f"# of {match_type}", len(matches))
