from common.db import session_context
from common.models import CarMake, CarModel, CarPart


class CarDataPersister:
    async def save(self, data: dict[str, dict[str, list[str]]]):
        async with session_context() as session:
            for make_name, models in data.items():
                make = CarMake(name=make_name)
                session.add(make)
                await session.flush()

                for model_name, parts in models.items():
                    model = CarModel(name=model_name, make_id=make.id)
                    session.add(model)
                    await session.flush()

                    for part_name in parts:
                        part = CarPart(name=part_name, model_id=model.id)
                        session.add(part)

            await session.commit()