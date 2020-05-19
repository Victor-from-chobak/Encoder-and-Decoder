# Note

**Very important to choose language - to encode/decode russian text add --language=rus**


# Read examples

You can use such command

**python3 encode.py read --input_file=read.in --output_file.data.in**

You can use my big file(data.txt) to make file (data.in) for **hack**


# Caesar examples

This is simple text

we will see how it will change 123

**python3 encode.py --encode --cipher=caesar --key=17**

+yzJnzJnJzDGCvnKvOKmNvnNzCCnJvvnyFNnzKnNzCCntyrExvndef

**python3 decode.py --decode --cipher=caesar --key=17**

This is simple text

we will see how it will change 123

#### or we can hack

**python3 hack --AnalyzedDataFile=data.in**

This is simple text

we will see how it will change 123


### russian example 

Это простой текст,

Его не сложно зашивровать

**python3 encode.py encode --cipher=caesar --key=10 --language=rus**

(ъшещьшыъшуеъофыъ@дОмшечоеыхшрчшесйВтльшлйъД

**python3 encode.py decode --cipher=caesar --key=10 --language=rus**


Это простой текст,

Его не сложно зашивровать



# Vigenere examples
Let's try something harder:

Tom Pinkerton, son of Deacon Pinkerton, had just returned from Brooklyn,
and while there had witnessed a match game between two professional
clubs. On his return he proposed that the boys of Crawford should
establish a club, to be known as the Excelsior Club of Crawford, to play
among themselves, and on suitable occasions — to challenge clubs belonging
to other villages. This proposal was received with instant approval.

“I move that Tom Pinkerton address the meeting,” said one boy.

“Second the motion,” said another.

As there was no chairman, James Briggs was appointed to that position,
and put the motion, which was unanimously carried.


**python3 main.py encode --cipher=vigenere --key=ba**

Uon Qiokfruoo,”spn”og Eebcpn”Pjnlestpn- iae kutt”rftvroee grpm”Bsopkmyo, aod”wiime”tiese”hbd”wjtoetsfd”a”mbtdh”gbmf ceuwfeo uwp qrpffstipnbl cmucs/ Pn”hjs”rftvro ie”psoqotee uhbt”tie”bpyt pf”Csaxfpre thpumd ettbbmith”a”cmuc,”tp ce”kooxn”at uhf Fxdemsjos Dlvb”og Drbwgosd- uo”pmaz
bmpnh uhfmtemvfs- bne pn”sviuaclf pcdatipnt a uo”ciamlfnhe”cmucs”bflpnhiog tp pties wimlbgfs/ Uhjs”psoqotam xat sedejvfd”wjti jnttbnu bpqrpvbl/
 “J nowe”tiau Uon Qiokfruoo bderfst uhf neftjnh,“ tajd”ooe”bpy/
 “Tedood”tie”mptjoo,“ tajd”aoouhfr/
 At uhfrf xat oo”ciajrnao,”Jbmfs”Bsihgt xat bpqojnuee uo”tiau qotiuipn-
bne quu uhf nouipn- xhjci xat vnbnjmputlz dasrjee.

**python3 encode.py decode --cipher=vigenere --key=ba**

Tom Pinkerton, son of Deacon Pinkerton, had just returned from Brooklyn,
and while there had witnessed a match game between two professional
clubs. On his return he proposed that the boys of Crawford should
establish a club, to be known as the Excelsior Club of Crawford, to play
among themselves, and on suitable occasions — to challenge clubs belonging
to other villages. This proposal was received with instant approval.

“I move that Tom Pinkerton address the meeting,” said one boy.

“Second the motion,” said another.

As there was no chairman, James Briggs was appointed to that position,
and put the motion, which was unanimously carried.


### or

**python3 hack python3 main.py hack --AnalyzedDataFile=data.in**

we will get the same text

**Russian examples**

Текст побольше из русских букв

Попробуем его зашивровать

ла-ла-ла русский Текст,

побольше!. знаков! препинания, смотрим

Последнее предложение!

**python3 encode.py encode --cipher=vigenere --key=слово --language=rus**

%рщуБмыэгээЁЖжйьуйтВГэщкДммВмрлЫэсяАмВжымрсрйщлЖкрВьрвБЛёьв`эл`номъВуАъфш“"ццАф_лыэгээЁЖж:~жцпоъьр#йБъусчялъкН|жАоэДъчои"ьАнухщужйБъуёьАтупчц-



# Vernam examples
For this encoding you need file for **key text(--random_file)** 
and file **output file** for encoded text dumped with **pickle** 

**python3 encode.py encode --cipher=vernam --random_file=rand.in --input_file=f.in --output_file=f.out**

**python3 encode.py decode --cipher=vernam --random_file=rand.in --input_file=f.out**

