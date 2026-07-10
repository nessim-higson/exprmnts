import struct, sys, json

raw=open(sys.argv[1],'rb').read()
nbits=raw[8]>>3; pos=8+(5+4*nbits+7)//8+4

class BR:
    def __init__(s,b,off=0): s.b=b; s.byte=off; s.bit=0
    def ub(s,n):
        v=0
        for _ in range(n):
            v=(v<<1)|((s.b[s.byte]>>(7-s.bit))&1); s.bit+=1
            if s.bit==8: s.bit=0; s.byte+=1
        return v
    def sb(s,n):
        if n==0: return 0
        v=s.ub(n)
        if v&(1<<(n-1)): v-=1<<n
        return v
    def align(s):
        if s.bit: s.bit=0; s.byte+=1

shapes={}; sprites={}; exports={}; places={}

def parse_shape(body, code):
    cid=struct.unpack('<H',body[:2])[0]
    br=BR(body,2)
    n=br.ub(5); bounds=[br.sb(n) for _ in range(4)]  # xmin xmax ymin ymax (twips)
    br.align()
    # FILLSTYLEARRAY
    def fills():
        cnt=body[br.byte]; br.byte+=1
        if cnt==0xff: cnt=struct.unpack('<H',body[br.byte:br.byte+2])[0]; br.byte+=2
        arr=[]
        for _ in range(cnt):
            t=body[br.byte]; br.byte+=1
            if t==0:
                if code>=32: c=body[br.byte:br.byte+4]; br.byte+=4; arr.append('#%02x%02x%02x'%(c[0],c[1],c[2]))
                else: c=body[br.byte:br.byte+3]; br.byte+=3; arr.append('#%02x%02x%02x'%(c[0],c[1],c[2]))
            elif t in (0x10,0x12,0x13):  # gradients — skip matrix+stops, use grey
                br.align(); 
                if br.ub(1): nn=br.ub(5); br.sb(nn); br.sb(nn)
                if br.ub(1): nn=br.ub(5); br.sb(nn); br.sb(nn)
                nn=br.ub(5); br.sb(nn); br.sb(nn); br.align()
                ng=body[br.byte]&0x0f; br.byte+=1
                step=5 if code>=32 else 4
                br.byte+=ng*step
                arr.append('#888888')
            elif t in (0x40,0x41,0x42,0x43):  # bitmap fill
                br.byte+=2
                br.align()
                if br.ub(1): nn=br.ub(5); br.sb(nn); br.sb(nn)
                if br.ub(1): nn=br.ub(5); br.sb(nn); br.sb(nn)
                nn=br.ub(5); br.sb(nn); br.sb(nn); br.align()
                arr.append('#777777')
        return arr
    def lines():
        cnt=body[br.byte]; br.byte+=1
        if cnt==0xff: cnt=struct.unpack('<H',body[br.byte:br.byte+2])[0]; br.byte+=2
        for _ in range(cnt):
            br.byte+=2
            br.byte+= 4 if code>=32 else 3
    fillArr=fills(); lines()
    nf=br.ub(4); nl=br.ub(4)
    x=y=0; f0=f1=None
    paths={}  # fillindex -> [d strings]
    def emit(fi, seg):
        if fi is None or fi==0: return
        paths.setdefault(fi,[]).append(seg)
    while True:
        if br.ub(1)==0:   # non-edge
            flags=br.ub(5)
            if flags==0: break
            if flags&1:
                mb=br.ub(5); x=br.sb(mb); y=br.sb(mb)
                cur='M%g %g'%(x/20,y/20)
                emit(f0,cur); emit(f1,cur)
            if flags&2:
                f0=br.ub(nf)
                emit(f0,'M%g %g'%(x/20,y/20))
            if flags&4:
                f1=br.ub(nf)
                emit(f1,'M%g %g'%(x/20,y/20))
            if flags&8: br.ub(nl)
            if flags&16:
                fillArr=fills(); lines()
                nf=br.ub(4); nl=br.ub(4)
        else:
            if br.ub(1):  # straight
                nb=br.ub(4)+2
                if br.ub(1): dx=br.sb(nb); dy=br.sb(nb)
                else:
                    if br.ub(1): dx=0; dy=br.sb(nb)
                    else: dx=br.sb(nb); dy=0
                x+=dx; y+=dy
                seg='L%g %g'%(x/20,y/20)
                emit(f0,seg); emit(f1,seg)
            else:  # curved
                nb=br.ub(4)+2
                cdx=br.sb(nb); cdy=br.sb(nb); adx=br.sb(nb); ady=br.sb(nb)
                cx_,cy_=x+cdx,y+cdy; x,y=cx_+adx,cy_+ady
                seg='Q%g %g %g %g'%(cx_/20,cy_/20,x/20,y/20)
                emit(f0,seg); emit(f1,seg)
    shapes[cid]={'bounds':[b/20 for b in bounds],'paths':paths,'fills':fillArr}

while pos<len(raw)-2:
    cl=struct.unpack('<H',raw[pos:pos+2])[0]; code,ln=cl>>6,cl&0x3f; pos+=2
    if ln==0x3f: ln=struct.unpack('<I',raw[pos:pos+4])[0]; pos+=4
    body=raw[pos:pos+ln]; pos+=ln
    if code in (2,22,32):
        try: parse_shape(body, {2:1,22:2,32:32}[code])
        except Exception as e: pass
    elif code==39:
        sid=struct.unpack('<H',body[:2])[0]
        q=4; content=[]
        while q<len(body)-1:
            scl=struct.unpack('<H',body[q:q+2])[0]; sc,sl=scl>>6,scl&0x3f; q+=2
            if sl==0x3f: sl=struct.unpack('<I',body[q:q+4])[0]; q+=4
            sb_=body[q:q+sl]; q+=sl
            if sc==26:
                fl=sb_[0]; r=1+2
                if fl&2:
                    cid=struct.unpack('<H',sb_[r:r+2])[0]; r+=2
                    mtx=None
                    if fl&4:
                        br=BR(sb_,r)
                        m={'sx':1,'sy':1,'tx':0,'ty':0}
                        if br.ub(1): nn=br.ub(5); m['sx']=br.sb(nn)/65536; m['sy']=br.sb(nn)/65536
                        if br.ub(1): nn=br.ub(5); br.sb(nn); br.sb(nn)
                        nn=br.ub(5); m['tx']=br.sb(nn)/20; m['ty']=br.sb(nn)/20
                        mtx=m
                    content.append((cid,mtx))
            elif sc==1: content.append(('FRAME',None))
        sprites[sid]=content
    elif code==56:
        n=struct.unpack('<H',body[:2])[0]; q=2
        for _ in range(n):
            cid=struct.unpack('<H',body[q:q+2])[0]; q+=2
            e=body.index(0,q); exports[body[q:e].decode('latin1')]=cid; q=e+1
    if code==0: break

pid=exports.get('principalAni')
print('principalAni charid:', pid)
print('sprite content (first 30):', sprites.get(pid,[])[:30])
json.dump({'exports':{k:v for k,v in exports.items()}, 'spriteKeys':list(sprites.keys())[:0]}, open('/dev/null','w'))
# save shapes for later assembly
import pickle
pickle.dump({'shapes':shapes,'sprites':sprites,'exports':exports}, open('/tmp/swfshapes.pkl','wb'))
print('shapes parsed:', len(shapes))
