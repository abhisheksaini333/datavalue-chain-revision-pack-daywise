from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

class IncidentState(TypedDict):
    incident_id: str 
    evidence: str 
    plan: str 
    approval: str 
    final_state: str

def monitor(state: IncidentState):
    print("node monitor: claims feed schema drift detetcted")
    return { "evidence": "dbt test failed: claim_amount missing" }

def diagnose(state: IncidentState):
    print("node diagnose: claim_amount missing; amount_paid present")
    return { "evidence": state["evidence"] +  "; candidate=amount_paid" }

def plan_fix(state: IncidentState):
    print("node plan_fix: propose mapping amount_paid -> claim_amount, confidence 0.72")
    return { "plan": "map amount_paid to claim_amount in staging (confidence 0.72)" }

def human_approval(state: IncidentState):
    decision = interrupt({
        "question": "Approve schema mapping ?",
        "plan": state["plan"],
        "evidence": state["evidence"]
    })
    print(f"node human_approval: approval = {decision}")
    return { "approval": decision }

def apply_repair(state: IncidentState):
    if state["approval"] != "approved":
        print("node apply_repair: BLOCKED - no approval")
        return { "final_state": "waiting_for_approval" }
    print("node apply_repair: schema mapping aplied in staging")
    return { "final_state": "repair_applied" }

def verify(state: IncidentState):
    if state["final_state"] != "repair_applied":
        return { "final_state": "waiting_for_approval" }
    print("node verify: required columns present; duplicate count 0")
    return { "final_state": "verified" }


builder = StateGraph(IncidentState)

for name, fn in [("monitor", monitor), ("diagnose", diagnose), ("plan_fix", plan_fix), ("human_approval", human_approval), ("apply_repair", apply_repair), ("verify", monitor)]:
    builder.add_node(name, fn)


builder.add_edge(START, "monitor")
builder.add_edge("monitor", "diagnose")
builder.add_edge("diagnose", "plan_fix")
builder.add_edge("plan_fix", "human_approval")
builder.add_edge("human_approval", "apply_repair")
builder.add_edge("apply_repair", "verify")
builder.add_edge("verify", END)

graph = builder.compile(checkpointer=InMemorySaver())
config = { "configurable": { "thread_id": "INC-CLAIMS-007" }}

print("===== RUN 1: start incident =====")
result = graph.invoke({ "incident_id": "INC-CLAIMS-007" }, config=config)


if "__interrupt__" in result:
    print(" GRAPH PAUSED at interrupt: ", result["__interrupt__"][0].value["question"])

snapshot = graph.get_state(config)
print("   checkpoint next node: ", snapshot.next)



print("===== RUN 2: owner approves, graph resumes =====")
final = graph.invoke(Command(resume="approved"), config=config)
print("FINAL State:", final["final_state"])