from datetime import datetime, time, timedelta, timezone

# Entries must not outlive the daily reset: 00:00 UTC-3 == 03:00 UTC.
DAILY_RESET_UTC = time(hour=3, minute=0, tzinfo=timezone.utc)


def seconds_until_next_reset(now: datetime) -> float:
    """Seconds from `now` (tz-aware) until the next 03:00 UTC."""
    target = datetime.combine(now.date(), DAILY_RESET_UTC)
    if target <= now:
        target += timedelta(days=1)
    return (target - now).total_seconds()


def capped_ttl(ttl: int, now: datetime | None = None) -> float:
    """Requested ttl, capped so the entry expires no later than the next
    daily reset."""
    if now is None:
        now = datetime.now(timezone.utc)

    return min(ttl, seconds_until_next_reset(now))
