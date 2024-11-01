"""
This is a Python script for exporting a CSV of the instances produced by geometry nodes
in Blender, including their reference object name, position, rotation and scale. This
effectively exports what you see in the 'Spreadsheet' view in Blender.

To run this script in the in-built Python console of Blender, run:

```
import os
script = os.path.join(bpy.path.abspath("//"),"assets","get_geometry_node_stats.py")
exec(compile(open(script).read(), script, "exec"))
```

"""

import os

import bpy
import numpy as np

# User-defined parameters
csv_path = os.path.join(bpy.path.abspath("//"), "geometry_instances.csv") # output CSV path
object_name = "Plane" # name of object in Blender
geometry_nodes = ["GeometryNodes"] # list of geometry node names from the above object

# Check output file
if os.path.exists(csv_path):
    raise FileExistsError(f"Output file {csv_path} already exists, cancelling script.")

# Initialise objects from project
depsgraph = bpy.context.evaluated_depsgraph_get()
obj = bpy.data.objects[object_name]
evaluated_obj = obj.evaluated_get(depsgraph)

# Make the object and geometry nodes of interest visible in the viewport (note, this 
# script will not pick them up if either of these is set to 'hidden')
obj.hide_set(False) # Set 'hidden' to False (ie 'unhide')
for gn in geometry_nodes:
    obj.modifiers[gn].show_viewport = True # Make geometry node visible
depsgraph.update() 

# Write data to file
with open(csv_path, "w") as file:
    # Header
    fields = [
        "reference_object",
        "position_x", "position_y", "position_z",
        "rotation_x", "rotation_y", "rotation_z",
        "scale_x", "scale_y", "scale_z",
        "\n",
    ]
    file.write(",".join(fields))

    # Loop through each instance
    for i in depsgraph.object_instances:
        # If the element is an instance and is the child of the object of interest, include it
        if i.is_instance and i.parent==evaluated_obj:
            # Get the name of the reference object for the instance
            reference_object = i.object.name # if this doesn't look right, try `i.object.data.name`

            # Get info about the instance
            position = list(i.matrix_world.to_translation())
            rotation = list(i.matrix_world.to_euler())
            scale = list(i.matrix_world.to_scale())

            # Write results to csv
            info = ""
            for n in [reference_object]+position+rotation+scale:
                info += (str(n)+",")
            file.write(info[:-1])
            file.write("\n")

# Record success
print(f"Results written to {csv_path}")

"""
Note, to see what other parameters may be collected from each instance, run:
```
object_instances = iter(depsgraph.object_instances)
oi = next(object_instances)
while not oi.is_instance:
    oi = next(object_instances)
```
and then explore `oi`.
"""