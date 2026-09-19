# Research Plan — Modern Rap "Instant Proof" Playlist

## Mission
Build a definitive 50–70 track playlist of modern rap (2012–2024, peak center 2016) selected purely on **ignition velocity and cultural detonation** — songs that were undeniably on fire the moment they dropped. The playlist must make someone who "doesn't like modern rap" instantly understand why this era was lit.

## Qualifying rules (hard)
- **Songs, not artists.** No one-per-artist limit. If one artist had 4 world-burning tracks, all 4 go in.
- **Overnight hype / explosive energy.** Abnormal first-week or first-month surges: YouTube view velocity, SoundCloud play counts, WorldStar / Lyrical Lemonade premiere numbers, Vine/TikTok detonation, Reddit r/hiphopheads freakout threads.
- **"You had to be there."** Include tracks whose *moment* was seismic even if they aren't replay staples today (Panda, Hot Nigga).
- **Exclude:** slow-burn radio hits, soft pop crossovers, songs that only qualify via Billboard longevity. Raw hype, club/street disruption, moshpit energy only.
- Era: 2012–2024. 2010s are the core; 2020s tracks must clear the same "planet screamed it on day one" bar.

## Vibe benchmarks (calibrate against these exact energies)
I Don't Like (Chief Keef) · Shotta Flow (NLE Choppa) · Magnolia (Playboi Carti) · Ransom (Lil Tecca) · Lucid Dreams (Juice WRLD) · Panda (Desiigner) · Hot Nigga (Bobby Shmurda)

## Hype signals to collect per song (for scoring)
Release/leak date; first-week & first-month YouTube views; SoundCloud plays at ~30/90 days; premiere channel (WSHH, Lyrical Lemonade, Elevator, No Jumper, artist-owned); Vine/TikTok/Triller virality (dance, meme, challenge); r/hiphopheads thread upvotes/comment volume on drop day; "did an unknown go famous overnight?"; club/street/moshpit adoption; Billboard peak only as a *secondary* footnote.

## Research angles (5 Opus 5 agents, non-overlapping)

1. **Drill & street detonations, 2012–2016** — Chicago drill (Keef, Durk, Reese, Herb/G Herbo, Bibby), Brooklyn/NYC street wave (Shmurda, Rowdy Rebel), Atlanta trap explosions (Migos "Versace"/"Bad and Boujee", Future 2014–2017 run, Young Thug, Rich Gang, 21 Savage/Metro, Gucci post-release), Bay/West street records (Mozzy era), Panda. Search: "I Don't Like" WorldStar views 2012, "Versace" leak YouTube, "Bad and Boujee" meme velocity, "Hot Nigga" Vine, drill mixtape SoundCloud numbers. Also Chicago-era premieres via WSHH and the "Raingutter/Bank Roll" channels.

2. **SoundCloud rap & the Cole Bennett / Lyrical Lemonade machine, 2015–2019** — Uzi, XXXTentacion, Ski Mask, Carti, Lil Pump, Smokepurpp, Juice WRLD, Trippie Redd, Lil Peep, Ronny J era, Yung Bans, Comethazine, Lil Tecca, NLE Choppa, Lil Skies, YBN. Search Lyrical Lemonade drop-day view counts (Gucci Gang, Look at Me, Lucid Dreams, Shotta Flow, Ransom), SoundCloud play records, "SoundCloud rap" Rolling Loud moshpit clips, XXL Freshman cyphers as spark events.

3. **Meme / platform virality: Vine, TikTok, Triller, YouTube challenges, 2013–2024** — songs whose detonation was platform-driven: Vine (Shmurda, "Watch Me", ILoveMakonnen "Tuesday", Fetty Wap "Trap Queen" *only if hype-first*), dance/challenge songs (Migos "Look at My Dab", BlocBoy JB "Look Alive", "Old Town Road" *evaluate against pop-exclusion*), TikTok era (Roddy Ricch "The Box", Pop Smoke, "WAP" *evaluate*, Lil Nas X *evaluate*, Ice Spice "Munch", Sexyy Red, Central Cee/Dave "Sprinter" UK crossover, Yeat, Ken Carson opium wave). Collect first-2-week velocity and creator-count data.

4. **2016 peak & the moshpit/festival era + 2020s fire** — what made 2016–2017 the peak (Kendrick "HUMBLE." day-one records, Travis "goosebumps"/"SICKO MODE", Kanye "Father Stretch My Hands", Drake club/dancehall *evaluate hype-only*, Cardi "Bodak Yellow", Sheck Wes "Mo Bamba", Lil Uzi "XO Tour Llif3", "Bad and Boujee"), plus 2020s moments that cleared the bar (Pop Smoke "Dior", Playboi Carti *Whole Lotta Red* leaks/drops, Yeat, Kendrick "Not Like Us" 2024 detonation, Drake/Kendrick beef velocity records, Ken Carson, Baby Keem/Kendrick "family ties", Fivio/Brooklyn drill, Lil Durk "Laugh Now Cry Later" *evaluate*). Pull Spotify/YouTube first-day and first-week records.

5. **Community ground-zero archives & contrarian check** — r/hiphopheads yearly "biggest moments" threads, "songs that took over the internet overnight" threads, Genius/Complex/Pitchfork "songs that defined the decade" lists, Rap Radar/DJBooth/Kanye-to-the/KTT2 drop-day threads, Spotify "RapCaviar" history, Lyrical Lemonade and WSHH all-time-most-viewed lists. Also hunt for **regional street smashes** the other angles may miss (Detroit: Sada Baby "Whole Lotta Choppas", BabyTron; Memphis: Yo Gotti/Moneybagg, Key Glock, GloRilla "FNF"; Louisiana: NBA YoungBoy velocity records, Kevin Gates; DMV; Bay/LA: YG "My Nigga", Drakeo, Shoreline Mafia, Blueface "Thotiana", Kodak Black, Kendrick "m.A.A.d city"). This agent's second job: flag songs the other angles are likely to over-include (pop crossovers) and under-include (street records without pop numbers).

## Known unknowns to resolve
Actual first-week view/play numbers (many are only in contemporary tweets/press — cite dated sources); which 2020s tracks genuinely match 2016 energy vs. mere streaming size; a defensible cutoff for "pop crossover" (rule: if the *first* wave of listeners was radio/Top 40 rather than hip-hop communities, exclude).

## Researcher grounding rules (in every agent prompt)
ONLINE RESEARCH ONLY (WebSearch + WebFetch). Cite URL + date for every number. Distinguish hard velocity data from vibes/retrospective punditry. For each candidate song return: title, artist, year, hype signals with numbers, premiere channel, one-sentence "spark," and a 1–5 ignition score. Write to `<scratchpad>/research-<N>-<slug>.md` with a Sources section. 30–60 candidates per agent is fine; over-collect, the synthesizer cuts.

## Synthesis (Fable) — output contract
Read all research files + plan. Cross-check, dedupe, resolve conflicting numbers (say which source wins). Apply the exclusion rule strictly. Produce `knowledge/modern-rap-instant-proof-playlist.md` containing:

1. **Core truths** (10–15 sentences: what made this era detonate, which waves, why 2016).
2. **Master Playlist, 50–70 tracks, ordered by wave then chronologically** — table: # · Song · Artist · Year · Wave · Hype Moment (one concrete sentence with the actual spark/number).
3. **The 10-Song "Instant Proof" Pack** — the hardest, most undeniable tracks with a two-line justification each and a recommended play order.
4. **Honorable mentions / cut list** — 15–20 songs that nearly made it and the one-line reason they were cut.
5. **Low-confidence flags** — numbers that couldn't be verified.
6. Research date + full source list.

Also export the master list as `knowledge/modern-rap-instant-proof-playlist.csv` (song,artist,year,wave,hype_moment).
