# import xml.etree.ElementTree as ET

# def determine_left_right(xml_file):
#     tree = ET.parse(xml_file)
#     root = tree.getroot()

#     limbmount_positions = {}
#     for body in root.findall(".//body"):
#         body_name = body.get("name")
#         pos_values = [float(val) for val in body.get("pos").split()]
#         limbmount_positions[body_name] = pos_values

#     # Assuming limbmounts are named limbmount1, limbmount2, limbmount3, limbmount4
#     left_limbmounts = ["limbmount2", "limbmount3"]
#     right_limbmounts = ["limbmount1", "limbmount4"]

#     return left_limbmounts, right_limbmounts

# def rotate_components_recursive(element, rotation_angle=180):
#     # Rotate the current element
#     current_euler = element.get("euler")
#     if current_euler:
#         euler_values = [float(val) for val in current_euler.split()]
#         # euler_values[2] += rotation_angle
#         euler_values[0] = -euler_values[0]
#         element.set("euler", " ".join(str(val) for val in euler_values))

#     # Recursively rotate descendants
#     for child in element:
#         rotate_components_recursive(child, rotation_angle)

# def rotate_components(xml_file, limbmounts, rotation_angle=180):
#     tree = ET.parse(xml_file)
#     root = tree.getroot()

#     for limbmount in limbmounts:
#         # Find the body associated with the limbmount
#         body = root.find(f".//body[@name='{limbmount}']")

#         # Rotate the body and its descendants recursively
#         rotate_components_recursive(body, rotation_angle)

#     # Save the modified XML to a new file or overwrite the existing one
#     tree.write("mjcf_model\\xmlrobot_1.xml")


# xml_file_path = "mjcf_model\\xmlrobot.xml"



# def rotate_conn_components(xml_file, limbmounts, rotation_angle=180):
#     tree = ET.parse(xml_file)
#     root = tree.getroot()

#     for limbmount in limbmounts:
#         # Find the body associated with the limbmount
#         body = root.find(f".//body[@name='{limbmount}']")
        
#         # Rotate only the direct children of limbmount
#         for child in body:
#             current_euler = child.get("euler")
#             if current_euler:
#                 euler_values = [float(val) for val in current_euler.split()]
#                 euler_values[2] += rotation_angle
#                 child.set("euler", " ".join(str(val) for val in euler_values))

#     # Save the modified XML to a new file or overwrite the existing one
#     tree.write("mjcf_model\\xmlrobot_1.xml")

# def rotate_direct_children_of_limb_mounts(xml_file, limbmounts, rotation_angle=180):
#     tree = ET.parse(xml_file)
#     root = tree.getroot()

#     for limbmount in limbmounts:
#         # Find the body associated with the limbmount
#         body = root.find(f".//body[@name='{limbmount}']")
        
#         # Rotate the euler angles of direct children of limb_mount's body
#         for child in body:
#             current_euler = child.get("euler")
#             if current_euler:
#                 euler_values = [float(val) for val in current_euler.split()]
#                 euler_values[2] += rotation_angle
#                 child.set("euler", " ".join(str(val) for val in euler_values))

#     # Save the modified XML to a new file or overwrite the existing one
#     tree.write("mjcf_model\\xmlrobot_1.xml")

# xml_file_path = "mjcf_model\\xmlrobot.xml"

# # Determine left and right limbmounts
# left_limbmounts, right_limbmounts = determine_left_right(xml_file_path)

# # Rotate components associated with left limbmounts
# # rotate_direct_children_of_limb_mounts(xml_file_path, left_limbmounts)

# # # Rotate components associated with right limbmounts
# # rotate_components(xml_file_path, right_limbmounts)

# # Now the modified XML file with recursively rotated components is saved as "modified_xml_file.xml"

# def trans_op():
#     left_limbmounts, right_limbmounts = determine_left_right(xml_file_path)

# # Rotate components associated with left limbmounts
#     rotate_direct_children_of_limb_mounts(xml_file_path, left_limbmounts)







########################################################################
import xml.etree.ElementTree as ET
import numpy as np
from scipy.spatial.transform import Rotation

def determine_left_right(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    limbmount_positions = {}
    for body in root.findall(".//body"):
        body_name = body.get("name")
        pos_values = [float(val) for val in body.get("pos").split()]
        limbmount_positions[body_name] = pos_values

    # Assuming limbmounts are named limbmount1, limbmount2, limbmount3, limbmount4
    left_limbmounts = ["limbmount2", "limbmount3"]
    right_limbmounts = ["limbmount1", "limbmount4"]

    return left_limbmounts, right_limbmounts

def rotate_components_recursive(element, rotation_angle_degrees=180):
    # Rotate the current element
    current_quaternion = element.get("quat")
    if current_quaternion:
        quat_values = [float(val) for val in current_quaternion.split()]
        # Convert quaternion to rotation matrix
        rotation_matrix = Rotation.from_quat(quat_values).as_matrix()
        
        # Rotate around the z-axis (third column in the rotation matrix)
        rotation_matrix = np.dot(rotation_matrix, Rotation.from_euler('z', rotation_angle_degrees, degrees=True).as_matrix())
        
        # Convert the rotated rotation matrix back to quaternion
        rotated_quaternion = Rotation.from_matrix(rotation_matrix).as_quat()
        
        element.set("quat", " ".join(str(val) for val in rotated_quaternion))

    # Recursively rotate descendants
    for child in element:
        rotate_components_recursive(child, rotation_angle_degrees)

def rotate_direct_children_of_limb_mounts(xml_file, limbmounts, rotation_angle_degrees=180, xml_out_path="mjcf_model\\xmlrobot_1.xml"):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for limbmount in limbmounts:
        # Find the body associated with the limbmount
        body = root.find(f".//body[@name='{limbmount}']")
        
        # Rotate the euler angles of direct children of limb_mount's body
        for child in body:
            current_quaternion = child.get("quat")
            if current_quaternion:
                quat_values = [float(val) for val in current_quaternion.split()]
                # Convert quaternion to rotation matrix
                rotation_matrix = Rotation.from_quat(quat_values).as_matrix()

                # Rotate around the z-axis (third column in the rotation matrix)
                rotation_matrix = np.dot(rotation_matrix, Rotation.from_euler('z', rotation_angle_degrees, degrees=True).as_matrix())

                # Convert the rotated rotation matrix back to quaternion
                rotated_quaternion = Rotation.from_matrix(rotation_matrix).as_quat()

                child.set("quat", " ".join(str(val) for val in rotated_quaternion))

    # Save the modified XML to a new file or overwrite the existing one
    tree.write(xml_out_path)



def trans_op(xml_file_path = "mjcf_model\\xmlrobot.xml", xml_out_path="mjcf_model\\xmlrobot_1.xml"):
    left_limbmounts, right_limbmounts = determine_left_right(xml_file_path)

# Rotate components associated with left limbmounts
    rotate_direct_children_of_limb_mounts(xml_file_path, left_limbmounts, rotation_angle_degrees=180, xml_out_path=xml_out_path)