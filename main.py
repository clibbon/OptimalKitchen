import json

from kitchenoptimiser import io
from kitchenoptimiser.utils import draw_layout, draw_process, parse

things = io.read_things(r'example\things.json')
places = io.read_locations(r'example\locations.json')
layout = io.read_layout(r'example\layout.json')
process_details = io.read_process_details(r'example\process_details2.json')


print(process_details['cup_of_tea']['process'].edges(data=True))
draw_process(process_details['cup_of_tea']['process'])
