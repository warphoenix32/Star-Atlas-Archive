# Star Atlas Build

## Metadata

- Source ID: `SRC-OFF-585BABA910AC9649`
- URL: https://build.staratlas.com/dev-resources/apis-and-data/fleet-rentals
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

- SAGE
- ATLAS

## Actors and Organizations

- Solana

## Governance

- None identified.

## Lore

- None identified.

## Classified Claims

- Fleet Rentals | Star Atlas Build Skip to contentStar Atlas BuildSearchK Appearance MenuReturn to top Fleet Rentals ​ The SRSLY program enables on–chain rental agreements for fleets in the Star Atlas ecosystem.
- It lets fleet owners create rental contracts and borrowers accept rentals, automate recurring payments via threads, and later cancel, close, or reset rentals.
- This guide provides a comprehensive walkthrough of how to set up your environment, load the program, and interact with key instructions using the updated IDL.
- Program Details ​ Program Name: srsly Version: 1.0.0 (spec: 0.1.0 ) Program Address: SRSLY1fq9TJqCk1gNSE7VZL2bztvTn9wm4VR8u8jMKT Description: SRSLY is a rental contract system for Star Atlas.
- It enables fleet owners to define rental terms (e.g.
- rate, duration, payment frequency) and borrowers to accept rentals using in–game ATLAS tokens.
- Token Used: ATLAS (ATLAS mint address: ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx ) IDL Attachment: srsly (1).json Setting Up Your Environment ​ Before you begin, make sure you have the proper dependencies installed: 🔧 Required Versions ​ Anchor: 0.31.0 Solana CLI: 2.1.6 You can verify your versions with: bash solana --version # Expected: solana-cli 2.1.6 anchor --version # Expected: anchor-cli 0.30.1 If you need updates, follow the standard update procedures for Anchor and Solana CLI.
- Loading the SRSLY Program in a TypeScript Project ​ In your project, set up your Anchor provider and load the SRSLY program as follows.
- Quick Start: Running Sample Scripts ​ Once your environment is set, you can run sample scripts.
- Below are two examples for fetching account data.
- Example: Fetch a Rental Contract Account ​ Assume you have already derived the program–derived address (PDA) for the contract.
- It stores the essential terms, fleet details, and owner information which govern the rental agreement.
- Purpose: • Establish terms for the rental (rental rate, duration limits, and payment frequency).
- • Track the fleet being offered for rent and its ownership details.
- • Maintain the current rental state (or indicate if no rental is active, via a default value such as the system program’s ID).

## Official Cross-References

- https://build.staratlas.com/dev-resources/apis-and-data/fleet-rentals
- https://build.staratlas.com/

## Temporal Validity

- Status: `CURRENT_DOCUMENTATION`
- Current validity: `CURRENT_PAGE_NOT_HISTORICAL_PROOF`
- Warning: Official publication does not independently prove successful execution, completeness, or continued current validity.

## Open Questions

- Which claims are independently corroborated or later superseded?

## Preserved Official Text

Fleet Rentals | Star Atlas Build
Skip to contentStar Atlas BuildSearchK
Appearance
MenuReturn to top
Fleet Rentals ​
The SRSLY program enables on–chain rental agreements for fleets in the Star Atlas ecosystem. It lets fleet owners create rental contracts and borrowers accept rentals, automate recurring payments via threads, and later cancel, close, or reset rentals. This guide provides a comprehensive walkthrough of how to set up your environment, load the program, and interact with key instructions using the updated IDL.
Program Details ​
Program Name:
srsly
Version:
1.0.0
(spec:
0.1.0
)
Program Address:
SRSLY1fq9TJqCk1gNSE7VZL2bztvTn9wm4VR8u8jMKT
Description: SRSLY is a rental contract system for Star Atlas. It enables fleet owners to define rental terms (e.g. rate, duration, payment frequency) and borrowers to accept rentals using in–game ATLAS tokens.
Token Used:
ATLAS
(ATLAS mint address:
ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx
)
IDL Attachment:
srsly (1).json
Setting Up Your Environment ​
Before you begin, make sure you have the proper dependencies installed:
🔧 Required Versions ​
Anchor: 0.31.0
Solana CLI: 2.1.6
You can verify your versions with:
bash
solana --version # Expected: solana-cli 2.1.6
anchor --version # Expected: anchor-cli 0.30.1
If you need updates, follow the standard update procedures for Anchor and Solana CLI.
Loading the SRSLY Program in a TypeScript Project ​
In your project, set up your Anchor provider and load the SRSLY program as follows.
1️⃣ Import Required Dependencies ​
In your TypeScript file, import the necessary modules:
tsx
import { Program, AnchorProvider, BN, setProvider, workspace } from "@coral-xyz/anchor";
import { PublicKey } from "@solana/web3.js";
import { Srsly } from "./srsly"; // Adjust the path to point to your IDL file
2️⃣ Set Up the Anchor Provider ​
Establish your Solana connection and wallet provider:
tsx
const provider = AnchorProvider.local();
setProvider(provider);
3️⃣ Load the SRSLY Program ​
Once the provider is set, load the SRSLY program from your local workspace:
tsx
const program = workspace.Srsly as Program<Srsly>;
console.log("SRSLY Program ID:", program.programId.toBase58());
This confirms that you have the correct program loaded.
Quick Start: Running Sample Scripts ​
Once your environment is set, you can run sample scripts. Below are two examples for fetching account data.
Example: Fetch a Rental Contract Account ​
Assume you have already derived the program–derived address (PDA) for the contract. For example:
tsx
const fleetPublicKey = new PublicKey("..."); // Replace with your fleet's public key
const [contractPDA] = PublicKey.findProgramAddressSync(
[Buffer.from("rental_contract"), fleetPublicKey.toBuffer()],
program.programId
);
async function getContract() {
const contract = await program.account.contractState.fetch(contractPDA);
console.log("Fleet:", contract.fleet.toBase58());
console.log("Rental Rate:", contract.rate.toString());
console.log("Owner:", contract.owner.toBase58());
}
getContract();
Example: Fetch a Rental State Account ​
Derive the rental state PDA using the contract PDA and borrower's key:
tsx
const borrowerPublicKey = new PublicKey("..."); // Replace with your borrower's public key
const [rentalStatePDA] = PublicKey.findProgramAddressSync(
[
Buffer.from("rental_state"),
contractPDA.toBuffer(),
borrowerPublicKey.toBuffer()
],
program.programId
);
async function getRentalState() {
const rental = await program.account.rentalState.fetch(rentalStatePDA);
console.log("Borrower:", rental.borrower.toBase58());
console.log("Rental Effective Rate:", rental.rate.toString());
console.log("Rental End Time:", rental.end_time.toString());
}
getRentalState();
Key Accounts & Structures ​
Rental Contract Account (contractState) ​
This account defines the overall rental contract parameters for a fleet. It stores the essential terms, fleet details, and owner information which govern the rental agreement.
Purpose:
• Establish terms for the rental (rental rate, duration limits, and payment frequency).
• Track the fleet being offered for rent and its ownership details.
• Maintain the current rental state (or indicate if no rental is active, via a default value such as the system program’s ID).
PDA Derivation:
The contract account is derived using the following seed:
• Seeds:
[ "rental_contract", fleet.publicKey ]
For example, in TypeScript:
tsx
const [contractPDA] = PublicKey.findProgramAddressSync(
[Buffer.from("rental_contract"), fleetPublicKey.toBuffer()],
program.programId
);
Data Structure:
Field Name
Type
Description
version
u8
The account version (typically set to 1).
to_close
bool
Flag indicating if the contract is scheduled for closure.
rate
u64
The rental price per period (converted from Stardust to ATLAS).
duration_min
u64
The minimum duration allowed for the rental session.
duration_max
u64
The maximum allowable rental duration.
payments_feq
PaymentFrequency
Enum representing the payment frequency (Daily)
fleet
pubkey
Public key representing the fleet asset being rented.
game_id
pubkey
Identifier for the associated game.
current_rental_state
pubkey
Tracks the PDA of the active rental state. Defaults to system program’s ID when free.
owner
pubkey
The fleet owner’s public key.
owner_token_account
pubkey
Owner’s token account used for receiving rental payments.
owner_profile
pubkey
The owner’s profile account from the Sage program.
bump
u8
The bump seed value from the PDA derivation.
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Rental State Account (rentalState) ​
The Rental State account captures all details specific to an active rental session. It keeps track of payment details, session timings, cancellation status, and the thread that automates recurring payments.
Purpose:
• Record the active rental details including the borrower, effective payment rate, and the overall timeline of the rental.
• Coordinate with a recurring payment thread to automate the transfer of rental fees over the rental period.
PDA Derivation:
This account is derived using:
• Seeds:
[ "rental_state", contractPDA, borrower.publicKey ]
For example, in TypeScript:
tsx
const [rentalStatePDA] = PublicKey.findProgramAddressSync(
[Buffer.from("rental_state"), contractPDA.toBuffer(), borrowerPublicKey.toBuffer()],
program.programId
);
Data Structure:
Field Name
Type
Description
version
u8
The account version (typically 1).
borrower
pubkey
Public key of the user borrowing the fleet.
thread
pubkey
The public key of the thread account managing recurring payments for this rental.
contract
pubkey
The rental contract’s public key associated with this rental session.
owner_token_account
pubkey
The owner’s token account; payments are routed here.
rate
f64
The effective rental rate for this session (after fee adjustments).
start_time
i64
Unix timestamp when the rental session started.
end_time
i64
Unix timestamp when the rental session is scheduled to end.
cancelled
bool
Flag indicating whether the rental was cancelled before the agreed end time.
bump
u8
The PDA bump seed used during derivation.
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
These two accounts work together to support the full lifecycle of a rental: the contract establishes the rules and availability for renting a fleet, while the rental state captures each active session’s details, enabling automated payment processing and control via associated threads.
Feel free to modify the formatting in Notion as needed to match your style preferences.
Detailed Step–by–Step Instruction Guide ​
The following instructions detail how to work with the major functionalities of the SRSLY program using Anchor and the updated IDL.
1️⃣ Create a Rental Contract ​
This instruction creates a new rental contract and registers the fleet with defined terms.
Instruction:
create_contract
​
Key Accounts:
mint: (ATLAS mint account)
owner: (Signer – fleet owner)
owner_token_account: (Owner’s token account; often a PDA)
fleet: (Fleet account from Sage)
owner_profile: (Owner’s profile)
game_id: (Identifier for the game)
contract: (Writable PDA; derived using seeds
[ "rental_contract", fleet.publicKey ]
)
rental_authority: (PDA using seed
"rental_authority"
)
sage_program, token_program, system_program: (For CPI and token transfers)
Arguments:
rate: u64
– Rental price per period
duration_min: u64
– Minimum rental duration
duration_max: u64
– Maximum rental duration
payments_feq: string
– Payment frequency (e.g.,
@daily
)
owner_key_index: u16
– Owner profile key index
Example Usage:
tsx
await program.methods.createContract(
new BN(5000), // rate (in ATLAS)
new BN(1), // minimum duration (days)
new BN(10), // maximum duration (days)
"@daily", // payment frequency
0 // owner key index
).accounts({
owner: ownerPublicKey,
fleet: fleetPublicKey,
owner_profile: ownerProfilePublicKey,
game_id: gameIdPublicKey,
mint: new PublicKey("ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx"),
owner_token_account: ownerTokenAccountPublicKey,
contract: contractPDA,
rental_authority: rentalAuthorityPDA,
sage_program: new PublicKey("sAgezwJpDb1aHvzNr3o24cKjsETmFEKghBEyJ1askDi"),
token_program: new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
system_program: new PublicKey("11111111111111111111111111111111")
}).rpc();
2️⃣ Accept a Rental ​
This call allows a borrower to accept a rental contract. It sets up a rental state, transfers tokens into an escrow account, and creates a recurring payment thread.
Instruction:
accept_rental
​
Key Accounts:
mint: ATLAS mint (provided account)
borrower: Signer accepting the rental
borrower_profile & borrower_profile_faction: (Sage accounts)
borrower_token_account: (Writable, PDA derived from borrower and mint)
fleet: (Writable; must follow
sub_profile
rules)
game_id, starbase, starbase_player: (Sage integration accounts)
contract: (Writable PDA from
[ "rental_contract", fleet ]
)
rental_state: (Writable PDA from
[ "rental_state", contract, borrower ]
)
rental_authority: PDA using seed
"rental_authority"
rental_token_account: (Escrow account for rental payments)
rental_thread: (Thread account for recurring payments)
fee_token_account: (For fee collection)
sage_program, antegen_program, token_program, associated_token_program, system_program: (For CPI and transfers)
Arguments:
amount: u64
– Payment amount
duration: u64
– Duration (in days, etc.)
Example Usage:
tsx
await program.methods.acceptRental(
new BN(5000), // Payment amount in ATLAS
new BN(5) // Rental duration (5 days)
).accounts({
borrower: borrowerPublicKey,
fleet: fleetPublicKey,
game_id: gameIdPublicKey,
borrower_profile: borrowerProfilePublicKey,
borrower_profile_faction: borrowerProfileFactionPublicKey,
rental_state: rentalStatePDA,
mint: new PublicKey("ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx"),
rental_token_account: rentalTokenAccountPDA,
rental_thread: rentalThreadPublicKey,
sage_program: new PublicKey("sAgezwJpDb1aHvzNr3o24cKjsETmFEKghBEyJ1askDi"),
token_program: new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
antegen_program: new PublicKey("AgThdyi1P5RkVeZD2rQahTvs8HePJoGFFxKtvok5s2J1"),
associated_token_program: new PublicKey("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"),
system_program: new PublicKey("11111111111111111111111111111111")
}).rpc();
3️⃣ Pay Rental ​
This instruction handles ongoing rental payments. It transfers tokens from the escrow to the owner, evaluates whether the rental term is complete, and—if needed—finalizes and closes or resets the rental.
Instruction:
pay_rental
​
Key Accounts:
borrower & borrower_token_account: (For sending payment details)
owner & owner_token_account: (For receiving rental payments)
fleet, game_id, starbase, starbase_player: (Related Sage accounts)
contract: (Writable PDA for the rental contract)
rental_state: (Writable current rental state)
rental_authority: PDA for automated execution
rental_token_account: (Escrow account)
rental_thread: (Signer; thread account for payment scheduling)
sage_program, antegen_program, token_program: (For CPI and transfers)
Example Usage:
tsx
const response = await program.methods.payRental().accounts({
borrower: borrowerPublicKey,
borrower_token_account: borrowerTokenAccountPublicKey,
owner: ownerPublicKey,
owner_token_account: ownerTokenAccountPublicKey,
fleet: fleetPublicKey,
game_id: gameIdPublicKey,
starbase: starbasePublicKey,
starbase_player: starbasePlayerPublicKey,
contract: contractPDA,
rental_state: rentalStatePDA,
rental_authority: rentalAuthorityPDA,
rental_token_account: rentalTokenAccountPDA,
rental_thread: rentalThreadPublicKey,
sage_program: new PublicKey("sAgezwJpDb1aHvzNr3o24cKjsETmFEKghBEyJ1askDi"),
antegen_program: new PublicKey("AgThdyi1P5RkVeZD2rQahTvs8HePJoGFFxKtvok5s2J1"),
token_program: new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
}).rpc();
console.log("Thread Response:", response);
The returned value is a ThreadResponse that may include a new trigger or a close–to account if the rental session is finalized.
4️⃣ Cancel Rental ​
This instruction allows the borrower to cancel an active rental early. It updates the rental state (setting a cancellation flag and adjusting the end time) so that final payment logic can refund funds accordingly.
Instruction:
cancel_rental
​
Key Accounts:
borrower: (Signer requesting cancellation)
rental_thread: (Thread account associated with the rental)
contract: (Rental contract account)
rental_state: (Writable PDA representing the active rental)
Example Usage:
tsx
await program.methods.cancelRental().accounts({
borrower: borrowerPublicKey,
rental_thread: rentalThreadPublicKey,
contract: contractPDA,
rental_state: rentalStatePDA
}).rpc();
5️⃣ Close Rental ​
Close an active rental session by processing any remaining payments, deleting the recurring thread, and finalizing the rental state.
Instruction:
close_rental
​
Key Accounts:
borrower: (Signer)
borrower_token_account & owner_token_account: (For final token transfers)
contract: (Rental contract account)
rental_state: (Writable PDA for the active rental)
rental_token_account: (Escrow token account)
rental_authority: (PDA)
rental_thread: (Thread account)
antegen_program, token_program, system_program: (For final transfers and thread deletion)
Example Usage:
tsx
await program.methods.closeRental().accounts({
borrower: borrowerPublicKey,
borrower_token_account: borrowerTokenAccountPublicKey,
owner_token_account: ownerTokenAccountPublicKey,
contract: contractPDA,
rental_state: rentalStatePDA,
rental_token_account: rentalTokenAccountPDA,
rental_authority: rentalAuthorityPDA,
rental_thread: rentalThreadPublicKey,
antegen_program: new PublicKey("AgThdyi1P5RkVeZD2rQahTvs8HePJoGFFxKtvok5s2J1"),
token_program: new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
system_program: new PublicKey("11111111111111111111111111111111")
}).rpc();
6️⃣ Close Contract ​
Shut down a rental contract. If a rental is in progress, final payments are processed before closure. Otherwise, the contract is closed immediately.
Instruction:
close_contract
​
Key Accounts:
owner: (Signer, fleet owner)
contract: (Writable rental contract account)
owner_token_account, rental_token_account, borrower_token_account, rental_state: (Optional accounts if an active rental exists)
fleet, game_id, starbase, starbase_player: (Additional Sage accounts)
rental_authority: (PDA)
sage_program, token_program: (For CPI transfers)
Example Usage:
tsx
await program.methods.closeContract().accounts({
owner: ownerPublicKey,
contract: contractPDA,
sage_program: new PublicKey("sAgezwJpDb1aHvzNr3o24cKjsETmFEKghBEyJ1askDi"),
token_program: new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
}).rpc();
7️⃣ Reset Rental ​
Reset the rental state (for example, after an early cancellation or when cleaning up state). This call uses a Sage CPI call to invalidate the rental.
Instruction:
reset_rental
​
Key Accounts:
fleet, game_id, starbase, starbase_player: (Writable or checked accounts for rental reset)
rental_state: (Must be empty – ensures no active rental state exists)
contract: (Writable rental contract account)
rental_authority: (PDA)
sage_program: (For CPI calls)
Example Usage:
tsx
await program.methods.resetRental().accounts({
fleet: fleetPublicKey,
game_id: gameIdPublicKey,
starbase: starbasePublicKey,
starbase_player: starbasePlayerPublicKey,
rental_state: rentalStatePublicKey, // Should be empty
contract: contractPDA,
rental_authority: rentalAuthorityPDA,
sage_program: new PublicKey("sAgezwJpDb1aHvzNr3o24cKjsETmFEKghBEyJ1askDi")
}).rpc();
PDA Derivation Summary ​
Many key accounts in the SRSLY program are derived using Program Derived Addresses (PDAs).
Rental Contract PDA ​
tsx
const [contractPDA] = PublicKey.findProgramAddressSync(
[Buffer.from("rental_contract"), fleetPublicKey.toBuffer()],
program.programId
);
Rental State PDA ​
tsx
const [rentalStatePDA] = PublicKey.findProgramAddressSync(
[Buffer.from("rental_state"), contractPDA.toBuffer(), borrowerPublicKey.toBuffer()],
program.programId
);
Rental Authority PDA ​
tsx
const [rentalAuthorityPDA] = PublicKey.findProgramAddressSync(
[Buffer.from("rental_authority")],
program.programId
);
Rental Token Account PDA Example ​
Often, the rental token escrow account is derived using a combination of the rental state, the token program, and the ATLAS mint:
tsx
const [rentalTokenAccountPDA] = PublicKey.findProgramAddressSync(
[
rentalStatePDA.toBuffer(),
new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA").toBuffer(),
new PublicKey("ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx").toBuffer()
],
new PublicKey("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
);
Rental Payment Thread PDA ​
tsx
const [rentalThreadPDA] = PublicKey.findProgramAddressSync(
[rentalAuthorityPDA.toBuffer(), rentalStatePDA.toBuffer()],
new PublicKey("AgThdyi1P5RkVeZD2rQahTvs8HePJoGFFxKtvok5s2J1")
);
Program Errors ​
The SRSLY program uses custom error codes to enforce rules and validations throughout its instructions. Each error code provides a descriptive message that helps in diagnosing issues during contract interactions.
Error Code
Error Name
Description
6000
InvalidDurationMinimum
"Invalid duration minimum. Must be between 1 and the duration maximum."
6001
InvalidDurationMaximum
"Invalid duration maximum. Must be greater than or equal to the duration minimum."
6002
InvalidRateCalculation
"The contract rate multiplied by duration exceeds the payment amount."
6003
FleetAlreadyRented
"Fleet is already rented (sub_profile is not empty)."
6004
InvalidRate
"Contract rate must be greater than or equal to 0."
6005
InvalidPaymentFrequency
"Invalid payment frequency. Must be one of: @daily"
6006
InvalidSubProfileInvalidator
"Invalid sub_profile invalidator."
6007
InsufficientCancellationNotice
"Rental time remaining is less than minimum cancellation notice required."
6008
ContractClosed
"The contract is closed."
6009
DevOnlyFrequency
"This frequency is only allowed in development."
6010
ExpectedDailyFrequency
"Expected daily frequency but contract is set differently."
6011
InvalidThreadContext
"Thread has invalid context set."
6012
RentalIsActive
"Rental is still active."
6013
RentalStateExists
"Rental reset requires rental state to not exist."
Key Constants ​
These public keys are essential for interacting with the SRSLY rental program and related Solana programs:
Constant Name
Public Key
Description
SAGE_PROGRAM
SAGE2HAwep459SNq61LHvjxPk4pLPEJLoMETef7f7EE
Sage in-game asset control.
SRSLY_PROGRAM
SRSLY1fq9TJqCk1gNSE7VZL2bztvTn9wm4VR8u8jMKT
SRSLY rental program ID.
ANTIGEN_PROGRAM
AgThdyi1P5RkVeZD2rQahTvs8HePJoGFFxKtvok5s2J1
Thread automation framework.
SYSTEM_PROGRAM
11111111111111111111111111111111
Solana’s system program.
TOKEN_PROGRAM
TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA
SPL token program.
ASSOCIATED_TOKEN_PROGRAM
ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL
Creates associated token accounts.
FACTION_PROGRAM
pFACSRuobDmvfMKq1bAzwj27t6d2GJhSCHb1VcfnRmq
Manages player factions.
GAME_STATE
DeXGvdhyVUMSbmGWZtwFm5NM3q3TmRDKaAF3KgGx3dBJ
Sage global game state. (Will Change)
GAME_ID
GAMEzqJehF8yAnKiTARUuhZMvLvkZVAsCVri5vSfemLr
Unique game instance in Star Atlas.
ATLAS_MINT
ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx
Official
ATLAS
token mint.
Final Remarks ​
Integration with Sage:
Many instructions (like accepting a rental and resetting) require interaction with Sage program accounts (such as the fleet’s
sub_profile
and
sub_profile_invalidator
).
Token Transfers & Escrow:
The program uses the Anchor SPL Token library. Account addresses are derived via a mix of constant seeds and account keys.
Happy Renting on Solana!
Ensure you review the full IDL (attached above) for all details and updates before integration.
