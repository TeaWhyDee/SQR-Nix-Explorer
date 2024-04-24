import os
import re

import pytest

from tests.conftest import TEST_ROOT


def test_add_store(NixAPI_empty):
    store_name = "test_store"

    NixAPI_empty.add_store(store_name)
    assert os.path.exists(os.path.join(TEST_ROOT, store_name))

    with pytest.raises(Exception):
        NixAPI_empty.add_store(store_name)


def test_remove_store(NixAPI_empty):
    store_name = "test_store"

    # Try to delete non-existent store
    with pytest.raises(Exception):
        NixAPI_empty.remove_store(store_name)

    # Try to delete existent store
    directory_path = os.path.join(TEST_ROOT, store_name)
    os.makedirs(directory_path)

    NixAPI_empty.remove_store(store_name)
    assert not os.path.exists(os.path.join(TEST_ROOT, store_name))


def test_get_ValidPaths(NixAPI):
    store_name = "test_store"

    NixAPI.add_package_to_store(store_name, "nixpkgs#glibc")

    assert len(NixAPI.get_ValidPaths(store_name)) == 160


def test_remove_package_from_store(NixAPI):
    store_name = "test_store"

    NixAPI.add_package_to_store(store_name, "nixpkgs#glibc")
    paths_directory = os.path.join(TEST_ROOT, store_name, "nix/store/")

    found = False
    for dir_name in os.listdir(paths_directory):
        dir_path = os.path.join(paths_directory, dir_name)
        if os.path.isdir(dir_path) and re.match(".*glibc-.*-bin", dir_name):
            found = True
            break
    assert found

    NixAPI.remove_package_from_store(store_name, "nixpkgs#glibc")
    found = False
    for dir_name in os.listdir(paths_directory):
        dir_path = os.path.join(paths_directory, dir_name)
        if os.path.isdir(dir_path) and re.match("glibc-*-bin", dir_name):
            found = True
            break
    assert not found


def test_get_package_closure_size(NixAPI):
    store_name = "test_store"
    package_name = "nixpkgs#glibc"

    NixAPI.add_package_to_store(store_name, package_name)

    assert NixAPI.get_package_closure_size(store_name, package_name) == 35635152


def test_check_package_exists(NixAPI):
    store_name = "test_store"
    package_name = "nixpkgs#glibc"

    NixAPI.add_package_to_store(store_name, package_name)

    assert NixAPI.check_package_exists(store_name, package_name)
    assert not NixAPI.check_package_exists(store_name, "nixpkgs#rustc")


def test_get_difference_of_paths(NixAPI):
    store_name1 = "test_store"
    store_name2 = "test_store2"

    package_name1 = "nixpkgs#glibc"
    package_name2 = "nixpkgs#busybox"

    NixAPI.add_store(store_name2)

    NixAPI.add_package_to_store(store_name1, package_name1)
    NixAPI.add_package_to_store(store_name2, package_name2)

    assert len(NixAPI.get_difference_of_paths(store_name1, store_name2)) == 1
    assert len(NixAPI.get_difference_of_paths(store_name2, store_name1)) == 157


def test_get_difference_of_package_closures(NixAPI):
    store_name1 = "test_store"
    store_name2 = "test_store2"

    package_name1 = "nixpkgs#glibc"
    package_name2 = "nixpkgs#busybox"

    NixAPI.add_store(store_name2)

    NixAPI.add_package_to_store(store_name1, package_name1)
    NixAPI.add_package_to_store(store_name2, package_name2)

    assert (
        len(
            NixAPI.get_difference_of_package_closures(
                store_name1, package_name1, store_name2, package_name2
            )
        )
        == 1
    )
    assert (
        len(
            NixAPI.get_difference_of_package_closures(
                store_name2, package_name2, store_name1, package_name1
            )
        )
        == 1
    )
