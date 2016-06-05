#!/bin/bash

#[ImageMagick] convertコマンドの使い方 https://sites.google.com/site/infoaofd/Home/computer/unix-linux/command/imagemagikconvertkomandonotsukaikata


#echo $1
hoge=""
if [[ $1 = $hoge ]] ; then
echo -n "source directory = "
read SRC_DIR
else
SRC_DIR=$1
fi

cd $SRC_DIR

for f in *.eps; 
do 
convert -quality 80 $f ${f%.eps}.png; 
echo $f" done."
done
