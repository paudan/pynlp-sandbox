#!/usr/bin/env bash

sudo apt-get install pkg-config autoconf-archive
sudo apt-get install frogdata libfolia-dev libticcutils2-dev

### Install Frog from source ###
git clone https://github.com/LanguageMachines/timbl.git
cd timbl
bash bootstrap.sh; ./configure; make; sudo make install
cd ..

git clone https://github.com/LanguageMachines/mbt.git
cd mbt
bash bootstrap.sh; ./configure; make; sudo make install
cd ..

git clone https://github.com/LanguageMachines/libfolia.git
cd libfolia
bash bootstrap.sh; ./configure; make; sudo make install
cd ..

git clone https://github.com/LanguageMachines/ucto.git
cd ucto
bash bootstrap.sh; ./configure; make; sudo make install
cd ..

git clone https://github.com/LanguageMachines/uctodata.git
cd uctodata
bash bootstrap.sh; ./configure; make; sudo make install
cd ..

git clone https://github.com/LanguageMachines/frog.git
git checkout 3fb42d9866a1983fff32ceac7be444c9a4a2f22c # Last working revision
cd frog
bash bootstrap.sh; ./configure; make; sudo make install
cd ..

sudo pip install python-frog