#!/bin/bash

function pythonScieszka
{
  python3 -c "import sys; print(sys.executable)"
}

echo "HOME: $HOME"
Slideshow="$HOME""/slideshow"
echo "$Slideshow"
PythonEnv="$(pythonScieszka)"
echo "$PythonEnv"
pwd
#$@ - pomocny tylko przy debugu - przekazuje wszystkie argumenty podane przy wywolaniu basha - dalej do pythona
"$PythonEnv" "$Slideshow"/slideshow.py "$@"
