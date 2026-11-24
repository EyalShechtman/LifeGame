import json,struct,sys
b=open(sys.argv[1],'rb').read()
l=struct.unpack('<I',b[12:16])[0]
j=json.loads(b[20:20+l])
print('generator',j.get('asset'))
print('meshes',[(m.get('name'),len(m['primitives'])) for m in j.get('meshes',[])])
print('skins',len(j.get('skins',[])),'joints',[len(s['joints']) for s in j.get('skins',[])])
print('anims',[a.get('name') for a in j.get('animations',[])])
print('materials',[m.get('name') for m in j.get('materials',[])])
print('images',[(i.get('mimeType'),i.get('name')) for i in j.get('images',[])])
for a in j['accessors']:
  if 'min' in a and a.get('type')=='VEC3' and len(a['min'])==3: print('pos?',a['count'],a['min'],a['max']); 
print('nodes',[(n.get('name'),n.get('scale'),n.get('rotation')) for n in j['nodes']][:10])
