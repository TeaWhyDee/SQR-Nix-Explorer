import re
from typing import Iterator
import os
import shutil

import pytest

from back.nix import Nix


TEST_ROOT = "/tmp/nix"


@pytest.fixture
def NixAPI() -> Iterator[Nix]:
    nix = Nix(stores_root=TEST_ROOT)

    yield nix

    # Cleanup:
    # 1. Set permissions for deletion
    # 2. Delete tree
    for root, dirs, files in os.walk(TEST_ROOT):
        for momo in dirs:
            os.chmod(os.path.join(root, momo), 0o722)

    shutil.rmtree(TEST_ROOT)


def test_add_store(NixAPI):
    store_name = "test_store"

    NixAPI.add_store(store_name)
    assert os.path.exists(os.path.join(TEST_ROOT, store_name))

    with pytest.raises(Exception):
        NixAPI.add_store(store_name)


def test_remove_store(NixAPI):
    store_name = "test_store"

    # Try to delete non-existent store
    with pytest.raises(FileNotFoundError):
        NixAPI.remove_store(store_name)

    # Try to delete existent store
    directory_path = os.path.join(TEST_ROOT, store_name)
    os.makedirs(directory_path)

    NixAPI.remove_store(store_name)
    assert not os.path.exists(os.path.join(TEST_ROOT, store_name))


# def test_get_ValidPaths(NixAPI):
#     store_name = "test_store"

#     directory_path = os.path.join(TEST_ROOT, store_name)
#     os.makedirs(directory_path)
    
#     NixAPI.add_package_to_store(store_name, "nixpkgs#glibc")

#     assert len(NixAPI.get_ValidPaths(store_name)) == 215
    

def test_remove_package_from_store(NixAPI):
    store_name = "test_store"

    directory_path = os.path.join(TEST_ROOT, store_name)
    os.makedirs(directory_path)
    
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
    
    
def test_check_package_exists(NixAPI):
    pass

    
def test_get_difference_of_paths(NixAPI):
    pass

def test_get_difference_of_package_closures(NixAPI):
    pass