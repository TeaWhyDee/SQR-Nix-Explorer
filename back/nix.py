from typing import List
import shutil
import os
import subprocess

import sqlite3


STORES_ROOT = "/nix_stores/"
NIX_DB_PATH = "nix/var/nix/db/db.sqlite"


def _run_cmd(command, throw_on_fail: bool = True):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0 and throw_on_fail:
        error_message = stderr.decode().strip()
        raise Exception(f"Error during nix execution:\n{error_message}")

    return process.returncode, stdout, stderr


def _get_store_paths(store_id: str):
    store_path = get_store_path(store_id)

    command = ["nix", "--store", store_path, "path-info", "--all"]
    _, stdout, _ = _run_cmd(command)
    paths = stdout.decode().strip().split("\n")

    return paths


def _get_package_closure(store_id: str, package):
    store_path = get_store_path(store_id)

    command = ["nix", "--store", store_path, "path-info", "--recursive", package]
    _, stdout, _ = _run_cmd(command)
    paths = stdout.decode().strip().split("\n")

    return paths


def get_ValidPaths(store_id: str):
    """
    Returns ValidPaths table from db.sqlite of a store
    """
    connection = sqlite3.connect("db.sqlite")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ValidPaths")
    results = cursor.fetchall()

    return results


def get_store_path(store_name: str) -> str:
    return os.path.abspath(os.path.join(STORES_ROOT, store_name))


def add_store(store_name: str) -> str:
    """
    Creates a new directory for a new store.
    Raises exception if store already exists.
    @returns: A path to created store (store ID).
    """

    directory_path = get_store_path(store_name)

    if os.path.exists(directory_path):
        raise Exception(f"Store named {store_name} already exists in the filetree.")

    # Create store directory
    os.makedirs(directory_path)

    return store_name


def remove_store(store_id: str):
    """
    Expects sanitized input.
    Removes a store directory.
    """

    directory_path = get_store_path(store_id)

    # Check that we are deleting a directory we should (against malicious user)
    abs_root = os.path.abspath(STORES_ROOT)
    if os.path.commonpath([directory_path, abs_root]) != abs_root:
        raise Exception("Attempted to delete something outside stores dir.")

    shutil.rmtree(directory_path)


def add_package_to_store(store_id: str, package_name: str):
    """
    Adds (builds) a package to a store.
    """

    store_path = get_store_path(store_id)
    command = ["nix", "--store", store_path, "build", "--no-link", package_name]

    _run_cmd(command)


def remove_package_from_store(store_id: str, package_name: str):
    """
    Deletes a package recursively (closure of it's path).
    Throws an exception on nix error.
    """

    store_path = get_store_path(store_id)
    command = [
        "nix",
        "--store",
        store_path,
        "store",
        "delete",
        "--ignore-liveness",
        "--recursive",
        package_name,
    ]

    _run_cmd(command)


def check_package_exists(store_id: str, package_name: str) -> bool:
    """
    Checks if specified package exists in a store by invoking nix path-info.
    """

    store_path = get_store_path(store_id)
    command = ["nix", "--store", store_path, "path-info", package_name]
    ret, _, _ = _run_cmd(command, throw_on_fail=False)
    if ret == 0:
        return True
    else:
        return False


def get_difference_of_paths(store_id1: str, store_id2: str) -> List[str]:
    """
    Returns a list of paths that are in first store but not in second.
    Throws an exception on nix error.
    """

    paths1 = _get_store_paths(store_id1)
    paths2 = _get_store_paths(store_id2)

    return list(set(paths1) - set(paths2))


def get_difference_of_package_closures(store1: str, package1: str, store2: str, package2: str) -> List[str]:
    """
    Returns a list of paths that are in first package but not in second.
    Throws an exception on nix error.
    """

    paths1 = _get_package_closure(store1, package1)
    paths2 = _get_package_closure(store2, package2)

    return list(set(paths1) - set(paths2))
