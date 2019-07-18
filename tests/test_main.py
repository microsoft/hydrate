"""Test the __main__.py file."""

from hydrate.__main__ import main
from hydrate.__main__ import parse_args


def test_main(mocker):
    """Test the main function."""
    # Setup mock, test objects, etc.
    tst_args = "test-args"
    mock_HLD_Generator = mocker.patch('hydrate.__main__.HLD_Generator')
    mock_HLD_Generator.return_value.generate = mocker.MagicMock()

    # Call the function
    main(tst_args)

    # Assert the results
    mock_HLD_Generator.assert_called_once()
    mock_HLD_Generator.return_value.generate.assert_called_once()


def test_parse_args(mocker):
    """Test the parse_args function."""
    # Setup mock, test objects, etc
    tst_argv = ['-n', 'test-name',
                '-k', 'test-kubeconfig',
                '-o', 'test-output',
                '-v',
                '-d',
                'run']
    mock_Argument_Parser = mocker.patch('hydrate.__main__.ArgumentParser')
    mock_Argument_Parser.return_value.add_argument = mocker.MagicMock()
    mock_Argument_Parser.return_value.parse_args = mocker.MagicMock()

    # Call the function
    args = parse_args(tst_argv)

    # Assert the results
    assert args.run
    assert args.name
    assert args.kubeconfig
    assert args.output
    assert args.verbose
    assert args.dry_run
