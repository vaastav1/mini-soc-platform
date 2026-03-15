import re
from typing import Optional

FAILED_LOGIN_RE  = re.compile(r"Failed password for (?:invalid user )?(\S+) from ([\d.]+) port \d+")
SUCCESS_LOGIN_RE = re.compile(r"Accepted password for (\S+) from ([\d.]+) port \d+")
SUDO_FAIL_RE     = re.compile(r"sudo:.*?(\S+)\s*:.*NOT in sudoers")

def parse_log_line(line: str) -> Optional[dict]:
    m = FAILED_LOGIN_RE.search(line)
    if m:
        return {"type": "failed_login", "user": m.group(1), "ip": m.group(2), "raw": line.strip()}
    m = SUCCESS_LOGIN_RE.search(line)
    if m:
        return {"type": "successful_login", "user": m.group(1), "ip": m.group(2), "raw": line.strip()}
    m = SUDO_FAIL_RE.search(line)
    if m:
        return {"type": "sudo_failure", "user": m.group(1), "ip": "0.0.0.0", "raw": line.strip()}
    return None