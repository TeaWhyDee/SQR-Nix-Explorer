import os
import signal

import time
import subprocess


def test_add_package_interrupted(client1, NixAPI_empty):
    PACKAGE = "nixpkgs#glibc"
    command = ["poetry", "run", "dev"]

    pro = subprocess.Popen(command, shell=False, preexec_fn=os.setsid)

    client1.post("/store", params={"store_name": "aboba"})
    client1.post(
        "/store/package", params={"store_name": "aboba", "package_name": PACKAGE}
    )

    time.sleep(3)
    os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

    valid_paths = NixAPI_empty.get_ValidPaths("aboba")

    for valid_path_tuple in valid_paths:
        nix_path = valid_path_tuple[1]

        ROOT = "/tmp/nix/aboba"
        abs_path = os.path.join(ROOT, nix_path[1:])

        assert os.path.exists(abs_path)
