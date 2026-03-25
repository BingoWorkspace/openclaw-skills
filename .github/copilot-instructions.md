# Copilot Instructions - PNG to Drawio Converter

## When the user asks to convert a flowchart image to .drawio format:

### Step 1: Analyze the Image

Look at the PNG/image carefully and identify:
- All shapes (rectangles, diamonds, ovals, parallelograms, rounded rectangles)
- Text labels inside each shape
- Arrows/connections between shapes and their labels
- Approximate positions and layout direction (top-to-bottom or left-to-right)
- Colors of shapes (fill and border)

### Step 2: Output JSON

Generate a JSON object following this exact schema:

```json
{
  "direction": "TB",
  "nodes": [
    {
      "id": "1",
      "label": "Node Text",
      "shape": "rectangle",
      "x": 300,
      "y": 50,
      "width": 120,
      "height": 60,
      "fillColor": "#dae8fc",
      "strokeColor": "#6c8ebf"
    }
  ],
  "edges": [
    {
      "source": "1",
      "target": "2",
      "label": ""
    }
  ]
}
```

### Shape Mapping

| Flowchart Element | shape value |
|---|---|
| Process (rectangle) | `rectangle` |
| Decision (diamond) | `rhombus` |
| Start/End (oval) | `ellipse` |
| Input/Output (parallelogram) | `parallelogram` |
| Rounded box | `rounded_rectangle` |

### Default Colors

| Element | fillColor | strokeColor |
|---|---|---|
| Process | `#dae8fc` | `#6c8ebf` |
| Decision | `#fff2cc` | `#d6b656` |
| Start/End | `#d5e8d4` | `#82b366` |
| Error/Warning | `#f8cecc` | `#b85450` |
| Highlight | `#e1d5e7` | `#9673a6` |
| Neutral/Background | `#f5f5f5` | `#666666` |

### Position Guidelines

- Top-to-bottom (TB): increment y by ~120-150 per row
- Left-to-right (LR): increment x by ~200-250 per column
- Center the diagram starting around x=300
- Typical node size: width=120-160, height=50-70
- Decision diamonds: width=140, height=80

### Step 3: Generate .drawio File

Save the JSON to a file (e.g., `diagram.json`), then run:

```bash
python png-to-drawio/scripts/generate_drawio.py --input diagram.json --output diagram.drawio
```

Or pipe JSON directly:

```bash
echo '{ ... }' | python png-to-drawio/scripts/generate_drawio.py --stdin --output diagram.drawio
```

### Step 4: Inform the User

Tell the user to open the generated `.drawio` file with VS Code's **Draw.io Integration** extension to view and edit.

## Important Notes

- The script is at `png-to-drawio/scripts/generate_drawio.py`
- Requires Python 3.7+ with no external dependencies
- Position accuracy is approximate — users can adjust in the drawio editor
- Always use unique string IDs for each node
- Ensure every edge references valid source and target node IDs
