"""Raft Joint Consensus Dynamic Membership Protocol.
100% Python Standard Library.
"""

class RaftJointConsensus:
    """Raft joint consensus membership transition (C_old -> C_old,new -> C_new)."""
    def __init__(self, initial_nodes):
        self.c_old = set(initial_nodes)
        self.c_new = set()
        self.in_joint = False

    def enter_joint_consensus(self, new_nodes):
        self.c_new = set(new_nodes)
        self.in_joint = True

    def check_majority(self, votes):
        votes_set = set(votes)
        old_majority = len(votes_set & self.c_old) > len(self.c_old) // 2
        if not self.in_joint:
            return old_majority
        new_majority = len(votes_set & self.c_new) > len(self.c_new) // 2
        return old_majority and new_majority

    def leave_joint_consensus(self):
        self.c_old = set(self.c_new)
        self.c_new = set()
        self.in_joint = False
