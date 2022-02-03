# Optimise your Kitchen
In a needlessly complex way. This project aims to provide an optimal arrangement for your kitchen, based on provided information about the layout, the things you wish to store, and the 'user journeys' you make. An example (for my own kitchen) is provided in the "example" folder, as well as optimise.ipynb which demonstrates how I set up my own kitchen.

The process is basically:
1. Define *Things*, objects you wish to store and use. These can be of a fixed shape, like a Magimix, or just take up a surface area like spices in little jars. Things also include more abstract concepts, like prep space.
2. Define *Places*, these are locations in the kitchen things can live, and also have properties like visibility, number of sockets.
3. Define fixed locations. This is a good way to handle special cases like the Oven, Hobs, Fridge, and Sink. It's not likely you'd want to store something in the oven. These don't need to be fully fledged Things or Places, a dictionary of string is sufficient.
4. Define *Processes*, journeys you go on in your kitchen. For example this could be making a cup of tea which would look like: Teabags -> Mugs -> Kettle -> Fridge (milk) -> Sink. Processes are defined as graphs, so you can use edge weights to handle the fact sometimes you may want to use a fancy mug.
5. Define *Process Frequencies*, basically how often each journey is conducted. This is used to upweight important journeys. The easiest way to do this is set the weight to the number of times a week you perform a process (can be fractions for rare things!).
6. Set up the optimiser.
7. Optimise!