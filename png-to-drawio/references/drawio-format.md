# .drawio XML Format Reference

## File Structure

A .drawio file is XML with this hierarchy:
```
mxfile > diagram > mxGraphModel > root > mxCell(s)
```

## Node Shapes (mxCell style attribute)

| Flowchart Element | Shape Key | Style |
|---|---|---|
| Process | rectangle | `rounded=0;whiteSpace=wrap;html=1;` |
| Decision | rhombus | `rhombus;whiteSpace=wrap;html=1;` |
| Start/End | ellipse | `ellipse;whiteSpace=wrap;html=1;` |
| I/O | parallelogram | `shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;` |
| Rounded box | rounded_rectangle | `rounded=1;whiteSpace=wrap;html=1;arcSize=20;` |

## Color Properties

Added to style string:
- `fillColor=#hex` - Background fill
- `strokeColor=#hex` - Border color
- `fontColor=#hex` - Text color

## Common Default Colors

| Element | fillColor | strokeColor |
|---|---|---|
| Process | #dae8fc | #6c8ebf |
| Decision | #fff2cc | #d6b656 |
| Start/End | #d5e8d4 | #82b366 |
| Error/Stop | #f8cecc | #b85450 |
| Highlight | #e1d5e7 | #9673a6 |

## Edge Styles

Standard orthogonal edge:
```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;
```

## Geometry

Each mxCell with vertex="1" has an mxGeometry child:
```xml
<mxGeometry x="300" y="50" width="120" height="60" as="geometry" />
```

Edges use relative geometry:
```xml
<mxGeometry relative="1" as="geometry" />
```
