# TeeChart-for-Python
TeeChart charting plotting graphing library of controls for Python Tkinter and PyQt 

### Notes:

Tested in Windows with Python version 3.14

Usage:

```python
py test_teechart.py
```

This creates a simple chart:

<img alt="TeeChart for Python example pie chart" src="https://github.com/user-attachments/assets/cce821ab-21c9-4809-8789-0f72d05afd0b" />

##

## Python code: 

```python
from __future__ import annotations

import argparse
import struct
import sys

from teechart import TeeChart, TeeChartError


def main() -> int:
    parser = argparse.ArgumentParser(description="teechart.dll test")
    parser.add_argument("dll", nargs="?", default="teechart.dll", help="Optional TeeChart DLL path")
    args = parser.parse_args()

    try:
        chart = TeeChart(args.dll)
        chart.render(
            x=[],
            y=[2.5, 3.2, 2.8, 4.1],
            z=[],
            texts=["One", "Two", "Three", "Four"],
            output_type="modal",
            width=800,
            height=500,
            style="pie",
            title="TeeChart for Python",
            footer="",
            horiz=False,
            commander=False,
            opengl=False,
        )
        print("TeeChartRender correctly executed")

    except (FileNotFoundError, TeeChartError, OSError, TypeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

