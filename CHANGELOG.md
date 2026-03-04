# Changelog


## v0.5.0

  * Overlay: Further improve position calculation
  * Publish `:dev` tagged containers on git pushes to the `main` and `dev` branches
  * Change caching directory to `media/picture-of-the-day/cache/` for improved path mappings (i.e. for my Home Assistant app)


## v0.4.0a6

  * Make random POD permanent for the respective day
  * Add API endpoint for random photo


## v0.4.0a5

  * Overlay: Improve position calculation


## v0.4.0a4

  * Overlay
    * Make configurable on a per-album basis
    * Try to predict cropping for target screen and position overlay accordingly so that it is still visible
    * Improve outline


## v0.4.0a3

  * Overlay: Further adjustments to font size, margins and outline


## v0.4.0a2

  * Overlay: Make font size and margins bigger


## v0.4.0a1

  * Overlay: Print photo creation time on the photo if info available


## v0.3.0a2

  * Make containers available for arm64 too (was previously only amd64)
  * Enabling setting timezone via environment variable `POD_TIMEZONE` (only if all 'core' environemt variables are set too)


## v0.3.0a1

  * Initial version published on PyPI and as container on GHCR
