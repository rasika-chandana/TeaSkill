#!/usr/bin/env bash

REMOTE_DIR="/opt/mycroft/skills/assist_mc_skill/"

THIS_SCRIPT=$(realpath $0)
SOURCE_DIR=$(realpath $(dirname ${THIS_SCRIPT}))/../

echo "Copying from ${SOURCE_DIR} to ${REMOTE_HOST}:${REMOTE_DIR}"

rsync -rzo \
        --exclude=*.pyc \
        --exclude=migrations \
        --exclude=.* \
        ${SOURCE_DIR}/* -e ${REMOTE_DIR}

echo "Done."
