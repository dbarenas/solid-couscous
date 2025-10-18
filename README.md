# solid-couscous
Protocol : Reputation-Aware Web of Trust for Encrypted Content

**Principal Developer:** David Buitrago Arenas (dabuiar@gmail.com)

# ReputationChain Protocol Specification (Draft v1.0)

**Title:** A Reputation-Aware Web of Trust Protocol for Encrypted Content Lineage
**Version:** 1.0 DRAFT
**Status:** Protocol Outline
**Date:** October 18, 2025

---

## 1. Introduction

The **ReputationChain Protocol** defines a mechanism for establishing a verifiable, confidential, and reputation-aware chain of custody for digital content shared across decentralized networks. It combines public-key cryptography (Web of Trust), content addressability (Chain Linkage), and a reputation model (Accountability Ledger) to ensure that every participant is held accountable for the authenticity and lineage of the content they distribute.

---

## 2. Core Data Structures

### 2.1 Message Envelope ($\mathcal{E}$)

The fundamental unit of exchange, encapsulating the confidential content, key material, and cryptographic proofs for verification.

$$\mathcal{E} = \{C, E_K, \text{Sig}, \text{parent\_sig\_id}, \text{root\_fp}, \text{endorsements}[]\}$$

| Field | Type | Description |
| :--- | :--- | :--- |
| **$C$** | `Ciphertext` | The message body encrypted with the session key $K_s$. |
| **$E_K$** | `EncryptedKey` | $K_s$ encrypted with the recipient's public key, $E(\text{Pub}_{\text{Recipient}}, K_s)$. |
| **Sig** | `Signature` | Digital signature over the content hash and chain linkage. |
| **parent\_sig\_id** | `HashID` | A reference to the **Sig** of the immediately preceding Message Envelope in the chain. Null for the originating envelope. |
| **root\_fp** | `Fingerprint` | The Public Key Fingerprint of the original creator (Source of Provenance). |
| **endorsements**[] | `List<I>` | An optional array of Endorsement Objects ($\mathcal{I}$) from third-party keys. |

### 2.2 Endorsement Object ($\mathcal{I}$)

A cryptographic assertion by a third-party key attesting to the perceived veracity and chain integrity of the associated message hash.

$$\mathcal{I} = \{\text{issuer\_fp}, \text{endorse\_sig}\}$$

| Field | Type | Description |
| :--- | :--- |
| **issuer\_fp** | `Fingerprint` | The Public Key Fingerprint of the endorser. |
| **endorse\_sig** | `Signature` | Signature by $\text{Priv}_{\text{Issuer}}$ over $\text{Hash}(M)$. |

### 2.3 Reputation Ledger Entry ($\mathcal{L}$)

A record maintained within a secure, globally verifiable ledger (e.g., a blockchain or distributed hash table) that maps a public key fingerprint to an associated trust score and history.

$$\mathcal{L}_{\text{fp}} = \{\text{fingerprint}, \text{reputation\_score}, \text{action\_log}\}$$

| Field | Type | Description |
| :--- | :--- | :--- |
| **fingerprint** | `Fingerprint` | Unique Public Key Identifier. |
| **reputation\_score** | `Integer/Float` | The cumulative credibility score, beginning at a default value (e.g., 100). |
| **action\_log** | `List<Event>` | A history of transactions affecting the score (Endorsements, Penalties). |

---

## 3. Protocol Operations

### 3.1 Initial Message Creation (Alice)

1.  **Key Generation:** Alice generates a random symmetric session key $K_s$.
2.  **Encryption (Content):** Alice encrypts the message $M$ to create $C$:
    $$C = E(K_s, M)$$
3.  **Encryption (Key):** Alice encrypts $K_s$ for the recipient, Bob:
    $$E_K = E(\text{Pub}_{\text{Bob}}, K_s)$$
4.  **Provenance:** Alice defines the content hash $h = \text{Hash}(M)$ and sets $\text{root\_fp} = \text{Fingerprint}(\text{Pub}_{\text{Alice}})$.
5.  **Signature/Chain Link:** Alice signs the core state to create the first link:
    $$\text{Sig} = \text{Sign}(\text{Priv}_{\text{Alice}}, h \ \| \ \text{null} \ \| \ \text{root\_fp})$$
6.  **Transmission:** Alice broadcasts the Envelope $\mathcal{E}$ to Bob.

### 3.2 Content Resharing (Chain Extension) (Bob $\rightarrow$ Charlie)

When Bob shares the *original, unmodified* content:

1.  **Verification:** Bob verifies Alice’s $\text{Sig}$ using $\text{Pub}_{\text{Alice}}$.
2.  **Chain Linkage:** Bob sets $\text{parent\_sig\_id} = \text{Sig}_{\text{Alice}}$.
3.  **Key Re-Encryption:** Bob re-encrypts $K_s$ for Charlie:
    $$E_{K\_C} = E(\text{Pub}_{\text{Charlie}}, K_s)$$
4.  **New Signature:** Bob signs the transaction, extending the chain:
    $$\text{Sig}_{\text{Bob}} = \text{Sign}(\text{Priv}_{\text{Bob}}, h \ \| \ \text{parent\_sig\_id} \ \| \ \text{root\_fp})$$
5.  **Transmission:** Bob sends the new Envelope $\mathcal{E}'$ to Charlie.
    *Note: The content hash ($h$) and $\text{root\_fp}$ remain identical.*

### 3.3 Content Modification (Fork Creation) (Bob $\rightarrow$ Charlie)

When Bob shares *modified* content $M'$:

1.  **New Hash:** Bob computes a new content hash $h' = \text{Hash}(M')$.
2.  **New Chain Link:** Bob sets $\text{parent\_sig\_id} = \text{Sig}_{\text{Alice}}$.
3.  **New Signature:** Bob signs the modification. This creates a fork, traceable to the original:
    $$\text{Sig}_{\text{Bob}}' = \text{Sign}(\text{Priv}_{\text{Bob}}, h' \ \| \ \text{parent\_sig\_id} \ \| \ \text{root\_fp})$$
    *Note: The $\text{root\_fp}$ remains linked to Alice, but the content hash ($h'$) changes.*

### 3.4 Endorsement (Third Party $X$)

1.  **Verification:** Issuer $X$ verifies the message $M$ and its associated chain up to $\text{root\_fp}$.
2.  **Assertion:** Issuer $X$ creates an endorsement signature over the hash:
    $$\text{endorse\_sig} = \text{Sign}(\text{Priv}_X, \text{Hash}(M))$$
3.  **Inclusion:** Issuer $X$ creates an $\mathcal{I}$ object and attaches it to the message envelope $\mathcal{E}$'s $\text{endorsements}[]$ array.
4.  **Reputation Update (Positive):** Issuer $X$ commits a transaction to the $\mathcal{L}$ where:
    $$\mathcal{L}_{\text{fp}_X} . \text{reputation\_score} \leftarrow \mathcal{L}_{\text{fp}_X} . \text{reputation\_score} + \Delta_{\text{Endorse}}$$

---

## 4. Reputation Management and Accountability

### 4.1 Chain Verification

Any recipient verifies the Envelope $\mathcal{E}$ by recursively checking two conditions:
1.  **Content Integrity:** The signature $\text{Sig}$ is valid for the content hash $h$.
2.  **Chain Integrity:** The $\text{parent\_sig\_id}$ refers to a valid previous signature, linking the content back to the $\text{root\_fp}$.

### 4.2 Penalty Enforcement (Fake Content / Misinformation)

If an authorized governing body (or consensus mechanism) tags a message $M$ as verifiably **FALSE** or malicious:

1.  **Lineage Trace:** The system traverses the entire chain lineage, identifying all keys that:
    * **Signed** the malicious message or any subsequent messages/forks in the chain.
    * **Endorsed** the malicious message or any of its predecessors/successors.
2.  **Penalty Application (Negative):** All identified fingerprints are penalized via a ledger transaction:
    $$\mathcal{L}_{\text{fp}} . \text{reputation\_score} \leftarrow \mathcal{L}_{\text{fp}} . \text{reputation\_score} - \Delta_{\text{Penalty}}$$
    *The penalty value ($\Delta_{\text{Penalty}}$) may be weighted based on the position in the chain or the severity of the misinformation.*

### 4.3 Trust Weighting

A recipient's software uses the reputation score from $\mathcal{L}$ to assign a **Trust Weight** to any incoming message or endorsement.

$$\text{Trust\_Weight}(\text{Sig}) = f(\mathcal{L}_{\text{Signer\_fp}} . \text{reputation\_score})$$

If a key's score falls below a predefined threshold, its signatures and endorsements are flagged as *Low-Trust*, *Ignored*, or displayed with an *Extreme Caution* warning.

---

## 5. License

MIT License

Copyright (c) 2025 David Buitrago Arenas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.