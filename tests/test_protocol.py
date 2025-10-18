import unittest
import json
from reputation_chain.crypto import SimulatedCryptoProvider
from reputation_chain.ledger import ReputationLedger
from reputation_chain.entities import Actor
from reputation_chain import protocol

class TestReputationChainProtocol(unittest.TestCase):

    def setUp(self):
        """Set up a common environment for all tests."""
        self.crypto = SimulatedCryptoProvider()
        self.ledger = ReputationLedger()
        self.alice = Actor("Alice", self.crypto)
        self.bob = Actor("Bob", self.crypto)
        self.carol = Actor("Carol", self.crypto)
        self.david = Actor("David", self.crypto)
        self.original_message = "The secret plan is code Red."

    def test_chain_of_custody_and_penalties(self):
        """
        Verify that the chain of custody is correctly established and that
        penalties are applied to all involved parties.
        """
        # 1. Create the initial message from Alice to Bob
        env_a = protocol.create_initial_message(
            self.original_message, self.alice, self.bob, self.crypto
        )
        self.assertEqual(env_a.root_fp, self.alice.fingerprint)
        self.assertEqual(env_a.parent_sig_id, "NULL_ROOT")

        # 2. Bob reshares the message with Carol
        env_b = protocol.reshare_message(
            self.original_message, env_a, self.bob, self.carol, self.crypto
        )
        self.assertEqual(env_b.parent_sig_id, env_a.Sig)
        self.assertEqual(env_b.root_fp, self.alice.fingerprint) # Root remains the same

        # 3. David endorses the message
        endorsement = protocol.endorse_message(env_b, self.david, self.ledger, self.crypto)
        self.assertEqual(self.ledger.get_score(self.david.fingerprint), 105)
        self.assertIn(endorsement.to_dict(), env_b.endorsements)

        # 4. The chain is flagged, and penalties are applied
        chain = [env_a, env_b]
        actors = [self.alice, self.bob, self.david]

        culprits = protocol.penalize_chain(chain, actors, self.ledger, penalty_amount=-25)

        # 5. Verify that all involved parties were penalized
        self.assertIn(self.alice.fingerprint, culprits)
        self.assertIn(self.bob.fingerprint, culprits)
        self.assertIn(self.david.fingerprint, culprits)

        # 6. Verify final scores
        self.assertEqual(self.ledger.get_score(self.alice.fingerprint), 75)
        self.assertEqual(self.ledger.get_score(self.bob.fingerprint), 75)
        self.assertEqual(self.ledger.get_score(self.david.fingerprint), 80) # 105 - 25

if __name__ == '__main__':
    unittest.main()