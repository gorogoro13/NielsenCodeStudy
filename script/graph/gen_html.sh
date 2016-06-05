#!/bin/bash

dest_dir=`pwd`
#echo $dest_dir
if $1="";then
	echo -n "output file name = "
	read FILENAME
else
	FILENAME=$1
fi

if $2="";then
	echo -n "source directory = "
	read SRC_DIR
else
	SRC_DIR=$2
fi

echo "output file name = "$FILENAME
echo "source directory = "$SRC_DIR

cat << EOS > $FILENAME
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja"><!-- InstanceBegin template="../../Templates/default.dwt" codeOutsideHTMLIsLocked="false" -->
<head>
<!-- メタ情報 -->
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-Language" content="ja" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<meta http-equiv="Content-Script-Type" content="text/javascript" />
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
<meta name="author" content="Hideki Nakajima" />
<meta name="copyright" content="Copyright (C)GoroGoro13. All Rights Reserved." />

<!-- ページタイトル、キーワードと詳細 -->
<!-- InstanceBeginEditable name="Title" -->
<title>28by28 weights(Layer-02 node-j0001)</title>
<!-- CSS -->
<link rel="stylesheet" href="../css/28by28.css" type="text/css" charset="utf-8" />

<body id="m-school" class="category5 ">
<div id="grid">
<ul>
EOS

cd $SRC_DIR
for f in *.png; 
do 
#cd ../
echo '<li><img src="'$SRC_DIR'/'$f'" width="50" height="50" /></li>' >> '../'$FILENAME; 
done

cd $dest_dir
cat << EOS >> $FILENAME
</ul>
</div>
</body>
<!-- InstanceEnd --></html>
EOS
