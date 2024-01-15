def is_htmx(request, boost_check=True):
    hx_boost = request.headers.get("Hx-Boosted")
    hx_request = request.headers.get("Hx-Request")
    if boost_check and hx_boost:
        return False

    elif boost_check and not hx_boost and hx_request:
        return True
