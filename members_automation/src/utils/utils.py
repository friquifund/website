from typing import List


def merge_dict(dict_1, dict_2):
    """ Update a first dictionary recursively with the contents of a second dictionary."""
    if not isinstance(dict_2, dict):
        return dict_2
    dict_merged = dict_1.copy()
    for k, v in dict_2.items():
        if k in dict_merged and isinstance(dict_merged[k], dict):
            dict_merged[k] = merge_dict(dict_merged[k], v)
        else:
            dict_merged[k] = v
    return dict_merged


def list_intersection(list1: List[str], list2: List[str]) -> List[str]:
    """
    Returns the intersection between two lists
    :param list1:
    :param list2:
    :return: intersection
    """
    return list(set(list1).intersection(set(list2)))
