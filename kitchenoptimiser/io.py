"""Reading and writing data structures"""

from dataclasses import dataclass
import json
import networkx as nx


@dataclass
class Thing:
    """Dataclass for things that are kept in the kitchen"""
    name: str
    needs_socket: bool
    needs_surface: bool  # Should be placed on a surface
    width: float  # in cm
    depth: float  # in cm
    height: float  # height in cm
    is_solid: bool  # if True the thing must keep the dimensions given, like a box. If false the thing is 'liquid',
    # like spices
    visibility_need: float  # 0-1 indicating how visible this thing should be


@dataclass
class Place:
    """Dataclass for kitchen locations"""
    name: str
    height: float  # Height in cm
    width: float  # Width in cm
    depth: float  # Depth in cm
    sockets: int  # Number of sockets at this location
    is_surface: bool
    visibility: float  # 0-1 indicating how visible the contents of this space will be


def read_things(path) -> dict[str: Thing]:
    """Import things from file. Expects JSON format objects."""
    things = {}

    with open(path, 'r') as f:
        name_details_dict = json.load(f)

    for _, details in name_details_dict.items():
        things[details['name']] = Thing(name=details['name'],
                                        height=details['height'],
                                        depth=details['depth'],
                                        width=details['width'],
                                        needs_surface=details['needs_surface'],
                                        needs_socket=details['needs_socket'],
                                        is_solid=details['is_solid'],
                                        visibility_need=details['visibility_need']
                                        )
    return things


def read_locations(path) -> dict[str: Place]:
    locations = {}

    with open(path, 'r') as f:
        name_details_dict = json.load(f)

    for _, details in name_details_dict.items():
        locations[details['name']] = Place(name=details['name'],
                                           height=details['height'],
                                           depth=details['depth'],
                                           width=details['width'],
                                           is_surface=details['is_surface'],
                                           sockets=details['sockets'],
                                           visibility=details['visibility']
                                           )
    return locations


def read_layout(path) -> nx.Graph:
    with open(path, 'r') as f:
        layout = json.load(f)
        return nx.Graph(layout)


def read_process_details(path):
    """Read process details. Returns a dict with the format {process_name: {freq: float, process: Process}}
    freq is usually the number of times this process occurs in a normal week. A Process is an nx Graph between locations
    where the edge weights represent the probability of traversing that path."""
    with open(path, 'r') as f:
        process_details = json.load(f)

    parsed_details = {}

    for process_name, details in process_details.items():
        frequency = details['frequency']
        process = nx.Graph(details['process'])
        parsed_details[process_name] = {'frequency': frequency,
                                        'process': process}

    return parsed_details
