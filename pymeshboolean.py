
import pymesh
import numpy as np
import sys

def mesh_trans(mesh, x, y, z):
    return pymesh.form_mesh(mesh.vertices + [[x, y, z]], mesh.faces)

def mesh_scale(mesh, x, y, z):
    return pymesh.form_mesh(mesh.vertices * [[x, y, z]], mesh.faces)

def make_vertice_height_dict(mesh):
    height_to_vertices_dict = dict()

    for vertice in keycap.vertices:
        #print(vertice)
        height = vertice[2]
        #height = vertice[2]
        # if key not exist, add it
        if height not in height_to_vertices_dict.keys():
            height_to_vertices_dict[height]= []
        # append to key list
        height_to_vertices_dict[height].append(vertice)

    #print(y_to_vertices_dict)
    return height_to_vertices_dict

def get_max_dict_key_list(input_dict):
    keys = list(input_dict.keys())
    key_max = max(keys)
    return key_max
def get_min_dict_key_list(input_dict):
    keys = list(input_dict.keys())
    key_min = min(keys)
    return key_min

def planar_coords_from_points_list(input_list):
    planar_coords = []
    for point in input_list:
        #print(point)
        #print(point[0])# x
        #print(point[1])# y
        #print(point[2])# z
        coords = (point[0],point[1])
        #coords = (point[0],point[1])
        planar_coords.append(coords)
    return planar_coords

def center_of_planar_coords(coords_list):
    x,y=zip(*coords_list)
    center=(max(x)+min(x))/2., (max(y)+min(y))/2.
    return center

def center_mesh(mesh,debug=False):

    # get tallest vertices
    height_dict = make_vertice_height_dict(mesh)
    tallest_vertice_y = get_max_dict_key_list(height_dict)
    tallest_vertices = height_dict[tallest_vertice_y]
    lowest_vertice_y = get_min_dict_key_list(height_dict)
    lowest_vertices = height_dict[lowest_vertice_y]
    print("tallest",tallest_vertices)
    print("tallest len",len(tallest_vertices))
    print("lowest",lowest_vertices)
    planar_coords_tallest = planar_coords_from_points_list(tallest_vertices)
    planar_coords_lowest = planar_coords_from_points_list(lowest_vertices)
    print("tallest p",planar_coords_tallest)
    print("lowest p",planar_coords_lowest)
    planar_center_tallest = center_of_planar_coords(planar_coords_tallest)
    planar_center_lowest = center_of_planar_coords(planar_coords_lowest)
    print("tallest c",planar_center_tallest)
    print("lowest c",planar_center_lowest)






    moved_mesh = mesh_trans(mesh,-1*planar_center_tallest[0],0,-1*planar_center_tallest[1])

    if debug:
        
        # summon cube
        cube = pymesh.load_mesh("/local/cube.stl")
        # scale cube
        cube = mesh_scale(cube,0.025,0.025,0.025)
        # center cube
        cube = center_mesh(cube)
        # move cube to coord
        cube = mesh_trans(cube,planar_center_tallest[0],0,planar_center_tallest[1])
        
        # merge mesh together
        moved_mesh = pymesh.boolean(moved_mesh, cube,
                                operation="union",
                                engine="igl")

        # summon cube
        cube = pymesh.load_mesh("/local/cube.stl")
        # scale cube
        cube = mesh_scale(cube,0.045,0.045,0.045)
        # center cube
        cube = center_mesh(cube)
        
        # merge mesh together
        moved_mesh = pymesh.boolean(moved_mesh, cube,
                                operation="union",
                                engine="igl")

        export_cubes_mesh_at_vertices(planar_coords_lowest,mesh,moved_mesh)



    return moved_mesh


def get_z_depth_of_mesh(mesh):
    z_values = []
    for vertice in mesh.vertices:
        z_values.append(list(vertice)[2])
    z_max = max(z_values)
    z_min = min(z_values)
    return abs(z_max-z_min) 



def center_mesh_new(mesh):
    moved_mesh = mesh
    coords =[]
    for vertice in mesh.vertices:
        coords.append(list(vertice))
          
    x,y,z=zip(*coords)
    center=(max(x)+min(x))/2., (max(y)+min(y))/2., (max(z)+min(z))/2.
    #print("center of mesh is ",center)
    x_to_move = -1*center[0]
    y_to_move = -1*center[1]
    z_to_move = -1*center[2]
    moved_mesh = mesh_trans(mesh,x_to_move,y_to_move,z_to_move)

    return moved_mesh





def export_cubes_mesh_at_vertices(list_of_vertices,mesh,moved_mesh):
    print()
    output_mesh = mesh
    # for each vertice
    for coord in list_of_vertices:
        print(coord)
        # summon cube
        cube = pymesh.load_mesh("/local/cube.stl")
        # scale cube
        cube = mesh_scale(cube,0.025,0.025,0.025)
        # center cube
        cube = center_mesh(cube)
        # move cube to coord
        cube = mesh_trans(cube,coord[0],0,coord[1])
        # merge mesh together
        output_mesh = pymesh.boolean(output_mesh, cube,
                                operation="union",
                                engine="igl")
    # merge moved mesh together
    moved_mesh = mesh_trans(moved_mesh,0,1,0)
    output_mesh = pymesh.boolean(output_mesh, moved_mesh,
                            operation="union",
                            engine="igl")
    
    pymesh.save_mesh("/local/debug_cubes_vertices.obj", output_mesh)


print("getitn used to this keybaord")

import os
print(os.listdir("/local"))
# load model
keycap = pymesh.load_mesh("/local/keycap.stl")
font = pymesh.load_mesh("/local/font.stl")

# save obj versions
pymesh.save_mesh("/local/keycap.obj", keycap)
pymesh.save_mesh("/local/font.obj", font)
# load obj versions for easy debugging
keycap = pymesh.load_mesh("/local/keycap.obj")
font = pymesh.load_mesh("/local/font.obj")

# move keycap to 0,0,0
print("center keycap")
keycap = center_mesh_new(keycap)

print("font")

# TODO center take optional offset per font
# TODO calc offset automatically
font_x_offset = 0
font_y_offset = 0
font_scale = 12
font_carve_depth = 10
font_carve_depth = 30
# insert is smaller
font_insert_scale = font_scale#*0.9
#font = center_mesh(font,True)
#pymesh.save_mesh("/local/font_center.obj", font)
print("scale font")
# x,y is scale, z is thicccness

#insert scale seperate but same depth
font_insert = mesh_scale(font,font_insert_scale,font_insert_scale,font_carve_depth)

font = mesh_scale(font,font_scale,font_scale,font_carve_depth)
#insert scale seperate but same depth
#font_insert = mesh_scale(font,font_insert_scale,font_insert_scale,font_carve_depth)

# move to center
font = center_mesh_new(font)
# move by offset
# set to highest value that the difference is no longer cut out

# move font mesh to the surface of the keycap
print("finding surface of keycap")
z_offset_increment = 0.01
z_offset = 0
while True:
    # add to z offset
    z_offset+=z_offset_increment
    # make a copy with increment
    font_incremented = mesh_trans(font,0,0,z_offset)
    # check difference with the keycap
    intersection = pymesh.boolean(font_incremented, keycap,
                                operation="intersection",
                                engine="igl")
    #print("intersection",len(intersection.vertices),z_offset)
    meshes_touch = len(intersection.vertices)

    #pymesh.save_mesh("/local/intersection_"+str(z_offset)+".obj", intersection)
    # if nolonger is touching, break
    if not meshes_touch > 5:
        break


# move it down by height offset from new location

height_offset = z_offset
font_depth = get_z_depth_of_mesh(font)
print("font depth is ",font_depth)
# subtract the whole font depth from the depth, so whatever thiccness scale is is how cut in it goes
height_offset -= font_depth 
print("moving font into keycap = to its depth")
font = mesh_trans(font,0,0,height_offset)

# do difference carve
output_mesh = pymesh.boolean(keycap, font,
                                operation="difference",
                                engine="igl")



# uncomment to show both mesh's for debugging
#output_mesh = pymesh.boolean(keycap, font,
#                                operation="union",
#                                engine="igl")
"""

# uncomment to show both mesh's for debugging
cube = pymesh.load_mesh("/local/cube.stl")
output_mesh = pymesh.boolean(output_mesh, cube,
                                operation="union",
                                engine="igl")
"""


# save keycap
pymesh.save_mesh("/local/keycap_with_cutout.obj", output_mesh)
pymesh.save_mesh("/local/combined.obj", output_mesh)

# save font insert
pymesh.save_mesh("/local/font_insert.obj", font_insert)