const base=import.meta.env.VITE_API_URL||"http://localhost:8000/api";
async function read(response:Response){const body=await response.json();if(!response.ok)throw new Error(typeof body.detail==="string"?body.detail:body.detail?.message||"Request failed");return body;}
export const runWorkflow=(requirement_text:string)=>fetch(`${base}/workflow/run`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({requirement_text})}).then(read);
export const approve=(gate:"brd"|"code-plan")=>fetch(`${base}/workflow/approve/${gate}`,{method:"POST"}).then(read);
export const getWorkflowStatus=()=>fetch(`${base}/workflow/status`).then(read);
export const getArtifacts=()=>fetch(`${base}/artifacts`).then(read);
export const getArtifact=(name:string)=>fetch(`${base}/artifacts/${name}`).then(read);
export const getTraceability=()=>fetch(`${base}/traceability`).then(read);
