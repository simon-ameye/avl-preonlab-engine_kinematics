"""
Script written by Simon Ameye, AVL France, for RENAULT
This will create transform groups to help setting of engine kinematics
Just drag and drop to your PreonLab window !
Please contact simon.ameye@avl.com for help
For PreonLab V4.3.0

Parameters description : 

           __________
          |    |     |
               /  ^
         O    /  /
      ^   \  /  / b
     r \   \/  v
        v

         <---->
           d
"""

#User data
rotation_direction = 1 #[-] - direction of rotation
r = 0.0406 #[m] - crankshaft radius
b = 0.128 #[m] - connecting rod length
d = 30e-3 #[m] - cylinder offcet
vel = 4500 #[RPM] - rotation speed
initial_rotation = 89.6 #[deg] - initial rotation : Useful to set up multiple cylinder !

#Advanced data
nb_samples = 20 #[-] - nb of samples
loop_end_time = 10 #[s] - looping end time

#Import
import math
import preonpy

#Code
s = preonpy.current_scene
main = s.create_object("Transform group")
crank = s.create_object("Transform group")
rod = s.create_object("Transform group")
piston = s.create_object("Transform group")

main["name"] = "main"
crank["name"] = "crankshaft"
rod["name"] = "connecting_rod"
piston["name"] = "piston"

preonpy.connect_objects(main, crank, "Transform")
preonpy.connect_objects(main, rod, "Transform")
preonpy.connect_objects(main, piston, "Transform")

crank["orientation control mode"] = "revolutions_PerSecond"
crank["revolution axis"] = [0, 1, 0]
crank["revolutions per second"] = vel /60 * rotation_direction

piston["position"] = [d, 0, 0]

w = vel /60 * 2*math.pi
t_end = 1/(vel/60)

piston_z_keys = []
rod_x_keys = []
rod_z_keys = []
rod_theta_keys = []

initial_piston_z = r + math.sqrt(b**2 - (d)**2)

t = 0
while t <= t_end:
    theta = (w * t + + initial_rotation / 180 * math.pi) * rotation_direction
    
    piston_z = r*math.cos(theta) + math.sqrt(b**2 - (r*math.sin(theta) - d)**2)
    
    rod_big_end_x = r * math.sin(theta)
    rod_big_end_z = r * math.cos(theta)

    rod_small_end_x = d
    rod_small_end_z = piston_z

    rod_theta = math.atan((-rod_big_end_x + rod_small_end_x) / (-rod_big_end_z + rod_small_end_z))
    
    piston_z_keys = piston_z_keys + [(t, piston_z, "Linear")]
    rod_x_keys = rod_x_keys +  [(t, rod_big_end_x, "Linear")]
    rod_z_keys = rod_z_keys +  [(t, rod_big_end_z, "Linear")]
    rod_theta_keys = rod_theta_keys +  [(t, rod_theta * 180 / math.pi, "Linear")]

    t = t + (t_end / nb_samples)

piston.set_keyframes("position z", piston_z_keys)
rod.set_keyframes("position x", rod_x_keys)
rod.set_keyframes("position z", rod_z_keys)
rod.set_keyframes("euler angles theta", rod_theta_keys)

piston.set_loop_keyframes("position z",[(loop_end_time, nb_samples + 1)])
rod.set_loop_keyframes("position x",[(loop_end_time, nb_samples + 1)])
rod.set_loop_keyframes("position z",[(loop_end_time, nb_samples + 1)])
rod.set_loop_keyframes("euler angles theta",[(loop_end_time, nb_samples + 1)])

s.load_frame(0)

print("Done!")
