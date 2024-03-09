import bpy
import numpy as np
from mathutils import Matrix
import math


def r2blender(r: np.ndarray):
    adjustment_mat = np.array([[1.,  0.,  0.],
                               [0., -1.,  0.], 
                               [0.,  0., -1.]])
    blender_camera_rotation = Matrix(r.T @ adjustment_mat).to_euler()
    return blender_camera_rotation


def set_camera(k, r, t, w, h):
    scene = bpy.context.scene
    camera = scene.camera
    
    camera.data.sensor_height = h
    camera.data.sensor_width = w
    
    scene.render.resolution_x = w
    scene.render.resolution_y = h
    scene.render.resolution_percentage = 100
    
    f = (k[0, 0] + k[1, 1]) / 2.
    camera.data.lens = f

    cam_pose = -r.T @ t
    camera.location = cam_pose
    
    camera.rotation_euler = r2blender(r)
    
    bpy.context.view_layer.update()


if __name__ == '__main__':
    a = np.load('/Users/alexhe/Desktop/annots.npy', allow_pickle=True).item()['cams'] 
    rs = np.load('/Users/alexhe/Downloads/nhr_sport1_rs.npy')
    ts = np.load('/Users/alexhe/Downloads/nhr_sport1_ts.npy')
    W, H = 1024, 768

    k = a['K'][0]
    r = rs[0]
    t = ts[0]
    
    set_camera(k, r, t, W, H)
