#!/usr/bin/env bash
curl -sSL https://get.rvm.io | bash
source /home/<usuario>/.rvm/scripts/rvm
rvm install ruby-2.3.1
rvm use 2.3.1
sudo apt-get install zlib1g-dev
gem uninstall pdf-reader
gem install pdf-reader -v 1.1.1
gem install pdf-extract
