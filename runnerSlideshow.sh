#!/bin/bash

echo "HOME: $HOME"
Slideshow="$HOME""/Projects/czujnikSnapshot"
echo "$Slideshow"
PythonEnv="$HOME""/Projects/czujnikSnapshot/venv/bin/python"
echo "$PythonEnv"
pwd
#$@ - pomocny tylko przy debugu - przekazuje wszystkie argumenty podane przy wywolaniu basha - dalej do pythona
"$PythonEnv" "$Slideshow"/slideshow.py "$@"
