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
    python3 ./src/daily_exchange_rate.py $@
}

CreateVenv
RunPython $@
DeactivateVenv
#Cleanup