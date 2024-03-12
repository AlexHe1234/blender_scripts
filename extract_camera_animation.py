import bpy
import numpy as np
from mathutils import Matrix, Vector


def r2blender(r: np.ndarray):
    adjustment_mat = np.array([[1.,  0.,  0.],
                               [0., -1.,  0.], 
                               [0.,  0., -1.]])
    blender_camera_rotation = Matrix(r.T @ adjustment_mat).to_euler()
    return blender_camera_rotation


def blender_euler2opencv_r(euler):
    mat_raw = np.asarray(euler.to_matrix())
    adjustment_mat = np.array([[1.,  0.,  0.],
                               [0., -1.,  0.], 
                               [0.,  0., -1.]])
    r = (mat_raw @ adjustment_mat).T
    return r


# return opencv k, r, t matrices
def extract_camera_param():
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
    cam_euler = camera.rotation_euler
    r = blender_euler2opencv_r(cam_euler)
    
    # t
    cam_pose = camera.location
    t = -r @ cam_pose
    
    return k, r, t


def extract_camera_animation(frame_start: int,  # inclusive
                             frame_end: int,  # inclusive
                             ):
    ks = []
    rs = []
    ts = []
    for f in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(f)
        k, r, t = extract_camera_param()
        ks.append(k)
        rs.append(r)
        ts.append(t)
    
    ks = np.stack(ks)  # F, 3, 3
    rs = np.stack(rs)  # F, 3, 3
    ts = np.stack(ts)  # F, 3
    
    return ks, rs, ts


if __name__ == '__main__':
    ks, rs, ts = extract_camera_animation(1, 201)
    np.save('/Users/alexhe/Downloads/camera_animation.npy', {'k': ks, 'r': rs, 't': ts})
