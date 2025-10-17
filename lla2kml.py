# written with Anthropic Claude 4 Sonnet
"""
LLA to KML Converter
Converts LLA (Latitude, Longitude, Altitude) files to KML format for Google Earth visualization.
"""

import argparse
import os
import sys
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def read_lla_file(filepath):
    """
    Read LLA file and return list of coordinates.
    Expected format: lat, lon, alt (one point per line)
    Supports various delimiters: comma, space, tab
    """
    points = []
    
    try:
        with open(filepath, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Try different delimiters
                if ',' in line:
                    parts = line.split(',')
                elif '\t' in line:
                    parts = line.split('\t')
                else:
                    parts = line.split()
                
                # Clean up parts
                parts = [part.strip() for part in parts]
                
                if len(parts) < 2:
                    print(f"Warning: Line {line_num} has insufficient data: {line}")
                    continue
                
                try:
                    lat = float(parts[0])
                    lon = float(parts[1])
                    alt = float(parts[2]) if len(parts) > 2 else 0.0
                    
                    # Validate coordinates
                    if not (-90 <= lat <= 90):
                        print(f"Warning: Invalid latitude {lat} on line {line_num}")
                        continue
                    if not (-180 <= lon <= 180):
                        print(f"Warning: Invalid longitude {lon} on line {line_num}")
                        continue
                    
                    points.append((lat, lon, alt))
                    
                except ValueError as e:
                    print(f"Warning: Could not parse line {line_num}: {line} - {e}")
                    continue
                    
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    return points

def create_kml_document(points, name="LLA Data", description="Converted from LLA file"):
    """
    Create KML document from list of coordinate points.
    """
    # Create root KML element
    kml = Element('kml')
    kml.set('xmlns', 'http://www.opengis.net/kml/2.2')
    
    # Create document
    document = SubElement(kml, 'Document')
    
    # Add document info
    doc_name = SubElement(document, 'name')
    doc_name.text = name
    
    doc_description = SubElement(document, 'description')
    doc_description.text = f"{description}\nGenerated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nTotal points: {len(points)}"
    
    # Define styles
    create_styles(document)
    
    return kml, document

def create_styles(document):
    """
    Create KML styles for points and lines.
    """
    # Point style
    point_style = SubElement(document, 'Style')
    point_style.set('id', 'pointStyle')
    
    icon_style = SubElement(point_style, 'IconStyle')
    icon_scale = SubElement(icon_style, 'scale')
    icon_scale.text = '1'
    
    icon = SubElement(icon_style, 'Icon')
    href = SubElement(icon, 'href')
    href.text = 'http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png'
    
    # Line style
    line_style = SubElement(document, 'Style')
    line_style.set('id', 'lineStyle')
    
    line_style_elem = SubElement(line_style, 'LineStyle')
    color = SubElement(line_style_elem, 'color')
    color.text = 'ff0000ff'  # Red line
    width = SubElement(line_style_elem, 'width')
    width.text = '2'

def add_points_as_placemarks(document, points):
    """
    Add individual points as placemarks.
    """
    points_folder = SubElement(document, 'Folder')
    folder_name = SubElement(points_folder, 'name')
    folder_name.text = 'Points'
        
    for i, (lat, lon, alt) in enumerate(points):
        placemark = SubElement(points_folder, 'Placemark')
        
        name = SubElement(placemark, 'name')
        name.text = f'Point {i+1}'
        
        description = SubElement(placemark, 'description')
        description.text = f'Lat: {lat:.6f}, Lon: {lon:.6f}, Alt: {alt:.3f}m'
        
        style_url = SubElement(placemark, 'styleUrl')
        style_url.text = '#pointStyle'
        
        point = SubElement(placemark, 'Point')
        coordinates = SubElement(point, 'coordinates')
        coordinates.text = f'{lon},{lat},{alt}'

def add_path_as_linestring(document, points):
    """
    Add all points as a connected path (LineString).
    """
    if len(points) < 2:
        raise ValueError("Must have atleast 2 points to create a line.")
    
    placemark = SubElement(document, 'Placemark')
    
    name = SubElement(placemark, 'name')
    name.text = 'Path'
    
    description = SubElement(placemark, 'description')
    description.text = f'Path connecting {len(points)} points'
    
    style_url = SubElement(placemark, 'styleUrl')
    style_url.text = '#lineStyle'
    
    linestring = SubElement(placemark, 'LineString')
    tessellate = SubElement(linestring, 'tessellate')
    tessellate.text = '1'
    
    altitude_mode = SubElement(linestring, 'altitudeMode')
    altitude_mode.text = 'absolute'
    
    coordinates = SubElement(linestring, 'coordinates')
    coord_text = []
    for lat, lon, alt in points:
        coord_text.append(f'{lon},{lat},{alt}')
    coordinates.text = '\n'.join(coord_text)

def write_kml_file(kml, output_path):
    """
    Write KML to file with proper formatting.
    """
    # Convert to string and format
    rough_string = tostring(kml, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent="  ")[23:])  # Remove XML declaration
        print(f"KML file written successfully...")
    except Exception as e:
        print(f"Error writing KML file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Convert LLA (Latitude, Longitude, Altitude) files to KML format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
            \rExamples:
            \r\tpython {sys.argv[0]} input.txt
            \r\tpython {sys.argv[0]} input.txt -o output.kml
            \r\tpython {sys.argv[0]} input.txt --points
            \r\tpython {sys.argv[0]} input.txt --path
            
            \rLLA file format:
            \r\tEach line should contain: latitude, longitude, altitude
            \r\tSupported delimiters: comma, space, tab
            \rExample:
            \r\t37.7749, -122.4194, 10.5
            \r\t40.7128, -74.0060, 5.2
        """
    )
    
    parser.add_argument('input_file', help='Input LLA file path')
    parser.add_argument('-o', '--output', help='Output KML file path (default: input_file.kml)')
    parser.add_argument('-n','--name', default='LLA Data', help='Name for the KML document')
    parser.add_argument('-d','--description', help='Description for the KML document')
    parser.add_argument('-t','--type',choices=["points","path"],default="path",type=str,help="Choose what kind of KML object to make")
    parser.add_argument('--points', action='store_true', help='Create point placemarks')
    parser.add_argument('--path', action='store_true', help='Create path')
    
    args = parser.parse_args()
    
    
    # Read LLA file
    print(f"Reading LLA file: {args.input_file}")
    points = read_lla_file(args.input_file)
    
    if not points:
        print("Error: No valid points found in the input file")
        sys.exit(1)
    
    print(f"Successfully read {len(points)} points...")
    
    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        base_name = os.path.splitext(args.input_file)[0]
        output_file = f"{base_name}.kml"
    
    # Create KML document
    description = args.description or f"Converted from {args.input_file}"
    kml, document = create_kml_document(points, args.name, description)
    
    # Add content based on options
    match args.type:
        case "path":
            print("Adding path...")
            add_path_as_linestring(document, points)
        case "points":
            print("Adding individual points...")
            add_points_as_placemarks(document, points)
        
    
    # Write KML file
    write_kml_file(kml, output_file)
    print(f"Done...Generated: {output_file}")

if __name__ == "__main__":
    main()


