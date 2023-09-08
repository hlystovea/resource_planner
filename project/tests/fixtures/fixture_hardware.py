import pytest

from hardware.models import (Component, ComponentDesign,
                             ComponentFunction, ComponentRepairMethod,
                             Manufacturer)


@pytest.fixture
def facility():
    from hardware.models import Facility
    return Facility.objects.create(
        name='facility',
        abbreviation='f',
    )


@pytest.fixture
def connection(facility):
    from hardware.models import Connection
    return Connection.objects.create(
        name='connection',
        abbreviation='c',
        facility=facility,
    )


@pytest.fixture
def group():
    from hardware.models import Group
    return Group.objects.create(
        name='group',
    )


@pytest.fixture
def hardware(connection, group):
    from hardware.models import Hardware
    return Hardware.objects.create(
        name='hardware',
        inventory_number='007',
        connection=connection,
        group=group,
    )


@pytest.fixture
def manufacturer_1():
    return Manufacturer.objects.create(name='manufacturer_1')


@pytest.fixture
def manufacturer_2():
    return Manufacturer.objects.create(name='manufacturer_2')


@pytest.fixture
def function():
    return ComponentFunction.objects.create(name='function')


@pytest.fixture
def design():
    return ComponentDesign.objects.create(name='design', abbreviation='abb')


@pytest.fixture
def component_1(function, design, manufacturer_1):
    return Component.objects.create(
        name='component_1',
        function=function,
        design=design,
        manufacturer=manufacturer_1
    )


@pytest.fixture
def component_2(function, design, manufacturer_2):
    return Component.objects.create(
        name='component_2',
        function=function,
        design=design,
        manufacturer=manufacturer_2
    )


@pytest.fixture
def cabinet(hardware, manufacturer_1):
    from hardware.models import Cabinet
    return Cabinet.objects.create(
        name='cabinet',
        abbreviation='c',
        hardware=hardware,
        manufacturer=manufacturer_1,
        release_year=2000,
        launch_year=2000,
    )


@pytest.fixture
def part(cabinet, component_1):
    from hardware.models import Part
    return Part.objects.create(
        name='part',
        release_year=2000,
        launch_year=2000,
        cabinet=cabinet,
        component=component_1,
    )
