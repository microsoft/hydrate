"""Test suite for cluster.py."""
import pytest
from hydrate.cluster import get_first_word
from hydrate.cluster import count_first_word
from hydrate.cluster import sort_dict_by_value


tst_string = "fabrikate-elasticsearch"
exp_string = "fabrikate"

@pytest.mark.parametrize('string, delimiter, expected',
                         [(tst_string, "-", exp_string)])
def test_get_first_word(string, delimiter, expected):
    """Test get_first_word function."""
    assert get_first_word(string, delimiter) == expected


tst_str_list = ["apple", "apple", "orange", "apple", "banana", "orange"]
exp_str_list = {"apple": 3, "orange": 2, "banana": 1}

@pytest.mark.parametrize('str_list, expected',
                         [(tst_str_list, exp_str_list)])
def test_count_first_word(str_list, expected):
    """Test count_first_word function."""
    assert count_first_word(str_list) == expected


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
