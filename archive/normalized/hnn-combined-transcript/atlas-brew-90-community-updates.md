# Atlas Brew #90 - Community Updates

- **Source ID:** `SRC-HNN-0069`
- **Publisher:** Hologram News Network
- **Source type:** Video transcript
- **Classification:** Community media / secondary reporting unless direct interview or quoted primary material
- **Publication date:** Unknown from transcript
- **Original URL:** Not included in supplied transcript
- **Raw artifact:** `archive/raw/hnn-combined-transcript/The Hologram News Network_combined_transcript(1).txt`
- **Normalized artifact:** `archive/normalized/hnn-combined-transcript/atlas-brew-90-community-updates.md`
- **Timestamp coverage:** 00:06:40–00:59:53
- **Extraction confidence:** MEDIUM

## Synopsis

Transcript segment preserved and normalized for archival ingestion. Semantic claims and historical conclusions are not promoted at this stage.

## Known limitations

- Original video URL and publication date were not present in the supplied combined transcript.
- Speaker identification is not inferred unless explicitly stated in the text.
- Automated corrections are conservative and logged in the campaign correction log.

## Transcript

[00:06:40] Um I posted the link on the chat here in
[00:06:43] The Ampitheater chat for the atlas Rune
[00:06:46] 91 uh where we will be Chris will be
[00:06:49] Coming on stage as well with us and
[00:06:52] We'll be covering just an overall update
[00:06:55] On theas economy and how our economists
[00:06:58] Are watching what is how everything is
[00:07:01] Developing um here in this ATLAS
[00:07:03] Ecosystem so yeah um I see a question
[00:07:08] When the physical copy of the graphic
[00:07:10] Novel will be dropped that's at the end
[00:07:12] At the very end of all the episodes so
[00:07:15] Still some time still some time um
[00:07:20] But other than that did I miss anything
[00:07:22] Don't
[00:07:23] Just no think you got it no yep okay so
[00:07:28] Let's go to the main topic for the
[00:07:30] Today which is community updates um as I
[00:07:34] Said we have a different projects
[00:07:36] Presenting today just a disclaimer uh
[00:07:38] Before we get into that none of these
[00:07:41] Projects are endorsed or audited by
[00:07:43] Theas team the team is just providing a
[00:07:45] Space for them to present to the
[00:07:46] Community and the commune of course has
[00:07:49] To make the decisions to engage with
[00:07:51] These projects and products doing their
[00:07:53] Own research and at their own risk um
[00:07:57] That said we have some really cool
[00:07:59] Projects presenting today um I think
[00:08:02] First we'll have Shadow Legacy with
[00:08:04] Groove coming to Stage so I'll invite
[00:08:07] Groove to
[00:08:08] Stage speak
[00:08:12] First GM Groove how are you doing friend
[00:08:15] Gro GM man you guys hear me all right y
[00:08:18] We a little low if you can maybe
[00:08:21] Turn that maybe I should turn you up
[00:08:23] Actually yeah well okay yeah is that
[00:08:27] Good now yeah s good
[00:08:30] All right
[00:08:31] Perfect I think if I can I can I can
[00:08:35] Share out right yep go for then all
[00:08:38] Right yeah I'll start there I'll just uh
[00:08:40] Share out my screen
[00:08:44] Here let's do that pardon the mess I'm
[00:08:47] Just going to share my whole my whole
[00:08:49] Screen um so uh what we're talking about
[00:08:54] Is a tool that uh my guild uh we
[00:08:59] Actually we rebranded we're Shadow loyal
[00:09:02] Um but still Sly uh so we're Shadow
[00:09:06] Loyal we built this tool to try to give
[00:09:09] Back to the community hopefully make
[00:09:11] Everyone's lives a little bit easier and
[00:09:15] Hopefully add some or showcase a little
[00:09:18] Bit of additional functionality that is
[00:09:22] Possible due to the amazing job that the
[00:09:24] Sa team uh did in developing all of
[00:09:27] These programs so
[00:09:30] Everything uh is open source it's
[00:09:33] Available here on our GI GitHub and uh
[00:09:36] There's a few other tools in there if
[00:09:37] You wanted to look around but this is
[00:09:39] The most relevant one right now lab
[00:09:41] Assistant um one of our members uh was
[00:09:45] Nice enough to take it a b himself to
[00:09:47] Make some cool graphics so we've got
[00:09:49] That going for us uh and one thing that
[00:09:52] I want to mention up front before I
[00:09:53] Really get into everything uh everything
[00:09:57] That we've developed it's it's all very
[00:09:59] Much Community Based we have several
[00:10:01] People that have provided code uh and
[00:10:04] Direct input for the actual
[00:10:07] Development we've got several people
[00:10:09] That are provided resources and te as
[00:10:13] Far as like testing and suggestions
[00:10:15] Recommendations things like that um' got
[00:10:18] The graphics input as well so uh this is
[00:10:21] Not just a solo show this is we've got
[00:10:23] Several people helping us out so Kudos I
[00:10:26] Just kind of wanted to send a shout out
[00:10:27] To everybody that has been involved
[00:10:30] All right now getting into it um so this
[00:10:33] Is all based on uh client side
[00:10:37] JavaScript uh it runs in your browser
[00:10:39] You control the code no code executes
[00:10:42] Unless you authorize it to execute
[00:10:45] Basically uh so the code is available
[00:10:52] Here
[00:10:54] It's pretty it's pretty big we're over
[00:10:57] 3,000 lines of code in here now so
[00:10:59] It would be kind of a pain to audit
[00:11:02] Unfortunately um the one feature that
[00:11:06] I'm going to talk about first is the
[00:11:08] Newest and that is uh an implementation
[00:11:11] Of player profiles so uh
[00:11:15] Sage uh has an npm package and you can
[00:11:20] Browse the folders in the mpm package I
[00:11:23] Don't know if everybody knew that but uh
[00:11:27] One of the libraries within this package
[00:11:30] Is
[00:11:33] Permissions so this gives all the
[00:11:36] Context that we need to actually
[00:11:38] Implement and utilize these permissions
[00:11:41] So I want to make that clear as well
[00:11:43] We're we're not we didn't create this
[00:11:45] Permission system uh star outlist did
[00:11:47] We're just using it so that's all the
[00:11:51] Source code
[00:11:53] There um all right so as far as how it
[00:11:56] Works right so what we're trying to do
[00:11:59] I'm logged in with my uh let's call this
[00:12:02] My main account okay uh Shadow loyal up
[00:12:04] Here starts with
[00:12:07] Ewf um I don't want you guys to be
[00:12:09] Intimidated by my massive single airbike
[00:12:12] Fleet um so yeah just take it's all
[00:12:15] Right uh so this is my one Fleet here
[00:12:18] Right called for Science and I think
[00:12:21] We're all familiar with this we've all
[00:12:22] Seen how Labs works and everything so
[00:12:25] What I want to do is I have a second
[00:12:27] Account over here on my soul flare
[00:12:30] Wallet um this just a like a burner
[00:12:33] Soulare account this Solflare account
[00:12:36] Has not interacted with Labs at all if I
[00:12:39] Were to try
[00:12:41] To see like I have to I haven't even
[00:12:43] Accepted like the agreement or anything
[00:12:45] On here so it hasn't interacted with
[00:12:48] Labs at all it's just
[00:12:50] There what I want to do
[00:12:54] Is set things up so that my soul flare
[00:12:57] Account can control my
[00:13:00] Fleet so that way I don't have to
[00:13:04] Connect with my ledger to interact with
[00:13:08] Sage does that make
[00:13:11] Sense y all right so the way that we do
[00:13:15] That is uh through the lab assistant
[00:13:18] These are the extra little buttons that
[00:13:20] Lab assistant adds right up
[00:13:23] Here I'll go into
[00:13:26] Config and
[00:13:29] I'll click this button that's add
[00:13:31] Restricted
[00:13:33] Account and I just need to copy this is
[00:13:37] Just my public key for that burner
[00:13:40] Account okay so I'm going to drop that
[00:13:41] Public key in here and click add
[00:13:44] Account so this is going to prompt me to
[00:13:48] Authorize this transaction right so from
[00:13:50] My main account I have to authorize it
[00:13:53] No I can't just do this willy-nilly um
[00:13:56] Somebody has to authorize this
[00:13:58] Edition so I'm
[00:14:00] Authorizing this burner account to
[00:14:03] Interact with my sage account hopefully
[00:14:07] That makes sense it can get a little
[00:14:09] Confusing so stop me if uh keeping up so
[00:14:12] Far I'm keeping up so far so far so good
[00:14:17] Okay good so that's that now I'm
[00:14:20] Gonna jump over to my soul flare account
[00:14:23] Okay this is the one that I just
[00:14:25] Added um if I refresh
[00:14:31] And if we give lab assistant just a
[00:14:33] Couple seconds it says wait up here
[00:14:37] Hopefully normally it takes about a
[00:14:40] Minute or so uh if all goes well that'll
[00:14:44] Connect and I'll get the this will
[00:14:46] Change to start there we go so that
[00:14:49] Changes to start now if I go
[00:14:53] Into
[00:14:54] Config this is that same Fleet uh that's
[00:14:58] On my account so now I can through lab
[00:15:03] Assistant interact with this Fleet um so
[00:15:07] Let's just say I wanted it to scan the
[00:15:10] Downside
[00:15:12] Is lab
[00:15:14] Assistant um Can communicate with
[00:15:16] The Fleets but it doesn't provide a
[00:15:19] Whole lot of feedback right now all of
[00:15:21] The feedback is through this status
[00:15:23] Window and Labs itself doesn't support
[00:15:28] Profiles in the same way so if I tried
[00:15:31] To launch I still couldn't connect
[00:15:34] Because uh Labs is trying to
[00:15:37] Use this
[00:15:39] Account it doesn't recognize the
[00:15:42] Profiled account so if I want to monitor
[00:15:46] Things through the lab's UI I still have
[00:15:49] To come back over here so I can see
[00:15:52] Right now that this Fleet
[00:15:54] Is at these coordinates right - 4030
[00:15:58] Because on is awesome so that's that's
[00:16:00] Where I
[00:16:01] Live so I'm going to come in
[00:16:03] Here and I'm going to set up it Al also
[00:16:07] Obviously this won't do anything right
[00:16:09] Because there's nothing to scan for at
[00:16:13] The um Central space station but just
[00:16:16] For demo purposes right so I'm going to
[00:16:19] Set it up to scan I set the coordinates
[00:16:21] That I want to scan
[00:16:23] At uh this is a kind of a newer feature
[00:16:26] Uh whenever you scan
[00:16:29] After the scan is complete you get a
[00:16:31] Response back from uh from Sage that
[00:16:33] Says the probability of finding scus in
[00:16:36] That sector so I can set this to a
[00:16:40] Minimum threshold and what that would do
[00:16:43] Is if that scan after two it will
[00:16:47] Scan in one sector for two minutes and
[00:16:49] After two minutes if that minimum isn't
[00:16:51] Met it moves on to another sector so
[00:16:56] I'll just leave that very useful yeah
[00:16:58] Yeah hopefully yeah it seems to be
[00:17:00] Working out all right so far and in
[00:17:02] Order for that movement function to work
[00:17:05] Um this checkbox needs to be checked as
[00:17:08] Well so that's the minimum to get
[00:17:11] Scanning going right so I've selected
[00:17:13] Scan select the target minimum
[00:17:15] Probability and then either check this
[00:17:18] Or not it's up to
[00:17:20] You um it also optionally supports
[00:17:23] Warping uh the default is to subw warp
[00:17:25] When it moves around but if I check to
[00:17:27] This it would use um warping
[00:17:32] Instead so I can save that oh yeah see
[00:17:41] Uh have to put a shorter distance
[00:17:45] Yeah there we go because uh so what
[00:17:48] Happened there is I did not fill in uh
[00:17:50] The star base
[00:17:52] Destination uh so it defaults to 0 0 uh
[00:17:56] Which was actually causing a bug earlier
[00:17:58] On but that has since been fixed I
[00:18:00] Hope um so it calculates the distance
[00:18:04] Between these two points and it's
[00:18:08] Supposed to act as like a fail safe so
[00:18:10] That you don't accidentally put in you
[00:18:13] Don't typo coordinates and then end up
[00:18:16] Trying to warp or subw warp all the way
[00:18:18] Across the map uh so it checks and make
[00:18:21] Sure that your Fleet actually has enough
[00:18:23] Fuel to go from point A to point B
[00:18:26] Before it allows you to save
[00:18:29] So anyway I can save that and then uh
[00:18:32] When I click Start my little status
[00:18:35] Window over
[00:18:37] Here you'll see right now it won't do
[00:18:39] Anything because it's actually uh docked
[00:18:42] Um
[00:18:44] So in order for any of this to work the
[00:18:48] Fleet has to be the fleet that you want
[00:18:50] To control has to be idle so it can't be
[00:18:54] Docked it can't be mining it can't be
[00:18:57] Crafting oh fleets can't craft but you
[00:18:59] Get the point um so it has to be
[00:19:02] Idle so in order to actually initiate
[00:19:06] This and get the script to work properly
[00:19:11] With it I would have to come back here
[00:19:13] And
[00:19:14] Undock and part of the reason that I
[00:19:16] Didn't do that is because I don't think
[00:19:19] This is a brand new account yeah I
[00:19:21] Don't have any fuel so I can't undock um
[00:19:24] So apologies for that won't make for a
[00:19:26] Great demonstration but um hopefully you
[00:19:30] Can see here that my burner account is
[00:19:34] Interacting with my main account so I
[00:19:38] Could if this were on if this account
[00:19:40] Were on a ledger I could completely
[00:19:42] Disconnect that ledger put it my safe or
[00:19:44] Whatever you want to do with it and not
[00:19:48] Have to mess with it uh for purposes of
[00:19:51] Of this so once I get my fleets idle and
[00:19:54] Into a place where the script can pick
[00:19:55] It up um I would be good to go so that's
[00:20:00] It for
[00:20:02] Profiles uh as far as the actual tool
[00:20:05] Itself some of the capabilities I'll
[00:20:08] Just kind of run through them real quick
[00:20:09] So first I have a status window up here
[00:20:12] Um this will give some high level
[00:20:15] Information on what your fleets are
[00:20:17] Doing if you have a dozen fleets they'll
[00:20:19] All be listed here uh and the state
[00:20:22] Changes between in this case this means
[00:20:24] It's docked um if it's scanning it will
[00:20:27] Show scan with the last known
[00:20:30] Probability uh if it's mining it'll show
[00:20:33] That it's mining with the time stamp for
[00:20:37] When it will be finished
[00:20:39] Mining um if it's moving or warping
[00:20:43] It'll show the estimated time for when
[00:20:45] The warp is finished uh so that's the uh
[00:20:49] That's the status window
[00:20:53] There got this surveillance feature
[00:20:57] That
[00:20:59] Is actually I mean it's pretty helpful
[00:21:02] Still and I I think it's pretty cool
[00:21:06] But it's also mostly superseded by
[00:21:10] Evis tool I don't know if you hopefully
[00:21:13] You guys have all seen that one um some
[00:21:16] Yeah we have it we'll probably C that
[00:21:18] One today as well awesome yeah he's
[00:21:20] A's he's got a really cool tool really
[00:21:22] Cool website and actually we've got a
[00:21:24] Little bit of um integration that we're
[00:21:27] Going to do
[00:21:28] So he's I think he might have already he
[00:21:31] Already beat me to it but um he set it
[00:21:34] Up so that you can export so you can
[00:21:38] Select um you can select coordinates
[00:21:41] For your fleets on his map and then
[00:21:44] Export it so if you have a dozen
[00:21:46] Different places and you want to send
[00:21:48] Your fleets to all of those locations
[00:21:50] You can export those locations and then
[00:21:53] We're going to have an import function
[00:21:56] That will sit right here where you can
[00:21:58] Import those
[00:22:00] Locations so that the script will be
[00:22:05] Able to tell The Fleets that those are
[00:22:07] The new locations now um so it's kind of
[00:22:10] Like a shortcut to configure here if you
[00:22:13] Have a bunch of fleets and if you're
[00:22:15] Using Evis to identify Prime locations
[00:22:18] For scanning or something like
[00:22:21] That so as far as uh functionality right
[00:22:24] So that was the Recon or excuse me
[00:22:26] Surveillance uh that's here the this
[00:22:29] Just shows you how many fleets are
[00:22:31] Currently in each of these locations uh
[00:22:34] You can choose between 3x3 5x5 or 7 by
[00:22:37] Seven squares and uh it will quer the
[00:22:40] Blockchain and determine how many fleets
[00:22:41] Are currently idle at each of these
[00:22:44] Spots um so that was initially helpful
[00:22:48] For scanning uh not so much now but
[00:22:52] Uh we plan to build on this later down
[00:22:55] The line uh I think it will become
[00:22:57] Relevant again when PVP becomes a
[00:22:59] Thing uh so that feature is
[00:23:05] There status I've covered already and
[00:23:07] Then the last thing is config so the
[00:23:10] Tool uh itself
[00:23:13] Supports three different uh I call them
[00:23:15] Assignments but um yeah three different
[00:23:17] Assignments it can scan it can mine and
[00:23:22] It can transport so scanning
[00:23:25] Is relatively self- explanatory the
[00:23:29] Loop is it will travel to the Target
[00:23:34] Destination it will scan while it's
[00:23:37] There and when it is out of toolkits or
[00:23:41] In the case of The Fleets that don't
[00:23:44] Require toolkits when uh the max cargo
[00:23:50] Is getting close if it's getting close
[00:23:52] To being filled it will return to the
[00:23:54] Star base when it returns to Star base
[00:23:57] It unloads Lo s all of the toolkits it
[00:24:00] Resupplies toolkit excuse me it unloads
[00:24:02] All of the uh sdus it resupplies
[00:24:07] Toolkits resupplies
[00:24:08] Fuel and then flies back out to the
[00:24:11] Target location so that's the scanning
[00:24:14] Loop we've also got a mining Loop which
[00:24:17] Supports mining in place so uh in this
[00:24:20] Case right I would just be
[00:24:23] Mining at my
[00:24:26] CSS and you would choose I forget
[00:24:30] CSS has hydrogen I think um so you would
[00:24:34] Mine at this location and dock for
[00:24:38] Resupply at this location so the mining
[00:24:40] Loop is uh
[00:24:42] Dock fill fuel fill
[00:24:46] Ammo
[00:24:48] Undock start Mining and then when the
[00:24:51] Mining is complete it will stop mining
[00:24:55] Dock unload reload so on and so forth so
[00:24:59] That's the mining Loop uh it also does
[00:25:01] Support travel um that's that's also new
[00:25:03] In this version so previously you could
[00:25:06] Only
[00:25:07] Mine and resupply at the same location
[00:25:11] But now it can travel back and
[00:25:13] Forth then the last one and probably the
[00:25:16] Most complicated to configure is the
[00:25:18] Transport um so this allows you to
[00:25:22] Transport whatever
[00:25:24] Resources almost all resources I don't
[00:25:26] Have any craft materials in here aside
[00:25:29] From R4 but uh you can transport those
[00:25:33] Resources from one location to the other
[00:25:37] And then you can Al simultaneously
[00:25:40] Transfer uh on the return trip right so
[00:25:43] Like if I wanted to bring I don't know
[00:25:45] Fuel out to my
[00:25:48] Destination and then end that
[00:25:49] Destination I don't know say I was
[00:25:51] Mining Arco right so I would bring fuel
[00:25:55] To the destination and then on the
[00:25:57] Return trip it would bring back Arco so
[00:26:01] Hopefully uh that makes the
[00:26:04] Transportation uh a little bit easier
[00:26:07] For everyone and uh a little bit more
[00:26:09] Efficient since you can sort of
[00:26:11] Configure up to four resources in each
[00:26:16] Direction the last the last piece is
[00:26:19] Just a an attempt like a convenience
[00:26:23] Feature you can Import and Export your
[00:26:25] Config um I know a lot of people have uh
[00:26:28] Dozens of fleets so it was pretty
[00:26:30] Tedious every time I pushed out a new
[00:26:32] Version their config got wiped um so you
[00:26:35] Can export this uh the export is just is
[00:26:38] Just a copy right because it's just text
[00:26:40] So you just copy it off to notepad or
[00:26:42] Whatever and then you can import it
[00:26:45] Here the end thank you guys for your
[00:26:48] Time thank you man thank you man lots of
[00:26:52] Hard work certainly went to this so
[00:26:55] Congratulations for the two just the um
[00:26:59] Sorry for this but I have to give the
[00:27:01] Disclaimer that none of this is endorsed
[00:27:04] Or audited by theist team so if anyone
[00:27:07] Wants to use the tool um use it at your
[00:27:10] Own risk um but thank you thank you
[00:27:13] Group for presenting my friend sure and
[00:27:15] And one thing that I do want to mention
[00:27:16] On that note um if anybody is interested
[00:27:20] In or curious in doing their
[00:27:23] Own I'm going to say audit but it
[00:27:25] Wouldn't really be an audit right but if
[00:27:27] Anybody just kind of wants a walk
[00:27:28] Through of the code I'm happy to provide
[00:27:29] That um just reach out to me through DM
[00:27:32] And we can hop on a share and kind of go
[00:27:34] Through the
[00:27:35] Code nice y thank you all appreciate
[00:27:39] Your time thank you man thank you man
[00:27:41] Appreciate
[00:27:43] It awesome um now we also have Builders
[00:27:48] More Builders here in this for this brew
[00:27:52] And we'll have th from so a
[00:27:56] Presenting um a tool they have been
[00:27:58] Working on also for stage Labs so th I
[00:28:01] Invited you to
[00:28:06] Stage let's see if he can
[00:28:09] Join welcome
[00:28:12] Welcome thank you thank
[00:28:18] You how are you guys how is it all
[00:28:21] Properly yeah all great man nice oh
[00:28:27] First of all uh thanks to gr to sharing
[00:28:30] All this information all this software
[00:28:33] It's incredible to be honest I'm I'm
[00:28:36] Surprised that I mean it's great
[00:28:39] To see the community creating in this
[00:28:41] Line amazing
[00:28:44] Amazing yeah
[00:28:46] Man okay from my side so have been
[00:28:51] Working in
[00:28:53] Some tools that uh we are trying to
[00:28:56] Finish and to bring here and well from
[00:28:59] Our site it's a teeny update is not
[00:29:02] Too much but it's practical but I think
[00:29:04] That is going to be interesting for
[00:29:06] Us so in this line with your permission
[00:29:09] I will share my screen please go
[00:29:22] Ahead I think you have push to talk also
[00:29:25] Set
[00:29:26] Up
[00:29:28] Yeah I have it I was trying to you
[00:29:30] Know to recharge and all at the same
[00:29:32] Time and yeah with this push it's not so
[00:29:34] Easy for me okay
[00:29:38] Great okay uh like you know or tool is a
[00:29:42] Little
[00:29:43] Extension that what two is to try to
[00:29:46] Integrate and to allows the community to
[00:29:49] Can share their Creations in the
[00:29:53] Into the tension and in this line
[00:29:56] Into the labs
[00:29:57] So our first objective is that the
[00:30:02] Player have not to jump out from the
[00:30:05] From the main bar or from the m page and
[00:30:09] Can have all
[00:30:10] Integrated as you can know uh we have
[00:30:15] Create uh different tools that we
[00:30:17] Integrate like is the
[00:30:18] Map uh like the clock like the
[00:30:23] [Music]
[00:30:24] Crafting and just now uh we are working
[00:30:28] Or we had finished to update one of the
[00:30:30] Things that we told in the past time in
[00:30:32] The past moment
[00:30:39] So looking good looking
[00:30:42] Good uh we have both I mean the
[00:30:45] Integrated part and the outside part is
[00:30:48] So simple like make click twice in the
[00:30:51] Button the first one will uh make appear
[00:30:54] The integrated version the second one
[00:30:56] Will uh bring the popup
[00:30:59] Page okay and about the spaces we have
[00:31:03] To do it in the IDE window in the popup
[00:31:07] One about the bar and this stuff
[00:31:10] So
[00:31:11] And in this line we have dat we have
[00:31:14] Simplification and try to make it more U
[00:31:17] Nice to see and more practical so the
[00:31:19] First thing that we do here is to
[00:31:22] Copy the address of our
[00:31:26] Wallet if he wants to come here we
[00:31:39] Are sorry I was speaking without press
[00:31:42] The
[00:31:45] Sorry
[00:31:47] Yeah okay so I was saying that once that
[00:31:51] We have the wallet copied in
[00:31:55] Our uh in our Mouse
[00:31:57] We only have to CL click into the CBR
[00:32:02] Symbol and we'll bring from cbris with
[00:32:05] Page the fle that we have organiz
[00:32:09] There that we had um that we are
[00:32:11] Managing there so with this we can
[00:32:15] Easily select one of The Fleets this one
[00:32:18] For example the first one and we can go
[00:32:20] To anywhere to see uh to see how is
[00:32:25] Going to be arranged what mean with it
[00:32:27] Is that for example if we click at here
[00:32:31] We can see a little
[00:32:33] Circle that is arrange it means that in
[00:32:36] A visual way you can see quickly until
[00:32:39] Where you can go where you cannot go and
[00:32:41] Which is the no back line or no
[00:32:44] Return line you know this line that once
[00:32:47] That you cross it you have not enough
[00:32:48] Full to come back so you will have
[00:32:51] Toost you have to refu in some sector or
[00:32:55] Something like this so use that you can
[00:32:57] Take care about it so like I was saying
[00:32:59] I'm going to make in a cleaner place for
[00:33:01] Example here with this you have the no
[00:33:05] Back for war it means that once that you
[00:33:08] Cross this circle in this case I think
[00:33:11] That I'm with B strange me B okay so
[00:33:15] That we have the no back
[00:33:17] Warp the here will appear the max warp I
[00:33:21] Mean the maximum range that I can do
[00:33:24] With my little uni bomba and
[00:33:27] At I would say a SARP the no back of
[00:33:31] Surar we can easily see that we had
[00:33:34] Decided to don't put the fourth uh
[00:33:36] Circle because isy to see that it's
[00:33:38] Going to be the double and also you see
[00:33:40] It when you are making the movement
[00:33:43] In the in the interface of Star ATLAS
[00:33:46] Of laps so we thought that it was not
[00:33:49] Necessary we had simplify in this slide
[00:33:52] Okay this one was of one of the things
[00:33:55] That we say that we was going to do and
[00:33:57] We did and
[00:34:00] Now we try to uh implement it some more
[00:34:04] Features some more information so once
[00:34:07] That K is publishing the a lot of dates
[00:34:11] About L about ships about te a lot of
[00:34:15] Information we have drink for it and
[00:34:18] What we decid is to just bring to the
[00:34:21] User the chance of the ability to
[00:34:24] Can click in one of the resources and in
[00:34:28] This sorry the control again and in this
[00:34:31] Line we can see for this specific um
[00:34:37] Resource how much
[00:34:40] Munition food and time you are going to
[00:34:44] Need if you are meaning using this place
[00:34:47] With a richness of one and half and
[00:34:51] A hardness of one in this line we also
[00:34:55] See that our maximum car will be of 244
[00:34:59] 74
[00:35:00] Sorry and it's our way to show or to
[00:35:04] Bring a quickly information to the user
[00:35:06] To the player so and without have to
[00:35:09] Jump from one place to another place
[00:35:11] They can see it quickly how it's going
[00:35:12] To be or how much they need okay these
[00:35:16] Are two of the three features that I'm
[00:35:18] Bringing today I'm going to jump to the
[00:35:20] Third one I don't know if it's a
[00:35:22] Question if it's some curiosity any
[00:35:25] Anything I'll let know if I see any
[00:35:26] Thing in the chat if anyone has any
[00:35:28] Questions for th on the tool he's
[00:35:30] Building uh please shoot it on the on
[00:35:34] The chat I'll let you know if there's
[00:35:35] Any question yes please hit me as
[00:35:38] Strong as you can yeah it's
[00:35:41] Our okay so I continue the last but not
[00:35:45] Less of the features that we had bring
[00:35:48] Is that we have to date we had add a
[00:35:52] Feature in our exension but bring us the
[00:35:55] Market here up in the right we have
[00:35:59] Little bton would bring us the prices of
[00:36:02] The market this line the other L just a
[00:36:06] Second thank
[00:36:08] You so in this line some values are not
[00:36:11] Charged just now but we have the prices
[00:36:15] Of the market in a five minutes window
[00:36:19] Time window I mean every five minutes
[00:36:22] This one is updated we think that is
[00:36:24] Enough um iur it's enough time to don't
[00:36:28] Me too much and not too short so the
[00:36:31] User can see what is the real price of
[00:36:34] The things that he is mining crafting
[00:36:39] Whatever so he can make a Bri storm
[00:36:44] Idea about how much is going to be U if
[00:36:48] He sells if uh if he's going to buy also
[00:36:52] We have that a little feature here that
[00:36:54] Is a little arrow and a percentage the
[00:36:58] Meaning of this is that if the arrow is
[00:37:03] Up and it's black we are speaking about
[00:37:05] The
[00:37:06] A is the price of Star ATLAS is going to
[00:37:10] Be uh better sale than the dollar
[00:37:15] Ones how we know it because it's going
[00:37:17] To be a around
[00:37:19] 1% we can see all the prices are really
[00:37:23] Um fighting we can say adust stated is
[00:37:26] Not so much difference but we can found
[00:37:29] Sometimes for example in a golden ticket
[00:37:31] That in this case the price is going to
[00:37:34] Be better for a dollar sorry I'm going
[00:37:38] To scroll up yeah just this better the
[00:37:41] Price is going to be better at dollars
[00:37:45] With a profit a better profit of H near
[00:37:48] 12% so in a quick I hit the user can see
[00:37:54] What is the price of what he's producing
[00:37:58] And in which coin is going to be better
[00:38:00] Or could be better for him to sell just
[00:38:03] Like a up this is very cool man so
[00:38:06] Basically allows someone who is playing
[00:38:09] SAGE Labs to see the how the market is
[00:38:12] Looking like pretty much in real time
[00:38:14] You said it's it updates every five
[00:38:16] Minutes correct y okay so updating every
[00:38:19] Five minutes how the overall resources
[00:38:22] Market and crafting markets are
[00:38:25] Looking like right all in the same place
[00:38:27] And if you click in there it redirects
[00:38:29] You to the exact to the market right
[00:38:36] Nice
[00:38:39] Nice it bring yeah it brings up and
[00:38:42] Directly you can click and create your
[00:38:45] Order to sell or to buy whatever it
[00:38:47] Brings you directly to the resource you
[00:38:49] Have not to be looking for no you
[00:38:52] Have click and here we can so here you
[00:38:54] Can you can put your order or
[00:38:57] Accept the order or how you better
[00:39:00] See yeah so these two are the these
[00:39:05] Three are the maximum features also we
[00:39:07] Have H improve some little bags that we
[00:39:10] Have found for example we had a little
[00:39:12] Bag and in the in the math of the
[00:39:16] Toolkit in our craftings in this case
[00:39:19] It's for the rtion but yeah it was a
[00:39:22] Little error the toolkit was not um
[00:39:25] Integrated so we fix this one another
[00:39:27] Pair of details visual
[00:39:29] Details and well the for us the point is
[00:39:34] That all of this is going to be launched
[00:39:35] In the next uh in the next version what
[00:39:38] Is going to be if all goes
[00:39:42] Properly if all goes properly we hope
[00:39:45] That this one is going to come in I will
[00:39:48] Use your expression 4 to six for to
[00:39:51] Six days or less we really have to
[00:39:54] Launch it really quickly uh because it's
[00:39:57] Done so it's the last details and we are
[00:40:01] Making ready uh another tools that we
[00:40:05] Are not um ready to say when are going
[00:40:07] To go out but well you can see a little
[00:40:10] Advance of how we are working how is our
[00:40:13] Idea to work and more or less this is
[00:40:17] All I don't know any question
[00:40:19] Commentaries you know always
[00:40:23] Appreciated uh I see a couple I see a
[00:40:25] Couple suggestions group tagged you and
[00:40:27] Said do you have a section to show the
[00:40:30] Mining Coast uh example fuel to get
[00:40:33] Their ammo food if not that will be an
[00:40:35] Incredible addition to tie all the
[00:40:36] Pieces
[00:40:38] Together suggestion from gr okay I don't
[00:40:42] Know if I had catch it properly uh the
[00:40:44] Suggestion is to bring a calcu of how
[00:40:48] Much um full un need to achieve to
[00:40:51] Arrive the mining place I guess yeah
[00:40:53] The full Coast for mining um m that
[00:40:56] Place Bally with a transport included
[00:40:59] Okay yeah with we uh we are implemented
[00:41:02] This one the or problem was how to say
[00:41:06] That first your origin sector is this
[00:41:09] One or is the other one we was going to
[00:41:11] Take in the C style the CSS like
[00:41:16] Origin but we see that could be that the
[00:41:19] People is making in another areas
[00:41:21] Because it's some kind of strategies
[00:41:23] That we are seen there so this is the
[00:41:25] Unique Reon why is not putting the
[00:41:27] Origin yet but yes thank you thank you
[00:41:29] For the for the
[00:41:31] Suggestion awesome uh a couple of people
[00:41:34] Also said that the tool is awesome
[00:41:36] Wicked tool best committee so far it's a
[00:41:38] Very nice tool and Well Done friend
[00:41:40] Thank you for your efforts um this says
[00:41:44] A suggestion would be to add the
[00:41:45] Quantity available at the price and or
[00:41:48] Set a minimum for it to Aggregate and
[00:41:50] Average the price example minimum of
[00:41:53] Quantity for each resource is 10K units
[00:41:56] So it's realistic in the price that
[00:42:00] Is totally true yep I take note I take
[00:42:03] Note about it thank you thank you very
[00:42:05] Much yeah thank you for building for
[00:42:08] Thisas Community man yeah thank you man
[00:42:11] Was great thanks to you thanks to you
[00:42:14] For all the fors that you are doing and
[00:42:15] For sharing food with us thank you very
[00:42:17] Much thank you
[00:42:20] Br yep uh very nice tool by th um
[00:42:25] I think
[00:42:26] Now we have also apia they wanted to
[00:42:30] Update on what they have been working on
[00:42:32] So fun cracker welcome to the stage I
[00:42:36] Think I justed you yeah thank you for
[00:42:39] Having me can you guys understand me am
[00:42:41] I is my audio
[00:42:42] Working can we underst understand I love
[00:42:45] That how you doing Ronald okay I agree
[00:42:48] Those are two different questions can
[00:42:50] You hear me and you understand what I am
[00:42:53] Telling
[00:42:55] You stff as far as I still understand
[00:42:58] English today which is great good stuff
[00:43:01] Thanks for having me major kudos to the
[00:43:04] Previous two speakers really
[00:43:06] Great tools um really love to see what
[00:43:08] The community is building and um yeah
[00:43:10] I'm I'm happy uh that you guys gave me
[00:43:12] Some time to talk about something
[00:43:14] Completely different so um let me just
[00:43:17] Kick things off I'll try to keep it well
[00:43:19] Actually I will keep it very brief um I
[00:43:21] Think most of you I think since you're
[00:43:23] All enthusiasts have read the uh the
[00:43:25] Region article posted by Jose concerning
[00:43:28] Of course the 100y year anniversary of
[00:43:30] The Treaty of peace or the signing of
[00:43:32] The Treaty of Peace um uh great story um
[00:43:36] And we have embraced that uh in a short
[00:43:40] Story writing competition so perhaps for
[00:43:43] Those who have been around for a while I
[00:43:45] Would say like two years ago we created
[00:43:47] A little bit of a reputation for
[00:43:48] Ourselves around story writing and
[00:43:50] Running story writing competitions
[00:43:52] However the last one of these has been
[00:43:54] Well over a year so
[00:43:56] Uh yeah we figured it's time to
[00:43:58] Organize a new uh story writing
[00:44:00] Competition for the whole community of
[00:44:02] Course uh especially in this nice
[00:44:04] Christmas period and what better theme
[00:44:07] To write about than about the peace
[00:44:09] Between our factions uh people banter
[00:44:12] Back and forth uh of course the whole
[00:44:15] Year trying to uh to rile people up uh
[00:44:18] But this seems like an appropriate
[00:44:20] Moment in time to instead focus on the
[00:44:22] Wonderful things that uh that came from
[00:44:25] This of P so um yeah without further Ado
[00:44:29] Let me let me just share a link briefly
[00:44:32] For with all of you it's a it's a quite
[00:44:34] Lengthy uh article but it has all the
[00:44:37] Details it to keep it very short um the
[00:44:40] Reason why we announce it now not all
[00:44:42] The details are super finalized but we
[00:44:44] Want to of course give people time to
[00:44:46] Actually well start writing uh the
[00:44:48] Deadline uh is the December
[00:44:52] 24th um and in short uh prizes will uh
[00:44:57] Partially be coming from the team very
[00:44:58] Thankful for that uh even perhaps more
[00:45:01] Important is that judging uh of the
[00:45:03] Stories will be done in round two by
[00:45:06] Yose and two of his colleagues while
[00:45:09] There will be a round before that where
[00:45:12] The community gets to vote in order to
[00:45:14] To narrow the list and make sure that
[00:45:16] The team is not spending uh well days
[00:45:19] And days just read into all stories
[00:45:21] We'll make a short list of the top
[00:45:23] Community f stories like we also did in
[00:45:24] The past uh and hand that off to the
[00:45:26] Team uh most likely January 8th um which
[00:45:31] Means there's like two weeks roughly for
[00:45:33] The community to vote uh and there's
[00:45:35] What is there three weeks um something
[00:45:37] Like that a little bit more to write the
[00:45:39] Actual story um that's pretty cool the
[00:45:43] Downside is I hope it's not too big of a
[00:45:45] Downside but you will have to join our
[00:45:47] Discord because that is where the
[00:45:48] Channels are to both talk about it and
[00:45:50] Also to link your submission so you can
[00:45:53] Either um write if it's a short enough
[00:45:56] Story you can basically plug it straight
[00:45:58] Up into a Discord post um if not then
[00:46:01] You can use a platform like medium or
[00:46:04] Or anything else um and simply place a
[00:46:07] Link and then the reason why we need
[00:46:09] That is because that's where people can
[00:46:11] Then with their heart uh vote for the
[00:46:13] Stories and yeah we hope everybody uh
[00:46:16] There's no things attached you can
[00:46:18] Leave a server afterwards if you want no
[00:46:20] Issue but uh yeah it's okay with doing
[00:46:22] That you don't have to join apia you
[00:46:24] Just have to join the Discord server um
[00:46:27] The article explains but uh
[00:46:29] Hopefully that's okay we looked into
[00:46:32] Different things but we simply uh found
[00:46:34] This the best solution to get community
[00:46:36] Voting uh in there as well so all right
[00:46:40] Um that's a thing of course besides uh
[00:46:43] Cool prizing from the team we are also
[00:46:46] Doing our bit here we are going to give
[00:46:49] Away uh a number of our elf nfts uh to
[00:46:53] The top three um and well kind of
[00:46:57] Speaking of that is probably a very good
[00:46:59] Segway into the second part what I
[00:47:02] Wanted to talk about um going on a
[00:47:05] Monologue can people still follow what
[00:47:06] I'm saying yeah cool cool
[00:47:10] All right uh I'm going quite fast but I
[00:47:12] I feel people want to also do other
[00:47:14] Stuff so very briefly um we've been in
[00:47:17] The past uh not everybody equally happy
[00:47:20] So I keep it very short but we are uh
[00:47:23] Minting our own nft collection which is
[00:47:27] Stlas inspired and not only that it is
[00:47:29] Also uh making sure the atlas reaches um
[00:47:33] Yeah venues uh outside of the stratas
[00:47:36] Ecosystem to also bring the gospel of
[00:47:38] Stratas um currently sold a little bit
[00:47:41] Over 1,000 uh of the 2220 or the
[00:47:45] 2222 that will be in total circulation
[00:47:48] After mint um if anybody here just
[00:47:51] Interested join the Discord you can get
[00:47:53] Information reach out to me you can get
[00:47:54] More information all good and well
[00:47:58] Um but more importantly uh I'm here
[00:48:01] Because as is H well not super uh
[00:48:05] Uncommon in nft uh projects we have a
[00:48:10] Few honorary one of ones that we are
[00:48:13] Going to Mint officially right after the
[00:48:17] The mint the Mt date but that I
[00:48:19] Wanted to come on here briefly to hand
[00:48:22] Out because there are two of those
[00:48:24] Specifically for the
[00:48:26] Uh Star ATLAS team and the very first is
[00:48:29] This one I'm posting right now uh which
[00:48:32] Is for uh our community director
[00:48:35] Stany um wow that looks so good thank
[00:48:40] You thanks a ton for everything you
[00:48:42] Did for us so um yeah in downside
[00:48:45] Honorary nfts they have no strict
[00:48:47] Utility or value but nonetheless it's a
[00:48:49] One of one we'll make sure you get of
[00:48:51] Course the actual minted one as I
[00:48:53] Mentioned as soon as the mint is done um
[00:48:57] But feel free to uh yeah do with it what
[00:48:59] You want um and thanks for everything
[00:49:01] You have been doing since the very
[00:49:03] Beginning U of this community so uh well
[00:49:06] Well deserved of course and then the
[00:49:09] SEC yeah well happy to hear and we
[00:49:12] Appreciate you so that's why um second
[00:49:15] Uh and let me before I post the second
[00:49:17] One do mention that artwork has been
[00:49:19] Designed by Brutus one of our apan super
[00:49:22] Talented artist and he spent a whole
[00:49:25] Bunch of time to make some cool oneof
[00:49:26] One for you guys so major shout out to
[00:49:28] Him um but lastly of course can't really
[00:49:31] Do it anything any way different we have
[00:49:33] One for Michael I don't think Michael is
[00:49:34] Currently in the audience but
[00:49:35] Nonetheless uh figured this is an
[00:49:37] Appropriate moment to also uh share that
[00:49:39] One so uh there is this one and I'll
[00:49:42] Make sure to reach out through DM as
[00:49:43] Well to him to actually look at the hair
[00:49:50] [Laughter]
[00:49:54] Bro yes that's so
[00:49:57] Funny that is awesome right cool so yeah
[00:50:00] That's said I keep it short that's
[00:50:02] Everything I have thanks a bunch for
[00:50:04] Having me if there's any questions about
[00:50:06] The ster writing or well I mean let's do
[00:50:09] Elf questions not here but again go to
[00:50:11] Me go to my our Discord but if there any
[00:50:13] Question about the story writing
[00:50:13] Competition of course I'm here uh do
[00:50:15] Read the article and yeah love to get to
[00:50:19] See what people are going to write this
[00:50:21] Uh this holiday
[00:50:23] Season thank you man thank you for all
[00:50:25] The upates thank you Ronald epic update
[00:50:29] Brother question agent us I'll reach out
[00:50:31] To through
[00:50:33] DM awesome I'm screen Shing the
[00:50:39] Mic bro this is too much for me bro look
[00:50:44] At this Maya look at this Maya bro
[00:50:46] Look at this Maya
[00:50:49] Bro how can you make a toi look like
[00:50:54] Michael
[00:50:57] Oh
[00:50:59] Jesus
[00:51:03] Fun oh man I love it I like it so yeah I
[00:51:08] Hope Michael thinks the same but we
[00:51:09] We'll see we'll
[00:51:11] See super cool man thank you for sharing
[00:51:14] It h
[00:51:18] Awesome it's the little SM get me dude
[00:51:22] Because Michael's such a troll
[00:51:24] Head yeah the headset the headset as
[00:51:26] Well oh my this is yeah this is perfect
[00:51:30] Yeah it's awesome
[00:51:34] Manome cool well thanks for having me
[00:51:36] And yeah enjoy the rest of the show see
[00:51:39] You appreciate it man yeah appreciate it
[00:51:42] Thanks
[00:51:43] L so we had um before we close we had
[00:51:46] Another couple cool things that we
[00:51:48] Wanted to show um of community created
[00:51:52] Projects I will screen share one of them
[00:51:55] That I'm sure people already know about
[00:51:59] This one but I will screen share it
[00:52:03] Here um do you see my screen
[00:52:07] Yes cool so this is evi um they created
[00:52:12] Rising son is the username of the person
[00:52:15] Who created this um website and it's
[00:52:18] Basically the G expans and it has
[00:52:20] Different configurations that you can
[00:52:22] Use to visualize whatever you want to
[00:52:24] See in this case he created this part
[00:52:28] Which is you can see the latest sdu
[00:52:32] Probabilities
[00:52:34] So you can see wherever you are in the
[00:52:36] Map what's the probability of finding
[00:52:39] Sdus um in here so super cool uh tool
[00:52:44] And we wanted to give it a shout out
[00:52:46] Because we know that also some of some
[00:52:49] Of these projects are running into
[00:52:51] Coasts as well because you have to
[00:52:53] Basically get data from the
[00:52:55] Blockchain all the time uh and that
[00:52:59] Getting that data is expensive so major
[00:53:03] Major kudos to evi for putting this
[00:53:06] Together in
[00:53:07] The in this map and so guys you can go
[00:53:12] And check it out I'll will link it in
[00:53:14] The chat I know they also have a
[00:53:16] Donation link um and you can use their
[00:53:20] Starpath code as well so you can for
[00:53:25] Them because I know that they are
[00:53:26] Running into Coast for hosting these
[00:53:28] Websites so wanted to give a shout out
[00:53:31] Here uh and I think Groove are
[00:53:35] You I think Gro said that their project
[00:53:38] Is even uh taking data from this
[00:53:41] Page
[00:53:42] To automate something so that is
[00:53:46] Pretty cool as well to see the
[00:53:48] Collaboration so yeah you guys can go
[00:53:51] And check it out I posted the link in
[00:53:52] The atlas Amphitheater chat
[00:53:57] And another tool well not a tool but a
[00:53:59] Project that we wanted to highlight is
[00:54:01] Atlas Grace they just hit a huge
[00:54:04] Milestone if you don't know what ATLAS
[00:54:05] Grace is it's a project being run by
[00:54:07] Arch type and basically what they do is
[00:54:10] They compound the earnings in Star ATLAS
[00:54:13] And then they donate every month I think
[00:54:15] 50% they reinvest and the other 50% they
[00:54:19] Donate to a charity that the community
[00:54:21] Can choose by themselves just by voting
[00:54:24] On Twitter profile and they got uh they
[00:54:28] Reached the Milestone of 7,000 poce
[00:54:31] Locked so congratulations to ATLAS Grace
[00:54:34] And if you guys want to be part of ATLAS
[00:54:36] Grace I think they can donate as well to
[00:54:39] ATLAS grace. Soul so in case you want to
[00:54:42] Get involved it's one of the most
[00:54:44] Beautiful initiatives yeah man this
[00:54:47] Makes me feel good having this kind of
[00:54:49] Project in Star ATLAS bro it really
[00:54:52] Makes my day y yeah I think we also had
[00:54:56] Updates from Galia Merchants as
[00:54:59] Well um they created a video that they
[00:55:02] Wanted us to share let me
[00:55:04] Actually screen share it
[00:55:07] Here really quickly they have a cyber
[00:55:11] Monday promotion
[00:55:12] Running so they sent this over because
[00:55:15] They couldn't make it to this rou but
[00:55:17] Wanted us to share it for them so let me
[00:55:20] Know if you guys can see
[00:55:24] It
[00:55:25] Can you see my screen yep
[00:55:34] [Music]
[00:55:43] [Music]
[00:55:54] Okay
[00:55:59] Bro look at the
[00:56:01] Sand the sand notebook
[00:56:07] [Music]
[00:56:16] Bro very
[00:56:19] Nice again bro look at my boy's hand man
[00:56:22] Looking clean man damn s looks good
[00:56:27] That's for sure I actually bought one
[00:56:30] One of their t-shirts last week saying
[00:56:34] Blessed by Iris protected by the cosmic
[00:56:37] Currents I love it should be here soon
[00:56:41] Let me drop the link to the G merchants
[00:56:45] In case you guys want to purchase from
[00:56:47] Their
[00:56:50] Store just posted the link on the chat
[00:56:54] Uh and use the code what was the code
[00:56:56] Pew pew2 you use that code and I think
[00:56:59] You get a get a discount for Cyber
[00:57:01] Monday so I appreciate our friends from
[00:57:04] Gia Merchants for putting together all
[00:57:06] This very cool stratas merch um and with
[00:57:10] That I think we conclude our round of
[00:57:13] Community updates for the day as always
[00:57:16] The objective of these roots they happen
[00:57:18] Every month at the end at the end of the
[00:57:21] Month it's the last R of the month and
[00:57:23] The objective is just for the community
[00:57:25] To be able to come here and share what
[00:57:28] They have been working on and the only
[00:57:30] Thing you have to do is just message me
[00:57:33] Or Dom and we will be able to get you in
[00:57:36] Here um on stage um literally the
[00:57:39] Objective of this is again for the
[00:57:41] Community to be able to share the cool
[00:57:44] Things they have been working on and so
[00:57:47] Don't hesitate to reach out if you're
[00:57:48] Building something for Star ATLAS and
[00:57:51] The
[00:57:52] Community with that said anything
[00:57:54] Anything else before we close Jose or
[00:57:57] D uh no just thank you to all the
[00:58:00] Builders continuing to build in the St
[00:58:02] Eco system you guys are a major part of
[00:58:05] What makes Star ATLAS so unique and
[00:58:07] Killer and um we just sincerely
[00:58:10] Appreciate it from everyone at the
[00:58:12] Team yeah thank you guys always a
[00:58:15] Pleasure to watch our development it
[00:58:18] Makes me super proud seeing all those
[00:58:20] Product coming to
[00:58:21] Life yeah it's it's able to have this
[00:58:25] Community of Builders I think it's one
[00:58:27] Of the key areas that sets Star ATLAS
[00:58:30] Apart from other projects I may be a
[00:58:32] Little bit biased here uh but the Easter
[00:58:34] ATLAS Community is definitely one of the
[00:58:36] Best in the world so uh yeah we'll see
[00:58:39] You also at the next
[00:58:40] Brew which is about economics we'll have
[00:58:44] A Chris and probably Gareth as well from
[00:58:46] Our econ team joining uh next week so I
[00:58:51] Just posted the link also on the at Brew
[00:58:55] Chat sorry here in the amphitheater chat
[00:58:58] So make sure to mark it as interested so
[00:59:01] You can come and join and get the
[00:59:02] Updates what's going on in the atlas
[00:59:04] Economy from our experts uh also this
[00:59:08] Friday we have the golden Carnival
[00:59:11] Number five where we check what's going
[00:59:13] On with the golden ticket event live Al
[00:59:17] Together and sometimes we have the
[00:59:19] Winners in there as well and probably
[00:59:22] Next week also in the golden Carnival
[00:59:23] Number six we will be deciding what are
[00:59:27] The prices for week eight as you know
[00:59:29] That's the community boat week so it's
[00:59:31] Important for us to get together and
[00:59:33] Decide what we want to have on that week
[00:59:36] Weekly price um this said thank you
[00:59:39] Everyone for joining the atlas R number
[00:59:41] 90 and thanks to all the builders that
[00:59:44] Keep building on top of Star ATLAS we
[00:59:47] Love you and we'll see you next week
[00:59:53] Soowoo
