"""Test suite for hld.py."""
import pytest
import io
from collections import namedtuple

from hydrate.component import Component
from hydrate.hld import HLD_Generator


class Test_HLD_Generator():
    """Test Suite for the HLD_Generator class."""

    MODULE = 'hydrate.hld'
    CLASS = f'{MODULE}.HLD_Generator'
    tst_args = namedtuple('tst_args', ['name',
                                       'kubeconfig',
                                       'dry_run',
                                       'output',
                                       'verbose'])
    class_tst_args = tst_args
    class_tst_args.name = "tst_name"
    class_tst_args.kubeconfig = "tst_kubeconfig"
    class_tst_args.dry_run = "tst_dry_run"
    class_tst_args.output = "tst_output"
    class_tst_args.verbose = "tst_verbose"

    def test_generate(self, mocker):
        """Test the generate method."""
        # Setup, mock, etc.
        tst_hld_generator = HLD_Generator(self.tst_args)
        tst_cluster_components = [Component(name='test-comp-1'),
                                  Component(name='test-comp-2')]
        tst_repo_components = [Component(name='repo-comp-1'),
                               Component(name='repo-comp-2')]
        mock_get_cc = mocker.patch(f'{self.CLASS}._get_cluster_components',
                                   return_value=tst_cluster_components)
        mock_get_cd = mocker.patch(f'{self.CLASS}._get_component_definitions',
                                   return_value=tst_repo_components)
        mock_get_matches = mocker.patch(f'{self.CLASS}._get_matches')
        mock_gen_HLD = mocker.patch(f'{self.CLASS}._generate_HLD')
        mock_gen_manifests = mocker.patch(f'{self.CLASS}._generate_manifests')

        # Call function
        tst_hld_generator.generate()

        # Assert results
        mock_get_cc.assert_called_once()
        mock_get_cd.assert_called_once()
        mock_get_matches.assert_called_once()
        mock_gen_HLD.assert_called_once()
        mock_gen_manifests.assert_called_once()

    def test_get_cluster_components(self, mocker):
        """Test the _get_cluster_components method."""
        # Setup, mock, etc.
        tst_hld_generator = HLD_Generator(self.tst_args)
        mock_cluster = mocker.patch.object(tst_hld_generator, 'cluster')
        mock_cluster.connect_to_cluster = mocker.MagicMock()
        mock_cluster.get_components = mocker.MagicMock()

        # Call function
        tst_hld_generator._get_cluster_components()

        # Assert results
        mock_cluster.connect_to_cluster.assert_called_once()
        mock_cluster.get_components.assert_called_once()

    def test_get_component_definitions(self, mocker):
        """Test the _get_component_definitions method."""
        # Setup, mock, etc.
        tst_hld_generator = HLD_Generator(self.tst_args)
        mock_scraper = mocker.patch(f'{self.MODULE}.Scraper')
        mock_scraper.return_value.get_repo_components = mocker.MagicMock()

        # Call function
        tst_hld_generator._get_component_definitions()

        # Assert results
        mock_scraper.assert_called_once()
        mock_scraper.return_value.get_repo_components.assert_called_once()

    def test_get_matches(self, mocker):
        """Test the _get_matches method."""
        # Setup, mock, etc.
        tst_hld_generator = HLD_Generator(self.tst_args)
        tst_cc = [Component("Test-Component")]
        mock_matcher = mocker.patch.object(tst_hld_generator, 'matcher')
        mock_matcher.match_components = mocker.MagicMock()

        # Call function
        tst_hld_generator._get_matches(tst_cc)

        # Assert results
        mock_matcher.match_components.assert_called_once()

    tst_args_1 = tst_args(dry_run=True,
                          name=None, kubeconfig=None, output=None, verbose=None)
    tst_args_2 = tst_args(output=True,
                          name=None, kubeconfig=None, dry_run=None, verbose=None)

    gen_hld_tst_args = [tst_args_1, tst_args_2]

    @pytest.mark.parametrize('tst_args', gen_hld_tst_args)
    def test_generate_HLD(self, mocker, tst_args):
        """Test the _generate_HLD method."""
        # Setup, mock, etc.
        tst_hld_generator = HLD_Generator(tst_args)
        tst_data = "test-data"
        tst_match_categories = ["full", "partial", "none"]
        mock_stdout = mocker.patch(f'{self.MODULE}.stdout')
        mock_set_subcomponents = mocker.patch(f'{self.CLASS}._set_subcomponents',
                                              return_value=tst_data)
        mock_dump_yaml = mocker.patch(f'{self.CLASS}.dump_yaml',
                                      return_value=None)

        # Call function
        tst_hld_generator._generate_HLD(tst_match_categories)

        # Assert results
        mock_set_subcomponents.assert_called()
        if tst_args.dry_run:
            mock_dump_yaml.assert_called_with(tst_data, mock_stdout)
        mock_dump_yaml.assert_called_once()

    def test_set_subcomponents(self):
        """Test the _set_subcomponents method."""
        # TODO
        # Setup, mock, etc.
        # Call function
        # Assert results
        pass

    def test_dump_yaml(self, mocker):
        """Test the dump_yaml method."""
        # Setup, mock, etc.
        tst_hld_generator = HLD_Generator(self.tst_args)
        tst_data = {"key": "value"}
        tst_output = io.StringIO()

        mock_yaml = mocker.patch(f'{self.MODULE}.yaml')
        mock_yaml.indent = mocker.MagicMock()
        mock_yaml.dump = mocker.MagicMock()

        # Call function
        tst_hld_generator.dump_yaml(tst_data, tst_output)

        # Assert results
        mock_yaml.indent.assert_called_once()
        mock_yaml.dump.assert_called_once()
