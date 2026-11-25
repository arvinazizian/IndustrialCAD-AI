import os, secrets, tempfile
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
import cadquery as cq
from export_step import build
app=FastAPI()
@app.post('/step')
async def step(request: Request):
    token=os.environ.get('CAD_KERNEL_TOKEN')
    if not token or not secrets.compare_digest(request.headers.get('authorization',''),'Bearer '+token):
        raise HTTPException(401)
    raw=await request.body()
    if len(raw)>500000: raise HTTPException(413)
    data=await request.json()
    parts=data.get('parts',[])
    if not 0<len(parts)<=50 or any(len(p.get('cuts',[]))>30 for p in parts): raise HTTPException(400)
    try:
        assembly=cq.Assembly()
        for i,p in enumerate(parts): assembly.add(build(p),name='part_'+str(i))
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'model.step'
            assembly.save(str(path))
            result=path.read_bytes()
        if len(result)>4000000: raise HTTPException(413)
        return Response(result,media_type='application/step')
    except HTTPException: raise
    except Exception: raise HTTPException(400,'Invalid geometry')
