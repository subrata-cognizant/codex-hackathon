import {useEffect,useState} from "react";
import {approve,getArtifact,getArtifacts,getDemoData,getTraceability,runWorkflow} from "./api/client";
import {AgentAuditTrail} from "./components/AgentAuditTrail";
import {ApprovalGate} from "./components/ApprovalGate";
import {ApprovalStatus} from "./components/ApprovalStatus";
import {ArtifactGallery} from "./components/ArtifactGallery";
import {ArtifactViewer} from "./components/ArtifactViewer";
import {BusinessImpact} from "./components/BusinessImpact";
import {DashboardCards} from "./components/DashboardCards";
import {RequirementInput} from "./components/RequirementInput";
import {TraceabilityGraph} from "./components/TraceabilityGraph";
import {WorkflowStepper} from "./components/WorkflowStepper";
import "./style.css";
const sample=`Employee Leave Management System\n\nEmployees should be able to submit leave requests and check leave balance. Managers should approve or reject leave requests. The system sends notifications and maintains an audit trail. Insufficient balance and duplicate date ranges must be rejected. Manager approval is mandatory. APIs validate mandatory fields and return clear errors.`;
type Workflow={status:string;stages:string[];artifact_references:string[];approval_gates?:Record<string,string>;agent_audit?:any[];business_impact?:any};
export default function App(){
 const [text,setText]=useState(sample); const [state,setState]=useState<Workflow>({status:"idle",stages:[],artifact_references:[]});
 const [artifact,setArtifact]=useState<{name:string;content:unknown}|null>(null); const [graph,setGraph]=useState<any>(); const [error,setError]=useState(""); const [busy,setBusy]=useState(false);
 useEffect(()=>{getArtifacts().then(data=>setState(current=>({...current,artifact_references:data.artifacts}))).catch(()=>undefined)},[]);
 async function action(operation:()=>Promise<Workflow>){setBusy(true);setError("");try{setState(await operation())}catch(cause){setError(cause instanceof Error?cause.message:String(cause))}finally{setBusy(false)}}
 async function show(name:string){try{const result=await getArtifact(name);setArtifact(result)}catch(cause){setError(String(cause))}}
 async function loadGraph(){try{setGraph(await getTraceability())}catch(cause){setError(String(cause))}}
 async function loadDemo(){setBusy(true);setError("");try{setText(JSON.stringify(await getDemoData(),null,2))}catch(cause){setError(cause instanceof Error?cause.message:String(cause))}finally{setBusy(false)}}
 return <><header><div className="hero"><div><span className="eyebrow">THEME B · LOCAL-FIRST AGENTIC DELIVERY</span><h1>From requirement to release.<br/><em>One governed workflow.</em></h1><p>Twelve coordinated agents create implementation-ready evidence while people retain control at critical decisions.</p></div><div className="hero-badge"><strong>100%</strong><span>Local & traceable</span><small>No paid APIs required</small></div></div></header><main>
  <DashboardCards status={state.status} count={state.artifact_references.length}/>
  <RequirementInput value={text} onChange={setText} onRun={()=>action(()=>runWorkflow(text))} onLoadDemo={loadDemo}/>{busy&&<div className="notice">Loading local data or assembling traceable artifacts…</div>}{error&&<p className="error">{error}</p>}
  <section className="panel workflow"><div className="section-title"><div><small>LIVE ORCHESTRATION</small><h2>Delivery workflow</h2></div><span className={`status ${state.status}`}>{state.status.replaceAll("_"," ")}</span></div><WorkflowStepper done={state.stages}/>
   {state.status==="awaiting_brd_approval"&&<ApprovalGate label="BRD" onApprove={()=>action(()=>approve("brd"))}/>} {state.status==="awaiting_code_plan_approval"&&<ApprovalGate label="Code Plan" onApprove={()=>action(()=>approve("code-plan"))}/>}</section>
  <BusinessImpact impact={state.business_impact}/><div className="two-column"><ApprovalStatus gates={state.approval_gates}/><AgentAuditTrail events={state.agent_audit}/></div>
  <ArtifactGallery items={state.artifact_references} onSelect={show}/>{artifact&&<div className="modal-backdrop" onClick={()=>setArtifact(null)}><div className="modal" onClick={e=>e.stopPropagation()}><button className="close" onClick={()=>setArtifact(null)}>×</button><ArtifactViewer title={artifact.name} content={artifact.content}/></div></div>}
  <section className="panel"><div className="section-title"><div><small>KNOWLEDGE LINEAGE</small><h2>Requirement-to-release traceability</h2></div><button onClick={loadGraph}>Load lineage graph</button></div><TraceabilityGraph graph={graph}/></section>
 </main><footer>SDLC Agentic Framework · Hackathon Proof of Concept · Deterministic by design</footer></>;
}
