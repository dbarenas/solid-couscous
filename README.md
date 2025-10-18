# solid-couscous  
**Protocol:** Reputation-Aware Web of Trust for Encrypted Content  

**Principal Developer:** David Buitrago Arenas ([dabuiar@gmail.com](mailto:dabuiar@gmail.com))  

---

# ReputationChain Protocol Specification (Draft v1.0)

**Title:** A Reputation-Aware Web of Trust Protocol for Encrypted Content Lineage  
**Version:** 1.0 DRAFT  
**Status:** Protocol Outline  
**Date:** October 18, 2025  

---

## 1. Introduction

The **ReputationChain Protocol** defines a mechanism for establishing a verifiable, confidential, and reputation-aware chain of custody for digital content shared across decentralized networks. It combines **public-key cryptography** (Web of Trust), **content addressability** (Chain Linkage), and a **reputation model** (Accountability Ledger) to ensure that every participant is held accountable for the authenticity and lineage of the content they distribute.

---

## 2. Core Data Structures

### 2.1 Message Envelope ($\mathcal{E}$)

The fundamental unit of exchange, encapsulating the confidential content, key material, and cryptographic proofs for verification.

$$
\mathcal{E} = \{C, E_K, \text{Sig}, \text{parent\_sig\_id}, \text{root\_fp}, \text{endorsements}[]\}
$$

| Field | Type | Description |
| :--- | :--- | :--- |
| **$C$** | `Ciphertext` | The message body encrypted with the session key $K_s$. |
| **$E_K$** | `EncryptedKey` | $K_s$ encrypted with the recipient's public key, $E(\text{Pub}_{\text{Recipient}}, K_s)$. |
| **Sig** | `Signature` | Digital signature over the content hash and chain linkage. |
| **parent\_sig\_id** | `HashID` | A reference to the **Sig** of the immediately preceding Message Envelope in the chain. Null for the originating envelope. |
| **root\_fp** | `Fingerprint` | The Public Key Fingerprint of the original creator (Source of Provenance). |
| **endorsements**[] | `List<I>` | An optional array of Endorsement Objects ($\mathcal{I}$) from third-party keys. |

---

### 2.2 Endorsement Object ($\mathcal{I}$)

A cryptographic assertion by a third-party key attesting to the perceived veracity and chain integrity of the associated message hash.

$$
\mathcal{I} = \{\text{issuer\_fp}, \text{endorse\_sig}\}
$$

| Field | Type | Description |
| :--- | :--- | :--- |
| **issuer\_fp** | `Fingerprint` | The Public Key Fingerprint of the endorser. |
| **endorse\_sig** | `Signature` | Signature by $\text{Priv}_{\text{Issuer}}$ over $\text{Hash}(M)$. |

---

### 2.3 Reputation Ledger Entry ($\mathcal{L}$)

A record maintained within a secure, globally verifiable ledger (e.g., a blockchain or distributed hash table) that maps a public key fingerprint to an associated trust score and history.

$$
\mathcal{L}_{\text{fp}} = \{\text{fingerprint}, \text{reputation\_score}, \text{action\_log}\}
$$

| Field | Type | Description |
| :--- | :--- | :--- |
| **fingerprint** | `Fingerprint` | Unique Public Key Identifier. |
| **reputation\_score** | `Integer/Float` | The cumulative credibility score, beginning at a default value (e.g., 100). |
| **action\_log** | `List<Event>` | A history of transactions affecting the score (Endorsements, Penalties). |

---

## 3. Protocol Operations

### 3.1 Initial Message Creation (Alice)

1. **Key Generation:** Alice generates a random symmetric session key $K_s$.  
2. **Encryption (Content):**  
   $$
   C = E(K_s, M)
   $$
3. **Encryption (Key):**  
   $$
   E_K = E(\text{Pub}_{\text{Bob}}, K_s)
   $$
4. **Provenance:** Alice defines the content hash $h = \text{Hash}(M)$ and sets $\text{root\_fp} = \text{Fingerprint}(\text{Pub}_{\text{Alice}})$.  
5. **Signature/Chain Link:**  
   $$
   \text{Sig} = \text{Sign}(\text{Priv}_{\text{Alice}}, h \ \| \ \text{null} \ \| \ \text{root\_fp})
   $$
6. **Transmission:** Alice broadcasts the Envelope $\mathcal{E}$ to Bob.

---

### 3.2 Content Resharing (Chain Extension) (Bob → Charlie)

When Bob shares the *original, unmodified* content:

1. **Verification:** Bob verifies Alice’s $\text{Sig}$ using $\text{Pub}_{\text{Alice}}$.  
2. **Chain Linkage:**  
   $\text{parent\_sig\_id} = \text{Sig}_{\text{Alice}}$  
3. **Key Re-Encryption:**  
   $$
   E_{K_C} = E(\text{Pub}_{\text{Charlie}}, K_s)
   $$
4. **New Signature:**  
   $$
   \text{Sig}_{\text{Bob}} = \text{Sign}(\text{Priv}_{\text{Bob}}, h \ \| \ \text{parent\_sig\_id} \ \| \ \text{root\_fp})
   $$
5. **Transmission:** Bob sends the new Envelope $\mathcal{E}'$ to Charlie.  
   *Note: The content hash ($h$) and $\text{root\_fp}$ remain identical.*

---

### 3.3 Content Modification (Fork Creation) (Bob → Charlie)

When Bob shares *modified* content $M'$:

1. **New Hash:**  
   $$
   h' = \text{Hash}(M')
   $$
2. **New Chain Link:**  
   $\text{parent\_sig\_id} = \text{Sig}_{\text{Alice}}$  
3. **New Signature (Fork):**  
   $$
   \text{Sig}_{\text{Bob}}' = \text{Sign}(\text{Priv}_{\text{Bob}}, h' \ \| \ \text{parent\_sig\_id} \ \| \ \text{root\_fp})
   $$
   *Note: The $\text{root\_fp}$ remains linked to Alice, but the content hash ($h'$) changes.*

---

### 3.4 Endorsement (Third Party $X$)

1. **Verification:** Issuer $X$ verifies the message $M$ and its chain up to $\text{root\_fp}$.  
2. **Assertion:**  
   $$
   \text{endorse\_sig} = \text{Sign}(\text{Priv}_X, \text{Hash}(M))
   $$
3. **Inclusion:** $X$ attaches $\mathcal{I}$ to the message envelope’s $\text{endorsements}[]$ array.  
4. **Reputation Update (Positive):**  
   $$
   \mathcal{L}_{\text{fp}_X}.\text{reputation\_score} \leftarrow \mathcal{L}_{\text{fp}_X}.\text{reputation\_score} + \Delta_{\text{Endorse}}
   $$

---

## 4. Reputation Management and Accountability

### 4.1 Chain Verification

Recipients verify $\mathcal{E}$ recursively by checking:  
1. **Content Integrity:** $\text{Sig}$ is valid for the hash $h$.  
2. **Chain Integrity:** $\text{parent\_sig\_id}$ refers to a valid previous signature linking back to $\text{root\_fp}$.

---

### 4.2 Penalty Enforcement (Fake Content / Misinformation)

If a message $M$ is verified as **FALSE** or malicious:

1. **Lineage Trace:** Identify all keys that:  
   - **Signed** or **endorsed** the malicious or derivative messages.  
2. **Penalty Application:**  
   $$
   \mathcal{L}_{\text{fp}}.\text{reputation\_score} \leftarrow \mathcal{L}_{\text{fp}}.\text{reputation\_score} - \Delta_{\text{Penalty}}
   $$
   *Penalty magnitude ($\Delta_{\text{Penalty}}$) may depend on chain depth or severity.*

---

### 4.3 Trust Weighting

Trust assigned to any message or endorsement is derived from its key’s reputation:

$$
\text{Trust\_Weight}(\text{Sig}) = f(\mathcal{L}_{\text{Signer\_fp}}.\text{reputation\_score})
$$

If the reputation falls below a threshold, the system flags signatures as **Low-Trust**, **Ignored**, or **Extreme Caution**.

---

## 5. License

**MIT License**

