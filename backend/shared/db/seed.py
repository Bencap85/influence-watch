import json
import logging
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from shared.db.entity.flag import Flag
from shared.db.session import SessionLocal
from shared.db.entity.source import Source

logger = logging.getLogger(__name__)

def load_sources():

    SOURCE_DATA_PATH = "shared/db/sources/sources.json"

    with SessionLocal() as db:
        try:
            with open(SOURCE_DATA_PATH) as f:
                data = json.load(f)

                for src in data["sources"]:
                    stmt = insert(Source).values(
                        name=src["name"],
                        base_url=src["url"],
                        country_code=src["country_code"],
                        is_state_affiliated=src["is_state_affiliated"]
                    ).on_conflict_do_nothing()

                    db.execute(stmt)

                db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

def data_load_completed() -> bool:
    with SessionLocal() as db:
        try:
            stmt = select(Flag.completed).where(Flag.name == "initial_data_load")
            result = db.execute(stmt).scalar()

            return bool(result)

        finally:
            db.close()

def mark_data_load_completed():
    with SessionLocal() as db:
        try:
            stmt = insert(Flag).values(
                name="initial_data_load",
                completed=True
            ).on_conflict_do_update(
                index_elements=[Flag.name],
                set_={"completed": True}
            )

            db.execute(stmt)
            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


def main():
    if data_load_completed():
        logger.info("Countries and sources previously loaded. Skipping...")
        return

    logger.info("Loading sources...")
    load_sources()

    mark_data_load_completed()

if __name__ == "__main__":
    main()
