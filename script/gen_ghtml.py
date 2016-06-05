-*- coding: utf-8 -*-
"""
gen_ghtml.py
~~~~~~~~~~
"""
pict_dir = "epoch_01_a/"

meta = """
<!--
疑似フレームページの作成 http://onohp.com/sonota/zatuki/homepage/giji_frame/index.html
特定の要素の中身をごっそり書き換える http://www.nishishi.com/javascript/2007/innerhtml.html
-->
<!-- メタ情報 -->
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja"><!-- InstanceBegin template="../../Templates/default.dwt" codeOutsideHTMLIsLocked="false" -->
"""

head_1 = """<HEAD>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-Language" content="ja" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<meta http-equiv="Content-Script-Type" content="text/javascript" />
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
<meta name="author" content="Hideki Nakajima" />
<meta name="copyright" content="Copyright (C)GoroGoro13. All Rights Reserved." />
<title>28by28weights</title>
<!-- CSS -->
<LINK rel="stylesheet" href="css/style_yoko.css" type="text/css" id="print_style">
<link rel="stylesheet" href="css/28by28.css" type="text/css" charset="utf-8" />
<SCRIPT type="text/javascript">
<!--
function escape_html (string) {
if(typeof string !== 'string') {
return string;
}
return string.replace(/[&'`"<>]/g, function(match) {
return {
    '&': '&amp;',
    "'": '&#x27;',
    '`': '&#x60;',
    '"': '&quot;',
    '<': '&lt;',
    '>': '&gt;',
}[match]
});
}

function page_print(){
    document.getElementById('print_style').href = "css/style_print.css";//-- スタイルシートの変更
print()   ;//-- 印刷
document.getElementById('print_style').href = "css/style_yoko.css" ;//-- スタイルシートを元に戻す
}
"""
#<li><img src="epoch_01_a/w_L2_j0001/w_L2_j0001_w_0001.png" width="50" height="50" /></li>
f_gossori = "//<li><img src=\"epoch_01_a/w_L2_j0001/w_L2_j0001_w_0001.png\" width=\"50\" height=\"50\" /></li>\n"
for j in xrange(1,31):
    prm_layer_node = "w_L2_j"
    dig4 = "{0:04d}".format(j)
    f_gossori += "function gossori_" + dig4 + "(){ \n"
    f_gossori +=  "  document.getElementById('Main_area').innerHTML = ' <div id=\"grid\">' + \n "
    f_gossori += "  '<ul>' + \n"
    for k in xrange(1, 785):
        k4 = prm_layer_node + "{0:04d}".format(k)
        w4 = "_w_" + "{0:04d}".format(k)
        f_gossori += "'<li><img src=\"" + pict_dir  + prm_layer_node + dig4  + "/" + prm_layer_node + dig4 + w4 + ".png\"" + \
        " width=\"50\" height=\"50\" />"  + "</li>' + \n"
    f_gossori += "'  </ul>' + \n "
    f_gossori += "'</div>' \n "
    f_gossori += "}\n"

f_left = """
                function left(){
                    for(a=1 ; a<31 ; a++){
                        var cc = ''
                        cc +='<div class="link_btn">'
                        cc +='<form action="./" id="w_L2_j0001" name="w_L2_j0001">'
                        cc +='    <input type="button" value="w_L2_j' +
                                ("0000"+a).slice(-4) +
                                '" onclick="gossori_' +
                                ("0000"+a).slice(-4) + '();" />'
                        cc +='</form>'
                        cc +='</div>'
                        cc +='<BR>'
                        document.write(cc)
                    }
                }
"""
head_close = """
-->
</SCRIPT>
</HEAD>
"""
body = """
<BODY>
<DIV id="Header_area" align="center">
　　　　レイヤー　　
<A href="index.html" onfocus="this.blur()"><B>Layer-01(入力)</B></A>　
<A href="index.html" onfocus="this.blur()"><B>Layer-02</B></A>
<A href="index.html" onfocus="this.blur()"><B>Layer-03</B></A>
<A href="javascript:page_print()" onfocus="this.blur()">印刷</A>
</DIV>

<DIV id="Left_area"  align="center">
<BR>
<SCRIPT type="text/javascript">
<!--
//--- 行数が３００行となるために Javascript で作成してあります
left()
//-->
</SCRIPT>
  </DIV>
    <DIV id="Main_area" align="center">

  </DIV>
</BODY>
"""
print meta
print head_1
print f_gossori
print f_left
print head_close
print body
