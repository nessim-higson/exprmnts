import struct, json, sys

raw = open(sys.argv[1],'rb').read()
nbits = raw[8]>>3
pos = 8+(5+4*nbits+7)//8+4

class BR:  # bit reader
    def __init__(s,b,off=0): s.b=b; s.byte=off; s.bit=0
    def ub(s,n):
        v=0
        for _ in range(n):
            v=(v<<1)|((s.b[s.byte]>>(7-s.bit))&1)
            s.bit+=1
            if s.bit==8: s.bit=0; s.byte+=1
        return v
    def sb(s,n):
        if n==0: return 0
        v=s.ub(n)
        if v & (1<<(n-1)): v-=1<<n
        return v
    def align(s):
        if s.bit: s.bit=0; s.byte+=1

def rect(br):
    n=br.ub(5); return [br.sb(n) for _ in range(4)]
def matrix(br):
    m={'sx':1,'sy':1,'r0':0,'r1':0,'tx':0,'ty':0}
    if br.ub(1): n=br.ub(5); m['sx']=br.sb(n)/65536; m['sy']=br.sb(n)/65536
    if br.ub(1): n=br.ub(5); m['r0']=br.sb(n)/65536; m['r1']=br.sb(n)/65536
    n=br.ub(5); m['tx']=br.sb(n); m['ty']=br.sb(n)
    return m

fonts={}      # id -> {codes:[...]}
texts={}      # charid -> [(fontid, string, textheight, color, x, y)]
sprites={}    # spriteid -> [placed char ids]
exports={}    # name -> charid
edittexts={}

def parse_font2(body, tag):
    fid=struct.unpack('<H',body[:2])[0]
    p=2
    flags=body[p]; p+=1
    wideOffsets=flags&8; wideCodes=flags&4
    p+=1  # langcode
    nl=body[p]; p+=1; p+=nl  # fontname
    ng=struct.unpack('<H',body[p:p+2])[0]; p+=2
    start=p
    if wideOffsets:
        offs=[struct.unpack('<I',body[p+4*i:p+4*i+4])[0] for i in range(ng+1)]
        p+=4*(ng+1)
    else:
        offs=[struct.unpack('<H',body[p+2*i:p+2*i+2])[0] for i in range(ng+1)]
        p+=2*(ng+1)
    codeoff = start+offs[ng] if ng else p
    ct=[]
    q=codeoff
    for i in range(ng):
        if wideCodes: ct.append(struct.unpack('<H',body[q:q+2])[0]); q+=2
        else: ct.append(body[q]); q+=1
    fonts[fid]={'codes':ct}

def parse_text(body, tagcode, cid_holder):
    cid=struct.unpack('<H',body[:2])[0]
    br=BR(body,2)
    rect(br); br.align()
    m=matrix(br); br.align()
    gbits=body[br.byte]; abits=body[br.byte+1]
    p=br.byte+2
    out=[]
    fid=None; th=None; col=None; xo=0; yo=0
    while p<len(body):
        f=body[p]
        if f==0: break
        if f&0x80:  # style record
            p+=1
            if f&8: fid=struct.unpack('<H',body[p:p+2])[0]; p+=2
            if f&4:
                col=body[p:p+(4 if tagcode==33 else 3)]; p+=4 if tagcode==33 else 3
            if f&1: xo=struct.unpack('<h',body[p:p+2])[0]; p+=2
            if f&2: yo=struct.unpack('<h',body[p:p+2])[0]; p+=2
            if f&8: th=struct.unpack('<H',body[p:p+2])[0]; p+=2
        else:  # glyph record
            cnt=f; p+=1
            br2=BR(body,p)
            chars=[]
            for _ in range(cnt):
                gi=br2.ub(gbits); br2.ub(abits)
                codes=fonts.get(fid,{}).get('codes',[])
                chars.append(chr(codes[gi]) if gi<len(codes) else '?')
            p=br2.byte+(1 if br2.bit else 0)
            out.append({'text':''.join(chars),'x':xo+int(m['tx']),'y':yo+int(m['ty']),'size':th})
    texts[cid]=out

while pos<len(raw)-2:
    cl=struct.unpack('<H',raw[pos:pos+2])[0]; code,ln=cl>>6,cl&0x3f; pos+=2
    if ln==0x3f: ln=struct.unpack('<I',raw[pos:pos+4])[0]; pos+=4
    body=raw[pos:pos+ln]; pos+=ln
    if code in (48,75): parse_font2(body,code)
    elif code==10:  # DefineFont v1: id, offset table (first offset/2 = nGlyphs)
        fid=struct.unpack('<H',body[:2])[0]
        ng=struct.unpack('<H',body[2:4])[0]//2
        fonts.setdefault(fid,{'codes':[]})['nglyphs']=ng
    elif code in (13,62):  # DefineFontInfo / 2: code table for a v1 font
        fid=struct.unpack('<H',body[:2])[0]
        q=2; nl=body[q]; q+=1+nl
        flags=body[q]; q+=1
        if code==62: q+=1  # langcode
        wide=flags&1
        ct=[]
        while q<len(body):
            if wide: ct.append(struct.unpack('<H',body[q:q+2])[0]); q+=2
            else: ct.append(body[q]); q+=1
        fonts.setdefault(fid,{})['codes']=ct
    elif code in (11,33): parse_text(body,code,None)
    elif code==37:  # DefineEditText
        cid=struct.unpack('<H',body[:2])[0]
        # rect then flags; initial text if hasText
        br=BR(body,2); rect(br); br.align()
        p=br.byte
        flags=struct.unpack('<H',body[p:p+2])[0]; p+=2
        hasText=flags&0x80; hasFont=flags&0x1; hasColor=flags&0x4
        hasMaxLen=flags&0x2; hasLayout=flags&0x20
        if hasFont: p+=4
        if flags&0x8000: p+=2   # hasFontClass? (skip)
        if hasColor: p+=4
        if hasMaxLen: p+=2
        if hasLayout: p+=9
        e=body.index(0,p); var=body[p:e].decode('latin1'); p=e+1
        txt=''
        if hasText:
            e=body.index(0,p); txt=body[p:e].decode('latin1')
        edittexts[cid]={'var':var,'text':txt}
    elif code==39:
        sid=struct.unpack('<H',body[:2])[0]
        q=4; placed=[]
        while q<len(body)-1:
            scl=struct.unpack('<H',body[q:q+2])[0]; sc,sl=scl>>6,scl&0x3f; q+=2
            if sl==0x3f: sl=struct.unpack('<I',body[q:q+4])[0]; q+=4
            sb=body[q:q+sl]; q+=sl
            if sc==26:  # PlaceObject2
                fl=sb[0]
                r=1+2
                if fl&2:
                    cid2=struct.unpack('<H',sb[r:r+2])[0]; r+=2
                    tx=ty=0
                    if fl&4:
                        br2=BR(sb,r)
                        if br2.ub(1): nn=br2.ub(5); br2.sb(nn); br2.sb(nn)
                        if br2.ub(1): nn=br2.ub(5); br2.sb(nn); br2.sb(nn)
                        nn=br2.ub(5); tx=br2.sb(nn); ty=br2.sb(nn)
                    placed.append((cid2,tx,ty))
        sprites[sid]=placed
    elif code==56:  # ExportAssets
        n=struct.unpack('<H',body[:2])[0]; q=2
        for _ in range(n):
            cid=struct.unpack('<H',body[q:q+2])[0]; q+=2
            e=body.index(0,q); name=body[q:e].decode('latin1'); q=e+1
            exports[name]=cid
    if code==0: break

# resolve: for each exported *Text symbol, gather text from placed chars (recursively)
def gather(cid, depth=0, ox=0, oy=0):
    outs=[]
    if cid in texts:
        outs += [{'text':t['text'],'x':t['x']+ox,'y':t['y']+oy,'size':t['size']} for t in texts[cid]]
    if cid in edittexts and edittexts[cid]['text']:
        outs.append({'text':edittexts[cid]['text'],'x':ox,'y':oy,'size':0})
    if cid in sprites and depth<4:
        for c,tx,ty in sprites[cid]: outs += gather(c,depth+1,ox+tx,oy+ty)
    return outs

result={}
for name,cid in exports.items():
    g=gather(cid)
    if g: result[name]=g
json.dump(result, open('/tmp/swf_texts.json','w'), indent=1)
print("fonts:",len(fonts)," texts:",len(texts)," sprites:",len(sprites)," exports:",len(exports))
print("exported-with-text:", len(result))
print(sorted(result.keys())[:40])
