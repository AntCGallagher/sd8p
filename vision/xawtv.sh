#!/bin/sh
v4lctl capture grabdisplay &> /dev/null
v4lctl setnorm PAL-DK &> /dev/null
v4lctl setinput S-Video &> /dev/null
#v4lctl bright 10% &> /dev/null
#v4lctl hue 20% &> /dev/null
#v4lctl contrast 30% &> /dev/null
v4lctl color 50% &> /dev/null
v4lctl setattr 'whitecrush lower' 50% &> /dev/null
v4lctl setattr 'whitecrush upper' 50% &> /dev/null
v4lctl setattr 'uv ratio' 50% &> /dev/null
v4lctl setattr 'coring' 0% &> /dev/null
v4lctl setattr 'chroma agc' off &> /dev/null
v4lctl setattr 'color killer' off &> /dev/null
v4lctl setattr 'comb filter' off &> /dev/null
v4lctl setattr 'auto mute' on &> /dev/null
v4lctl setattr 'luma decimation filter' off &> /dev/null
v4lctl setattr 'agc crush' off &> /dev/null
v4lctl setattr 'vcr hack' off &> /dev/null
v4lctl setattr 'full luma range' off &> /dev/null
#video source S-Video
