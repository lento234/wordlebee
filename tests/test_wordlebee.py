import numpy as np

from wordlebee.__main__ import filter_array


def test_filter_array():
    init_list = np.array(["apple", "orange", "banana", "kiwi"])
    filtered_list = filter_array(lambda x: x.find("b") == -1, init_list)
    assert "banana" not in filtered_list

    filtered_list = filter_array(lambda x: x.find("g") == 4, init_list)
    assert filtered_list[0] == "orange"

    filtered_list = filter_array(lambda x: x.find("a") != 0, init_list)
    assert "apple" not in filtered_list
