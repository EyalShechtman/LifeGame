import sys,zipfile,numpy as np
z=zipfile.ZipFile(sys.argv[1]); fs=[l for l in z.read('dog.obj').decode().split('\n') if l.startswith('f ')]
F=np.array([[int(t.split('/')[0])-1 for t in l.split()[1:]] for l in fs]); n=F.max()+1
p=list(range(n))
def fd(x):
  while p[x]!=x: p[x]=p[p[x]]; x=p[x]
  return x
for a,b,c in F:
  ra,rb,rc=fd(a),fd(b),fd(c); p[rb]=ra; p[fd(rc)]=ra
roots=[fd(i) for i in set(F.flatten())]; from collections import Counter; c=Counter(roots); print('islands',len(c),'biggest',c.most_common(3))
