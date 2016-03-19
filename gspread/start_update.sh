#!/usr/bin/env bash
curr_dir=`dirname "$BASH_SOURCE"`

cd $curr_dir ;
source my_env/bin/activate
python update.py
