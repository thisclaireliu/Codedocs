# PageTrail

PageTrail is a small personal CLI tool to track reading progress for books.

The idea is simple:
- keep a local JSON file with your books
- log how many pages you read at different times
- get a quick overview of how your reading habit evolves

This is a solo side project and is not meant to be a polished product. It is just a lightweight helper to keep notes about reading sessions from the terminal.

## Quick usage

At the moment the CLI is a plain Python entry point:

```bash
python -m pagetrail.cli add dune \"Dune\" --author \"Frank Herbert\" --pages 604
python -m pagetrail.cli log dune 25 --note \"tram ride\"
python -m pagetrail.cli list
python -m pagetrail.cli summary dune
```

Data is stored under `~/.pagetrail` by default. You can override that with the `PAGETRAIL_HOME` environment variable if you want to keep things in a different folder while trying it out.
