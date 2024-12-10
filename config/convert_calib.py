
import yaml


def convert_camchain_to_euroc(input_file, output_file):
    # Load the camchain YAML
    with open(input_file, 'r') as f:
        camchain_data = yaml.safe_load(f)
    # Flatten the transformation matrix data
    T_c1_c2_data = [item for row in camchain_data["cam1"]["T_cn_cnm1"] for item in row]   

    # Extract and reformat the data
    euroc_data = {
        "File.version": "1.0",
        "Camera.type": "PinHole",
        # Camera 1 parameters
        "Camera1.fx": camchain_data["cam0"]["intrinsics"][0],
        "Camera1.fy": camchain_data["cam0"]["intrinsics"][1],
        "Camera1.cx": camchain_data["cam0"]["intrinsics"][2],
        "Camera1.cy": camchain_data["cam0"]["intrinsics"][3],
        "Camera1.k1": camchain_data["cam0"]["distortion_coeffs"][0],
        "Camera1.k2": camchain_data["cam0"]["distortion_coeffs"][1],
        "Camera1.p1": camchain_data["cam0"]["distortion_coeffs"][2],
        "Camera1.p2": camchain_data["cam0"]["distortion_coeffs"][3],
        # Camera 2 parameters
        "Camera2.fx": camchain_data["cam1"]["intrinsics"][0],
        "Camera2.fy": camchain_data["cam1"]["intrinsics"][1],
        "Camera2.cx": camchain_data["cam1"]["intrinsics"][2],
        "Camera2.cy": camchain_data["cam1"]["intrinsics"][3],
        "Camera2.k1": camchain_data["cam1"]["distortion_coeffs"][0],
        "Camera2.k2": camchain_data["cam1"]["distortion_coeffs"][1],
        "Camera2.p1": camchain_data["cam1"]["distortion_coeffs"][2],
        "Camera2.p2": camchain_data["cam1"]["distortion_coeffs"][3],
        "Camera.width": camchain_data["cam0"]["resolution"][0],
        "Camera.height": camchain_data["cam0"]["resolution"][1],
        "Camera.fps": 20,  # Assuming default FPS; update if needed
        "Camera.RGB": 1,  # Assuming RGB; update if needed
        "Stereo.ThDepth": 60.0,  # Assuming default value; update if needed
        "Stereo.T_c1_c2": {
            "rows": 4,
            "cols": 4,
            "dt": "f",
            "data": T_c1_c2_data
        },
        "ORBextractor.nFeatures": 1200,
        "ORBextractor.scaleFactor": 1.2,
        "ORBextractor.nLevels": 8,
        "ORBextractor.iniThFAST": 20, 
        "ORBextractor.minThFAST": 7, 
        "Viewer.KeyFrameSize": 0.05, 
        "Viewer.KeyFrameSize": 0.05,
        "Viewer.KeyFrameLineWidth": 1.0,
        "Viewer.GraphLineWidth": 0.9,
        "Viewer.PointSize": 2.0,
        "Viewer.CameraSize": 0.08,
        "Viewer.CameraLineWidth": 3.0,
        "Viewer.ViewpointX": 0.0,
        "Viewer.ViewpointY": -0.7,
        "Viewer.ViewpointZ": -1.8,
        "Viewer.ViewpointF": 500.0,
        "Viewer.imageViewScale": 1.0,


    }

    # Custom dumping function for inline lists
    class InlineListDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):
            return super(InlineListDumper, self).increase_indent(flow=True)

    # Save to the EuRoC format YAML
    with open(output_file, 'w') as f:
        f.write("%YAML:1.0\n")
        yaml.dump(euroc_data, f, Dumper=InlineListDumper, default_flow_style=None)
    
    print(f"Converted file saved to {output_file}")

# Use the function
input_yaml = "close-camchain.yaml"
output_yaml = "camchain_home.yaml"
convert_camchain_to_euroc(input_yaml, output_yaml)
