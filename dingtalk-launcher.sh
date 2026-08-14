#!/usr/bin/sh

cd /opt/dingtalk-bin/*Release*/
export PATH=$(pwd):$PATH
# export LD_LIBRARY_PATH=$(pwd):$LD_LIBRARY_PATH
export QT_QPA_PLATFORM="wayland;xcb"
hook="$(pwd)/dingtalk-gray-hook.so"
if [ -f "$hook" ]; then
    export LD_PRELOAD="$hook${LD_PRELOAD:+:$LD_PRELOAD}"
fi
./com.alibabainc.dingtalk $1
