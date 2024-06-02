#!/bin/bash

set -e -u

VENV_PATH=./venv
SRC_PATH=./src

function CreateVenv() {
    python3 -m venv ${VENV_PATH}
    source venv/bin/activate

    pip3 install -q -r requirements.txt
}

function DeactivateVenv() {
    deactivate
}

function Cleanup() {
    if [ -d ${VENV_PATH} ]; then rm -rf ${VENV_PATH}; fi
}

function RunPython() {
    for value in $(python3 ./src/daily_exchange_rate.py $@); do
        echo $value
    done
}

function CheckArgs() {
    if [ "$#" -lt 1 ]; then
        echo "ERROR: No currency provided."
        echo "Usage: $0 <currency> [<file> | <date> ...]"
        exit 1
    fi

    if [ $# -lt 2 ]; then
        echo "ERROR: No files or dates provided."
        echo "Usage: $0 <currency> [<file> | <date> ...]"
        exit 1
    fi
}

CheckArgs $@
CreateVenv
RunPython $@
DeactivateVenv
#Cleanup