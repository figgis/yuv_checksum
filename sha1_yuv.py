#!/usr/bin/env python
# $head -c 152064 foreman_352x288.yuv | sha1sum 
# $dd skip=1234 count=5 bs=1
# $dd count=152064 bs=1 if=foreman_352x288.yuv | sha1sum
# $dd skip=152064 count=152064 bs=1 if=foreman_352x288.yuv | sha1sum 
import hashlib
import os

width=352
height=288
bytes=int(width*height*1.5)
f_name='foreman_352x288.yuv'

f=open(f_name, 'rb')

#calculate #frames
size_in_bytes=os.path.getsize(f_name)
frames=size_in_bytes/(bytes)

print size_in_bytes, frames

#loop through every frame and give the sha1
for i in range(0,int(frames)):
    buf=f.read(bytes)
    print i,hashlib.sha1(buf).hexdigest()
