#!/bin/bash

echo "HOME: $HOME"
Slideshow="$HOME""/Projects/czujnikSnapshot"
echo "$Slideshow"
PythonEnv="$HOME""/Projects/czujnikSnapshot/venv/bin/python"
echo "$PythonEnv"
pwd
"$PythonEnv" "$Slideshow"/slideshow.py
