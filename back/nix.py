from typing import List
import shutil
import os
import subprocess

import sqlite3


DEFAULT_STORES_ROOT = "/nix_stores/"
NIX_DB_PATH = "nix/var/nix/db/db.sqlite"


class Nix:
    def __init__(self, stores_root: str = DEFAULT_STORES_ROOT):
        self.stores_root = stores_root

        if not os.path.exists(self.stores_root):
            os.makedirs(self.stores_root)

    def _run_cmd(self, command, throw_on_fail: bool = True):
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0 and throw_on_fail:
            error_message = stderr.decode().strip()
            raise Exception(f"Error during nix execution:\n{error_message}")

        return process.returncode, stdout, stderr

    def _get_store_paths(self, store_id: str):
        store_path = self.get_store_path(store_id)

        command = ["nix", "--store", store_path, "path-info", "--all"]
        _, stdout, _ = self._run_cmd(command)
        paths = stdout.decode().strip().split("\n")

        return paths

    def _get_package_closure(self, store_id: str, package):
        store_path = self.get_store_path(store_id)

        command = [
            "nix",
            "--store",
            store_path,
            "path-info",
            "--recursive",
            package,
        ]
        _, stdout, _ = self._run_cmd(command)
        paths = stdout.decode().strip().split("\n")

        return paths

    def get_ValidPaths(self, store_id: str):
        """
        Returns ValidPaths table from db.sqlite of a store
        """

        store_path = self.get_store_path(store_id)
        db_path = os.path.join(store_path, NIX_DB_PATH)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ValidPaths")
        results = cursor.fetchall()

        return results

    def get_store_path(self, store_name: str) -> str:
        return os.path.abspath(os.path.join(self.stores_root, store_name))

    def add_store(self, store_name: str) -> str:
        """
        Creates a new directory for a new store.
        Raises exception if store already exists.
        @returns: A path to created store (store ID).
        """

        directory_path = self.get_store_path(store_name)

        if os.path.exists(directory_path):
            raise Exception(
                f"Store named {store_name} already exists in the filetree."
            )

        # Create store directory
        os.makedirs(directory_path)

        return store_name

    def remove_store(self, store_id: str):
        """
        Expects sanitized input.
        Removes a store directory.
        """

        directory_path = self.get_store_path(store_id)

        # Check that the dir to be deleted in a folder we manage.
        # TODO: decide if keep this check.
        abs_root = os.path.abspath(self.stores_root)
        if os.path.commonpath([directory_path, abs_root]) != abs_root:
            raise Exception("Attempted to delete something outside stores dir")

        shutil.rmtree(directory_path)

    def add_package_to_store(self, store_id: str, package_name: str):
        """
        Adds (builds) a package to a store.
        """

        store_path = self.get_store_path(store_id)
        command = [
            "nix",
            "--store",
            store_path,
            "build",
            "--no-link",
            package_name,
        ]

        self._run_cmd(command)

    def remove_package_from_store(self, store_id: str, package_name: str):
        """
        Deletes a package recursively (closure of it's path).
        Throws an exception on nix error.
        """

        store_path = self.get_store_path(store_id)
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

        self._run_cmd(command)

    def check_package_exists(self, store_id: str, package_name: str) -> bool:
        """
        Checks if specified package exists in a store by invoking nix path-info.
        """

        store_path = self.get_store_path(store_id)
        command = ["nix", "--store", store_path, "path-info", package_name]
        ret, _, _ = self._run_cmd(command, throw_on_fail=False)
        if ret == 0:
            return True
        else:
            return False

    def get_package_closure_size(self, store_id: str, package: str) -> int:
        """
        Returns closure size in bytes invoking `nix path-info --closure-size`.
        """

        store_path = self.get_store_path(store_id)

        command = [
            "nix",
            "--store",
            store_path,
            "path-info",
            "--closure-size",
            package,
        ]
        _, stdout, _ = self._run_cmd(command)

        size = stdout.decode().strip().split("\t")[1]
        return int(size)

    def get_difference_of_paths(
        self, store_id1: str, store_id2: str
    ) -> List[str]:
        """
        Returns a list of paths that are in first store but not in second.
        Throws an exception on nix error.
        """

        paths1 = self._get_store_paths(store_id1)
        paths2 = self._get_store_paths(store_id2)

        return list(set(paths1) - set(paths2))

    def get_difference_of_package_closures(
        self, store1: str, package1: str, store2: str, package2: str
    ) -> List[str]:
        """
        Returns a list of paths that are in first package but not in second.
        Throws an exception on nix error.
        """

        paths1 = self._get_package_closure(store1, package1)
        paths2 = self._get_package_closure(store2, package2)

        return list(set(paths1) - set(paths2))
