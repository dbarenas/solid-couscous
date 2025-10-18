# Principal Developer: David Buitrago Arenas (dabuiar@gmail.com)
# This module defines the Actor entity for the simulation.

class Actor:
    """
    Represents a participant in the ReputationChain network.

    Each actor has a name and a private key, which is used for all
    cryptographic operations like signing and generating a fingerprint.
    """
    def __init__(self, name, crypto_provider):
        self.name = name
        self.private_key = f"{name}_Key"
        self.crypto_provider = crypto_provider
        self.fingerprint = self.crypto_provider.get_fingerprint(self.private_key)

    def __repr__(self):
        return f"<Actor name='{self.name}' fp='{self.fingerprint}'>"