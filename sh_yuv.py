#!/usr/bin/env python
# first frame cif
#   head -c 152064 foreman_352x288.yuv | sha1sum
# first frame cif
#   dd count=152064 bs=1 if=foreman_352x288.yuv | sha1sum
# second frame cif
#   dd skip=152064 count=152064 bs=1 if=foreman_352x288.yuv | sha1sum
import hashlib
import os
import sys

class CHKSUM:
    def __init__(self,width,height,name,kind='sha1',level=1):
        self.width=width
        self.height=height
        self.bytes=0
        self.size_in_bytes=0
        self.frames=0
        self.f_name=name
        self.f=0;
        self.secure_dic={'sha1':self.__sha1,'sha224':self.__sha256,
                'sha256':self.__sha256,'sha384':self.__sha384,
                'sha512':self.__sha512,'md5':self.__md5}
        if kind in self.secure_dic:
            self.kind=kind
            self.sh=self.secure_dic[kind]
        else:
            raise Exception("wrong kind if chksum")
        if level in [1,2]:
            self.level=level
        else:
            raise Exception("wrong level")
        self.tot=[]
        self.y=[]
        self.u=[]
        self.v=[]

        self.__run()

    #dictionary of function pointers
    def __sha1(self,buf): return hashlib.sha1(buf).hexdigest()
    def __sha224(self,buf): return hashlib.sha224(buf).hexdigest()
    def __sha256(self,buf): return hashlib.sha256(buf).hexdigest()
    def __sha384(self,buf): return hashlib.sha384(buf).hexdigest()
    def __sha512(self,buf): return hashlib.sha512(buf).hexdigest()
    def __md5(self,buf): return hashlib.md5(buf).hexdigest()


    def __run(self):
        self.f=open(self.f_name,'rb')
        self.bytes=int(self.width*self.height*1.5)
        self.size_in_bytes=os.path.getsize(self.f_name)
        self.frames=int(self.size_in_bytes/self.bytes)

        #some helper variables, TODO: clean up
        ys=0
        ye=self.width*self.height
        us=ye
        ue=us+ye/4
        vs=ue
        ve=vs+ye/4

        for i in range(0,self.frames):
            buf=self.f.read(self.bytes)
            self.tot.append(self.sh(buf))
            self.y.append(self.sh(buf[ys:ye]))
            self.u.append(self.sh(buf[us:ue]))
            self.v.append(self.sh(buf[vs:ve]))

    def report(self):
        print "file name:\t",self.f_name
        print "width:\t\t",self.width
        print "height:\t\t",self.height
        print "# frames:\t",self.frames
        print "size (bytes):\t", self.size_in_bytes
        print

        print "%s\t%s\n%s\t%s" % ('frame',self.kind,'='*5,
                '='*len(self.y[0]))
        if self.level==1:
            for i,v in enumerate(self.tot):
                print "%.4d\t%s" % (i,v)
        else:
            for i in range(0,self.frames):
                print "%.4d\tY: %s"% (i,self.y[i])
                print "\tU: %s"% (self.u[i])
                print "\tV: %s"% (self.v[i])
                print "\tT: %s"% (self.tot[i])

def usage():
    print r"./sh_yuv.py file width height [level] [hash_algorithm]"
    print "level (int) - secure hash level"
    print "    1 - secure hash for complete frame"
    print "    2 - secure hash for Y, U, V and complete frame"
    print
    print "hash algorithm (string) to use, can be any of the following:"
    print "    sha1, sha224, sha256, sha384, sha512, mf5"
    print
    print "defaults to sha1, level 1"
    print "example:"
    print "./sh_yuv.py foreman_352x288.yuv 352 288"
    print "./sh_yuv.py foreman_352x288.yuv 352 288 2 md5"

if __name__ == "__main__":
    #TODO: implement using optparse instead of hard-code values
    if len(sys.argv)<4:
        usage()
        raise Exception("illegal # arguments")
    l=1
    k='sha1'
    f=sys.argv[1]
    w=int(sys.argv[2])
    h=int(sys.argv[3])
    if(len(sys.argv)==5):
        l=int(sys.argv[4])
    if(len(sys.argv)==6):
        l=int(sys.argv[4])
        k=sys.argv[5]
    x=CHKSUM(w,h,f,level=l,kind=k)
    x.report()


