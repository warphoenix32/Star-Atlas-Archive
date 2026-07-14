# Star Atlas Build

## Metadata

- Source ID: `SRC-OFF-55AABF6C02F3F53E`
- URL: https://build.staratlas.com/dev-resources/on-chain-game-systems/player-profile
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

## Actors and Organizations

- None identified.

## Governance

- None identified.

## Lore

- None identified.

## Classified Claims

- Player Profile | Star Atlas Build Skip to contentStar Atlas BuildSearchK Appearance MenuReturn to top Player Profile ​ Structure of a Player Profile ​ A player profile is an account with a header and then a list of ProfileKey s.
- The header contains meta-information such as the key-threshold (lite-multi-sig for auth keys) and the number of keys in the profile.
- Following this fixed size header are a number of ProfileKey s.
- The same key may appear more than once in a given profile to allow for different scopes and permissions to be added to a given key.
- PermissionKey fields: Field Type Description Purpose key Pubkey The public key that can act as the profile.
- Multi-sig) scope Pubkey Where the key can act as the profile.
- By convention the program id is the widest scope for a program and owned accounts can be used for lower permissions expire_time i64 (timestamp) When the key can no longer act as the profile.
- Allows keys to be ephemeral and act as session keys.
- permissions [u8; 8] What the key can do as the profile.
- By convention a set of bitflags stating what the key can do.
- Can move fleets in a game but not trade resources) Profile Permissions ​ The permissions the player profile program defines for itself are as follows: Permission Bitflag Description AUTH 1 << 0 Super-user authority over the profile.
- ADD_KEYS 1 << 1 Can add keys that have at most its permissions (by bitflag).
- REMOVE_KEYS 1 << 2 Can remove non- AUTH keys.
- CHANGE_NAME 1 << 3 Can change the profile's name.
- The only valid scope for the player profile program is the program id.

## Official Cross-References

- https://build.staratlas.com/dev-resources/on-chain-game-systems/player-profile
- https://build.staratlas.com/

## Temporal Validity

- Status: `CURRENT_DOCUMENTATION`
- Current validity: `CURRENT_PAGE_NOT_HISTORICAL_PROOF`
- Warning: Official publication does not independently prove successful execution, completeness, or continued current validity.

## Open Questions

- Which claims are independently corroborated or later superseded?

## Preserved Official Text

Player Profile | Star Atlas Build
Skip to contentStar Atlas BuildSearchK
Appearance
MenuReturn to top
Player Profile ​
Structure of a Player Profile ​
A player profile is an account with a header and then a list of
ProfileKey
s. The header contains meta-information such as the key-threshold (lite-multi-sig for auth keys) and the number of keys in the profile. Following this fixed size header are a number of
ProfileKey
s. The same key may appear more than once in a given profile to allow for different scopes and permissions to be added to a given key.
PermissionKey
fields:
Field
Type
Description
Purpose
key
Pubkey
The public key that can act as the profile.
Usually a wallet key but can be a program. (ex. Multi-sig)
scope
Pubkey
Where the
key
can act as the profile.
By convention the program id is the widest scope for a program and owned accounts can be used for lower permissions
expire_time
i64
(timestamp)
When the key can no longer act as the profile.
Allows keys to be ephemeral and act as session keys.
permissions
[u8; 8]
What the key can do as the profile.
By convention a set of bitflags stating what the key can do. (ex. Can move fleets in a game but not trade resources)
Profile Permissions ​
The permissions the player profile program defines for itself are as follows:
Permission
Bitflag
Description
AUTH
1 << 0
Super-user authority over the profile.
ADD_KEYS
1 << 1
Can add keys that have at most its permissions (by bitflag).
REMOVE_KEYS
1 << 2
Can remove non-
AUTH
keys.
CHANGE_NAME
1 << 3
Can change the profile's name.
The only valid scope for the player profile program is the program id.
AUTH
​
AUTH
permissions are the super-user of the player profile. There must always be at least
key_threshold
AUTH
keys in the profile.
AUTH
keys count as the super-set of all possible permissions. The only ways to add/remove auth keys is to call the
adjust_auth
instruction. This instruction requires the signatures of at least
key_threshold
(max of old and new)
AUTH
keys. The key threshold is only used to determine the number of signatures required to change the auth keys. It is not used when an
AUTH
key is signing a usage transaction, each auth key is a super-set on its own.
ADD_KEYS
​
ADD_KEYS
permissions allow a key to add new keys to the profile. The new keys must have at most the permissions of the key adding them. This is checked by bitflag comparison between another entry with the same key.
REMOVE_KEYS
​
REMOVE_KEYS
permissions allow a key to remove keys from the profile. This is only allowed for non-
AUTH
keys.
AUTH
keys can only be removed by the
adjust_auth
instruction.
CHANGE_NAME
​
Player profiles includes a profile name that is arbitrary bytes (intended for utf-8 bytes). This name can be changed by any key with
CHANGE_NAME
permissions. These names are non-unique and not even verfied for valid utf-8-ness.
Additional Overhead ​
Player profiles adds 1 account to each transaction as well as 2 instruction bytes and ~2k compute to each instruction. Using player profiles requires direct implementation into your program (or into a middleware program). Player profiles is a wallet replacement so does not require major shifts in each instruction. Player profiles can also be supported alongside normal wallets in programs with a simple ownership check for the signing key.
