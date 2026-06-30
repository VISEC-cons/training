# Dedicated — Triathlon & endurance training

## Context
- **Hoofddoel (huidig):** Marathon Amsterdam — oktober 2026 (datum bevestigen, ~18 okt) — eerste echte wegmarathon-doel na de IM
- **Afgerond:** Ironman Tours — 14 juni 2026 — gefinisht in **11:58** (extreme hitte, bewust conservatief gereden, geen PR-poging)
- **Atleet:** Niels Hof (kantoorbaan + ZZP, training vooral avond/weekend)
- **Coachrol:** Claude fungeert als "Coach Jean Claude van Dam" (zie `coach_prompt.md`)

## Huidige trainingsfocus (post-IM, vanaf 27 juni 2026)
Geen fietsvolume meer. Weekstructuur met **3× zwemmen / 2× rennen / 3× gym**:
- **Zwemmen** — plezier + sneller worden (techniek + CSS-werk rond 1:28/100m)
- **Rennen** — plezier + marathonbasis voor Amsterdam; af en toe wedstrijden (HM/marathon)
- **Gym** — spieropbouw, flexibiliteit, mobiliteit, **in dienst van** zwemmen/rennen + blessurepreventie (enkel/scheenbeen)

| Dag | Training |
|---|---|
| Ma | Zwemmen (techniek + CSS) |
| Di | Gym A — bovenlichaam compleet (push + pull) + core |
| Wo | Rennen — kwaliteit (tempo/intervallen) |
| Do | Zwemmen (CSS/drempel snelheid) |
| Vr | Gym B — onderlichaam + enkel/scheenbeen-preventie |
| Za | Rennen — lange duurloop |
| Zo | Zwemmen lang (zwembad 9-11) + Gym C — mobiliteit (+ optionele bovenlichaam-pomp) |

> **Zwembadtijden:** za 12-13 (te kort voor de lange zwem) → lange zwem op zo in het 9-11 venster; zo-zwem = actief herstel na de za-loop. Weekdagzwem ma/do-avond.

**Marathon-ramp:** vanaf ~eind augustus (~8 wk vóór Amsterdam) loopfrequentie naar 3×, gym terug naar 2×, marathon-specifiek blok.

## Werkwijze (uit coach_prompt.md)
Twee modi:
- **Schema-generatie** — JSON-output voor trainingsblokken (zie sectie 9 van `coach_prompt.md`)
- **Dagelijkse coaching** — proactieve check-in, gevoelsscore, aanpassing o.b.v. vermoeidheid/pijn

## Directory structuur
- `coach_prompt.md` — volledige systeemprompt (atletenprofiel, TSS-formules, zones, blessurebewaking)
- `zwemtechniek.md` — zwemtechniek-drilltoolbox (Effortless Swimming): 4 focuspunten (recovery, rotatie, lats/power diamond, kick) + wekelijkse focus-rotatie. Zwemsessies in `marathon2026/` verwijzen ernaar; lats/power diamond is de vaste cue elke sessie
- `marathon2026/week01.json` … `week04.json` — **huidig blok** (post-IM, 3 opbouw + 1 deload, start 27 juni)
- `week1.json` … `week11.json` — afgeronde IM Tours-cyclus (archief)
- `rookvrij.json` — rookvrij-tracker (sinds 26-04-2026)
- `garmin_sync.py` — Garmin Connect sync-script (zie Automatisering — nog niet actief)

## Periodisering — huidig blok (marathon2026/)
| Week | Datums | Fase |
|---|---|---|
| 1 | 27 jun – 5 jul | Re-entry + opbouw |
| 2 | 6 – 12 jul | Opbouw |
| 3 | 13 – 19 jul | Piek blok |
| 4 | 20 – 26 jul | Deload |

Volgende blok (vanaf 27 juli) bouwt loopvolume verder op richting Amsterdam.

**Zwemtechniek-focus per week** (zie `zwemtechniek.md`): wk1 recovery · wk2 rotatie · wk3 lats/power diamond (piek) · wk4 kick + integratie. Power diamond/lats is de vaste cue in élke sessie. De ochtend-briefing mag de focus van de dag/week kort tonen bij een zwemtraining.

## Automatisering — STATUS
- **Garmin-sync:** ⚠️ **nog niet actief.** `garmin_sync.py` bestaat, maar er is geen opgeslagen `~/.garth`-sessie en geen Windows scheduled task. Nog in te richten. Zou bij activatie `garmin_daily.json` (slaap/HRV/RHR/Body Battery) pushen — let op: publieke repo, dus health-data-privacy afwegen.
- **Morning briefing agent:** ⚠️ **moet herricht worden.** Was geconfigureerd voor de IM (root `weekN.json` + countdown 14 juni). Moet nu wijzen naar `marathon2026/weekNN.json` (blokstart 27 juni 2026) en countdown naar Marathon Amsterdam. Moet de volledige `description` + `structure`-stappen van de dagtraining tonen.

## Beperkingen
- Blessure: rechter enkel + shin splints → max 10% loopvolume-toename per week; tibialis-raises + excentrische kuiten staan elke gym-B-sessie
- Trainingsvensters: ma-do na 18:00 (60-90 min), vr flexibel, za/zo 09:00-14:00 (~5u)
- Yoga: elke ochtend (mobiliteit/herstel, telt niet als TSS)

## Naamgeving repo
GitHub-remote heet historisch `VISEC-cons/training` (publiek). Trainingsschema's zijn publiek; sessielogs (`.claude/`) blijven via `.gitignore` lokaal.
