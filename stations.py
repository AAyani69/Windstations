from dataclasses import dataclass


@dataclass
class Station:
    name: str
    code: str
    source: str


STATIONS = [
    Station("La Espasa", "15969", "W"),
    Station("Llanes", "15921", "W"),
    Station("Fiochi", "1668", "W"),
    Station("RCM", "1669", "W"),
    Station("RCNL", "15438", "W"),
    Station("Punta Galea", "C042", "E"),
    Station("Escuela Vela", "5776", "W"),
    Station("Galindo", "C038", "E"),
]
