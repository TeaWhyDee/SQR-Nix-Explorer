from typing import List


def add_store(store_name: str) -> str:
    """
    Raises exception if store already exists or on nix error.
    @returns: A path to created store (store ID).
    """

    raise Exception()


def remove_store(store_name: str):
    raise Exception()


def add_package_to_store(store_name: str, package_name: str):
    raise Exception()


def remove_package_from_store(store_name: str, package_name: str):
    raise Exception()


def check_package_exists(store_name: str, package_name: str) -> bool:
    return False
    raise Exception()


def get_difference_of_paths(store_name1: str, store_name2: str) -> List[str]:
    raise Exception()


def get_difference_of_package_closures(package1: str, package2: str) -> List[str]:
    # ex: store1#bash,  store2#hello
    raise Exception()
