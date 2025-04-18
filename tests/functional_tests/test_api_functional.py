import httpx
import pytest

BASE_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_health_check():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_list_makes_and_filter():
    async with httpx.AsyncClient() as client:
        # No filter
        response = await client.get(f"{BASE_URL}/makes")
        assert response.status_code == 200
        makes = response.json()
        assert isinstance(makes, list)
        if not makes:
            pytest.fail("No makes to filter")

        first_name = makes[0]["name"]
        # Filter with known name
        filtered = await client.get(f"{BASE_URL}/makes?name={first_name}")
        assert filtered.status_code == 200
        assert any(first_name.lower() in m["name"].lower() for m in filtered.json())

        # Pagination
        paginated = await client.get(f"{BASE_URL}/makes?limit=1&offset=0")
        assert paginated.status_code == 200
        assert isinstance(paginated.json(), list)
        assert len(paginated.json()) <= 1


@pytest.mark.asyncio
async def test_list_models_and_invalid_make():
    async with httpx.AsyncClient() as client:
        makes = (await client.get(f"{BASE_URL}/makes")).json()
        if not makes:
            pytest.fail("No makes found")
        make_id = makes[0]["id"]

        # Valid models
        models = (await client.get(f"{BASE_URL}/makes/{make_id}/models")).json()
        assert isinstance(models, list)

        # Filter by model name if exists
        if models:
            first_model = models[0]["name"]
            filtered = await client.get(f"{BASE_URL}/makes/{make_id}/models?name={first_model}")
            assert filtered.status_code == 200
            assert any(first_model.lower() in m["name"].lower() for m in filtered.json())

        # Invalid make
        resp = await client.get(f"{BASE_URL}/makes/999999/models")
        assert resp.status_code == 404


@pytest.mark.asyncio
async def test_list_parts_and_invalid_model():
    async with httpx.AsyncClient() as client:
        makes = (await client.get(f"{BASE_URL}/makes")).json()
        if not makes:
            pytest.fail("No makes found")
        models = (await client.get(f"{BASE_URL}/makes/{makes[0]['id']}/models")).json()
        if not models:
            pytest.fail("No models found")

        model_id = models[0]["id"]

        # Valid parts
        parts = (await client.get(f"{BASE_URL}/models/{model_id}/parts")).json()
        assert isinstance(parts, list)

        # Filter parts if any exist
        if parts:
            name = parts[0]["name"]
            filtered = await client.get(f"{BASE_URL}/models/{model_id}/parts?name={name}")
            assert filtered.status_code == 200
            assert any(name.lower() in p["name"].lower() for p in filtered.json())

        # Invalid model
        resp = await client.get(f"{BASE_URL}/models/999999/parts")
        assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_part_by_id_and_invalid():
    async with httpx.AsyncClient() as client:
        makes = (await client.get(f"{BASE_URL}/makes")).json()
        if not makes:
            pytest.fail("No makes found")
        models = (await client.get(f"{BASE_URL}/makes/{makes[0]['id']}/models")).json()
        if not models:
            pytest.fail("No models found")
        parts = (await client.get(f"{BASE_URL}/models/{models[0]['id']}/parts")).json()
        if not parts:
            pytest.fail("No parts found")

        part_id = parts[0]["id"]
        part_resp = await client.get(f"{BASE_URL}/parts/{part_id}")
        assert part_resp.status_code == 200
        assert part_resp.json()["id"] == part_id

        # Invalid part
        invalid = await client.get(f"{BASE_URL}/parts/999999")
        assert invalid.status_code == 404
