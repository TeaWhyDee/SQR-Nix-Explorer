from http import HTTPStatus


def test_access(client):
    resp = client.post("/store", params={"store_name": "aboba"})
    assert resp.status_code == HTTPStatus.UNAUTHORIZED


def test_store_itself(client1):
    resp = client1.post("/store", params={"store_name": "aboba"})
    assert resp.status_code == HTTPStatus.CREATED

    resp = client1.post("/store", params={"store_name": "aboba"})
    assert resp.status_code == HTTPStatus.BAD_REQUEST

    resp = client1.delete("/store", params={"store_name": "aboba"})
    assert resp.status_code == HTTPStatus.NO_CONTENT

    resp = client1.delete("/store", params={"store_name": "aboba"})
    assert resp.status_code == HTTPStatus.BAD_REQUEST

    resp = client1.post("/store", params={"store_name": "aboba"})
    assert resp.status_code == HTTPStatus.CREATED

    resp = client1.delete("/store", params={"store_name": "aboba"})
    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_package_crud(client1):
    PACKAGE = "nixpkgs#glibc"

    resp = client1.post(
        "/store/package", params={"store_name": "aboba", "package_name": PACKAGE}
    )
    assert resp.status_code == HTTPStatus.BAD_REQUEST

    resp = client1.post("/store", params={"store_name": "aboba"})
    assert resp.status_code == HTTPStatus.CREATED

    resp = client1.get(
        "/store/check_package_exists",
        params={"store_name": "aboba", "package_name": PACKAGE},
    )
    assert resp.json() is False

    resp = client1.post(
        "/store/package", params={"store_name": "aboba", "package_name": PACKAGE}
    )
    assert resp.status_code == HTTPStatus.CREATED

    resp = client1.post(
        "/store/package", params={"store_name": "aboba", "package_name": "aboba"}
    )
    assert resp.status_code == HTTPStatus.BAD_REQUEST

    resp = client1.get(
        "/store/check_package_exists",
        params={"store_name": "aboba", "package_name": "aboba"},
    )
    assert resp.json() is False

    resp = client1.get(
        "/store/check_package_exists",
        params={"store_name": "aboba", "package_name": PACKAGE},
    )
    assert resp.json() is True
