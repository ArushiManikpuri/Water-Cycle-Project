import pytest
import app as flask_app_module


@pytest.fixture
def client():
    """Create a Flask test client with a fresh state for each test."""
    flask_app_module.app.config["TESTING"] = True
    flask_app_module.water_cycle = flask_app_module.WaterCycleSM()
    flask_app_module.water_cycle.start()
    flask_app_module.history.clear()
    with flask_app_module.app.test_client() as client:
        yield client


class TestIndexRoute:
    def test_index_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_index_returns_welcome_message(self, client):
        response = client.get("/")
        assert b"Welcome to the Water Cycle Project" in response.data


class TestStateRoute:
    def test_state_returns_200(self, client):
        response = client.get("/state")
        assert response.status_code == 200

    def test_initial_state_is_liquid(self, client):
        response = client.get("/state")
        assert response.data.decode() == "liquid"

    def test_state_after_heat_up(self, client):
        client.get("/heat_up")
        response = client.get("/state")
        assert response.data.decode() == "gaseous"

    def test_state_after_cool_down(self, client):
        client.get("/cool_down")
        response = client.get("/state")
        assert response.data.decode() == "solid"


class TestHeatUpRoute:
    def test_heat_up_returns_200(self, client):
        response = client.get("/heat_up")
        assert response.status_code == 200

    def test_heat_up_from_liquid(self, client):
        response = client.get("/heat_up")
        assert b"Temperature increased" in response.data
        assert b"gaseous" in response.data

    def test_heat_up_from_solid(self, client):
        client.get("/cool_down")  # liquid -> solid
        response = client.get("/heat_up")
        assert b"Temperature increased" in response.data
        assert b"liquid" in response.data

    def test_heat_up_from_gaseous_stays(self, client):
        client.get("/heat_up")  # liquid -> gaseous
        response = client.get("/heat_up")  # gaseous -> gaseous
        assert b"Temperature increased" in response.data
        assert b"gaseous" in response.data


class TestCoolDownRoute:
    def test_cool_down_returns_200(self, client):
        response = client.get("/cool_down")
        assert response.status_code == 200

    def test_cool_down_from_liquid(self, client):
        response = client.get("/cool_down")
        assert b"Temperature decreased" in response.data
        assert b"solid" in response.data

    def test_cool_down_from_gaseous(self, client):
        client.get("/heat_up")  # liquid -> gaseous
        response = client.get("/cool_down")
        assert b"Temperature decreased" in response.data
        assert b"liquid" in response.data

    def test_cool_down_from_solid_stays(self, client):
        client.get("/cool_down")  # liquid -> solid
        response = client.get("/cool_down")  # solid -> solid
        assert b"Temperature decreased" in response.data
        assert b"solid" in response.data


class TestHistoryRoute:
    def test_history_returns_200(self, client):
        response = client.get("/history")
        assert response.status_code == 200

    def test_empty_history(self, client):
        response = client.get("/history")
        assert response.data.decode() == ""

    def test_history_records_transitions(self, client):
        client.get("/heat_up")
        response = client.get("/history")
        assert b"State changed from" in response.data

    def test_history_limited_to_5_entries(self, client):
        for _ in range(3):
            client.get("/heat_up")
            client.get("/cool_down")
        response = client.get("/history")
        entries = response.data.decode().split("<br>")
        entries = [e for e in entries if e.strip()]
        assert len(entries) <= 5

    def test_history_preserves_order(self, client):
        client.get("/heat_up")  # liquid -> gaseous
        client.get("/cool_down")  # gaseous -> liquid
        response = client.get("/history")
        text = response.data.decode()
        first = text.index("liquid to gaseous")
        second = text.index("gaseous to liquid")
        assert first < second
