import time
import jwt
import httpx
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def _make_token(secret: str) -> str:
    payload = {"iat": int(time.time())}
    return jwt.encode(payload, secret, algorithm="HS256")


def get_yesterday_links(
    shaarli_url: str,
    api_secret: str,
    exclude_tags: list[str] | None = None,
    timezone_name: str = "Europe/Paris",
) -> list[dict]:
    """Récupère les liens créés hier (00:00 -> 23:59) via l'API Shaarli."""
    token = _make_token(api_secret)
    headers = {"Authorization": f"Bearer {token}"}

    timezone = ZoneInfo(timezone_name)
    now = datetime.now(timezone)
    yesterday_end = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = yesterday_end - timedelta(days=1)

    def parse_created(value: str) -> datetime:
        created = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if created.tzinfo is None:
            return created.replace(tzinfo=timezone)
        return created.astimezone(timezone)

    links = []
    offset = 0
    limit = 100

    with httpx.Client(timeout=15) as client:
        while True:
            resp = client.get(
                f"{shaarli_url}/api/v1/links",
                headers=headers,
                params={"limit": limit, "offset": offset, "sort": "-date"},
            )
            resp.raise_for_status()
            batch = resp.json()
            if not batch:
                break

            stop = False
            for link in batch:
                created = parse_created(link["created"])
                if created >= yesterday_end:
                    continue
                if created < yesterday_start:
                    stop = True
                    break

                if exclude_tags and any(t in link.get("tags", []) for t in exclude_tags):
                    continue

                links.append(link)

            if stop or len(batch) < limit:
                break
            offset += limit

    links.sort(key=lambda link: parse_created(link["created"]))
    return links