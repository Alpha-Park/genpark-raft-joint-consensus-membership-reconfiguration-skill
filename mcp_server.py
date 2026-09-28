import sys
import json
from client import RaftJointConsensus

cluster = RaftJointConsensus(["Node1", "Node2", "Node3"])

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "raft_joint_consensus_eval",
                        "description": "Evaluate quorum under Raft joint consensus membership transition",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string", "enum": ["enter_joint", "check_majority", "leave_joint"]},
                                "nodes": {"type": "array", "items": {"type": "string"}},
                                "votes": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["action"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "raft_joint_consensus_eval":
            act = args["action"]
            if act == "enter_joint":
                cluster.enter_joint_consensus(args.get("nodes", []))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"status": "IN_JOINT", "c_old": list(cluster.c_old), "c_new": list(cluster.c_new)})}]}}
            elif act == "check_majority":
                maj = cluster.check_majority(args.get("votes", []))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"has_majority": maj, "in_joint": cluster.in_joint})}]}}
            elif act == "leave_joint":
                cluster.leave_joint_consensus()
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"status": "FINALIZED", "active_nodes": list(cluster.c_old)})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
