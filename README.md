## Description
This is an annotation software modeled after the Echo-Dynamic dataset. The primary function of this software is to annotate targets within videos and export the annotation results in CSV format. The exported CSV file includes the following columns:
- `filename`: The name of the video file.
- `frame`: The frame number within the video.
- `x`: The x-coordinate of the target.
- `y`: The y-coordinate of the target.
## Requirements
- Python 3.7+
- PySide6 6.5.2
- qtvscodestyle 0.1.1
## Use
1. start main.py
2. select data directory
3. double click on the video file you want to open
4. click on the video to select the target
5. export the result to csv
