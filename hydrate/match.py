"""Provide class to match cluster objects with Fabrikate component definitions."""

from collections import namedtuple
from .comments import FULL_MATCH_COMMENT
from .comments import PARTIAL_MATCH_COMMENT
from .comments import NO_MATCH_COMMENT


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
                                   ['category', 'start_index', 'subcomponents'])
        self.match_categories = []

        FullMatchResults = self.get_full_matches(cluster_components)

        if FullMatchResults.full_matches:
            self.match_categories.append(
                MatchCategory(category=FULL_MATCH_COMMENT,
                              start_index=self.get_start_index(),
                              subcomponents=FullMatchResults.full_matches))

        if FullMatchResults.leftovers:
            PartialMatchResults = self.get_partial_matches(FullMatchResults.leftovers)

            if PartialMatchResults.partial_matches:
                self.match_categories.append(
                    MatchCategory(category=PARTIAL_MATCH_COMMENT,
                                  start_index=self.get_start_index(),
                                  subcomponents=PartialMatchResults.partial_matches))

            if PartialMatchResults.leftovers:
                self.match_categories.append(
                    MatchCategory(category=NO_MATCH_COMMENT,
                                  start_index=self.get_start_index(),
                                  subcomponents=PartialMatchResults.leftovers))

        return self.match_categories

    def get_start_index(self):
        """Calculate start_index based on the last MatchCategory in the list."""
        start_idx = 0
        if self.match_categories:
            start_idx = len(self.match_categories[-1].subcomponents) \
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
        cluster_set = {cc.name for cc in cluster_components}

        for rc in self.repo_components:
            repo_set = set(rc.name.split('-'))
            if repo_set.issubset(cluster_set):
                cluster_set.difference_update(repo_set)
                full_matches.append(rc)

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
        PartialMatchResults = namedtuple('PartialMatchResults', ['partial_matches', 'leftovers'])
        PartialMatch = namedtuple('PartialMatch', ['cluster_components', 'repo_component'])

        partial_matches = []
        leftovers = None

        cluster_name_set = {leftover.name for leftover in full_match_leftovers}

        for repo_component in self.repo_components:
            repo_component_name_set = set(repo_component.name.split('-'))
            common_component_names = repo_component_name_set.intersection(cluster_name_set)
            if common_component_names:
                partial_matches.append(
                    PartialMatch(cluster_components=sorted(common_component_names),
                                 repo_component=repo_component))
                cluster_name_set.difference_update(common_component_names)

        if cluster_name_set:
            leftovers = [cc for cc in full_match_leftovers if cc.name in cluster_name_set]

        return PartialMatchResults(partial_matches, leftovers)
