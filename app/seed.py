import asyncio

from core.database import db_helper
from models import Building, Organization, OrganizationPhone, Activity


async def seed():
    async with db_helper.session_factory() as session:
        building1 = Building(
            address='ул. Блюхера, 32/1',
            latitude=55.7522,
            longitude=37.6156
        )

        building2 = Building(
            address='г. Ростов-на-Дону, ул. Ленина 1, офис 3',
            latitude=55.7600,
            longitude=37.6200
        )

        session.add_all([building1, building2])
        await session.flush()

        root_service1 = Activity(name='Еда')
        meat_product = Activity(name='Мясная продукция', parent=root_service1)
        dairy_product = Activity(name='Молочная продукция', parent=root_service1)

        root_service2 = Activity(name='Автомобили')
        freight = Activity(name='Грузовые', parent=root_service2)

        session.add_all([
            root_service1,
            meat_product, dairy_product,
            root_service2,
            freight
        ])
        await session.flush()

        org1 = Organization(
            name='ООО “Рога и Копыта”',
            building_id=building1.id,
            activities=[meat_product, dairy_product],
            phones=[
                OrganizationPhone(phone_number='2-222-222'),
                OrganizationPhone(phone_number='3-333-333'),
                OrganizationPhone(phone_number='8-923-666-13-13')
            ]
        )

        org2 = Organization(
            name='Сервис 24',
            building_id=building2.id,
            activities=[freight],
            phones=[
                OrganizationPhone(phone_number='+7 900 333-33-33'),
            ]
        )

        session.add_all([org1, org2])

        await session.commit()

    print('База успешно заполнена тестовыми данными!')


if __name__ == "__main__":
    asyncio.run(seed())
