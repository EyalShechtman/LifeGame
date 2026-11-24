import json,struct,io,sys,numpy as np
from PIL import Image, ImageFilter
def parts(f):
    b=open(f,'rb').read(); l=struct.unpack('<I',b[12:16])[0]; j=json.loads(b[20:20+l]); o=20+l+8; return b,j,o
def img(b,j,o):
    bv=j['bufferViews'][j['images'][0]['bufferView']]; return b[o+bv.get('byteOffset',0):o+bv.get('byteOffset',0)+bv['byteLength']]
rb,rj,ro=parts('anim/dog_rigged.glb'); tb,tj,to=parts('trellis/dog_tpose.glb')
a=Image.open(io.BytesIO(img(rb,rj,ro))).convert('RGB'); t=Image.open(io.BytesIO(img(tb,tj,to))).convert('RGB')
d=np.abs(np.asarray(a.resize((256,256)),float)-np.asarray(t.resize((256,256)),float)).mean(); print('mean diff vs original',d)
if d>12: sys.exit('layouts differ')
t=Image.open(sys.argv[1]).convert('RGB') if len(sys.argv)>1 else t.filter(ImageFilter.UnsharpMask(radius=2,percent=70,threshold=2))
jb=io.BytesIO(); t.save(jb,'JPEG',quality=93,subsampling=0); jb=jb.getvalue(); print('new jpeg',len(jb))
# rebuild bin: replace image bufferView bytes, shift later views
bin_=bytearray(rb[ro:ro+struct.unpack('<I',rb[20+struct.unpack('<I',rb[12:16])[0]:][:4])[0]])
iv=rj['images'][0]['bufferView']; views=rj['bufferViews']
chunks=[]; 
order=sorted(range(len(views)),key=lambda i:views[i].get('byteOffset',0))
out=bytearray()
for i in order:
    v=views[i]; data=jb if i==iv else bytes(bin_[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']])
    out+=b'\0'*((-len(out))%16); v['byteOffset']=len(out); v['byteLength']=len(data); out+=data
out+=b'\0'*((-len(out))%4)
rj['buffers'][0]['byteLength']=len(out)
js=json.dumps(rj).encode(); js+=b' '*((-len(js))%4)
open('anim/dog_rigged_sharp.glb','wb').write(b'glTF'+struct.pack('<II',2,12+8+len(js)+8+len(out))+struct.pack('<I',len(js))+b'JSON'+js+struct.pack('<I',len(out))+b'BIN\0'+out)
print('ok')
