from client import RaftJointConsensus

cluster = RaftJointConsensus(["N1", "N2", "N3"])
print("3-node cluster quorum with ['N1', 'N2']:", cluster.check_majority(["N1", "N2"]))

cluster.enter_joint_consensus(["N2", "N3", "N4", "N5"])
print("Joint consensus with ['N1', 'N4']:", cluster.check_majority(["N1", "N4"]))
print("Joint consensus with ['N2', 'N3']:", cluster.check_majority(["N2", "N3"]))

cluster.leave_joint_consensus()
print("Post-transition cluster nodes:", cluster.c_old)
