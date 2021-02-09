#!/bin/bash

echo "HOME: $HOME"
Slideshow="$HOME""/Projects/czujnikSnapshot"
echo "$Slideshow"
PythonEnv="$HOME""/Projects/czujnikSnapshot/venv/bin/python"
echo "$PythonEnv"
cd "$Slideshow"
pwd
"$PythonEnv" "$Slideshow"/slideshow.py
