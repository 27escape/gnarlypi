#!/usr/bin/env bash
# sync code to relevant rPi hosts

cd /Users/kevinmu/Repos/personal/python/gnarlypi

host=$1

if [ -z "$host" ] ; then
  echo "pass name of remote system, i.e $0 photos.local"
  exit 1
fi

echo "updating $host from $PWD"
rsync -ahviP  --progress --exclude="android_app" --exclude=".DS_store" --exclude="__pycache__" --exclude="node_modules" --delete --exclude=bin/start_displays.sh --exclude=gnarlypi.yml ./ "$host:/home/kevinmu/gnarlypi"
