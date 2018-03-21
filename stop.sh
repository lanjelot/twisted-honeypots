#!/bin/bash

source $(dirname $0)/vars.sh

test -f "$TWISTED_PID" && kill $(< "$TWISTED_PID") && rm -f "$TWISTED_PID"
