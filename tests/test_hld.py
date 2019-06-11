"""Test suite for hld.py."""
import pytest
import io
from hydrate.hld import Component
from hydrate.hld import generate_HLD


tst_component = Component("Test-Component")
str_stream = io.StringIO()
exp_str = """name: Test-Component
             generator: static
             method: git"""

@pytest.mark.parametrize('component, output, expected',
                         [(tst_component, str_stream, exp_str)])
def test_generate_HLD(component, output, expected):
    """Test generate_HLD function."""
    generate_HLD(component, output)
    str_stream == expected
