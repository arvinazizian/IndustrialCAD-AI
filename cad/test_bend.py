import unittest, math
from export_step import build
class BendTests(unittest.TestCase):
    def test_sector_volume(self):
        p=dict(kind='bend',w=12,h=2,d=100,radius=10,bendAngle=90,x=0,y=0,z=0,angle=0,cuts=[])
        self.assertAlmostEqual(build(p).val().Volume(),math.pi/4*(144-100)*100,places=4)
