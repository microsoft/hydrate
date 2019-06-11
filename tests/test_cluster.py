"""Test suite for cluster.py."""
import pytest
from hydrate.cluster import count_first_word
from hydrate.cluster import sort_dict_by_value

tst_dict_list = [{"name": "component-cluster"},
                 {"name": "component-api"}]
exp_dict_list = {"component": 2}

@pytest.mark.parametrize('dict_list, key, expected',
                         [(tst_dict_list, "name", exp_dict_list)])
def test_count_first_word(dict_list, key, expected):
    """Test count_first_word function."""
    assert count_first_word(dict_list, key) == expected


tst_fruits = {"apple": 1, "banana": 2, "orange": 3, "kiwi": 4,
              "mango": 5, "raspberry": 6, "peach": 7}
exp_fruits = [('peach', 7), ('raspberry', 6), ('mango', 5),
              ('kiwi', 4), ('orange', 3), ('banana', 2),
              ('apple', 1)]

@pytest.mark.parametrize('d, expected',
                         [(tst_fruits, exp_fruits)])
def test_sort_dict_by_value(d, expected):
    """Test sort_dict_by_value function."""
    assert sort_dict_by_value(d) == expected
