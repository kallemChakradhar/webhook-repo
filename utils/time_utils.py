from datetime import timezone, timedelta

IST_OFFSET = timedelta(hours=5, minutes=30)

def format_github_time(dt):
    # dt is already a datetime object now
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    ist_time = dt.astimezone(timezone(IST_OFFSET))
    return ist_time.strftime("%d %b %Y - %I:%M %p IST")
