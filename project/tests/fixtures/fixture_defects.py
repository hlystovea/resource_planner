import pytest


@pytest.fixture
def effect():
    from defects.models import Effect
    return Effect.objects.create(name='effect')


@pytest.fixture
def condition():
    from defects.models import Condition
    return Condition.objects.create(name='condition')


@pytest.fixture
def feature():
    from defects.models import Feature
    return Feature.objects.create(name='feature')


@pytest.fixture
def technical_reason():
    from defects.models import TechnicalReason
    return TechnicalReason.objects.create(name='technical_reason')


@pytest.fixture
def organizational_reason():
    from defects.models import OrganizationalReason
    return OrganizationalReason.objects.create(name='organizational_reason')


@pytest.fixture
def defect(part, user, effect, feature, condition):
    from defects.models import Defect
    defect = Defect(
        date='2000-01-01',
        part=part,
        employee=user,
        description='Описание дефекта',
        condition=condition
    )
    defect.save()
    defect.effects.set([effect])
    defect.features.set([feature])
    return defect
