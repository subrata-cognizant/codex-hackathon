const all=['intake','context','clarification','brd','story','sprint_plan','code_plan','code','review','sanity','release','knowledge_graph'];
export function WorkflowStepper({done=[]}:{done?:string[]}){return <div className="stepper">{all.map(x=><span className={done.includes(x)?'done':'pending'} key={x}>{done.includes(x)?'✓':'○'} {x.replace('_',' ')}</span>)}</div>}
