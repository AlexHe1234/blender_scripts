import bpy
import numpy as np
from mathutils import Matrix, Vector


def add_euler(e1, e2):
    quaternion_1 = e1.to_quaternion()
    quaternion_2 = e2.to_quaternion()

    combined_quaternion = quaternion_1 @ quaternion_2
    combined_euler = combined_quaternion.to_euler()
    
    return combined_euler


def add_animation(obj, rs, ts, fps=24):
    F = rs.shape[0]
    
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = F
    bpy.context.scene.render.fps = fps
    
    # use current position & rotation as first frame position
    pos_init = obj.location.copy()
    rot_init = obj.rotation_euler.copy()

    for frame in range(F):
        f = frame + 1
        bpy.context.scene.frame_set(f)
        
        obj.location = pos_init + Vector(ts[frame])
        obj.rotation_euler = add_euler(rot_init, Matrix(rs[frame]).to_euler())
        
        obj.keyframe_insert(data_path="location", index=-1)
        obj.keyframe_insert(data_path="rotation_euler", index=-1)
        
    bpy.context.scene.frame_set(0)


if __name__ == '__main__':
    objs = ['Cylinder', 'Cylinder.001', 'Cylinder.002', 'Cylinder.003', 'Plane', 'Sphere', 'Sphere.001']
    se3_path = '/Users/alexhe/Desktop/se3_000026.npy'
    
    se3 = np.load(se3_path, allow_pickle=True).item()
    rs = se3['R']  # F, 3, 3
    ts = se3['T']  # F, 3
    
    for obj in objs:
        obj_ = bpy.data.objects.get(obj) 
    
        add_animation(obj_, rs, ts)
