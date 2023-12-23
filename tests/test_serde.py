from app.models import FlightInfo


def get_fixture(name: str) -> str:
    with open(f"fixtures/{name}.json") as f:
        return f.read()


def test_rehydrate_detailed_flight_info():
    data = get_fixture("detailed_flight_info1")
    flight_info = FlightInfo.model_validate_json(data)

    assert flight_info.airport.origin.name == "Zurich Airport"
    assert flight_info.airport.destination.name == "Madrid Barajas Airport"
    assert flight_info.aircraft.model.code == "BCS3"
    assert flight_info.aircraft.model.text == "Airbus A220-300"

    assert flight_info.trail[0].lat == 41.5144
    assert flight_info.trail[0].lng == -1.203897
    assert flight_info.trail[0].alt == 36000
    assert flight_info.trail[0].spd == 480
