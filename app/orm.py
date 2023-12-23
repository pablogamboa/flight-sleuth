import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class Flight(Base):
    __tablename__ = "flights"
    date = mapped_column(sa.Date, primary_key=True)
    flight_number = mapped_column(sa.String, primary_key=True)
    aircraft_code = mapped_column(sa.String, nullable=False)
    aircraft_model = mapped_column(sa.String, nullable=False)
    origin = mapped_column(sa.String, nullable=False)
    destination = mapped_column(sa.String, nullable=False)
    updated_at = mapped_column(sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    data = mapped_column(sa.JSON, nullable=False)

    __table_args__ = (
        sa.Index("idx_flights_aircraft_code", aircraft_code),
        sa.Index("idx_flights_flight_number", flight_number),
        sa.Index("idx_flights_origin", origin),
        sa.Index("idx_flights_destination", destination),
    )
