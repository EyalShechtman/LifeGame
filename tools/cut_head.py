import json,struct,sys,io,numpy as np
from PIL import Image
src,out,cut=sys.argv[1],sys.argv[2],float(sys.argv[3])
b=open(src,'rb').read(); l=struct.unpack('<I',b[12:16])[0]; j=json.loads(b[20:20+l]); o0=20+l+8
def acc(i):
    a=j['accessors'][i]; bv=j['bufferViews'][a['bufferView']]; dt={5126:np.float32,5125:np.uint32,5123:np.uint16}[a['componentType']]
    n={'SCALAR':1,'VEC2':2,'VEC3':3}[a['type']]; isz=np.dtype(dt).itemsize; st=bv.get('byteStride') or n*isz
    o=o0+bv.get('byteOffset',0)+a.get('byteOffset',0)
    arr=np.frombuffer(b,dtype=np.uint8,count=st*a['count'],offset=o) if st*a['count']<=len(b)-o else np.frombuffer(b,dtype=np.uint8,offset=o)
    return np.array(np.lib.stride_tricks.as_strided(np.frombuffer(b,dtype=dt,offset=o,count=(st*(a['count']-1))//isz+n),shape=(a['count'],n),strides=(st,isz)))
pr=j['meshes'][0]['primitives'][0]
P=acc(pr['attributes']['POSITION']).astype(np.float64); UV=acc(pr['attributes']['TEXCOORD_0']).astype(np.float64); I=acc(pr['indices']).reshape(-1,3)
P-=[(P[:,0].max()+P[:,0].min())/2,P[:,1].min(),(P[:,2].max()+P[:,2].min())/2]; P/=P[:,1].max()
keep=(P[I,1].min(axis=1)>cut); T=I[keep]; used=np.unique(T); remap=-np.ones(len(P),np.int64); remap[used]=np.arange(len(used))
P2=P[used].astype(np.float32); UV2=UV[used].astype(np.float32); T2=remap[T].astype(np.uint32)
# texture: crop to used uv bbox, cap at 2048
img=Image.open(io.BytesIO(bytes(b[o0+j['bufferViews'][j['images'][0]['bufferView']].get('byteOffset',0):][:j['bufferViews'][j['images'][0]['bufferView']]['byteLength']]))).convert('RGB')
W,H=img.size; u0,v0=UV2.min(0); u1,v1=UV2.max(0); print('tris',len(T2),'verts',len(P2),'uv bbox',u0,v0,u1,v1,'img',W,H)
x0,y0,x1,y1=int(max(0,u0*W-4)),int(max(0,v0*H-4)),int(min(W,u1*W+4)),int(min(H,v1*H+4))
img=img.crop((x0,y0,x1,y1)); UV2[:,0]=(UV2[:,0]*W-x0)/(x1-x0); UV2[:,1]=(UV2[:,1]*H-y0)/(y1-y0)
s=min(1,2048/max(img.size)); img=img.resize((round(img.size[0]*s),round(img.size[1]*s)),Image.LANCZOS)
jb=io.BytesIO(); img.save(jb,'JPEG',quality=88); jb=jb.getvalue(); print('tex',img.size,len(jb))
bufs=[T2.tobytes(),P2.tobytes(),UV2.tobytes(),jb]; offs=[];cur=0;blob=b''
for x in bufs:
    offs.append(len(blob)); blob+=x; blob+=b'\0'*((-len(blob))%4)
g={'asset':{'version':'2.0'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0,'name':'head'}],
 'meshes':[{'primitives':[{'attributes':{'POSITION':1,'TEXCOORD_0':2},'indices':0,'material':0}]}],
 'materials':[{'pbrMetallicRoughness':{'baseColorTexture':{'index':0},'metallicFactor':0,'roughnessFactor':.8}}],
 'textures':[{'source':0,'sampler':0}],'samplers':[{'magFilter':9729,'minFilter':9987}],'images':[{'bufferView':3,'mimeType':'image/jpeg'}],
 'buffers':[{'byteLength':len(blob)}],
 'bufferViews':[{'buffer':0,'byteOffset':offs[0],'byteLength':len(bufs[0]),'target':34963},{'buffer':0,'byteOffset':offs[1],'byteLength':len(bufs[1]),'target':34962},{'buffer':0,'byteOffset':offs[2],'byteLength':len(bufs[2]),'target':34962},{'buffer':0,'byteOffset':offs[3],'byteLength':len(bufs[3])}],
 'accessors':[{'bufferView':0,'componentType':5125,'count':T2.size,'type':'SCALAR'},
  {'bufferView':1,'componentType':5126,'count':len(P2),'type':'VEC3','min':P2.min(0).tolist(),'max':P2.max(0).tolist()},
  {'bufferView':2,'componentType':5126,'count':len(P2),'type':'VEC2'}]}
js=json.dumps(g).encode(); js+=b' '*((-len(js))%4)
open(out,'wb').write(b'glTF'+struct.pack('<II',2,12+8+len(js)+8+len(blob))+struct.pack('<I',len(js))+b'JSON'+js+struct.pack('<I',len(blob))+b'BIN\0'+blob)
