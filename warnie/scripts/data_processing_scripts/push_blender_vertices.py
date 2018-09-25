import bpy
import random

#bpy.ops.object.editmode_toggle()
ob = bpy.data.objects["Sphere"]
ob_verts = ob.data.vertices
rp = 0.25
rn = -0.05
vertice_idxs = list(range(len(ob_verts)))
random.shuffle(vertice_idxs)
trim = int(len(vertice_idxs)*0.1)

for count, i in enumerate(vertice_idxs[:trim]):
    
    if count%4 == 0:
        ob_verts[i].co += rp * ob_verts[i].normal
        
    elif count%3 == 0:
        ob_verts[i].co += rn * ob_verts[i].normal
