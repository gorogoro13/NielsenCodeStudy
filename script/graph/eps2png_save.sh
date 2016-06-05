#!/bin/bash

#[ImageMagick] convertコマンドの使い方 https://sites.google.com/site/infoaofd/Home/computer/unix-linux/command/imagemagikconvertkomandonotsukaikata

dest_dir=`pwd`

hoge=""
if [[ $1 = $hoge ]] ; then
    echo -n "dir_prefix = "
    read DIR_PREFIX
else
    DIR_PREFIX=$1
fi


for n in 20 21 23 24 25 26 27 28 29 30;
do
    DIR=$DIR_PREFIX$n
    
    echo "cd "$DIR
    #read OK
    cd $DIR
    for f in *.eps; 
    do 
        convert -quality 80 $f ${f%.eps}.png; 
    echo $f" done."
    done
    cd $dest_dir
done
