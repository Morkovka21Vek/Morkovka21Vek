#!/bin/bash
cp -r $HOME/.config/qtile/ ./linux_files/
git status
git add linux_files/
git commit -S -m "Update linux_files"
git push
