#!/usr/bin/sh

cd /opt/dingtalk-bin/*Release*/
LD_LIBRARY_PATH=$(pwd):$LD_LIBRARY_PATH ./com.alibabainc.dingtalk $1
