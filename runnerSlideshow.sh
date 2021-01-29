#!/bin/bash

Czujniki="$HOME""/Projects/czujnikSnapshot"
PythonEnv="$HOME""/Projects/czujnikSnapshot/venv/bin/python"
cd "$Czujniki"
pwd
"$PythonEnv" "$Czujniki"/slideshow.py
