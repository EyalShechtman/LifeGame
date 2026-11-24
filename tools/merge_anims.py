import json,struct,sys,os,subprocess,tempfile
def load(p):
  b=open(p,'rb').read(); jl=struct.unpack('<I',b[12:16])[0]; j=json.loads(b[20:20+jl]); o=20+jl; bl=struct.unpack('<I',b[o:o+4])[0]; return j,bytearray(b[o+8:o+8+bl])
d,out=sys.argv[1],sys.argv[2]
order=[('breathing_idle','idle'),('walking','walk'),('stand_to_sit','sitdown'),('sitting_idle','sitidle'),('sit_to_stand','standup')]
J,BIN=load(os.path.join(d,'breathing_idle.glb'))
names=[n.get('name') for n in J['nodes']]
J['animations']=[]
def pad():
  while len(BIN)%4: BIN.append(0)
for f,nm in order:
  j,b=load(os.path.join(d,f+'.glb'))
  assert [n.get('name') for n in j['nodes']]==names, f
  for a in j['animations']:
    amap={}
    def copy_acc(i):
      if i in amap: return amap[i]
      acc=dict(j['accessors'][i]); bv=j['bufferViews'][acc['bufferView']]
      st=bv.get('byteOffset',0)+acc.get('byteOffset',0)
      n={'SCALAR':1,'VEC3':3,'VEC4':4}[acc['type']]*acc['count']*4
      pad(); off=len(BIN); BIN.extend(b[st:st+n])
      J['bufferViews'].append({'buffer':0,'byteOffset':off,'byteLength':n}); acc['bufferView']=len(J['bufferViews'])-1; acc.pop('byteOffset',None)
      J['accessors'].append(acc); amap[i]=len(J['accessors'])-1; return amap[i]
    samplers=[{'input':copy_acc(s['input']),'output':copy_acc(s['output']),'interpolation':s.get('interpolation','LINEAR')} for s in a['samplers']]
    J['animations'].append({'name':nm,'samplers':samplers,'channels':a['channels']})
# swap texture to jpg
img=J['images'][0]; bv=J['bufferViews'][img['bufferView']]; png=bytes(BIN[bv['byteOffset']:bv['byteOffset']+bv['byteLength']])
t=tempfile.mkdtemp(); open(t+'/t.png','wb').write(png)
subprocess.run(['sips','-s','format','jpeg','-s','formatOptions','85','-Z','2048',t+'/t.png','--out',t+'/t.jpg'],capture_output=True)
jpg=open(t+'/t.jpg','rb').read(); pad(); off=len(BIN); BIN.extend(jpg)
J['bufferViews'].append({'buffer':0,'byteOffset':off,'byteLength':len(jpg)}); img['bufferView']=len(J['bufferViews'])-1; img['mimeType']='image/jpeg'
pad(); J['buffers']=[{'byteLength':len(BIN)}]
js=json.dumps(J,separators=(',',':')).encode(); js+=b' '*((4-len(js)%4)%4)
blob=struct.pack('<III',0x46546C67,2,12+8+len(js)+8+len(BIN))+struct.pack('<II',len(js),0x4E4F534A)+js+struct.pack('<II',len(BIN),0x004E4942)+bytes(BIN)
open(out,'wb').write(blob); print('png',len(png),'jpg',len(jpg),'out',len(blob),[a['name'] for a in J['animations']])
