#!/bin/sh

cd "$(dirname "$0")"

# $1 -> config

if [ -z "$1" ]; then
    echo 'Provide the path to a yaml config!'
    echo "Example: $0 /path/to/config.yaml"
    exit 1
fi

if [ -z "$2" ]; then
    INTERACTIVE='true'
else
    INTERACTIVE=$2
fi

IMGNAME='sshake'
CFG_FILE=$(readlink -f "$1")

docker build -t $IMGNAME . > /dev/null 2>&1

if [ $INTERACTIVE = 'true' ]; then
    docker run -it --rm --network=host \
    -v "$CFG_FILE":"/usr/src/files/config.yml" \
    -v $(pwd)/ssh:/usr/src/ssh \
    $IMGNAME /usr/src/files/config.yml
else
    docker run --rm --network=host \
    -v "$CFG_FILE":"/usr/src/files/config.yml" \
    -v $(pwd)/ssh:/usr/src/ssh \
    $IMGNAME /usr/src/files/config.yml
fi


