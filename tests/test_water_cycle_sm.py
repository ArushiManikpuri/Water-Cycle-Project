import pytest
from water_cycle_SM import WaterCycleSM


@pytest.fixture
def sm():
    """Create a WaterCycleSM instance and start it in 'liquid' state."""
    machine = WaterCycleSM()
    machine.start()
    return machine


class TestInitialState:
    def test_initial_state_before_start(self):
        machine = WaterCycleSM()
        assert machine.state == "initial"

    def test_start_transitions_to_liquid(self):
        machine = WaterCycleSM()
        machine.start()
        assert machine.state == "liquid"


class TestHeatUpTransitions:
    def test_liquid_heat_up_goes_to_gaseous(self, sm):
        sm.heat_up()
        assert sm.state == "gaseous"

    def test_gaseous_heat_up_stays_gaseous(self, sm):
        sm.heat_up()  # liquid -> gaseous
        sm.heat_up()  # gaseous -> gaseous (=)
        assert sm.state == "gaseous"

    def test_solid_heat_up_goes_to_liquid(self, sm):
        sm.cool_down()  # liquid -> solid
        sm.heat_up()  # solid -> liquid
        assert sm.state == "liquid"


class TestCoolDownTransitions:
    def test_liquid_cool_down_goes_to_solid(self, sm):
        sm.cool_down()
        assert sm.state == "solid"

    def test_gaseous_cool_down_goes_to_liquid(self, sm):
        sm.heat_up()  # liquid -> gaseous
        sm.cool_down()  # gaseous -> liquid
        assert sm.state == "liquid"

    def test_solid_cool_down_stays_solid(self, sm):
        sm.cool_down()  # liquid -> solid
        sm.cool_down()  # solid -> solid (=)
        assert sm.state == "solid"


class TestFullCycleTransitions:
    def test_liquid_to_gaseous_to_liquid(self, sm):
        sm.heat_up()
        assert sm.state == "gaseous"
        sm.cool_down()
        assert sm.state == "liquid"

    def test_liquid_to_solid_to_liquid(self, sm):
        sm.cool_down()
        assert sm.state == "solid"
        sm.heat_up()
        assert sm.state == "liquid"

    def test_full_cycle(self, sm):
        assert sm.state == "liquid"
        sm.heat_up()
        assert sm.state == "gaseous"
        sm.cool_down()
        assert sm.state == "liquid"
        sm.cool_down()
        assert sm.state == "solid"
        sm.heat_up()
        assert sm.state == "liquid"


class TestCallbackMessages:
    def test_evaporate_returns_message(self, sm):
        assert sm.evaporate() == "Water is evaporating"

    def test_freeze_returns_message(self, sm):
        assert sm.freeze() == "Water is freezing"

    def test_melt_returns_message(self, sm):
        assert sm.melt() == "Ice is melting"

    def test_condense_returns_message(self, sm):
        assert sm.condense() == "Vapour is condensing"

    def test_remain_solid_returns_message(self, sm):
        assert sm.remain_solid() == "Ice is already at freezing point - cannot get any colder"

    def test_remain_gaseous_returns_message(self, sm):
        assert sm.remain_gaseous() == "Vapor is already at boiling point - cannot get any hotter"


class TestRepeatedTransitions:
    def test_multiple_heat_ups_from_gaseous(self, sm):
        sm.heat_up()  # liquid -> gaseous
        for _ in range(5):
            sm.heat_up()  # should stay gaseous
        assert sm.state == "gaseous"

    def test_multiple_cool_downs_from_solid(self, sm):
        sm.cool_down()  # liquid -> solid
        for _ in range(5):
            sm.cool_down()  # should stay solid
        assert sm.state == "solid"
