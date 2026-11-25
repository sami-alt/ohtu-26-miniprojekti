#!/bin/bash

echo "Running tests"

# Run DB setup script, if not ok, bail out with error message
if ! uv run python src/db_helper.py; then
  # 
  echo "DB setup failed" >&2
  exit 1
fi
echo "DB setup done"

# käynnistetään Flask-palvelin taustalle
uv run python3 src/index.py &

echo "started Flask server"


# Wait for Flask server to be ready
waited=0
until [[ "$(curl -s -o /dev/null --max-time 2 -w '%{http_code}' localhost:5001)" == "200" ]]; do
  if (( waited >= 20 )); then
    echo "Flask server was not ready within 20 seconds" >&2
    exit 1
  fi
  sleep 1
  waited=$((waited + 1))
done

echo "Flask server is ready"

# suoritetaan testit
uv run robot --variable HEADLESS:true src/story_tests

status=$?

# pysäytetään Flask-palvelin portissa 5001
kill $(lsof -t -i:5001)

exit $status
