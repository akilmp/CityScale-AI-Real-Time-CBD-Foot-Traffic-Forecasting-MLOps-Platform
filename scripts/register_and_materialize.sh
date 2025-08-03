#!/usr/bin/env bash
# Register all Tecton objects defined in the repo and materialize their data.
#
# Usage:
#   scripts/register_and_materialize.sh START_TIME END_TIME
#
# The start and end times should be provided in ISO-8601 format, e.g.
#   scripts/register_and_materialize.sh 2024-01-01T00:00:00Z 2024-01-02T00:00:00Z
#
# This script requires the Tecton CLI to be installed and configured with
# appropriate credentials (see https://docs.tecton.ai). It should be run from
# the root of the repository.
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 START_TIME END_TIME" >&2
  exit 1
fi

START=$1
END=$2

# Register (apply) feature definitions in the current repository.
tecton apply

# Materialize each feature view.
tecton materialize feature-view foot_traffic_rolling_counts --start-time "$START" --end-time "$END"
tecton materialize feature-view weather_lag --start-time "$START" --end-time "$END"
tecton materialize feature-view event_attendance --start-time "$START" --end-time "$END"
tecton materialize feature-view holiday_flag --start-time "$START" --end-time "$END"
