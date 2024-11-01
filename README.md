# Blender: Get Geometry Node Stats
This repo contains a Python script for exporting a CSV of the instances produced by geometry nodes in Blender, including 
their reference object name, position, rotation and scale, allowing you to do subsequent calculations of the generated
instances. This effectively exports what you see in the 'Spreadsheet' view in Blender.

To run this script in the in-built Python console of Blender, run:
```
import os
script = os.path.join(bpy.path.abspath("//"),"assets","get_geometry_node_stats.py")
exec(compile(open(script).read(), script, "exec"))
```
