#!/usr/bin/env bash
# Register all Tecton objects defined in the repo and materialize their data.
#
# Usage:
#   scripts/register_and_materialize.sh START_TIME END_TIME
#
# The start and end times should be provided in ISO-8601 format, e.g.
#   scripts/register_and_materialize.sh 2024-01-01T00:00:00Z 2024-01-02T00:00:00Z
#
# Steps performed:
#   1. `tecton apply` registers or updates the feature definitions in the
#      active workspace.
#   2. Each feature view is backfilled by calling `tecton materialize` for the
#      provided time window.
#
# Prerequisites:
#   * The Tecton CLI must be installed and configured with credentials
#     (`tecton login` and `tecton workspace use <workspace>`).
#   * Run this script from the root of the repository so that the feature
#     definitions under `features/` are discovered.
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
