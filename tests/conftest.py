import os
import shutil
import subprocess
from functools import lru_cache
from typing import Iterator

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import Engine
from sqlmodel import Session

from back.api.dependencies import get_db, get_nix
from back.db.base import (
    setup_logging,
    create_engine,
    create_db_and_tables,
    remove_db_and_tables,
)
from back.db.models import User
from back.db.repository import DB
from back.main import get_app
from back.nix import Nix
from back.utils import hash_password

setup_logging(debug=True)
TEST_DB_PATH = "./.test.db"


@fixture(scope="session")
def engine(worker_id) -> Engine:
    db_path = TEST_DB_PATH + str(worker_id)
    if os.path.exists(db_path):
        os.remove(db_path)

    engine = create_engine(db_path)

    yield engine

    if os.path.exists(db_path):
        os.remove(db_path)


@fixture()
def db(engine) -> DB:
    remove_db_and_tables(engine)
    create_db_and_tables(engine)

    return DB(engine)


@fixture()
def users(db, engine):
    with Session(engine) as session:
        users = [
            User(username="bob", password_hash=hash_password("bob")),
            User(username="alice", password_hash=hash_password("alice")),
        ]
        session.add_all(users)
        session.commit()

        for user in users:
            session.refresh(user)

    return users


@lru_cache
def get_app_cached():
    return get_app(debug=True)


TEST_ROOT = "/tmp/nix"


@fixture
def NixAPI() -> Iterator[Nix]:
    nix = Nix(stores_root=TEST_ROOT)
    store_name = "test_store"

    nix.add_store(store_name)
    command = [
        "nix",
        "copy",
        "--to",
        os.path.join(TEST_ROOT, store_name),
        "nixpkgs#glibc",
    ]
    subprocess.run(command)

    yield nix

    # Cleanup:
    # 1. Set permissions for deletion
    # 2. Delete tree
    for root, dirs, files in os.walk(TEST_ROOT):
        for momo in dirs:
            os.chmod(os.path.join(root, momo), 0o722)

    shutil.rmtree(TEST_ROOT)


@fixture
def NixAPI_empty() -> Iterator[Nix]:
    # Empty store (do not copy from cache)
    nix = Nix(stores_root=TEST_ROOT)

    yield nix

    for root, dirs, files in os.walk(TEST_ROOT):
        for momo in dirs:
            os.chmod(os.path.join(root, momo), 0o722)

    shutil.rmtree(TEST_ROOT)


@fixture()
def client(db, NixAPI_empty):
    app = get_app_cached()

    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_nix] = lambda: NixAPI_empty

    return TestClient(app)


def auth_user(client: TestClient, user: User) -> TestClient:
    response = client.post(
        "/auth/token",
        data={"username": user.username, "password": user.username},
    )
    assert response.status_code == 200

    data = response.json()
    access_token = data["access_token"]
    token_type = data["token_type"]

    client.headers = {"Authorization": f"{token_type} {access_token}"}
    return client


@fixture
def client1(users, client) -> TestClient:
    return auth_user(client, users[0])


@fixture
def client2(users, client) -> TestClient:
    return auth_user(client, users[1])
