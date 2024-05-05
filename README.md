# VisionSpace Coding Challenge

Coding Challenge by VisionSpace

The data in this repository is distributed by VisionSpace under the GPL-3.0 license in the repository [github.com/visionspacetec/ai-interview-challanges](https://github.com/visionspacetec/ai-interview-challanges).

## Description of the Data

(from the VisionSpace repository's README.md)

A sample of the Janus space mission data can be found in the file SatelliteDataSet.csv, with the following columns:

- ut_ms: timestamp.
- power: power consumption measurements.
- sa: angle of Janus' solar panels normal.
- sx: solar angle of the X axis of the satellite.
- sy: solar angle of the Y axis of the satellite.
- sz: solar angle of the Z axis of the satellite.
- sunmars_km: the distance in kilometers between the Sun and Mars.
- earthmars_km: the distance in kilometers between the Earth and Mars.
- sunmarsearthangle_deg: Sun-Mars-Earth angle in degrees.
- solarconstantmars: solar constant at Mars in W/m^2.
- eclipseduration_min: total duration of all eclipses in the day, in minutes.
- occultationduration_min: total duration of all occultations in the day, in minutes.
- flagcomms: TRUE if any communication device was used, else FALSE.

The remaining columns are spacecraft pointing events (Flight Dynamics TimeLine). They are pointing and action commands that can impact the attitude of the satellite, thus they also may impact the solar aspect angles of the orbiter and/or the switch ON/OFF of some instrumentation.

## Creating the Conda Environment

The commands are set-up to use mamba instead of conda. If you can't or don't want to use mamba, you can replace `mamba` by `conda` in the commands and scripts.

Create the environment:

    mamba env create -f environment.yml

Updating the environment after a change to the `environment.yml` file (this also creates a freeze of the new environment):

    ./update-environment.sh
