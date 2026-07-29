const host=typeof window==="undefined"?"localhost":window.location.hostname;
const base=import.meta.env.VITE_API_URL||`http://${host}:8000/api`;
async function read(response:Response){
 const type=response.headers.get("content-type")||"";
 const body=type.includes("application/json")?await response.json():{detail:await response.text()};
 if(!response.ok)throw new Error(typeof body.detail==="string"?body.detail:body.detail?.message||`Request failed (${response.status})`);
 return body;
}
async function request(path:string,options?:RequestInit){
 try{return await read(await fetch(`${base}${path}`,options));}
 catch(error){
  if(error instanceof TypeError)throw new Error(`Cannot reach the local backend at ${base}. Start it with: uvicorn main:app --reload`);
  throw error;
 }
}
export const runWorkflow=(requirement_text:string)=>request("/workflow/run",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({requirement_text})});
export const approve=(gate:"brd"|"code-plan")=>request(`/workflow/approve/${gate}`,{method:"POST"});
export const getWorkflowStatus=()=>request("/workflow/status");
export const getArtifacts=()=>request("/artifacts");
export const getArtifact=(name:string)=>request(`/artifacts/${name}`);
export const getTraceability=()=>request("/traceability");
export const getDemoData=()=>request("/demo-data");
