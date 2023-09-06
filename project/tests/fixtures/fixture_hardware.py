import pytest

from hardware.models import (Component, ComponentDesign,
                             ComponentFunction, ComponentRepairMethod,
                             Manufacturer)


@pytest.fixture
def manufacturer():
    return Manufacturer.objects.create(name='manufacturer')


@pytest.fixture
def function():
    return ComponentFunction.objects.create(name='function')


@pytest.fixture
def design():
    return ComponentDesign.objects.create(name='design', abbreviation='abb')


@pytest.fixture
def repair_method():
    return ComponentRepairMethod.objects.create(name='repair_method')


@pytest.fixture
def component(function, design, manufacturer, repair_method):
    return Component.objects.create(
        name='component',
        function=function,
        design=design,
        manufacturer=manufacturer,
        repair_method=repair_method
    )
