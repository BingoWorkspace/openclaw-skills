#!/usr/bin/env python3
"""
Generate .drawio XML files from structured JSON descriptions of flowcharts.
No external dependencies - uses only Python stdlib.

Usage:
    python generate_drawio.py --input diagram.json --output diagram.drawio
    echo '{"nodes":[...],"edges":[...]}' | python generate_drawio.py --stdin --output diagram.drawio
"""

import json
import sys
import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom


def get_shape_style(shape, fill_color="#dae8fc", stroke_color="#6c8ebf"):
    """Map shape types to drawio style strings."""
    base = f"fillColor={fill_color};strokeColor={stroke_color};fontColor=#333333;fontSize=12;"

    styles = {
        "rectangle": f"rounded=0;whiteSpace=wrap;html=1;{base}",
        "rounded_rectangle": f"rounded=1;whiteSpace=wrap;html=1;arcSize=20;{base}",
        "ellipse": f"ellipse;whiteSpace=wrap;html=1;{base}",
        "rhombus": f"rhombus;whiteSpace=wrap;html=1;{base}",
        "diamond": f"rhombus;whiteSpace=wrap;html=1;{base}",
        "parallelogram": f"shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;{base}",
        "circle": f"ellipse;whiteSpace=wrap;html=1;aspect=fixed;{base}",
    }

    return styles.get(shape, styles["rectangle"])


def get_edge_style(style=""):
    """Get edge style string."""
    base = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666666;fontColor=#333333;fontSize=11;"
    if style:
        base += style
    return base


def build_drawio_xml(data):
    """Build the complete .drawio XML from structured data."""
    # Root element
    mxfile = ET.Element("mxfile", {
        "host": "app.diagrams.net",
        "modified": "2024-01-01T00:00:00.000Z",
        "agent": "png-to-drawio-skill",
        "version": "1.0",
        "type": "device"
    })

    diagram = ET.SubElement(mxfile, "diagram", {
        "id": "diagram-1",
        "name": "Page-1"
    })

    graph_model = ET.SubElement(diagram, "mxGraphModel", {
        "dx": "1422",
        "dy": "794",
        "grid": "1",
        "gridSize": "10",
        "guides": "1",
        "tooltips": "1",
        "connect": "1",
        "arrows": "1",
        "fold": "1",
        "page": "1",
        "pageScale": "1",
        "pageWidth": "1169",
        "pageHeight": "827",
        "math": "0",
        "shadow": "0"
    })

    root = ET.SubElement(graph_model, "root")

    # Required parent cells
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    # Track node IDs for edge creation
    cell_id = 2

    # Create nodes
    node_id_map = {}  # maps user-defined id to internal cell id
    nodes = data.get("nodes", [])

    for node in nodes:
        user_id = str(node.get("id", cell_id))
        label = node.get("label", "")
        shape = node.get("shape", "rectangle")
        x = node.get("x", 0)
        y = node.get("y", 0)
        width = node.get("width", 120)
        height = node.get("height", 60)
        fill_color = node.get("fillColor", "#dae8fc")
        stroke_color = node.get("strokeColor", "#6c8ebf")

        internal_id = str(cell_id)
        node_id_map[user_id] = internal_id

        style = get_shape_style(shape, fill_color, stroke_color)

        cell = ET.SubElement(root, "mxCell", {
            "id": internal_id,
            "value": label,
            "style": style,
            "vertex": "1",
            "parent": "1"
        })

        ET.SubElement(cell, "mxGeometry", {
            "x": str(x),
            "y": str(y),
            "width": str(width),
            "height": str(height),
            "as": "geometry"
        })

        cell_id += 1

    # Create edges
    edges = data.get("edges", [])

    for edge in edges:
        source_user_id = str(edge.get("source", ""))
        target_user_id = str(edge.get("target", ""))
        label = edge.get("label", "")
        extra_style = edge.get("style", "")

        source_id = node_id_map.get(source_user_id, source_user_id)
        target_id = node_id_map.get(target_user_id, target_user_id)

        style = get_edge_style(extra_style)

        internal_id = str(cell_id)

        cell = ET.SubElement(root, "mxCell", {
            "id": internal_id,
            "value": label,
            "style": style,
            "edge": "1",
            "parent": "1",
            "source": source_id,
            "target": target_id
        })

        ET.SubElement(cell, "mxGeometry", {
            "relative": "1",
            "as": "geometry"
        })

        cell_id += 1

    return mxfile


def prettify_xml(element):
    """Pretty print XML with proper indentation."""
    rough_string = ET.tostring(element, encoding="unicode")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding=None)


def main():
    parser = argparse.ArgumentParser(description="Generate .drawio files from JSON")
    parser.add_argument("--input", "-i", help="Input JSON file path")
    parser.add_argument("--stdin", action="store_true", help="Read JSON from stdin")
    parser.add_argument("--output", "-o", required=True, help="Output .drawio file path")

    args = parser.parse_args()

    # Read input
    if args.stdin:
        raw = sys.stdin.read()
    elif args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            raw = f.read()
    else:
        print("Error: Provide --input <file> or --stdin", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        sys.exit(1)

    # Build and write
    mxfile = build_drawio_xml(data)
    xml_string = prettify_xml(mxfile)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(xml_string)

    node_count = len(data.get("nodes", []))
    edge_count = len(data.get("edges", []))
    print(f"Done! Generated {args.output} ({node_count} nodes, {edge_count} edges)")


if __name__ == "__main__":
    main()
