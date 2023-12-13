#!/usr/bin/env python3
import os
import inkex
from lxml import etree as ET

class SensorLayoutExtension(inkex.EffectExtension):

    def load_sensor_element(self, sensor_type, file_path):
        print(f"Loading sensor element: {sensor_type}")
        tree = ET.parse(file_path)
        root = tree.getroot()

        ns = {
            'svg': 'http://www.w3.org/2000/svg',
            'inkscape': 'http://www.inkscape.org/namespaces/inkscape'
        }

        for element in root.findall('.//svg:g', ns):
            inkscape_label = '{' + ns['inkscape'] + '}label'
            if inkscape_label in element.attrib and element.attrib[inkscape_label] == sensor_type:
                print(f"Found sensor element: {sensor_type}")
                return element

        print(f"Sensor element not found: {sensor_type}")
        return None

    def add_arguments(self, pars):
        pars.add_argument("--height", type=float, default=100.0, help="Height in mm")
        pars.add_argument("--width", type=float, default=100.0, help="Width in mm")
        sensor_types = ["Brickstream", "INTENTA S1000", "INTENTA S2000"]
        pars.add_argument("--sensor_type", type=str, default="Brickstream", choices=sensor_types, help="Choose Sensor Type")

    def effect(self):
        sensor_type = self.options.sensor_type
        file_path = os.path.join(os.path.dirname(__file__), "Extension.SVG")
        print(f"File path: {file_path}")

        sensor_element = self.load_sensor_element(sensor_type, file_path)
        if sensor_element is None:
            inkex.errormsg(f"Sensor type '{sensor_type}' not found in the SVG file.")
            return

        width_mm = self.options.width
        height_mm = self.options.height
        self.apply_transformations(sensor_element, width_mm, height_mm)
        self.svg.get_current_layer().append(sensor_element)

    def apply_transformations(self, element, width_mm, height_mm):
        # Original dimensions in mm
        original_width_mm = 100.0
        original_height_mm = 100.0

        # Calculate scale factors
        scale_x = width_mm / original_width_mm
        scale_y = height_mm / original_height_mm

        # Retrieve existing transformation, if any
        existing_transform = inkex.transforms.Transform(element.get('transform'))

        # Multiply the new scale with the existing transform
        new_transform = existing_transform @ inkex.transforms.Transform().add_scale(scale_x, scale_y)

        # Apply the combined transformation
        element.set('transform', str(new_transform))



if __name__ == '__main__':
    SensorLayoutExtension().run()
