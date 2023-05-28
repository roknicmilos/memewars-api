from dataclasses import dataclass


@dataclass
class GoogleUser:
    email: str
    given_name: str
    family_name: str
    picture: str
