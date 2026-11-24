import json,struct,io,sys,numpy as np
from PIL import Image
src='trellis/dog_tpose.glb'; ref=sys.argv[1]; out=sys.argv[2]
b=open(src,'rb').read(); l=struct.unpack('<I',b[12:16])[0]; j=json.loads(b[20:20+l]); o0=20+l+8
def acc(i):
    a=j['accessors'][i]; bv=j['bufferViews'][a['bufferView']]; dt={5126:np.float32,5125:np.uint32,5123:np.uint16}[a['componentType']]
    n={'SCALAR':1,'VEC2':2,'VEC3':3}[a['type']]; o=o0+bv.get('byteOffset',0)+a.get('byteOffset',0)
    return np.frombuffer(b,dtype=dt,count=a['count']*n,offset=o).reshape(a['count'],n).astype(np.float64)
pr=j['meshes'][0]['primitives'][0]
P=acc(pr['attributes']['POSITION']); UV=acc(pr['attributes']['TEXCOORD_0']); I=acc(pr['indices']).astype(np.int64).reshape(-1,3)
bv=j['bufferViews'][j['images'][0]['bufferView']]; tex=np.asarray(Image.open(io.BytesIO(b[o0+bv.get('byteOffset',0):][:bv['byteLength']])).convert('RGB'),np.float64)
T=tex.shape[0]
img=np.asarray(Image.open(ref).convert('RGB'),np.float64); H,W=img.shape[:2]
fg=(img.min(axis=2)<235); ys,xs=np.where(fg); ix0,ix1,iy0,iy1=xs.min(),xs.max(),ys.min(),ys.max()
xmin,xmax=P[:,0].min(),P[:,0].max(); ymin,ymax=P[:,1].min(),P[:,1].max()
print('img bbox',ix0,ix1,iy0,iy1,'mesh',xmin,xmax,ymin,ymax)
# mesh faces -z; viewer's left = +x
PX=ix0+(xmax-P[:,0])/(xmax-xmin)*(ix1-ix0); PY=iy0+(ymax-P[:,1])/(ymax-ymin)*(iy1-iy0); PZ=P[:,2]
# z-buffer in image space (smaller z = nearer the viewer)
Z=np.full((H,W),np.inf)
for t in I:
    x=PX[t];y=PY[t];z=PZ[t]
    x0,x1=int(np.floor(x.min())),int(np.ceil(x.max())); y0,y1=int(np.floor(y.min())),int(np.ceil(y.max()))
    x0=max(x0,0);y0=max(y0,0);x1=min(x1,W-1);y1=min(y1,H-1)
    if x1<x0 or y1<y0: continue
    gx,gy=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
    d=(y[1]-y[2])*(x[0]-x[2])+(x[2]-x[1])*(y[0]-y[2])
    if abs(d)<1e-9: continue
    w0=((y[1]-y[2])*(gx-x[2])+(x[2]-x[1])*(gy-y[2]))/d; w1=((y[2]-y[0])*(gx-x[2])+(x[0]-x[2])*(gy-y[2]))/d; w2=1-w0-w1
    m=(w0>=-1e-4)&(w1>=-1e-4)&(w2>=-1e-4)
    if not m.any(): continue
    zz=w0*z[0]+w1*z[1]+w2*z[2]; sub=Z[y0:y1+1,x0:x1+1]; upd=m&(zz<sub); sub[upd]=zz[upd]
# face normals
N=np.cross(P[I[:,1]]-P[I[:,0]],P[I[:,2]]-P[I[:,0]]); N/=np.linalg.norm(N,axis=1,keepdims=True)+1e-12
facing=-N[:,2]  # toward viewer at -z
outT=tex.copy(); zr=(PZ.max()-PZ.min())
def sample(im,x,y):
    x=np.clip(x,0,im.shape[1]-1.001); y=np.clip(y,0,im.shape[0]-1.001); x0=x.astype(int); y0=y.astype(int); fx=(x-x0)[:,None]; fy=(y-y0)[:,None]
    return im[y0,x0]*(1-fx)*(1-fy)+im[y0,x0+1]*fx*(1-fy)+im[y0+1,x0]*(1-fx)*fy+im[y0+1,x0+1]*fx*fy
cnt=0
for fi,t in enumerate(I):
    f=facing[fi]; ax=abs(P[t,0]).mean(); lo,hi=(.6,.85) if ax>.24 else (.3,.65)
    if f<lo: continue
    wgt=np.clip((f-lo)/(hi-lo),0,1)
    u=UV[t,0]*T; v=UV[t,1]*T
    x0,x1=int(np.floor(u.min())),int(np.ceil(u.max())); y0,y1=int(np.floor(v.min())),int(np.ceil(v.max()))
    x0=max(x0,0);y0=max(y0,0);x1=min(x1,T-1);y1=min(y1,T-1)
    gx,gy=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
    d=(v[1]-v[2])*(u[0]-u[2])+(u[2]-u[1])*(v[0]-v[2])
    if abs(d)<1e-12: continue
    w0=((v[1]-v[2])*(gx-u[2])+(u[2]-u[1])*(gy-v[2]))/d; w1=((v[2]-v[0])*(gx-u[2])+(u[0]-u[2])*(gy-v[2]))/d; w2=1-w0-w1
    m=(w0>=-.02)&(w1>=-.02)&(w2>=-.02)
    if not m.any(): continue
    w0,w1,w2=w0[m],w1[m],w2[m]
    sx=w0*PX[t[0]]+w1*PX[t[1]]+w2*PX[t[2]]; sy=w0*PY[t[0]]+w1*PY[t[1]]+w2*PY[t[2]]; sz=w0*PZ[t[0]]+w1*PZ[t[1]]+w2*PZ[t[2]]
    zi=Z[np.clip(sy.astype(int),0,H-1),np.clip(sx.astype(int),0,W-1)]
    vis=sz<=zi+zr*.012
    col=sample(img,sx-.5,sy-.5); bg=col.min(axis=1)>238
    ok=vis&~bg
    if not ok.any(): continue
    ty=(gy[m].astype(int))[ok]; tx=(gx[m].astype(int))[ok]
    outT[ty,tx]=outT[ty,tx]*(1-wgt)+col[ok]*wgt; cnt+=ok.sum()
print('texels painted',cnt)
# warm the white mitten hands and bare feet to the cream fur colour of the picture's paws
paw=np.array([236,214,172.]); done=np.zeros((T,T),bool)
for fi,t in enumerate(I):
    if not (abs(P[t,0]).mean()>.375 or P[t,1].max()<ymin+.07): continue
    u=UV[t,0]*T; v=UV[t,1]*T
    x0,x1=max(int(u.min())-1,0),min(int(u.max())+1,T-1); y0,y1=max(int(v.min())-1,0),min(int(v.max())+1,T-1)
    gx,gy=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
    d=(v[1]-v[2])*(u[0]-u[2])+(u[2]-u[1])*(v[0]-v[2])
    if abs(d)<1e-12: continue
    w0=((v[1]-v[2])*(gx-u[2])+(u[2]-u[1])*(gy-v[2]))/d; w1=((v[2]-v[0])*(gx-u[2])+(u[0]-u[2])*(gy-v[2]))/d; w2=1-w0-w1
    m=(w0>=-.08)&(w1>=-.08)&(w2>=-.08)
    ty=gy[m].astype(int); tx=gx[m].astype(int); keep=~done[ty,tx]; ty,tx=ty[keep],tx[keep]; done[ty,tx]=True
    c=outT[ty,tx]; lum=(c@[.3,.59,.11])[:,None]; light=lum>150
    outT[ty,tx]=np.where(light, np.minimum(lum,245)/235*paw, c)
Image.fromarray(np.clip(outT,0,255).astype(np.uint8)).save(out)
