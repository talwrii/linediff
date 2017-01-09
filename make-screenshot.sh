#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

mate-terminal --geometry 80x20 -e '/bin/bash -c "bash  make-cheat-sheet.sh; sleep 5;  scrot -u screenshot.png; echo "Took picture";u read"';
