---
name: png-to-drawio
description: Convert PNG flowchart screenshots into editable .drawio files. Use when the user provides a PNG image of a flowchart, process diagram, or workflow diagram and wants it converted into an editable .drawio format for VS Code draw.io plugin. Triggers on phrases like "convert this flowchart", "turn this screenshot into drawio", "make this diagram editable", "PNG to drawio", or when the user shares a flowchart image and wants to edit it.
---

# PNG to Drawio Converter

Convert PNG flowchart screenshots into editable .drawio files using AI vision + Python script.

## Workflow

1. **Analyze the PNG**: Use vision to examine the flowchart image and identify all elements:
   - Nodes: shapes (rectangles, diamonds, rounded rectangles, circles/ovals), their text labels, approximate positions, and colors
   - Edges: connections between nodes, arrow directions, and any labels on the connections
   - Layout: overall flow direction (top-to-bottom or left-to-right)

2. **Output structured JSON** following this exact schema:

```json
{
  "direction": "TB",
  "nodes": [
    {
      "id": "1",
      "label": "Start",
      "shape": "ellipse",
      "x": 300,
      "y": 50,
      "width": 120,
      "height": 60,
      "fillColor": "#d5e8d4",
      "strokeColor": "#82b366"
    }
  ],
  "edges": [
    {
      "source": "1",
      "target": "2",
      "label": "",
      "style": ""
    }
  ]
}
```

### Shape mapping:
- Start/End (oval/rounded) → `"ellipse"`
- Process (rectangle) → `"rectangle"`
- Decision (diamond) → `"rhombus"`
- Rounded rectangle → `"rounded_rectangle"`
- Circle → `"ellipse"`
- Parallelogram (I/O) → `"parallelogram"`

### Color format:
- Use hex colors like `"#d5e8d4"`. If colors are unclear, use defaults:
  - Process: fillColor `"#dae8fc"`, strokeColor `"#6c8ebf"`
  - Decision: fillColor `"#fff2cc"`, strokeColor `"#d6b656"`
  - Start/End: fillColor `"#d5e8d4"`, strokeColor `"#82b366"`

### Position guidelines:
- Estimate x, y coordinates based on the image layout
- Typical spacing: 200px vertical gap for TB direction, 250px horizontal gap for LR
- Center the diagram starting around x=300

3. **Generate .drawio file**: Run the conversion script:

```bash
python "{baseDir}/scripts/generate_drawio.py" --input diagram.json --output diagram.drawio
```

Or pipe JSON directly:

```bash
echo '<json_string>' | python "{baseDir}/scripts/generate_drawio.py" --stdin --output diagram.drawio
```

4. **Deliver the .drawio file** to the user. Remind them to open it with the VS Code Draw.io Integration extension.

## Notes

- `{baseDir}` refers to the directory containing this SKILL.md
- The script requires Python 3.7+ with no external dependencies (uses only stdlib xml and json)
- Position accuracy is approximate — users can easily adjust in the drawio editor
- For complex diagrams with many nodes, process in sections if needed
