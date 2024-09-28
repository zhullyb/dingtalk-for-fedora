#!/usr/bin/sh

cd /opt/dingtalk-bin/*Release*/
export PATH=$(pwd):$PATH
# export LD_LIBRARY_PATH=$(pwd):$LD_LIBRARY_PATH
export QT_QPA_PLATFORM="wayland;xcb"
./com.alibabainc.dingtalk $1
