# Star Atlas Build

## Metadata

- Source ID: `SRC-OFF-FA07F79C3878A4E5`
- URL: https://build.staratlas.com/dev-resources/unreal-engine-tooling/how-to-use-f-kit-blueprints
- Publication date: UNKNOWN
- Updated date: 2026-04-16T16:32:35.000Z
- Original date text: 2026-04-16T16:32:35.000Z
- Author: ATMTA / Star Atlas official publisher
- Publisher: Star Atlas Build / ATMTA
- Document classification: `TECHNICAL_DOCUMENTATION`
- Extraction confidence: `MEDIUM`

## Official Authority Boundary

This record establishes what the named official publisher publicly stated and when. It does not by itself prove execution, independent economic accuracy, historical completeness, or absence of contrary evidence.

## Archival Abstract

Official technical documentation titled “Star Atlas Build.” This record preserves what Star Atlas Build / ATMTA publicly stated at the recorded publication time; claims about delivery, economics, or outcomes remain limited to the wording of the source.

## Products

- ATLAS
- F-KIT

## Actors and Organizations

- None identified.

## Governance

- None identified.

## Lore

- None identified.

## Classified Claims

- How To Use F-Kit Blueprints | Star Atlas Build Skip to contentStar Atlas BuildSearchK Appearance MenuReturn to top How To Use F-Kit Blueprints ​ Create Wallet flow ​ The flow to create a new wallet is pretty straight forward It is enough to call the “CreateNewWallet” function from the SolanaWalletManager.
- From the returned Wallet object it is mandatory to set a new password: this can be done with the “SetPassword” function.
- Then it is mandatory to generate a Mnemonic for the given Wallet.
- This can be done with the “GenerateMnemonic” function.
- The Sting returned is the “SeedPhrase” that can be used to restore the wallet.
- An account can be generated with the “GenerateNewAccount” function.
- Finally, the created wallet can be saved to the local system.
- This is done with the “SetSaveSlotName” and “SaveWallet” functions.
- The SaveSlotName parameter is suggested to be a combination of the wallet name and the public key of the wallet.
- Recover Wallet flow ​ A wallet can be recovered both with “PrivateKey” or “SeedPhrase”.
- In order to restore a wallet you need to create a new Wallet object as shown in the first step of the “Create Wallet Flow”.
- Restore from seed phrase ​ From the created Wallet object, you need to restore the Mnemonic Then, in order to retrieve the accounts, a derivation path must be selected Then it is needed to set a new password for the wallet and save it as seen in the “Create Wallet” flow.
- Restore from private key ​ From the created wallet object, it is enough to call the “ImportAccountFromPrivateKey” Then it is needed to set a new password for the wallet and save it as seen in the “Create Wallet” flow.
- Unlock an existing wallet ​ In order to login to an existing wallet it is enought to retrieve the existing wallet from a “SaveSlotName” using the “GetOrCreateWallet” and then calll the “UnlockWallet” function providing the correct password.

## Official Cross-References

- https://build.staratlas.com/dev-resources/unreal-engine-tooling/how-to-use-f-kit-blueprints
- https://build.staratlas.com/

## Temporal Validity

- Status: `CURRENT_DOCUMENTATION`
- Current validity: `CURRENT_PAGE_NOT_HISTORICAL_PROOF`
- Warning: Official publication does not independently prove successful execution, completeness, or continued current validity.

## Open Questions

- Which claims are independently corroborated or later superseded?

## Preserved Official Text

How To Use F-Kit Blueprints | Star Atlas Build
Skip to contentStar Atlas BuildSearchK
Appearance
MenuReturn to top
How To Use F-Kit Blueprints ​
Create Wallet flow ​
The flow to create a new wallet is pretty straight forward
It is enough to call the “CreateNewWallet” function from the SolanaWalletManager.
From the returned Wallet object it is mandatory to set a new password: this can be done with the “SetPassword” function.
Then it is mandatory to generate a Mnemonic for the given Wallet. This can be done with the “GenerateMnemonic” function. The Sting returned is the “SeedPhrase” that can be used to restore the wallet.
The new Wallet needs at least an account. An account can be generated with the “GenerateNewAccount” function.
Finally, the created wallet can be saved to the local system. This is done with the “SetSaveSlotName” and “SaveWallet” functions. The SaveSlotName parameter is suggested to be a combination of the wallet name and the public key of the wallet.
Recover Wallet flow ​
A wallet can be recovered both with “PrivateKey” or “SeedPhrase”.
In order to restore a wallet you need to create a new Wallet object as shown in the first step of the “Create Wallet Flow”.
Restore from seed phrase ​
From the created Wallet object, you need to restore the Mnemonic
Then, in order to retrieve the accounts, a derivation path must be selected
Then it is needed to set a new password for the wallet and save it as seen in the “Create Wallet” flow.
Restore from private key ​
From the created wallet object, it is enough to call the “ImportAccountFromPrivateKey”
Then it is needed to set a new password for the wallet and save it as seen in the “Create Wallet” flow.
Unlock an existing wallet ​
In order to login to an existing wallet it is enought to retrieve the existing wallet from a “SaveSlotName” using the “GetOrCreateWallet” and then calll the “UnlockWallet” function providing the correct password.
