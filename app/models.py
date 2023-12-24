from datetime import datetime

from pydantic import BaseModel, Field


class TimeDA(BaseModel):
    departure: datetime | None = None
    arrival: datetime | None = None


class TimeOther(BaseModel):
    eta: None | datetime
    updated: datetime


class TimeHistorical(BaseModel):
    flight_time: str = Field(..., alias="flighttime")
    delay: str


class Time(BaseModel):
    estimated: TimeDA
    scheduled: TimeDA
    real: TimeDA
    other: TimeOther
    historical: None | TimeHistorical


class Trail(BaseModel):
    lat: float
    lng: float
    alt: float
    spd: float
    hd: float
    ts: datetime


class AircraftNumber(BaseModel):
    default: None | str = None


class AircraftIdentification(BaseModel):
    id: str
    number: AircraftNumber


class AircraftRealTime(BaseModel):
    departure: datetime
    arrival: datetime | None = None


class AircraftTime(BaseModel):
    real: AircraftRealTime


class AirportCode(BaseModel):
    iata: str
    icao: str


class AirportCountry(BaseModel):
    id: int | None
    name: str
    code: str
    code_long: str | None = Field(None, alias="codeLong")


class AirportRegion(BaseModel):
    city: str


class AirportPosition(BaseModel):
    latitude: float
    longitude: float
    altitude: int
    country: AirportCountry
    region: AirportRegion


class AirportTimezone(BaseModel):
    name: str
    offset: int
    offset_hours: str = Field(..., alias="offsetHours")
    abbr: str
    abbr_name: str = Field(..., alias="abbrName")
    is_dst: bool = Field(..., alias="isDst")


class AirportInfo(BaseModel):
    terminal: str | None
    baggage: str | None
    gate: str | None


class BaseAirport(BaseModel):
    name: str
    code: AirportCode
    position: AirportPosition
    timezone: AirportTimezone
    visible: bool
    website: None | str


class AirportWithInfo(BaseAirport):
    info: AirportInfo | None


class FlightInfoAirport(BaseModel):
    origin: AirportWithInfo
    destination: None | AirportWithInfo = None


class AircraftAirport(BaseModel):
    origin: None | BaseAirport
    destination: None | BaseAirport


class FlightHistoryAircraft(BaseModel):
    identification: AircraftIdentification
    airport: AircraftAirport
    time: AircraftTime


class FlightHistory(BaseModel):
    aircraft: list[FlightHistoryAircraft]


class AirlineCode(BaseModel):
    iata: None | str
    icao: None | str


class Airline(BaseModel):
    name: str
    short: str | None = None
    code: None | AirlineCode
    url: None | str


class AircraftModel(BaseModel):
    code: str
    text: str


class AircraftImage(BaseModel):
    src: str
    link: str
    copyright: str
    source: str


class AircraftImages(BaseModel):
    thumbnails: list[AircraftImage]
    medium: list[AircraftImage]
    large: list[AircraftImage]


class Aircraft(BaseModel):
    model: AircraftModel
    country_id: int = Field(..., alias="countryId")
    registration: str
    age: str | None
    msn: str | None
    images: AircraftImages
    hex: str


class GenericStatus(BaseModel):
    text: str
    color: str
    type: str


class EventTimeStatus(BaseModel):
    utc: datetime
    local: datetime


class Generic(BaseModel):
    status: GenericStatus
    event_time: None | EventTimeStatus = Field(None, alias="eventTime")


class Status(BaseModel):
    live: bool
    text: str
    icon: None | str
    estimated: None | str
    ambiguous: bool
    generic: Generic


class IdentificationNumber(BaseModel):
    default: str | None
    alternative: str | None


class Identification(BaseModel):
    id: str
    row: None | int
    callsign: None | str
    number: IdentificationNumber


class FlightInfo(BaseModel):
    first_timestamp: datetime = Field(..., alias="firstTimestamp")
    s: str
    ems: str | None
    availability: list[str]
    time: Time
    trail: list[Trail]
    airport: FlightInfoAirport
    airline: Airline
    aircraft: Aircraft
    promote: bool
    level: str
    status: Status
    identification: Identification
    flight_history: FlightHistory = Field(..., alias="flightHistory")
    airspace: str | None
    owner: dict | None
