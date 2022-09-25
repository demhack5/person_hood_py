#!/bin/bash
ROOT="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; cd .. ; pwd -P )"
mkdir $ROOT/demhack/state
python3 -m venv $ROOT/env
$ROOT/env/bin/python3 -m pip install -r $ROOT/requirements.txt
