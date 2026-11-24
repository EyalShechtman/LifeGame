import json,struct,sys,numpy as np
def load(path):
    b=open(path,'rb').read(); l=struct.unpack('<I',b[12:16])[0]; j=json.loads(b[20:20+l])
    bin_off=20+l+8; 
    a=j['accessors'][j['meshes'][0]['primitives'][0]['attributes']['POSITION']]; bv=j['bufferViews'][a['bufferView']]
    dt={5126:np.float32,5123:np.uint16,5122:np.int16}[a['componentType']]
    st=bv.get('byteStride') or 3*np.dtype(dt).itemsize; o=bin_off+bv.get('byteOffset',0)+a.get('byteOffset',0)
    raw=np.frombuffer(b,dtype=np.uint8,count=st*(a['count']-1)+3*np.dtype(dt).itemsize,offset=o)
    P=np.lib.stride_tricks.as_strided(raw[:0].view(dt) if False else np.frombuffer(b,dtype=dt,count=(st*a['count'])//np.dtype(dt).itemsize - (st//np.dtype(dt).itemsize-3),offset=o),shape=(a['count'],3),strides=(st,np.dtype(dt).itemsize))
    return j,np.array(P,dtype=np.float64)
for path in sys.argv[1:]:
    j,P=load(path)
    P=P-[ (P[:,0].max()+P[:,0].min())/2, P[:,1].min(), (P[:,2].max()+P[:,2].min())/2]; P/=P[:,1].max()
    print(path, j['nodes'][:2])
    for y in np.arange(.40,1.001,.025):
        m=(abs(P[:,1]-y)<.0125)&(abs(P[:,0])<.22)
        if m.sum(): print(f'{y:.3f} x[{P[m,0].min():+.3f},{P[m,0].max():+.3f}] z[{P[m,2].min():+.3f},{P[m,2].max():+.3f}]')
