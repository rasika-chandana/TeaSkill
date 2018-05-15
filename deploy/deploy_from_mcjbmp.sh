#!/usr/bin/env bash


REMOTE_HOST="parallels@10.211.55.3"
REMOTE_DIR="/opt/mycroft/skills/assist_mc_skill"

THIS_SCRIPT=$(realpath $0)
SOURCE_DIR=$(realpath $(dirname ${THIS_SCRIPT}))/../

git pull

echo "Copying from ${SOURCE_DIR} to ${REMOTE_HOST}:${REMOTE_DIR}"

rsync -rzo \
        --exclude=*.pyc \
        --exclude=migrations \
        --exclude=.* \
        ${SOURCE_DIR}/* -e ssh ${REMOTE_HOST}:${REMOTE_DIR}

echo "Done."
