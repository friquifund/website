import collections.abc
import os
import re
from typing import Dict, Any, List, Optional
import pathlib
import copy

import yaml
from box import Box


def _yaml_parse_environ(yaml_module):
    """Used to parse expressions of the form << ENVIRON_VARIABLE >> in YAML files.
    For more information, see: http://stackoverflow.com/a/27232341
    """
    pattern = re.compile(r"^(.*)\<\<(.*)\>\>(.*)$")
    yaml_module.add_implicit_resolver("!pathex", pattern)

    def pathex_constructor(loader, node):
        value = loader.construct_scalar(node)
        left, env_var, right = pattern.match(value).groups()
        env_var = env_var.strip()
        if env_var not in os.environ:
            msg = f"Environment variable {env_var} not defined"
            raise ValueError(msg)
        return left + os.environ[env_var] + right

    yaml_module.add_constructor("!pathex", pathex_constructor)

    return yaml_module


def join_path(loader, node):
    """Custom handler to join strings in YAML files"""
    seq = loader.construct_sequence(node)
    return os.path.join(*seq)


# Add the functionality to parse environment variables to YAML module
yaml = _yaml_parse_environ(yaml)
# Add the functionality to join strings to YAML module
yaml.add_constructor("!path", join_path)


def load_single_yaml(config_filename: str) -> Box:
    """Return a dictionary with the settings file in the file *path*."""
    with open(config_filename) as f:
        config = yaml.load(f, Loader=yaml.Loader)
    return config


def merge(old: Dict[Any, Any], new: Dict[Any, Any]) -> Dict:
    """
    Merge the two dictionaries together into a single dictionary.
    Priority will go to the ``new`` dictionary object when the same
    key exists in both of the dictionaries.
    Parameters
    ----------
    old:
        Dictionary to merge the new values into
    new:
        Dictionary to merge into the old dictionary
    Returns
    -------
    :
        Merged dictionary containing values from both of the dictionaries
    """
    for k, v in new.items():
        if isinstance(old, collections.abc.Mapping):
            if isinstance(v, collections.abc.Mapping):
                old[k] = merge(old.get(k, {}), v)
            else:
                old[k] = v
        else:
            old = {k: v}

    return old


def load_yaml_files(paths: List[str]) -> Dict[str, Any]:
    """
    Loads a list of yaml files and returns a single dictionary
    containing all of them. Note that files listed later in the list
    will have higher precedence since they may potentially overwrite
    values of yaml files loaded in before them in the list.
    This function is named ``raw`` since the ``load_yaml_files`` function
    performs additional steps on top of loading in the raw yaml files.
    Parameters
    ----------
    paths:
        List of absolute file paths to load
    Returns
    -------
    :
        Merged dictionary containing the config values
    """
    res = {}
    for p in paths:
        filename = pathlib.Path(p).stem
        config = load_single_yaml(p)
        res = merge(res, {filename: config})
    return res


def get_config_files_in_dir(dir_path: str) -> List[Optional[pathlib.Path]]:
    """
    Get a list of yaml config files (*.yaml, *.yml) that are in
    the given directory.
    Parameters
    ----------
    dir_path:
        Path to the directory to search under
    Returns
    -------
    :
        List of yaml config files in the directory
    """
    path = pathlib.Path(dir_path)
    types = ("*.yml", "*.yaml")
    config_files = []
    for files in types:
        config_files.extend(path.glob(files))
    return config_files


def resolve_paths(input_dict: dict) -> dict:
    """
    Resolves paths in config by concatenating all the sub-folders. For example
    output_files: [<< DATA >>, output_folder, filename.csv] will become
    << DATA >>/output_folder/filename.csv
    where << DATA >> is the environment variable pointing to the root path
    Parameters
    ----------
    input_dict: input dictionary

    Returns
    -------

    """
    for k in input_dict.keys():
        if isinstance(input_dict[k], list):
            input_dict[k] = os.path.join(*input_dict[k])
        else:
            input_dict[k] = resolve_paths(input_dict[k])
    return input_dict


def resolve_references(config: Box, config_cached: Box) -> Box:
    """
    Substitutes the references with the values specified in the dictionary. The reason it contains a function inside
    is to allow to parse from the original cached config
    Parameters
    ----------
    config
    config_cached

    Returns
    -------

    """

    for k, v in config.items():
        if isinstance(v, str):
            path_token = re.findall(r"{(.*?)}", v)
            for p in path_token:
                config[k] = v.replace("{" + p + "}", eval(f"config_cached.{p}"))
        elif isinstance(v, list):
            for idx, x in enumerate(v):
                path_token = re.findall(r"{(.*?)}", x)
                for p in path_token:
                    config[k][idx] = x.replace("{" + p + "}", eval(f"config_cached.{p}"))
        elif isinstance(v, dict):
            config[k] = resolve_references(v, config_cached)
    return config


def load_yaml_folder(path: str or List[str]) -> Dict:
    """
    Loads all yaml files in a folder
    """

    files = get_config_files_in_dir(path)
    config = load_yaml_files(files)

    return config


def load_yaml_recursively(path: pathlib.Path) -> Dict:
    is_node = check_if_node(path)
    if is_node:
        config = load_yaml_folder(str(path))
    else:
        config = load_yaml_folder(str(path))
        for item in path.iterdir():
            if item.is_dir():
                if any(os.scandir(item)):
                    config[item.stem] = load_yaml_recursively(item)

    return config


def check_if_node(path: pathlib.Path) -> Dict:
    for item in path.iterdir():
        if item.is_dir():
            return False
    return True


def load_configs(config_path: str, parse: bool = True) -> Box:
    """
    This function loads a set of configs from a folder. The function expects a tree of folders whose nodes are .yaml or
    .yml files. The function then will replicate the tree folder structure inside a dictionary and read and parse
    the config files at the nodes.
    For example if we have the following tree
    - config1.yaml
    - config2.yaml
    - config3.yaml
    - folder
        - config4.yaml
        - config5.yaml
    The output will be the following Box object:
    {
        "config1": config_1_dict
        "config2": config_2_dict
        "config3": config_3_dict
        "folder": {
            "config4": config_4_dict,
            "config5": config_5_dict
            }
    }
    Parameters
    ----------
    config_path

    Returns
    -------

    """
    dict_config = load_yaml_recursively(pathlib.Path(config_path))
    config = Box(dict_config)
    if parse:
        config = parse_config(config)
    return config


def parse_config(config: Box) -> Box:

    config_cached = copy.deepcopy(config)
    config = resolve_references(config, config_cached)
    return config
