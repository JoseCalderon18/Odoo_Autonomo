class LegalResponseError(Exception):
    pass


def require_status_ok(root):
    status = root.find("status")
    code = status.findtext("code") if status is not None else None
    text = status.findtext("text") if status is not None else None
    if code != "200":
        raise LegalResponseError(f"BOE API returned {code or 'unknown'}: {text or 'no status text'}")
