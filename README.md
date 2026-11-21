# The Passport Page of a Country That Isn't There

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/KimLyNamHa/the-passport-page-of-a-countr-2-20261121-0318-entry/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/KimLyNamHa/the-passport-page-of-a-countr-2-20261121-0318-entry/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

Built for the [make.fun](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318) bounty
"The Passport Page of a Country That Isn't There".

An invented passport spread for the **Republic of Meridia**, a seafaring
island nation: a data page for holder Elara Voss (issued 14 FEB 2024,
expires 14 FEB 2034) beside a stamps page of neighbouring ports, every
stamp dated after the issue date, with a seafarer's levy fee stamp and
the visa condition "HOLDER MUST GREET THE HARBOURMASTER ON ARRIVAL".

## Program

`main.py` (Python 3.13, standard library + Pillow, no network,
deterministic) draws the spread at 1024x1024 and writes it to
`/output/entry.png`. The portrait is a generated headshot embedded as
base64; all text is drawn with DejaVu fonts, and the machine-readable
zone's check digits are computed with the ICAO algorithm.
