import ssl
import urllib.request
import urllib.robotparser



_robots_cache = {}


def can_fetch(base_url, target_url):
    """Check if URL can be fetched according to robots.txt"""
    
   
    if base_url in _robots_cache:
        rp = _robots_cache[base_url]
        if rp is None:
            return True  # robots.txt failed, allow all
        return rp.can_fetch("*", target_url)
    
    robots_url = base_url.rstrip("/") + "/robots.txt"
    rp = urllib.robotparser.RobotFileParser()

    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(robots_url, context=ctx, timeout=3) as f:
            rp.parse(f.read().decode("utf-8").splitlines())
        _robots_cache[base_url] = rp
        return rp.can_fetch("*", target_url)

    except Exception as e:
      
        print(f"  ⚠️  robots.txt failed for {base_url}: {type(e).__name__}")
        _robots_cache[base_url] = None
        return True
