# SAGE: Escape Velocity – Everything we know!

## Source metadata

- Source ID: `SRC-AEPHIA-29A1AF8C2ABBD4D0`
- URL: https://aephia.com/star-atlas/sage-escape-velocity-everything-we-know/
- Publisher: Aephia
- Published: 2023-04-23T09:16:51
- Updated: 2023-05-17T09:46:31
- Document type: `REFERENCE`
- Extraction confidence: `HIGH`

## Neutral synopsis

Name: Star Atlas: Golden Era – Escape VelocityPlatform: All (browser game)Device: Desktop (mobile not supported)Release date: April 26th, 2023Designation: Alpha test, limited time window, temporaryStatus: Open to everyone who has 1000 ATLAS available to lock (temporarily) Welcome to this guide on the first playable, on-chain Star Atlas mini-game! Before we kick things off, let’s get some of the important stuff out of the way immediately: Escape Velocity is not SAGE. It’s a stand-alone module that is intended to test the end-to-end communication pipeline and technology behind the movement in the upcoming SAGE

## Historical importance

Contemporary Aephia coverage preserved as a community-institution source.

## Temporal warning

Operational, economic, governance, and roadmap statements may be historical and require reconciliation with later primary sources.

## Manual review

- Article was modified after publication; review temporal claims against later evidence.

## Extracted article text

Name: Star Atlas: Golden Era – Escape VelocityPlatform: All (browser game)Device: Desktop (mobile not supported)Release date: April 26th, 2023Designation: Alpha test, limited time window, temporaryStatus: Open to everyone who has 1000 ATLAS available to lock (temporarily)
Welcome to this guide on the first playable, on-chain Star Atlas mini-game! Before we kick things off, let’s get some of the important stuff out of the way immediately:
Escape Velocity is not SAGE. It’s a stand-alone module that is intended to test the end-to-end communication pipeline and technology behind the movement in the upcoming SAGE game.
A secondary objective is to provide some very rudimentary – and temporary – gameplay in the form of a scavenger hunt.
The movement mechanics are not representative of the final game! In SAGE, there will be warping, and impulse movement (and you’ll need to burn R4 to do anything in SAGE).
It will be available for a limited time only.
Before we dive in, let’s first step back and look at the bigger picture!
Video Instead?
If, rather than reading a wall of text, you prefer to get the quick and dirty in video format, check out Metaverse Explorer’s video below!
Note that this written guide goes deeper and contains more information. But the video will definitely get you up to speed quickly!
SAGE
The name SAGE, or Star Atlas: Golden Era, was announced during Solana Breakpoint in early November 2022. Up until that point, everyone referred to this game project as SCREAM. The actual gameplay that would become SAGE was unveiled during a Townhall meeting in early March of 2022.
During that meeting, Michael announced the team had decided to step away from their earlier plans to create a more simplistic and temporary mini-game. Instead, they would build a much more polished game that would stand the test of time, that would provide gameplay much more in line with the description in their Whitepaper. As such, that gameplay would come to overlap with (future) UE5 gameplay, allowing them to share the same on-chain foundation as their Unreal Engine 5 game, saving them time in the process.
In essence, SAGE (or SCREAM back then) would become a 3D (WebGL-powered) browser game, in which you will control your fleets of ships in a Grand Strategy MMO game.
Breaking It Down
After having missed the original deadline (EOY 2022) and realizing the front-end part of SAGE did not meet the team’s expectations, they decided on a more iterative approach for 2023. Instead of waiting for the full game to be released, the team would drip-feed us modules that would slowly expand the possibilities of SAGE, until it would reach the V0 status (originally meant to be the first release).
The release strategy now looks as follows:
Escape Velocity (Movement Test & Scavenger Hunt) [mainnet]
Resource Extracting & Crafting [devnet]
Pre-Alpha (Starbases & Combat) [devnet]
V0 (full version of SAGE; introduces Player-2-player economy, Cargo transfers, Player-2-player refueling) [mainnet]
Note that Escape Velocity is being released on Solana’s mainnet, whereas the next two modules will be released on devnet instead. The reason for this is that these could two greatly impact the economy, which means it is crucial to make sure everything is running smoothly before these are released to the mainnet.
What is Escape Velocity?
Though now carrying the flashy title “Escape Velocity”, the first module’s core goal is to test movement within SAGE. In an effort to make that first module a bit more interesting -and make sure that people would actually show up to participate- the team decided to create some custom code to facilitate a scavenger hunt inside of that module. During this hunt, players will be able to move through the galaxy (or, well, part thereof) and scan for loot.
Your ride in Escape Velocity – Fimbul Lowbie [Concept Art]
Movement Test
Though dubbed the “Movement Test”, we are not actually testing the Movement contract on-chain. In reality, the team wants to test the game server (Starcomm) that sits between the chain and the thousands of clients (your browser) that communicate with it.
Availability
Originally the team shared that they were planning to keep the scavenger hunt operational for at least one month. With the launch of the Never Alone campaign, however, it became clear that Escape Velocity will at least be available until the end of the first Mission (+/- July 11th). of course, depending on how the test goes – and how quickly the available loot is drying up – the team could opt to extend, or (with a heads-up well in advance) even shorten this period. All in all, the team did not guarantee a minimum availability window, so if you want to participate, best not to wait too long!
Galia Expanse
The map will contain 10.000 on-chain sectors, which are neatly laid out in a 100 x 100 grid. Every sector is an on-chain coordinate. You will be able to travel from sector to sector by warping your ship(s) there.
Though this iteration of the Galia Expanse consists of mostly empty space, you will encounter some stars here and there. Unfortunately, you won’t yet be able to visit their systems and check out the planets. And no, sectors with a star do not somehow improve the chance for loot appearing there.
Another thing you won’t see on the map in this test version is the distinction between the faction security zones and medium-risk zones. This is really a temporary map dedicated to Escape Velocity.
Preparations
Transaction Costs
As this game is being launched on mainnet, transactions will come with a standard SOL (gas) fee. This is important to take into account when you want to participate. It means that
The good news is that movement does not cost Fuel in this first installment. In the future, burning Fuel is required to navigate the galaxy, but the team simply did not get around to introducing this in this release.
Movement in Escape Velocity is limited to (non-starpath) warping only (see the SAGE manual). You will be able to jump up to 5 sectors in one go with your ships.
Solana Fees
Besides the transaction costs for movement, there are a few more fees you may want to know about:
Spawning a ship: 0.004012 SOL
Your very first move: 0.00022772 SOL
A regular move: 0.000005 SOL
Despawning a ship will return about half of the amount paid for spawning it.
Locking ATLAS
In order to participate in the scavenger hunt/movement test, you do not need to be registered to a faction, but you will need to lock at least 1000 ATLAS in a custom escrow contract. In other words: this is not the same on-chain program as the ATLAS Locker. Do not lock your ATLAS in the Locker! You can lock 1000 ATLAS several times, each time you do so, you will get control over an additional ship within the game.
Note that you can not lock ATLAS that is currently in the ATLAS Locker!
The ship(s) you will be using in Escape Velocity is a Fimbul Lowbie. For this test, you won’t be able to use your own ships. Though you can use the Fimbul Lowbie in the game, it’s not an asset in your wallet! You can right-click the ship and choose to leave the game, which will get you your 1000 ATLAS back.
Getting Started
To get in, go to sage.staratlas.com, read through & agree with the terms, and connect a wallet that contains at least 1000 ATLAS.
In the menu that follows, simply hit “Play” (or check out the Settings first). After having done so, you are greeted with the game map, consisting of many colored squares (more on that later – see “Where Is Everybody?”).
The first time you enter, you will see a “Spawn a Ship” button in the smack middle of the screen. Click it, lock 1000 ATLAS (should be in the wallet you connected), hit the “Continue” button, and you will see a Fimbul Lowbie appear!
Lock 1000 ATLAS to get a Ship in Escape Velocity
When you enter the game with a new ship, your Fimbul Lowbie (the ship the team selected for you) will spawn in the center of the universe (0, 0). From here, you can move around, scan, and potentially hit the jackpot!
Actions
Once you have a ship in-game, there are three actions it can perform. Clickig on your ship will make three buttons pop up: Warp, Scan, and Observe. Let’s briefly go through each of these.
There are three available actions for each ship.
Warp
Warping allows you to move your ship up to 5 sectors (squares). To be more precise, you can warp up to 5 sectors orthogonally (in a straight line), 3 diagonally, and 4 sectors in between these two directions.
After a ship performs a warp, it can not do so again for 30 seconds. See the Cooldowns section below for more information.
Movement happens on-chain, which means you will have to sign a transaction that will cost you a tiny bit of SOL. Besides time, this is the cost of participating in this test.
Scan
When you perform this action, you will get one of two results. A message will pop up in the bottom center of your screen, letting you know the result. If you are lucky, you will see a “You found loot!” message. if not so, then you will simply see that “The Scan did not reveal anything of interest”.
Oh, Happy Days!
When you hit scan, you will be asked to sign a transaction as well, but this one is more like signing a request. In that sense, it won’t be visible on-chain, and it won’t cost you any SOL.
After a ship performs a warp, it can not do so again for 30 seconds. See the Cooldowns section below for more information.
As scanning a sector is arguably the most interesting action for players to take, we dedicated an entire section to this below!
Observe
This shows you a close-up of your ship in space. It has no other utility. You can pan and move the camera around to view your ship from all sides.
Fleet Overview
Besides the map, your ship(s), and a couple of buttons, there is a big panel hovering over the map that shows some interesting data!
For every sector that contains at least one of your ships, an entry is added showing that sector’s coordinates. In this case (image above), the sector shown has coordinates S18E30. Each sector then shows a list of your ships that are currently present in that sector.
Your ships are identified by an ID (looks like an on-chain address), and show their current status. The ship above is idle, meaning it is not doing anything. You will see this change when you warp a ship to a different sector.
Note that the sector’s name did not change to “In Transit”, this is actually another main entry in the overview. As the ship is in between sectors, it is shown as being “in transit”.
There is another tab here with the title “Discovered”. We’ll get into that pane in the Scanning section below.
Ship Focusing
In the Overview pane, you can hover over a ship’s identifier to highlight it on the map (showing the green movement zone around it). If you click it, your view will speedily move to focus on this ship. If you have a lot of ships, this is the easiest way to quickly navigate from one to the other.
Where Is Everybody?
While you are moving around, you may wonder where everybody else is. At this point in time, the game does not yet render ships from other players in your view. Instead, there is a “heat map” that shows the presence of other ships in your current sector and the ones surrounding it.
There is no other source of information, meaning you will not know what part of the map is quieter without actually going there.
When you hover over a sector, a red diamond on a black background pops up in the lower-right corner. The number displayed next to that diamond is the number of ships currently residing in that sector.
Three different ships are currently within this sector
Fortunately, you can also get a lot of information without moving your mouse cursor around. By just looking at the color of a sector’s square, you can get a lot of information.
In general: the darker the square, the fewer ships are present. If there are 5 or more ships within a single sector, the color will be the brightest. There is no way to see at a glance if there are more than 5 ships, or “just” 5. However, hovering over such sectors will give you the required information.
0 ships
1 ship
2 ships
3 ships
4 ships
5+ ships
Interesting to note: This information is updated in real-time! You will constantly see colors changing, and when you hover over such sectors, you will notice that the number next to the diamond has been updated as well. This is the aspect we are actually testing. Not the contracts, but the Starcomm game server the team built.
Scanning
Each of your ships has the ability to move, scan and claim inside of Escape Velocity. When you perform a scan, you are scanning for potential loot within the sector that the ship is in. Scans are managed off-chain and cost nothing. However, you will still be asked to sign a transaction nonetheless. This transaction does nothing, however, and is not an on-chain transaction. It can be best compared to signing just to prove your identity. This is, in effect, what you are doing here.
Once you reach a good spot, you could potentially sit tight and wait until the loot comes to you. Depending on the number of ships actively participating in the game, and their spread across the map, this could be a good strategy or a less optimal one.
When you perform a scan, your ship will either detect some loot or not. When it does, it is automatically claimed. There is no need to move to any loot, nothing will actually show up on the map. If a scan is successful, the loot is yours!
Regardless of whether you found something, each scan will trigger a (less than) 30-second cooldown (exact number unknown) for that ship, during which its scanning equipment is recharged and can not be used. See the below section on Cooldowns for more information.
If you are the first to successfully find some loot, then it is yours for the taking! If there are others in the same neighborhood who scan a little later, the loot will be gone! They won’t see the loot anymore, as you already (automatically) claimed it.
Claiming Loot
Loot is claimed automatically when you find it!
However, it won’t show up in your wallet right away. The team will drop the loot you gathered once or twice a week (it seems). Initially, you had to wait longer. Though not confirmed, this likely was because they had not yet finished the work on that part of the game.
Whenever your scan is successful, there will be an entry added to your Discovered-pane in the hovering panel that is to the right of your screen. Note that there is currently a limit of 256 items being shown, due to a bug. Any loot you find past that is still being recorded, just not shown in the list (unfortunately).
Loot Logbook
This overview shows you the coordinates where you found the loot and the type (and amount) of loot found. Note that new-found loot entries will state it is currently Processing. After the team has dropped the claims to your wallet, this will instead show Delivered.
Loot
Scanning your sector might result in loot showing up, which you will then be able to claim. There will be numerous lootable items, which the team grouped into 6 different tiers. Note that these items are coming from the team’s own supply, so looting something in-game won’t affect the total supply for that item. This also means that most of these items are offered in limited quantities. It’s likely that the R4 bundles, and the special EV commemorative rewards, are the only ones that have a true limitless supply.
Escape Velocity – Loot Table (updated)
The full list (in text) is:
Copper Tier (99% probability):
[limitless*] A bundle of any of the R4 (Fuel, Ammunition, Food & Toolkits)
10 ATLAS
Bronze Tier (0.9% probability):
1000 ATLAS
[limitless*] Escape Velocity – Central Space Station – Hab Paint
[limitless*] Escape Velocity – Poster
CORE Episode 6
Claim Stake – Tier 1
Silver Tier (0.009% probability):
CORE Episode 4
CORE Episode 5
VZUS solos
Fimbul Airbike
Pearce X4
CSS Land – Tier 0
Gold Tier (0.00005% probability):
Pearce R6
Ogrika Tursic
Fimbul Mamba
CSS Land – Tier 1
Platinum Tier (0.000006% probability):
Ogrika Sunpaa
Pearce D9
Busan Maiden Heart
Diamond Tier (0.0000007% probability):
1 x Fimbul BYOS Tankship
There are two exclusive rewards that can be earned through playing the game, a special poster and hab paint. After Escape Velocity winds down, there is no longer a way to earn these through gameplay. Of course, players will no doubt offer their (excess) copies on the Galactic Marketplace.
* We assume the supply for these items is limitless (during the event). This has not been confirmed by the team!
Loot Spawns
There is a good chance you will want to gather as much loot as possible. In that case, it’s good to know how loot spawning actually works. In Escape Velocity, there is (nearly) always a fixed amount of loot present on the map. Every minute, a process spawns a new loot item for each item claimed in the last 60 seconds by players (there is actually a maximum, but it’s quite generous). In other words, (almost) as soon as somebody claims loot, a new loot bundle will spawn (invisibly, until scanned) somewhere else within the Galia Expanse. This is good news, as it means there will always be loot around, you just have to find it!
When new loot is spawned, an off-chain program will generate a random number and use that to select one of the six loot tiers. As you can see in the previous section, there is an 87% chance this will be the Copper Tier. After the tier has been determined, another randomly generated number will decide which of the items within that Loot Tier will be spawned specifically.
Of course, if an item is no longer available, it will no longer be spawned, and something else will spawn instead.
Loot Table Update
Before the game launched, another Loot Table had been presented, but the numbers have changed since. Though some may lament the changes (Copper Tier ATLAS went from 100 to 10, Copper Tier went from 87% probability to 99%), this is actually a change for good!
The team had received internal feedback that the map was just too empty, and there was hardly any loot to be found. So, they significantly increased the loot present on the map before launch. However, this means that they would race through the available loot with breakneck speed, which was, of course, not their intent. So, they updated the loot-tier probabilities so that the extra loot dropped (due to this change) would be Copper Tier loot.
So, there is now a lot more loot on the map, but by far most of it (99% to be exact) is Copper Tier loot. But this does mean your scans will be successful much more often than they would have been without this change.
Loot Despawns
When loot spawns, it does not stay on the map forever. After a few minutes (there is a range, but exact values are unknown), the loot is respawned, and new loot is spawned somewhere else on the map. Recently the team tweaked some numbers so that loot despawns more quickly.
Cooldowns
Every time you warp a ship, that ship won’t be able to warp again until its warp engines have cooled down sufficiently. This process takes 30 seconds, during which you will see a countdown indicator on top of that ship’s warp action.
Exactly the same applies to scans. Here too, each ship’s scan ability is hit with a 30-second cooldown after having been used.
But there is more! There also exists global cooldowns. These have been specifically added to combat automation (e.g. bots). When you actively employ a few ships, you might never notice this exists. But if you have amassed a huge fleet of Fimbul Lowbies, chances are you will hit this artificial ceiling.
According to the info provided, you will be able to perform the scan action on up to 15 ships within a 30-second window. In other words, when you click the scan action on 15 ships within 30 seconds, that is cool. But for every ship after the 15th (so, 16th, 17th, etc), you will not be allowed to scan within that same 30 seconds.
There is no cooldown indicator visible on ships beyond the 15th, but you will get the following message at the bottom of your screen: “Please wait for other scans to cool down”.
To spare you the math: You can perform a scan on one of your ships every 2 seconds without hitting this global cooldown.
“Scan, scan, scan!”
Managing (Multiple) Ships
Instead of playing around with a single ship, you can add as many as you want, provided you have the ATLAS to get them. There are two buttons at the bottom left corner of your screen that allow you to add ships and remove them.
Clicking on “Spawn a Ship” will right away trigger a transaction. Once successful, a new ship will appear in the center of the map. This means it (likely) won’t be near your other one(s) (unless you did not move that one very far or at all).
Clicking the “Despawn Ships” option will toggle a pop-up that shows you an overview of your ships and a “Despawn” button next to each of them. Clicking this button will toggle another popup that explains the ship will be removed from the game and your 1000 ATLAS returned. If you continue, an on-chain transaction will be performed, which you will have to sign to enact this.
Escape Velocity – First Surge Event
Surge Events
The team recently introduced so-called Surge Events in Escape Velocity. These events last several days, during which the non-Copper tier probabilities are increased. In effect, this means your chance of finding rarer loot is increased during that time window.
The first such event took place from May 12th till May 15th, but it’s expected more are forthcoming!
Updates
The team is already looking to update Escape Velocity soon! In the near future, some of the loot will consist of multiple charges. You will be able to claim one of these, but not all. Others, however, will be able to claim a charge as well. In other words, this makes it more interesting to go scavenge the map with a friend of a guild member close by, so you can give them a decent chance to claim it as well!
Note: There is no ETA on this new feature yet.
For now, enjoy the hunt!
Last updated May 17th
