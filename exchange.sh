#!/bin/bash

set -e -u

VENV_PATH=./venv
EXCEL_PATH=./files

function CreateVenv() {
    python3 -m venv ${VENV_PATH}
    source venv/bin/activate

    pip3 install -q -r requirements.txt
}

function DeactivateVenv() {
    deactivate
}

function RunPython() {
    for value in $(python3 ./mnbrate.py $@); do
        echo ${value}
    done
}

CreateVenv
RunPython $@
DeactivateVenv