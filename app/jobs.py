import datetime
import logging

from FlightRadar24 import FlightRadar24API
from models import FlightInfo
from orm import Base, Flight
from settings import settings
from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session
from utils import utcnow


logger = logging.getLogger(__name__)


def setup_engine():
    engine = create_engine("sqlite:////data/test.db")
    Base.metadata.create_all(engine)
    return engine


def process_flight(fr_api, flight, session):
    logger.info("processing flight %r", flight)
    data = fr_api.get_flight_details(flight)
    try:
        flight_info = FlightInfo(**data)
    except TypeError:
        logger.exception("could not parse flight info: %r", data)
        return

    stmt = insert(Flight).values(
        date=datetime.date.today(),
        flight_number=flight_info.identification.number.default,
        aircraft_code=flight_info.aircraft.model.code,
        aircraft_model=flight_info.aircraft.model.text,
        origin=flight_info.airport.origin.code.iata,
        destination=flight_info.airport.destination.code.iata,
        data=data,
    )
    do_update_stmt = stmt.on_conflict_do_update(
        index_elements=[Flight.date, Flight.flight_number],
        set_={"data": data, "updated_at": utcnow()},
    )
    session.execute(do_update_stmt)


def check_flights():
    engine = setup_engine()
    fr_api = FlightRadar24API()
    flights = fr_api.get_flights(bounds=settings.bounds, details=True)
    logger.info("these are the flights: %r", flights)
    with Session(engine) as session:
        for flight in flights:
            process_flight(fr_api, flight, session)
        session.commit()
