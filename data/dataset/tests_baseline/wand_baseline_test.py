import pytest
from data.dataset.baseline.wand_baseline import (
    Oak,
    Willow,
    Elder,
    PhoenixFeather,
    Ruby,
    Sapphire,
    Emerald,
    Wand,
    WandFactory,
)

def test_oak_phoenix_ruby_wand():
    factory = WandFactory()
    wand = factory.create_wand("oak_phoenix_ruby")

    assert isinstance(wand.wood, Oak)
    assert isinstance(wand.core, PhoenixFeather)
    assert isinstance(wand.gem, Ruby)

    expected_attack = 50 * (100 ** 1)  # 5000
    assert wand.attack == expected_attack

def test_willow_phoenix_sapphire_wand():
    factory = WandFactory()
    wand = factory.create_wand("willow_phoenix_sapphire")

    assert isinstance(wand.wood, Willow)
    assert isinstance(wand.core, PhoenixFeather)
    assert isinstance(wand.gem, Sapphire)

    expected_attack = 40 * (100 ** 1.25)  # ~12649.11064068
    assert abs(wand.attack - 12649.11064068) < 1e-6

def test_elder_phoenix_emerald_wand():
    factory = WandFactory()
    wand = factory.create_wand("elder_phoenix_emerald")

    assert isinstance(wand.wood, Elder)
    assert isinstance(wand.core, PhoenixFeather)
    assert isinstance(wand.gem, Emerald)

    expected_attack = 70 * (100 ** 1.5)  # 70000
    assert wand.attack == expected_attack

def test_invalid_wood():
    factory = WandFactory()
    with pytest.raises(ValueError):
        factory.create_wand("pine_phoenix_ruby")

def test_invalid_core():
    factory = WandFactory()
    with pytest.raises(ValueError):
        factory.create_wand("oak_dragon_ruby")

def test_invalid_gem():
    factory = WandFactory()
    with pytest.raises(ValueError):
        factory.create_wand("oak_phoenix_diamond")

