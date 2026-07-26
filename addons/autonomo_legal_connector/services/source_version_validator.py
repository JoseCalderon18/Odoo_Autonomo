def source_has_required_references(source):
    return bool(source.code and source.official_url and source.verified_at)
