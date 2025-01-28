import logging

from mitmproxy import ctx, http

from mitmproxyman import manager
from mitmproxyman.utils.cookies import (create_cookies_from_request_header,
                                        create_request_header_from_cookies,
                                        merge_and_replace_cookies)

profiles = manager.get_project_configuration()
logging.info(profiles)


processed_requests = set()


def request(flow: http.HTTPFlow):
    if flow.id in processed_requests:
        return

    processed_requests.add(flow.id)

    request_cookies = flow.request.headers.get("cookie", "")
    if not request_cookies:
        return

    for profile in profiles:
        if not profile.scope.search(flow.request.host):
            return

        flow_copy = flow.copy()

        cookies = create_cookies_from_request_header(request_cookies)
        cookies = merge_and_replace_cookies(cookies, profile.cookies)

        flow_copy.request.headers["cookie"] = create_request_header_from_cookies(
            cookies
        )

        logging.info(f"Sending request with {profile.name} profile")
        ctx.master.commands.call("replay.client", [flow_copy])
        processed_requests.add(flow_copy.id)
