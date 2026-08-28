# CSE Freshers CR Elections 2026

Candidate listing for the IIT (BHU) Varanasi CSE freshers' Class Representative
election. Online voting on 4 September 2026.

Live: https://thejaiv.github.io/cr-election-2026/

## Layout

| Path | What it is |
| --- | --- |
| `index.html` | The whole site — HTML, CSS and JS in one file. This is what GitHub Pages serves. |
| `photos/` | Candidate photos. Drop a file in, no code edit needed. |
| `build.py` | Bundles `index.html` + `photos/` into a single self-contained `dist/index.html`. |
| `dist/index.html` | Generated. One file with every photo embedded — email it, or host it anywhere. |
| `versions/` | Earlier designs, kept for reference. |

## Adding a photo

Drop the file in `photos/`. The page tries these names for each candidate, in
order, and falls back to an initials circle when none load:

```
photos/first-last.jpg  .jpeg  .png  .webp     <- preferred
photos/first_last.jpg  .jpeg  .png  .webp
photos/first.jpg       .jpeg  .png  .webp
```

Then publish:

```sh
python3 build.py          # optional — refreshes dist/index.html
git add -A && git commit -m "add photo" && git push
```

Pages redeploys in about a minute.

## Editing candidates, dates, seats

Everything editable sits at the top of the `<script>` block in `index.html`,
under `EDIT EVERYTHING BELOW THIS LINE`: `VOTING_OPENS`, `LOGISTICS`, `SEATS`,
`CANDIDATES`, `OPEN_SEAT`.
