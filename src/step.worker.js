import * as R from 'replicad';
import init from 'replicad-opencascadejs/src/replicad_single.js';
import wasm from 'replicad-opencascadejs/src/replicad_single.wasm?url';
let ready;
function solid(p){if(p.kind==='box')return R.makeBaseBox(p.w,p.d,p.h).translate([0,0,-p.h/2]);if(p.kind==='cylinder'&&Math.abs(p.w-p.d)<1e-8)return R.makeCylinder(p.w/2,p.h,[0,0,-p.h/2],[0,0,1]);throw Error('Browser STEP currently supports boxes and circular cylinders only');}
self.onmessage=async({data})=>{try{await (ready??=init({locateFile:()=>wasm}).then(R.setOC));const shapes=data.parts.map(p=>{let s=solid(p);for(const c of p.cuts){if(c.axis&&Math.abs(c.axis[1]/Math.hypot(...c.axis))<.999999)throw Error('Oriented cuts require server exporter');s=s.cut(solid(c).translate([c.x,-c.z,c.y]));}return {shape:s.rotate(p.angle,[0,0,0],[0,0,1]).translate([p.x,-p.z,p.y]),name:p.name||p.id}});const blob=R.exportSTEP(shapes,{unit:'MM'});if(!(await blob.text()).startsWith('ISO-10303-21;'))throw Error('Invalid STEP');self.postMessage({blob});}catch(e){self.postMessage({error:String(e.message||e)})}};
