# Games

A lightweight, responsive collection of browser games by Laxman Nepal.

## Architecture

- Shared header and footer
- Shared dark/light theme
- Shared fullscreen support for every game
- Game registry in `data/games.json`
- Individual games under `games/`
- Static-hosting friendly

New games should be added to the registry and receive the shared game shell/fullscreen controls.
