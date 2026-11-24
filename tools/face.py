import json,struct,sys
import numpy as np
b=open(sys.argv[1],'rb').read()
jl=struct.unpack('<I',b[12:16])[0]; j=json.loads(b[20:20+jl]); bin_=b[20+jl+8:]
a=j['accessors'][j['meshes'][0]['primitives'][0]['attributes']['POSITION']]; bv=j['bufferViews'][a['bufferView']]
p=np.frombuffer(bin_,dtype=np.float32,count=a['count']*3,offset=bv.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,3)
for lo,hi in [(0.4,0.6),(0.2,0.4),(0,0.2),(-0.4,-0.2),(-0.9,-0.6)]:
  s=p[(p[:,1]>lo)&(p[:,1]<hi)]
  print(lo,hi,'x',s[:,0].min().round(2),s[:,0].max().round(2),'z',s[:,2].min().round(2),s[:,2].max().round(2),'zmean',s[:,2].mean().round(3))
