import unittest, math
from export_step import build
class GeometryTests(unittest.TestCase):
    def test_through_hole(self):
        p=dict(kind='box',w=100,h=10,d=100,x=0,y=0,z=0,angle=0,cuts=[dict(kind='cylinder',w=20,h=20,d=20,x=0,y=0,z=0)])
        self.assertAlmostEqual(build(p).val().Volume(),100000-1000*math.pi,places=4)
if __name__=='__main__': unittest.main()
