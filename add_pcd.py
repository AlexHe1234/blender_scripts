import bpy
import numpy as np


def add_point_cloud(points):
    mesh = bpy.data.meshes.new(name="Point Cloud")
    mesh.from_pydata(points, [], [])
    mesh.update()

    obj = bpy.data.objects.new("Point Cloud", mesh)

    bpy.context.collection.objects.link(obj)
    
    
if __name__ == '__main__':
    points_array = np.load("/Users/alexhe/Downloads/sport1_seq.npy")[0]

    add_point_cloud(points_array)
