seeing
======
天体観測で得た画像に対して SExtractor を実行し，
星を検出して seeing を測るための script です．
Apogee U42 にあわせて作りました．

SExtractor の stellaritiy の判定には PSF size が必要なので，
まず最初にあてずっぽに SExtractor を走らせ，fwhm の meidan をとります．
小口径望遠鏡の場合は星ばかり写るので，
これはそこそこ PSF size のいい評価になります．
そしてこの値を使って SExtractor かけ直します．
出て来たカタログを利用して空間分布などいろいろ表示します．

夜間の Seeing 変化を評価するとかそういう用とに使えるように，
拡張して行こうと思っていますが，どこまでやるだろうか．

うつみ

![example](http://hinotori.hiroshima-u.ac.jp/ActivityReport/20140530/20140530-405obj.png)
![example](http://hinotori.hiroshima-u.ac.jp/ActivityReport/20140530/timeseries.png)

http://hinotori.hiroshima-u.ac.jp/ActivityReport/20140530/
