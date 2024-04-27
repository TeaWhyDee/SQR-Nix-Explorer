import httpx
from typing import List
from services.kv_store import KvStore
from services.nix_api import NixAPI

_TOKEN_KEY = "token"


class RestNixApi(NixAPI):
    def __init__(self, base_url: str, kv_store: KvStore) -> None:
        self.kv_store = kv_store
        self.client = httpx.AsyncClient(base_url=base_url)
        token = self.kv_store.get(_TOKEN_KEY)
        if token != "":
            self.client.headers = {"Authorization": f"Bearer {token}"}

    async def register(self, username: str, password: str):
        response = await self.client.post(
            "/auth/register", json={"username": username, "password": password}
        )
        response.raise_for_status()
        await self.login(username, password)

    async def login(self, username: str, password: str):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"username": username, "password": password}
        response = await self.client.post("/auth/token", data=data, headers=headers)
        response.raise_for_status()
        token = response.json()["access_token"]
        self.kv_store.set(_TOKEN_KEY, token)
        self.client.headers = {"Authorization": f"Bearer {token}"}

    async def is_logged_in(self) -> bool:
        return "Authorization" in self.client.headers

    async def add_store(self, name: str):
        response = await self.client.post(f"/store?store_name={name}")
        response.raise_for_status()

    async def rm_store(self, name: str):
        response = await self.client.delete(f"/store?store_name={name}")
        response.raise_for_status()

    async def stores(self) -> List[str]:
        response = await self.client.get("/store")
        response.raise_for_status()
        return map(lambda s: s["name"], response.json())

    async def add_package(self, store: str, name: str):
        response = await self.client.post(
            f"/store/package?store_name={store}&package_name={name}"
        )
        response.raise_for_status()

    async def rm_package(self, store: str, package: str):
        response = await self.client.delete(
            f"/store/package?store_name={store}&package_name={package}"
        )
        response.raise_for_status()

    async def packages(self, store: str) -> List[str]:
        response = await self.client.get(f"/store/package?store_name={store}")
        response.raise_for_status()
        return response.json()

    async def closure_size(self, store: str, package: str) -> int:
        response = await self.client.get(
            f"/store/get_package_closure_size?store_name={store}&package={package}",
        )
        response.raise_for_status()
        return response.json()

    async def difference_paths(self, store1: str, store2: str) -> List[str]:
        response = await self.client.get(
            f"/store/get_difference_paths?store_name1={store1}&store_name2={store2}",
        )
        response.raise_for_status()
        return response.json()

    async def difference_closures(
        self, store1: str, package1: str, store2: str, package2: str
    ) -> List[str]:
        response = await self.client.get(
            f"/store/get_difference_package_closures?store_name1={store1}&package1={package1}&store_name2={store2}&package2={package2}",
        )
        response.raise_for_status()
        return response.json()
