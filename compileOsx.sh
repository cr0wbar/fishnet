#!/bin/bash

echo "CLEANING BUILD DIR"
rm -rf build

echo "GENERATING SOURCE CODE"
pyqtdeploycli --project osxdeploy.pdy --output build build

echo "COMPILING Fishnet"
cp fishnet.icns ./build/
cd build
PRO=Fishnet.pro
echo "INCLUDEPATH += /usr/local/guroot-static/lib/libffi-3.1/include" >> $PRO
echo "LIBS += /usr/local/guroot-static/lib/libffi.a" >> $PRO
echo "ICON = fishnet.icns" >> $PRO
echo "QMAKE_LFLAGS += -Wl,-no_compact_unwind" >> $PRO
qmake && make && cp -r ../icons ../misc Fishnet.app/Contents/MacOs/
cd ..

echo "DEPLOYING APPLICATION"
macdeployqt build/Fishnet.app

echo "FINISHED"
