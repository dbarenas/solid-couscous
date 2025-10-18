class EndorsementObject:
    """
    Represents a third-party affirmation (I) of a message's content.

    An endorsement is a cryptographic signature from a third party (the issuer)
    over the hash of the original content, signifying their trust in it.
    """
    def __init__(self, issuer_key, content_hash, crypto_provider):
        self.issuer_fp = crypto_provider.get_fingerprint(issuer_key)
        # The signature links the endorser directly to the content hash
        self.endorse_sig = crypto_provider.sign_data(issuer_key, content_hash)

    def to_dict(self):
        """Returns a dictionary representation of the endorsement."""
        return {'issuer_fp': self.issuer_fp, 'endorse_sig': self.endorse_sig}


class MessageEnvelope:
    """
    The complete package for exchange (E), encapsulating content, lineage,
    and authenticity proofs.

    This class relies on a crypto provider to handle all cryptographic
    operations, adhering to the dependency inversion principle.
    """
    def __init__(self, content, sender_key, recipient_pub_key, crypto_provider,
                 parent_sig_id=None, root_fp=None, prev_envelope=None):

        self.crypto_provider = crypto_provider

        # 1. CONFIDENTIALITY (Simulated)
        self.C = f"Encrypted({content})"
        self.E_K = f"EncryptedKey({recipient_pub_key})"

        # The content hash is based on the original message for provenance
        self.content_hash = self.crypto_provider.hash_data(content)

        # 2. PROVENANCE & LINEAGE
        self.root_fp = root_fp or self.crypto_provider.get_fingerprint(sender_key)

        if prev_envelope:
            self.parent_sig_id = prev_envelope.Sig
        else:
            self.parent_sig_id = parent_sig_id or "NULL_ROOT"

        # 3. AUTHENTICITY & INTEGRITY
        data_to_sign = (self.content_hash, self.parent_sig_id, self.root_fp)
        self.Sig = self.crypto_provider.sign_data(sender_key, data_to_sign)

        # 4. REPUTATION
        self.endorsements = []

    def add_endorsement(self, endorsement_obj):
        """Adds a third-party endorsement to the message."""
        self.endorsements.append(endorsement_obj.to_dict())

    def to_dict(self):
        """Returns a dictionary representation of the envelope."""
        return {
            "C": self.C,
            "E_K": self.E_K,
            "Sig": self.Sig,
            "parent_sig_id": self.parent_sig_id,
            "root_fp": self.root_fp,
            "content_hash": self.content_hash,
            "endorsements": self.endorsements
        }