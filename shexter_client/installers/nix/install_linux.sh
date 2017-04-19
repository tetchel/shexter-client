#!/bin/sh

#short script to 'install' shexter
#copies shexter.py to /opt/, then symlinks the shexter executable to /usr/bin.

if [ -f /usr/bin/shexter ]; then
    echo "Removing existing symlink at /usr/bin/shexter"
    rm /usr/bin/shexter
fi

OPT_DIR='/opt/shexter/'

mkdir -p $OPT_DIR &&
        cp ../../shexter.py $OPT_DIR &&
        cp ./shexter_exec $OPT_DIR &&
        cp -r ../../shexter $OPT_DIR

if [ $? -ne 0 ]; then
    echo "Install failed. Make sure your working directory is the original installer location, and that you have the permission to write to "$OPT_DIR
    exit 1
fi

ln -s $OPT_DIR"shexter_exec" /usr/bin/shexter

NOW=`date +"%Y%m%d%H%M%S"`
FDATE1=`date -r $OPT_DIR"shexter.py" +"%Y%m%d%H%M%S"`

if [ -f $OPT_DIR"shexter.py" ] && [ `expr $NOW - $FDATE1` -lt 5 ]; then
    echo "shexter.py copied successfully"
else
    echo "shexter.py was not copied!"
    exit
fi

if [ -f /usr/bin/shexter ]; then
    echo "/usr/bin/shexter link created successfully"
else
    echo "/usr/bin/shexter was not copied!"
    exit
fi

if [ -d $OPT_DIR"shexter" ]; then
    echo "shexter module copied successfully"
else 
    echo "shexter module was not copied!"
    exit
fi

chmod -R a+rx /opt/shexter

echo "Success!"
