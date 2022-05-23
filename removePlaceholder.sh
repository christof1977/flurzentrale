#!/bin/bash

rm -rf gui/mainwindow.ui.tmp
mv gui/mainwindow.ui gui/mainwindow.ui.tmp
cat gui/mainwindow.ui.tmp | sed '/PlaceholderText/,+8 d' > gui/mainwindow.ui
