#!/usr/bin/sh

export QT_QPA_PLATFORM="wayland;xcb"
cd /opt/dingtalk-bin/*Release*/
LD_LIBRARY_PATH=$(pwd):$LD_LIBRARY_PATH ./com.alibabainc.dingtalk $1
