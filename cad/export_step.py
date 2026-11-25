import json, sys, math
import cadquery as cq

def solid(p):
    w,h,d=(float(p[k]) for k in ('w','h','d'))
    if not all(0<v<=100000 for v in (w,h,d)):
        raise ValueError('Invalid dimensions')
    if p['kind']=='box':
        return cq.Workplane('XY').box(w,d,h)
    if p['kind']=='cylinder':
        return cq.Workplane('XY').ellipse(w/2,d/2).extrude(h).translate((0,0,-h/2))
    raise ValueError('Unsupported shape')

def xyz(p):
    return (p['x'], -p['z'], p['y'])

def build(p):
    s=solid(p)
    for cut in p['cuts']:
        tool=solid(cut)
        if 'axis' in cut:
            x,y,z=map(float,cut['axis'])
            n=math.sqrt(x*x+y*y+z*z)
            if not n: raise ValueError('Invalid axis')
            x,y,z=x/n,y/n,z/n
            angle=math.degrees(math.acos(max(-1,min(1,y))))
            if abs(x)+abs(z)>1e-10:
                tool=tool.rotate((0,0,0),(z,x,0),angle)
            elif y<0:
                tool=tool.rotate((0,0,0),(1,0,0),180)
        s=s.cut(tool.translate(xyz(cut)))
    if not s.val().isValid() or s.val().Volume()<=0:
        raise ValueError('Invalid solid')
    return s.rotate((0,0,0),(0,0,1),p['angle']).translate(xyz(p))

if __name__=='__main__':
    with open(sys.argv[1]) as f:
        data=json.load(f)
    parts=data if isinstance(data,list) else data['parts']
    assembly=cq.Assembly()
    for i,p in enumerate(parts):
        assembly.add(build(p),name='part_'+str(i))
    assembly.save(sys.argv[2])
