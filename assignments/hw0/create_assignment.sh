#!/usr/bin/env bash

# Script to automate creation of assignments
# Usage: ./create_assignment <assignment_name>
# Example: ./create_assignment hw1

set -euo pipefail

ORG_NAME=ua-info521-sp25
SEMESTER=2025_spring
ASSIGNMENT=$1

pushd ~/git/ml4ai/INFO_521/$SEMESTER/$ASSIGNMENT > /dev/null
    ./make_release
popd > /dev/null


mkdir -p ~/git/$ORG_NAME/$ASSIGNMENT
pushd ~/git/$ORG_NAME/$ASSIGNMENT > /dev/null
    git init
    gh repo create $ORG_NAME/$ASSIGNMENT --private --source .
    cp -r ~/git/ml4ai/INFO_521/$SEMESTER/$ASSIGNMENT/release/* .
    git add .
    git commit -m "First commit"
    git push
popd > /dev/null
