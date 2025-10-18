# Principal Developer: David Buitrago Arenas (dabuiar@gmail.com)
# This module provides a simulated cryptographic provider for the protocol.

import hashlib
import json

class SimulatedCryptoProvider:
    """
    A simulated cryptography provider that mimics cryptographic operations
    for the ReputationChain protocol simulation.

    This class abstracts the hashing, signing, and key fingerprinting
    functionality, making it easy to swap with a real cryptographic library.
    """

    def hash_data(self, data):
        """
        Simulates a cryptographic hash (e.g., SHA-256) for content or linkage.
        """
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def sign_data(self, private_key_id, data_to_sign):
        """
        Simulates digital signing using a private key identifier.
        """
        # The signature is a combination of the key ID and a hash of the data
        return f"SIG_{private_key_id}_{self.hash_data(data_to_sign)[:8]}"

    def get_fingerprint(self, public_key_id):
        """
        Simulates generating a persistent public key fingerprint.
        """
        # The fingerprint is a simplified, predictable representation of a public key
        return f"FP_{public_key_id.upper()[:6]}"