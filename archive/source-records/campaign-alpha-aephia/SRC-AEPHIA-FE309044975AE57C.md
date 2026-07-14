# Weekly Star Atlas Newsletter #195

## Source metadata

- Source ID: `SRC-AEPHIA-FE309044975AE57C`
- URL: https://aephia.com/star-atlas/weekly-star-atlas-newsletter-195/
- Publisher: Aephia
- Published: 2025-09-01T17:59:29
- Updated: 2025-09-01T18:56:33
- Document type: `NEWSLETTER`
- Extraction confidence: `HIGH`

## Neutral synopsis

Welcome to our 195th newsletter on Star Atlas! This weekly newsletter, published by Aephia Industries, focuses entirely on the development of this ambitious game. Here, we attempt to aggregate all the newsworthy tidbits revealed, primarily by the team, throughout the past week. Star Atlas Summer has officially wrapped up! The third and final Town Hall of this summer took place this past week, closing the season on a high note with a wide range of updates. For the first time, UE5 has been tied into the SAGE economy through a new earnable resource, INK, marking a major step in unifying the game’s experiences. To celebrate, the team hosted a Double XP (and double INK) weekend, giving players…

## Historical importance

Contemporary Aephia coverage preserved as a community-institution source.

## Temporal warning

Operational, economic, governance, and roadmap statements may be historical and require reconciliation with later primary sources.

## Manual review

- Article was modified after publication; review temporal claims against later evidence.

## Extracted article text

Welcome to our 195th newsletter on Star Atlas! This weekly newsletter, published by Aephia Industries, focuses entirely on the development of this ambitious game. Here, we attempt to aggregate all the newsworthy tidbits revealed, primarily by the team, throughout the past week.
Star Atlas Summer has officially wrapped up! The third and final Town Hall of this summer took place this past week, closing the season on a high note with a wide range of updates. For the first time, UE5 has been tied into the SAGE economy through a new earnable resource, INK, marking a major step in unifying the game’s experiences. To celebrate, the team hosted a Double XP (and double INK) weekend, giving players an early taste of this new system.
At the same time, the team’s home-brewed SAGE Editor Suite was released to the public, allowing everyone to experiment with the tools and mechanics that will define SAGE C4 when it arrives on PTR later this year. Additionally, the team introduced Phantom Starbases to Starbase, shared the roadmap for Holosim, released a new UE5 patch, and launched Star Frame, the team’s brand-new open-source Solana framework set to replace Anchor.
Plenty to cover this week, so let’s dive in!
Star Atlas Summer – Town Hall #3
Summer Town Hall #3
The third and final Star Atlas Town Hall took place this past Wednesday, and unlike many hoped/expected, it did not come with a SAGE C4 PTR launch, or even an announcement as to when this could be expected. That is not to say C4 was not mentioned at all, as Danny (CPO) and his brother Joseph, went over the updated SAGE C4 tools they (vibe-)coded, and showed us many mechanics and relations that, although in need of tuning, we are to expect when C4 does become playable.
We’ll cover some of the major topics below, but, as you’ve come to expect from us, we also wrote a more extensive report on the Town Hall. Lastly, you can, of course, watch the recording to ensure you do not miss a thing.
Star Atlas – UE5 Inventory [showing off Ink]
Inter-nanite Kinematics (INK)
The team introduced a new resource called Inter-nanite Kinematic, or INK for short. It is a new resource that can be earned in UE5 and redeemed in SAGE, which, for the first time, connects UE5 to the grander Star Atlas economy. It provides yet another way to earn in UE5 beyond leveling up to earn Crew Packs. More importantly, this new earning route is fueled by player-to-player trades, rather than the team sponsoring it (as with the crew packs).
For every 100XP earned in UE5 gameplay (through the official matchmaking games that reward XP), players will earn 1 INK. Please note that this is not distributed immediately, but rather periodically by the team.
One INK can be exchanged for 100k Loyalty Points at your Faction’s new Phantom Starbase, which we will discuss below.
Note: For those wondering, the team previously often referred to Black Goo when discussing a similar resource mechanic. That is now INK. Michael axed the name Black Goo.
Double XP Weekend, with double the INK
Double XP Weekend
Unfortunately, it is over by the time you are reading this, but in honor of the introduction of INK, the team hosted a Double XP Weekend in UE5. There, as this suggests, players were able to earn twice as much XP as they ordinarily would. Of course, given the direct coupling between XP and Ink, this would also result in twice the amount of Ink.
The weekend ran from Friday to this past Sunday (yesterday, at the time of publication). The team did not comment on whether we can expect to see more of these going forward, but it seems like a no-brainer to do so, both for PR reasons and to appease the community.
SAGE – Infinite Starbase Update
Shortly after the Town Hall concluded, the team introduced a new type of temporary Starbase, the Phantom Starbase. Each Faction has received exactly one of these, which is positioned on the border between the Safe and Medium Risk Zone.
Lore dictates that these are from another dimension, and we already know they will disappear when C4 is introduced. Jose (Master Lore Writer) is integrating these into the lore of Star Atlas.
These new Starbases come with a number of interesting characteristics that set them apart from all others:
They offer all possible Tier upgrades, even though it is a Tier 1 Starbase. In other words, you can deposit your Tier 1 through Tier 5 upgrade materials here and gain LP as normal.
Bottomless Pits — The demand for upgrades is infinite for all materials. The Starbase will never upgrade to Tier 2, and it has an insatiable hunger for your resources. In short, you can continue to dump materials into these until C4 goes live.
Ephemeral — They are temporary and will not exist in C4. As they can not be upgraded beyond Tier 1 either, dumping materials here will not in any way contribute to your Factions’ starting positions, unlike all of the other Starbases in your Faction.
Holosim
During the Town Hall, John (Product Manager at Star Atlas), better known as XCode in the community, discussed the efforts the team had put in to get the game stable again, while also going over the Roadmap and what to expect for Chapter 2.
You can read more about this in our report, but in essence, the team has been replacing StarComm V2 bottlenecks with direct RPC calls. Because the team is hosting its own testnet, RPC calls are relatively inexpensive compared to when they would need to do this on the mainnet. Note that C4 is built on an upgraded StarComm, which should also mitigate these bottlenecks. By now, the team has succeeded in eliminating most bottlenecks, but they are not stopping until they remove all of them.
Star Atlas – Holosim Roadmap (Green = Done / Yellow = In progress / Gray = To Do)
As to the roadmap, the team is working towards Chapter 2, where they plan to:
Have Players start with a larger starter package of ships, allowing players to get into bigger ships sooner
Add the ability to zoom in on the map and show a different UI at different zoom levels
Have factions start with Safe Zone bases only. Players will need to overtake MRZ bases, which is one of the ways they can earn points for the leaderboard.
Reward players with these additional points by upgrading Starbases.
Enhance the battle UI
Experiment with micro-transactions
Looking at Season 2, the team expects to:
See their work done on Territorial control culminate in an NPC Faction
Integrate the Battle Pass into the new z.ink subscription
Note that the team may launch Chapters 3 and 4 in Season 1 if the timeline supports that. Meaning that this could happen if z.ink gets delayed.
UE5 Patch
A new patch was dropped late last week, before the Double XP weekend kicked off. This importantly introduces Ink to the earnings, while also allowing Ledgers to be connected to the game client. Below we list the full patch notes for your convenience:
Economy:
Added the new exclusive resource Ink. Every 100 XP earned is 1 Ink.
Wallet:
Fixed a bug where hardware wallets weren’t authenticating.
Progression:
Fixed a bug where XP ticking sounds wouldn’t stop properly.
Added new leaderboards for Racing, Arena, and Weapons
Increased Racing XP
Balance:
[BUFF] Increased Shotgun damage and projectile size, reduced range.
[BUFF/UPDATE] Updated Gatling Gun to shoot while spinning up, increased damage, and increased projectile size.
[NERF] Technically a bug fix, but heavy weapons no longer start with ammo. No more getting terrorized by snipers off spawn!
Adjusted spawn default loadout, including Jettie/Bubbie, in legacy gunplay mode.
Adjusted team-based match to place players in teams automatically, instead of choosing your team.
Adjusted team selection to happen between matches; however, full teams can’t be selected.
Adjusted Gun Game weapon cycle – Sniper is now first, and Gatling Gun is now second.
Gunplay:
Fixed some issues causing jittery character movement.
Removed white screen flash FX on respawn.
Adjusted jettie hover to now have the ability to descend by pressing the crouch input.
Fixed an issue where emotes would endlessly loop. ADS and firing now cancel ongoing emotes.
Adjusted Shield and Health bars to show partial bar fill for better fidelity.
Fixed an issue where character LOD can update while viewing the post-match sequence.
Improved visibility when inside a Surge/Zones point zone.
Updated weapon wheel to show correct weapon sizes in your loadout.
Updated weapon swap numerical key binds to not skip numbers due to a weapon’s size.
Added new icons for backstab and jettie boost ramming kills.
Improved the styling of the respawn countdown and the killed by indicator.
Adjusted game mode HUD to be visible during a death sequence
Fixed an issue where the loadout information in the pause menu was not showing the correct data
Racing/Vehicles:
Added racing spectating support.
Fixed an issue where incorrect standings are shown in the post-race sequence.
Fixed an issue where players can start a race stuck in flight mode
Fixed an issue where a player would crash when piloting the Floyd Liner
Fixed gravity issues around some ships with interiors.
Maps:
Fixed an issue on the Gateway map, causing dim light conditions
Fixed various collision issues on Paizul’s Arena
Made various refinements to Exinade
Menu & UI:
Adjusted title menu animations and UI
Updated crew levels tab to show current level, prestige, and correct level page per group track
Updated prestige banners to properly support higher than level 10 prestige
Updated title menu and spectator mode character cycling key binds to Q/E
Fixed inventory filters
Fixed an issue where players would crash when trying to bind a joystick input
Updated background scene for all participants in the lobby when the host switches between arena/racing game modes
Added a toggle button to hide the wallet public key
Optimization:
Optimized audio to be more robust and performant
Implemented significant functionality in various assets to improve CPU performance
Improved character animation CPU cost
Hotfix
Late last week, the team released a hotfix with the following additional changes:
Updated Shotgun to require purple ammo
Reduced Shotgun range and damage
SAGE – Editor Suite
SAGE Editor Suite
The team publicly released and open-sourced their (mostly vibe-)coded SAGE Editor tools.
Danny originally showed these off during the June 4th Town Hall, and the tool set has now been completed. That apparently also marked the moment where the team felt comfortable opening the suite up to the community.
The way it works is that there are data sources that only the team can update, which feed into all the various tools. However, you can make your own temporary adjustments to ensure these are taken into consideration throughout the suite.
Note that many numbers, recipes, and mechanics will very likely change between now and the launch on PTR. As such, don’t take these too seriously just yet. Many are placeholders or have been added without proper review.
The following tools are available:
Loot Matrix — An overview of all (final) components and loot in the game
Ship Configurator — Configure ships with components
Map Editor — View the map of C4 Galia, many metrics, resource distribution, etc
Claim Stakes — Simulate placing Crafting Stakes and expanding them
Crafting Habs — Simulate placing Crafting Habs and expanding them
Crafting Recipes — All Recipes available in C4
Research Nodes — Explore the Career Skill trees and the Council Rank system
Combat Simulator — Select fleets and their composition, then roll the dice to see who wins
Potential z.ink Delay
Michael (CEO) joined Cagy on his stream this past week to explain Holosim and assist Cagy through the first few missions (~90 minutes). If you’re new to the game, give this a watch!
Towards the end, they also discussed z.ink, and Michael revealed that z.ink may not launch in December of this year. He expects that Q1 of 2026 is more likely. He added that the airdrop farming season will kick off sometime during the next two months, which suggests that this could also move back on the timeline a bit.
Star Frame – Town Hall Presentation slide
Star Frame
The team has open-sourced the new foundational library they have been working on for the past two years, which replaces Anchor and is dubbed Star Frame. Star Frame is built on Pinocchio and is a lower-level replacement for Anchor on Solana. The team hopes that many other Solana development teams will recognize the potential of their solution and the numerous benefits it offers over Anchor, particularly when developing more complex on-chain programs.
Star Frame focuses on modularity, performance, and safety. Key components are its Unsized Type System, Account Set Lifecycle, and Trait-based Abstraction.
Beyond the documentation and source code, the team also released a Medium article highlighting this release, providing a deeper dive into the traits and components. If you are a Solana developer, this is a must-see!
Star Atlas – Galactic Marketplace Interface Upgrade
News Bits
To wrap this issue up, here are three small updates worth mentioning:
The Galactic Marketplace has received a new lick of paint.
During the stream with Cagy, Michael shared that the team’s ambition is to adapt the Port of Entry in SAGE Starbased so that when you move your assets out of Starbased, they are seamlessly migrated to C4 on z.ink, without any extra effort.
Michael shared that the team is thinking about adding combat to Starbased before C4’s release. Nothing final on this, however.
Michael not only discussed Star Atlas with Cagy last week. The two guys from Hold Up also had a great interview with him. Check it out on X!
That is it for this week. Thank you for reading!
