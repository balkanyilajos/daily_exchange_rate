VENV_PATH=./venv

function createVenv() {
    python3 -m venv ${VENV_PATH}
    source venv/bin/activate

    pip3 install -q -r requirements.txt
}

function deactivateVenv() {
    deactivate
}

function cleanup() {
    if [ -d ${VENV_PATH} ]; then rm -rf ${VENV_PATH}; fi
}

function run() {
    python3 ./daily_exchange_rate.py 2023.06.06
}

createVenv
run
deactivateVenv
#cleanup