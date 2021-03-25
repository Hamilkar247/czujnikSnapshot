#!/bin/bash

function pythonScieszka
{
  python -c "import sys; print(sys.executable)"
}

echo "HOME: $HOME"
echo "PROJECTS: $PROJECTS"
Slideshow="$PROJECTS/slideshow"
echo "$Slideshow"
PythonEnv="$Slideshow/venv/bin/python"
echo "$PythonEnv"
pwd
#$@ - pomocny tylko przy debugu - przekazuje wszystkie argumenty podane przy wywolaniu basha - dalej do pythona
"$PythonEnv" "$Slideshow"/slideshow.py "$@" -wd "$(pwd)"
