import json,struct,sys,os,zipfile
import numpy as np
src,outzip=sys.argv[1],sys.argv[2]
b=open(src,'rb').read(); jl=struct.unpack('<I',b[12:16])[0]; j=json.loads(b[20:20+jl]); B=b[20+jl+8:]
CT={5120:np.int8,5121:np.uint8,5122:np.int16,5123:np.uint16,5125:np.uint32,5126:np.float32}
NC={'SCALAR':1,'VEC2':2,'VEC3':3}
def acc(i):
  a=j['accessors'][i]; bv=j['bufferViews'][a['bufferView']]; t=CT[a['componentType']]; n=NC[a['type']]
  st=bv.get('byteStride',0); off=bv.get('byteOffset',0)+a.get('byteOffset',0); isz=np.dtype(t).itemsize
  if st and st!=n*isz:
    raw=np.frombuffer(B,dtype=np.uint8,count=st*a['count'],offset=off).reshape(a['count'],st)[:,:n*isz].copy()
    arr=raw.view(t).reshape(a['count'],n)
  else: arr=np.frombuffer(B,dtype=t,count=a['count']*n,offset=off).reshape(a['count'],n)
  arr=arr.astype(np.float64)
  if a.get('normalized'):
    arr=arr/{np.int8:127,np.uint8:255,np.int16:32767,np.uint16:65535}[t]
  return arr
pr=j['meshes'][0]['primitives'][0]; P=acc(pr['attributes']['POSITION']); UV=acc(pr['attributes']['TEXCOORD_0']); I=acc(pr['indices']).astype(np.int64).reshape(-1,3)
node=[n for n in j['nodes'] if 'mesh' in n][0]
s=np.array(node.get('scale',[1,1,1])); t=np.array(node.get('translation',[0,0,0]))
P=P*s+t
P=P*1.8  # ~1.8 units tall, human-ish scale for Mixamo
img=j['images'][0]; bv=j['bufferViews'][img['bufferView']]; jpg=B[bv.get('byteOffset',0):bv.get('byteOffset',0)+bv['byteLength']]
key=np.round(P,5); uniq,inv=np.unique(key,axis=0,return_inverse=True); inv=inv.reshape(-1)
F=I; FP=inv[F]
keep=(FP[:,0]!=FP[:,1])&(FP[:,1]!=FP[:,2])&(FP[:,0]!=FP[:,2]); F=F[keep]; FP=FP[keep]
print('verts',len(P),'->',len(uniq),'faces',len(F))
lines=['mtllib dog.mtl','usemtl dog']
lines+=['v %.5f %.5f %.5f'%tuple(p) for p in uniq]
lines+=['vt %.6f %.6f'%(u[0],1-u[1]) for u in UV]
lines+=['f %d/%d %d/%d %d/%d'%(pa+1,ta+1,pb+1,tb+1,pc+1,tc+1) for (pa,pb,pc),(ta,tb,tc) in zip(FP,F)]
ext='png' if img.get('mimeType')=='image/png' else 'jpg'; mtl='newmtl dog\nKd 1 1 1\nmap_Kd dog.'+ext+'\n'
with zipfile.ZipFile(outzip,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('dog.obj','\n'.join(lines)); z.writestr('dog.mtl',mtl); z.writestr('dog.'+ext,jpg)
print(P.min(0),P.max(0),len(I),os.path.getsize(outzip))
