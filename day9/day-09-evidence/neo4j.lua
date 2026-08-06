
MERGE (c:Customer {id: "C-001"})
MERGE (p:Policy {id: "POL-101"})
MERGE (cl:Claim {id: "CLM-9001"})
MERGE (pr:Provider {id: "P-77"})
MERGE (r:RiskSignal {id: "DISPUTE_SPIKE"})
MERGE (c)-[:HAS_POLICY]->(p)
MERGE (p)-[:HAS_CLAIM]->(cl)
MERGE (cl)-[:USES_PROVIDER]->(pr)
MERGE (pr)-[:HAS_RISK_SIGNAL]->(r);


MATCH path = (:Customer {id: "C-001"})-[:HAS_POLICY]->(:Policy)-[:HAS_CLAIM]->(:Claim)-[:USES_PROVIDER]->(:Provider)-[:HAS_RISK_SIGNAL]->(:RiskSignal)
RETURN path;


MATCH path = (:Customer {id: "C-001"})-[:HAS_POLICY]->(:Policy)-[:HAS_CLAIM]->(:Claim)-[:USES_PROVIDER]->(:Provider)-[:HAS_RISK_SIGNAL]->(:RiskSignal)
RETURN [n IN nodes(path) | n.id ] AS hops, length(path) AS hop_count;



cypher-shell -a bolt://localhost:7687 -u neo4j -p neo4jneo4j --format plain \
"MATCH path = (:Customer {id: 'C-001'})-[:HAS_POLICY]->(:Policy)-[:HAS_CLAIM]->(:Claim)-[:USES_PROVIDER]->(:Provider)-[:HAS_RISK_SIGNAL]->(:RiskSignal)
RETURN [n IN nodes(path) | n.id ] AS hops, length(path) AS hop_count;" \
| tee day-09-graph-path.txt
