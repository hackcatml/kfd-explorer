# kfd-explorer
Kernel memory explorer utilizing [kfund](https://github.com/wh1te4ever/kfund) project with frida-gadget

## Supported Device
iOS/iPadOS 16.0-16.6.1

## Usage
1.&nbsp;Install kfund-gadget.ipa using trollstroe or sideloadly<br>

2.&nbsp;Launch kfd app and kopen

3.&nbsp;Run kfd-explorer
```
# Git clone
git clone https://github.com/hackcatml/kfd-explorer
cd kfd-explorer

# Run
./kfd-explorer.sh
```

4.&nbsp;Attach<br>
If it cannot attach, try running Xcode briefly.

## Screenshots

## Build kfund-gadget.ipa
```
# Git clone kfund
git clone https://github.com/wh1te4ever/kfund

# Replace ContentView.swift
Replace the ContentView.swift in kfund with the one in the kfundfiles directory

# Include frida-gadget
Put frida-gadget-16.1.11.dylib, frida-gadget-16.1.11.config in the kfund project

# Build
Open kfund > Build Phases > Copy Bundle Resources > add frida-gadget-16.1.11.dylib, frida-gadget-16.1.11.config.
Build
```

## Credits
[kfund](https://github.com/wh1te4ever/kfund)<br>
