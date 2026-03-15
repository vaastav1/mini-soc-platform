PRIVATE_PREFIXES = ("10.", "192.168.", "172.16.", "172.17.", "172.18.",
                    "172.19.", "172.20.", "127.", "0.", "::1")

def enrich_ip(ip: str) -> dict:
    if any(ip.startswith(p) for p in PRIVATE_PREFIXES):
        return {"country": "Internal", "city": "LAN"}
    try:
        import geoip2.database
        from app.core.config import settings
        with geoip2.database.Reader(settings.geoip_db_path) as reader:
            r = reader.city(ip)
            return {"country": r.country.name or "Unknown", "city": r.city.name or "N/A"}
    except Exception:
        return {"country": "Unknown", "city": "N/A"}