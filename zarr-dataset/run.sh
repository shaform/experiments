#!/bin/bash
./clean_anime_faces.sh
python convert_anime_faces.py
python test_anime_faces.py
