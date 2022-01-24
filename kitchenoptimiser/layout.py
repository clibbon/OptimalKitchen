from dataclasses import dataclass
import json


@dataclass
class Thing:
    """Dataclass for things that are kept in the kitchen"""
    name: str
    height: float  # 0-1 with 1 indicating a full units height
    size: float  # 0-1 with 1 indicating it takes up a full kitchen unit
    needs_socket: bool
    needs_surface: bool  # Should be placed on a surface
    desired_visibility: float  # 0-1 indicating how visible this thing should be


@dataclass
class Location:
    """Dataclass for kitchen locations"""
    name: str
    height: float  # Height in cm
    width: float  # Width in cm
    depth: float  # Depth in cm

    sockets: int  # Number of sockets at this location
    is_surface: bool
    visibility: float  # 0-1 indicating how visible the contents of this space will be


def read_things(path) -> list[Thing]:
    """Import things from file. Expects JSON format objects."""
    things = []
    pass


def read_locations(path) -> list[Location]:
    locations = []

    with open('example/locations.json', 'r') as f:
        name_details_dict = json.load(f)

    for _, details in name_details_dict.items():
        new_location = Location(name=details['name'],
                                height=details['height'],
                                depth=details['depth'],
                                width=details['width'],
                                is_surface=details['is_surface'],
                                sockets=details['sockets'],
                                visibility=details['visibility']
                                )
        locations.append(new_location)
    return locations