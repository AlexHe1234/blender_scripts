import bpy
import numpy as np
from mathutils import Matrix, Vector


# return opencv k, r, t matrices
def extract_camera_param(camera_name: str):
    scene = bpy.context.scene
    camera = scene.camera
    
    # k
    focal = camera.data.lens
    W = camera.data.sensor_width
    H = camera.data.sensor_height
    
    k = np.zeros((3, 3))
    k[2, 2] = 1.
    k[0, 0] = k[1, 1] = focal
    k[0, 2] = W / 2.
    k[1, 2] = H / 2.
    
    # r
    
    
    # t
    cam_pose = camera.location
    
    return k, r, t


def extract_camera_animation(frame_start: int,  # inclusive
                             frame_end: int,  # inclusive
                             camera_name: str):
    ks = []
    rs = []
    ts = []
    for f in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(f)
        k, r, t = extract_camera_param(camera_name=camera_name)
        ks.append(k)
        rs.append(r)
        ts.append(t)
    
    ks = np.stack(ks)  # F, 3, 3
    rs = np.stack(rs)  # F, 3, 3
    ts = np.stack(ts)  # F, 3
    
    return ks, rs, ts
