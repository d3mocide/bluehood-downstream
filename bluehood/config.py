"""Configuration for bluehood."""

import logging
import os
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

logger = logging.getLogger(__name__)

# Data directory
DATA_DIR = Path(os.environ.get("BLUEHOOD_DATA_DIR", Path.home() / ".local" / "share" / "bluehood"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Database path (can be overridden directly)
DB_PATH = Path(os.environ.get("BLUEHOOD_DB_PATH", DATA_DIR / "bluehood.db"))

# Socket path for daemon communication
SOCKET_PATH = Path("/tmp/bluehood.sock")

# Web dashboard port. Overridable via env so Docker host-network deployments can
# remap the dashboard without editing the daemon command line. The CLI -p/--port
# flag still takes precedence when supplied.
WEB_PORT = int(os.environ.get("BLUEHOOD_WEB_PORT", "8080"))


def _resolve_display_timezone() -> str | None:
    """Resolve the timezone used to render timestamps in the web dashboard.

    Reads the standard ``TZ`` env var (the same one Docker/compose sets) so the
    frontend shows times in the configured zone instead of the viewer's browser
    locale. Returns the IANA name when valid, otherwise ``None`` (the dashboard
    then falls back to the browser's local time). Invalid names are logged so a
    typo like ``America/Los_Angles`` is easy to spot.
    """
    name = os.environ.get("TZ", "").strip()
    if not name:
        return None
    try:
        ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError):
        logger.warning(
            "Invalid TZ %r — dashboard will use the browser's local time. "
            "Use an IANA name such as 'America/Los_Angeles'.",
            name,
        )
        return None
    return name


# IANA timezone name for dashboard timestamp rendering (None = browser local).
DISPLAY_TIMEZONE = _resolve_display_timezone()

# Scanning interval in seconds
SCAN_INTERVAL = 10

# How long to scan for each cycle (seconds)
SCAN_DURATION = 5

# Bluetooth adapter (None = auto-select, or specify like "hci0")
BLUETOOTH_ADAPTER = os.environ.get("BLUEHOOD_ADAPTER", None)

# Prometheus metrics port (None = disabled)
METRICS_PORT = int(os.environ.get("BLUEHOOD_METRICS_PORT", 0)) or None

# Separate adapter for classic Bluetooth inquiry scans (None = use same as BLE).
# Setting this to a different adapter (e.g. a USB dongle) allows BLE and classic
# scans to run concurrently without adapter contention.
CLASSIC_BLUETOOTH_ADAPTER = os.environ.get("BLUEHOOD_CLASSIC_ADAPTER", None)

# Heartbeat check-in URL (None = disabled). POST JSON payload periodically.
HEARTBEAT_URL = os.environ.get("BLUEHOOD_HEARTBEAT_URL")
HEARTBEAT_INTERVAL = int(os.environ.get("BLUEHOOD_HEARTBEAT_INTERVAL", "300"))  # seconds

# Auto-prune sightings older than N days (0 = disabled)
PRUNE_DAYS = int(os.environ.get("BLUEHOOD_PRUNE_DAYS", "0"))
