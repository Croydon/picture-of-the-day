# Picture of the Day

This project provides a REST API endpoint for delivering a Picture of the Day.

It requires a connection to a Nextcloud instance with Nextcloud Photos being enabled. You can also use Memories for Nextcloud, but you need to have Nextcloud Photos enabled for photo album support (Memories and Photos are sharing their albums).

You can then specify an album from which the photos are fetched. Afterwards, you can assign for each calandar day a specific photo. For days for which there is no photo assigned, a random photo is choosen.

The app remembers which photos have already been delivered and prefers photos for the random assignment which haven't been picked yet. If there are no more new photos, the already delivered photos will be picked again.


## Motivation

My personal motivation for this app is to use it for an ESP32-S3-PhotoFrame, which has an e-ink display and therefore has ultra-low energy consumption and can run on a battery for months.


## Important

> [!CAUTION]  
> While this application has some form of basic authentication, I still recommend to only run this within a trusted home network without exposing it to the internet.


## Install

To install the latest release:  
`pip install picture-of-the-day`

To install from source:  
`pip install .


## Developing & Testing

Install all dependencies:

`pip install -U .[dev,tests]`

Run tests:

`pytest -v`


## License

This project is licensed under the terms of the [MIT license](LICENSE).
