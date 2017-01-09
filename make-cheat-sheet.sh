#!/bin/bash
set -o errexit

function echo_run {
    echo "\$ $1"
    eval "$1"
}
echo_run "echo -e \"melts\\nmember\\nmembers\\nmembership\\nmemberships\\nmembrane\" | linediff"
