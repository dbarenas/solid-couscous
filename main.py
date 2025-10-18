# Principal Developer: David Buitrago Arenas (dabuiar@gmail.com)
# This module orchestrates the ReputationChain protocol simulation.

import json
from reputation_chain.crypto import SimulatedCryptoProvider
from reputation_chain.ledger import ReputationLedger
from reputation_chain.entities import Actor
from reputation_chain import protocol

def run_simulation():
    """
    Orchestrates the entire ReputationChain protocol simulation, from setup
    to final verification and accountability.
    """
    print("--- ReputationChain Protocol Simulation (SOLID Refactor) ---")

    # 1. SETUP
    crypto = SimulatedCryptoProvider()
    ledger = ReputationLedger()

    # Create actors (participants)
    alice = Actor("Alice", crypto)
    bob = Actor("Bob", crypto)
    carol = Actor("Carol", crypto)
    david = Actor("David", crypto)

    original_message = "The secret plan is code Red."

    # 2. PROTOCOL EXECUTION

    # Alice creates the first message for Bob
    envelope_A = protocol.create_initial_message(original_message, alice, bob, crypto)
    print(f"Message Hash (H): {envelope_A.content_hash}")
    print(f"Root Fingerprint (FP): {envelope_A.root_fp}")
    print(f"Signature (SIG): {envelope_A.Sig}")

    # Bob reshares the message with Carol, extending the chain
    envelope_B = protocol.reshare_message(original_message, envelope_A, bob, carol, crypto)
    print(f"Previous Sig (Parent): {envelope_B.parent_sig_id}")
    print(f"New Signature (SIG): {envelope_B.Sig}")

    # David endorses the message from Bob's share
    protocol.endorse_message(envelope_B, david, ledger, crypto)

    # 3. ACCOUNTABILITY & PENALTY
    # An external entity flags the content as fake, triggering a penalty
    chain_of_custody = [envelope_A, envelope_B]

    # Manually add Bob's fingerprint to the culprits for the simulation
    culprits = {alice.fingerprint, david.fingerprint, bob.fingerprint}

    print(f"\n[PENALTY] Keys to penalize: {list(culprits)}")

    for fp in culprits:
        ledger.update_score(fp, -20, "Propagated/Endorsed fake content")

    # 4. FINAL STATE
    print("\n--- FINAL LEDGER STATE ---")
    print(json.dumps(ledger.ledger, indent=4))

    print("\n--- CONCLUSION ---")
    print("The final message envelope contains all elements for full verification:")
    print(json.dumps(envelope_B.to_dict(), indent=4))
    print("\n**The refactored system demonstrates:**")
    print("1. **Separation of Concerns:** Crypto, Core, Ledger, and Protocol are distinct.")
    print("2. **Dependency Inversion:** Components depend on abstractions (CryptoProvider).")
    print("3. **Clear Orchestration:** main.py clearly drives the simulation.")

if __name__ == '__main__':
    run_simulation()