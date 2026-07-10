import struct, sys
raw = open(sys.argv[1],'rb').read()
nbits = raw[8]>>3
p = 8+(5+4*nbits+7)//8+4
PROPS={0:'_x',1:'_y',2:'_xscale',3:'_yscale',4:'_currentframe',5:'_totalframes',6:'_alpha',7:'_visible',8:'_width',9:'_height',10:'_rotation',11:'_target',12:'_framesloaded',13:'_name',14:'_droptarget',15:'_url',16:'_highquality',17:'_focusrect',18:'_soundbuftime',19:'_quality',20:'_xmouse',21:'_ymouse'}
out=[]
def dis(code, pool, ind=0):
    i=0; stack=[]
    P=lambda s: out.append('  '*ind+s)
    def pop(): return stack.pop() if stack else '?'
    while i<len(code):
        op=code[i]; i+=1
        if op==0: break
        ln=0
        if op>=0x80: ln=struct.unpack('<H',code[i:i+2])[0]; i+=2
        data=code[i:i+ln]; i+=ln
        if op==0x88:  # constant pool
            n=struct.unpack('<H',data[:2])[0]; pool=[]; q=2
            for _ in range(n):
                e=data.index(0,q); pool.append(data[q:e].decode('latin1')); q=e+1
        elif op==0x96:  # push
            q=0
            while q<len(data):
                t=data[q]; q+=1
                if t==0: e=data.index(0,q); stack.append('"'+data[q:e].decode('latin1')+'"'); q=e+1
                elif t==1: stack.append(repr(struct.unpack('<f',data[q:q+4])[0])); q+=4
                elif t==2: stack.append('null')
                elif t==3: stack.append('undefined')
                elif t==4: stack.append('r%d'%data[q]); q+=1
                elif t==5: stack.append('true' if data[q] else 'false'); q+=1
                elif t==6:
                    hi,lo=struct.unpack('<II',data[q:q+8]); v=struct.unpack('<d',struct.pack('<II',lo,hi))[0]
                    stack.append(repr(v)); q+=8
                elif t==7: stack.append(str(struct.unpack('<i',data[q:q+4])[0])); q+=4
                elif t==8: stack.append('"'+pool[data[q]]+'"' if data[q]<len(pool) else '?c'); q+=1
                elif t==9: ix=struct.unpack('<H',data[q:q+2])[0]; stack.append('"'+pool[ix]+'"' if ix<len(pool) else '?c'); q+=2
                else: break
        elif op in (0x9b,0x8e):  # DefineFunction / 2
            e=data.index(0); name=data[:e].decode('latin1'); q=e+1
            np=struct.unpack('<H',data[q:q+2])[0]; q+=2
            params=[]
            if op==0x8e:
                q+=1; q+=2  # regcount, flags
                for _ in range(np):
                    q+=1; e2=data.index(0,q); params.append(data[q:e2].decode('latin1')); q=e2+1
            else:
                for _ in range(np):
                    e2=data.index(0,q); params.append(data[q:e2].decode('latin1')); q=e2+1
            bl=struct.unpack('<H',data[q:q+2])[0]
            body=code[i:i+bl]; i+=bl
            if name: P('function %s(%s) {'%(name,', '.join(params)))
            else: stack.append('<anonfn>'); P('function <anon>(%s) {'%', '.join(params))
            dis(body,pool,ind+1); P('}')
        elif op==0x1c: stack.append('GET('+pop()+')')
        elif op==0x1d: v=pop(); n=pop(); P('%s = %s'%(n.strip('"'),v))
        elif op==0x4e: m=pop(); o=pop(); stack.append(o+'.'+m.strip('"'))
        elif op==0x4f: v=pop(); m=pop(); o=pop(); P('%s.%s = %s'%(o,m.strip('"'),v))
        elif op==0x22: pr=pop(); t=pop(); stack.append(t+'.'+PROPS.get(int(float(pr)) if pr.replace('.','').replace('-','').isdigit() else -1, 'prop'+pr))
        elif op==0x23:
            v=pop(); pr=pop(); t=pop()
            pn=PROPS.get(int(float(pr)) if pr.replace('.','').replace('-','').isdigit() else -1,'prop'+pr)
            P('%s.%s = %s'%(t,pn,v))
        elif op==0x0a: b=pop(); a=pop(); stack.append('(%s + %s)'%(a,b))
        elif op==0x47: b=pop(); a=pop(); stack.append('(%s + %s)'%(a,b))
        elif op==0x0b: b=pop(); a=pop(); stack.append('(%s - %s)'%(a,b))
        elif op==0x0c: b=pop(); a=pop(); stack.append('(%s * %s)'%(a,b))
        elif op==0x0d: b=pop(); a=pop(); stack.append('(%s / %s)'%(a,b))
        elif op==0x3f: b=pop(); a=pop(); stack.append('(%s %% %s)'%(a,b))
        elif op==0x0e: b=pop(); a=pop(); stack.append('(%s == %s)'%(a,b))
        elif op==0x49: b=pop(); a=pop(); stack.append('(%s == %s)'%(a,b))
        elif op==0x0f: b=pop(); a=pop(); stack.append('(%s < %s)'%(a,b))
        elif op==0x48: b=pop(); a=pop(); stack.append('(%s < %s)'%(a,b))
        elif op==0x67: b=pop(); a=pop(); stack.append('(%s > %s)'%(a,b))
        elif op==0x10: b=pop(); a=pop(); stack.append('(%s && %s)'%(a,b))
        elif op==0x11: b=pop(); a=pop(); stack.append('(%s || %s)'%(a,b))
        elif op==0x12: stack.append('!'+pop())
        elif op==0x4c: stack.append(stack[-1] if stack else '?')
        elif op==0x17: v=pop(); P(v) if '(' in v else None
        elif op==0x87: P('r%d := %s'%(data[0], stack[-1] if stack else '?'))
        elif op==0x3c or op==0x41: v=pop(); n=pop(); P('var %s = %s'%(n.strip('"'),v))
        elif op==0x3d:
            fn=pop(); na=pop()
            try: n=int(float(na))
            except: n=0
            args=[pop() for _ in range(n)]
            stack.append('%s(%s)'%(fn.strip('"'),', '.join(args)))
        elif op==0x52:
            m=pop(); o=pop(); na=pop()
            try: n=int(float(na))
            except: n=0
            args=[pop() for _ in range(n)]
            stack.append('%s.%s(%s)'%(o,m.strip('"'),', '.join(args)))
        elif op==0x3e: P('return '+pop())
        elif op==0x9d: off=struct.unpack('<h',data[:2])[0]; P('if (%s) jump %+d'%(pop(),off))
        elif op==0x99: off=struct.unpack('<h',data[:2])[0]; P('jump %+d'%off)
        elif op==0x81: P('gotoFrame %d'%struct.unpack('<H',data[:2])[0])
        elif op==0x8c: P('gotoLabel "%s"'%data[:-1].decode('latin1'))
        elif op==0x8b: P('setTarget "%s"'%data[:-1].decode('latin1'))
        elif op==0x20: P('setTarget2 %s'%pop())
        elif op==0x34: stack.append('getTimer()')
        elif op==0x30: stack.append('random(%s)'%pop())
        elif op==0x06: P('play()')
        elif op==0x07: P('stop()')
        elif op==0x18: stack.append('int(%s)'%pop())
        elif op==0x15: b=pop(); a=pop(); stack.append('substring(%s,%s)'%(a,b))
        elif op==0x21: b=pop(); a=pop(); stack.append('(%s add %s)'%(a,b))
        elif op==0x40:
            cn=pop(); na=pop()
            try:n=int(float(na))
            except:n=0
            args=[pop() for _ in range(n)]
            stack.append('new %s(%s)'%(cn.strip('"'),', '.join(args)))
        elif op==0x42:
            na=pop()
            try:n=int(float(na))
            except:n=0
            stack.append('[%s]'%', '.join(pop() for _ in range(n)))
        else:
            pass
    return pool

# walk to DefineSprite #7 and dump its DoActions; also top-level DoActions
pool=[]
ti=0
while p < len(raw)-2:
    cl=struct.unpack('<H',raw[p:p+2])[0]; codeT,ln=cl>>6,cl&0x3f; p+=2
    if ln==0x3f: ln=struct.unpack('<I',raw[p:p+4])[0]; p+=4
    body=raw[p:p+ln]; p+=ln
    if codeT==39:  # DefineSprite: id,frames then subtags
        q=4
        while q<len(body)-1:
            scl=struct.unpack('<H',body[q:q+2])[0]; sc,sl=scl>>6,scl&0x3f; q+=2
            if sl==0x3f: sl=struct.unpack('<I',body[q:q+4])[0]; q+=4
            sb=body[q:q+sl]; q+=sl
            if sc==12 and (b'NavAni' in sb or b'navRun' in sb or b'buildMainNav' in sb or b'MainNav' in sb):
                out.append('===== DoAction in sprite (tag@) len=%d ====='%sl)
                pool=dis(sb,pool)
    elif codeT==12 and (b'NavAni' in body or b'navRun' in body):
        out.append('===== top-level DoAction len=%d ====='%ln)
        pool=dis(body,pool)
    if codeT==0: break
open(sys.argv[2],'w').write('\n'.join(out))
print('wrote', sys.argv[2], len(out), 'lines')
