from .core import MessageEnvelope, EndorsementObject

def create_initial_message(content, sender, recipient, crypto_provider):
    """
    Creates the first message in a new chain (the root).
    """
    print("\n[PROTOCOL] Creating Initial Message (Chain Root) 🌳")
    return MessageEnvelope(
        content=content,
        sender_key=sender.private_key,
        recipient_pub_key=recipient.private_key,
        crypto_provider=crypto_provider
    )

def reshare_message(original_content, previous_envelope, sender, recipient, crypto_provider):
    """
    Reshares an existing message, extending the chain of custody.
    """
    print("\n[PROTOCOL] Resharing Unmodified Message (Chain Extension) ⛓️")
    return MessageEnvelope(
        content=original_content,
        sender_key=sender.private_key,
        recipient_pub_key=recipient.private_key,
        crypto_provider=crypto_provider,
        prev_envelope=previous_envelope,
        root_fp=previous_envelope.root_fp  # Propagate the original root fingerprint
    )

def endorse_message(envelope, endorser, ledger, crypto_provider, endorsement_bonus=5):
    """
    Allows a third party to endorse a message, boosting their reputation.
    """
    print(f"\n[PROTOCOL] {endorser.name} Endorsing Message (Reputation Gain) 👍")
    endorsement = EndorsementObject(
        issuer_key=endorser.private_key,
        content_hash=envelope.content_hash,
        crypto_provider=crypto_provider
    )
    envelope.add_endorsement(endorsement)

    # The endorser gains reputation for their assertion
    ledger.update_score(
        endorsement.issuer_fp,
        endorsement_bonus,
        f"Endorsed content with hash: {envelope.content_hash[:8]}"
    )
    return endorsement

def penalize_chain(chain, actors, ledger, penalty_amount=-20):
    """
    Applies a reputation penalty to all participants in a fraudulent chain.
    This includes the original creator (root), anyone who reshared it,
    and anyone who endorsed it.
    """
    print("\n[PROTOCOL] Content Flagged 'Fake' (Applying Penalties) 🚨")

    culprits = set()
    actor_map = {actor.private_key: actor.fingerprint for actor in actors}

    for envelope in chain:
        # The root of the chain is always culpable
        culprits.add(envelope.root_fp)

        # Find the sender of the current envelope by their signature
        # This is a simulation; a real system would need a more robust way
        # to map signatures back to public keys.
        for key, fp in actor_map.items():
            if key in envelope.Sig:
                culprits.add(fp)

        # Add all endorsers of this envelope
        for endorsement in envelope.endorsements:
            culprits.add(endorsement['issuer_fp'])

    print(f"Keys to penalize: {list(culprits)}")

    for fp in culprits:
        ledger.update_score(fp, penalty_amount, "Propagated/Endorsed fake content")

    return culprits