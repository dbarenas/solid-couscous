# Principal Developer: David Buitrago Arenas (dabuiar@gmail.com)
# This module defines the ReputationLedger for tracking trust scores.

import time

class ReputationLedger:
    """
    The central source of truth for all key reputations (L).

    This ledger maps a public key fingerprint to its reputation score
    and a history of actions that have affected that score.
    """
    def __init__(self):
        # Maps fingerprint (str) to {score: int, history: list}
        self.ledger = {}

    def get_score(self, fp, default_score=100):
        """
        Retrieves the reputation score for a fingerprint.
        If the fingerprint is not in the ledger, it returns the default score.
        """
        return self.ledger.get(fp, {'score': default_score}).get('score', default_score)

    def update_score(self, fp, delta, reason, default_score=100):
        """
        Applies a reputation change (e.g., +5 for endorsement, -20 for penalty).
        """
        if fp not in self.ledger:
            self.ledger[fp] = {'score': default_score, 'history': []}

        self.ledger[fp]['score'] += delta
        self.ledger[fp]['history'].append({
            'time': time.time(),
            'change': delta,
            'reason': reason
        })
        print(f"    [LEDGER UPDATE] FP {fp} score changed by {delta}. New score: {self.ledger[fp]['score']}")