#!/bin/bash

function pythonScieszka
{
  python -c "import sys; print(sys.executable)"
}

echo "HOME: $HOME"
Slideshow="$HOME""/Projects/czujnikSnapshot"
echo "$Slideshow"
PythonEnv="/home/matball/Projects/czujnikSnapshot/venv/bin/python"
echo "$PythonEnv"
pwd
#$@ - pomocny tylko przy debugu - przekazuje wszystkie argumenty podane przy wywolaniu basha - dalej do pythona
"$PythonEnv" "$Slideshow"/slideshow.py "$@"
