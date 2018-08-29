from tld import get_tld
from urlparse import urlparse
import ipaddress
import json

DISCONNECT_JSON = "adblock/disconnect.json"


def get_tld_or_host(url):
    if not url.startswith("http"):
        url = 'http://' + url

    try:
        return get_tld(url, fail_silently=False)
    except Exception:
        hostname = urlparse(url).hostname
        try:
            ipaddress.ip_address(hostname)
            return hostname
        except Exception:
            return None


def is_third_party(url, site_url):
    # !!!: We return False when we have missing information
    if not site_url:
        return False

    site_ps1 = get_tld_or_host(site_url)
    if site_ps1 is None:
        return False

    req_ps1 = get_tld_or_host(url)
    if req_ps1 is None:
        # print url
        return False
    if (req_ps1 == site_ps1):
        return False

    return True


def get_disconnect_blocked_hosts(disconnect_json=DISCONNECT_JSON):
    blocked_hosts = set()
    disconnect = json.loads(open(disconnect_json).read())
    categories = disconnect["categories"]
    for _, entries in categories.iteritems():
        for entry in entries:
            adresses = entry.values()
            for address in adresses:
                address.pop("dnt", None)  # there's one such entry
                # and it's not a domain/host
                hosts_list = address.values()
                blocked_hosts.update(hosts_list[0])

    print len(blocked_hosts), "blocked hosts"
    # note that disconnect keep a list of blocked hosts, not PS+1s
    assert "adwords.google.com" in blocked_hosts
    assert "facebook.com" in blocked_hosts
    return list(blocked_hosts)


def is_blocked_by_disconnect_old(url, disconnect_blocked_hosts):
    return urlparse(url).hostname in disconnect_blocked_hosts


def is_blocked_by_disconnect(url, disconnect_blocked_hosts):
    host = urlparse(url).hostname
    if host in disconnect_blocked_hosts:
        return True
    while True:
        # strip one subdomain at a time
        host = host.split(".", 1)[-1]  # take foo.com from bar.foo.com
        if "." not in host:
            return False
        if host in disconnect_blocked_hosts:
            return True
    return False  # this shouldn't happen unless we are provided a corrupt hostname


if __name__ == '__main__':
    # Test for the is_blocked_by_disconnect
    # TODO: move to a separate file
    assert is_blocked_by_disconnect("http://adwords.google.com", ["facebook.com", "adwords.google.com"])
    assert not is_blocked_by_disconnect("http://example.com", ["facebook.com", "google.com"])
    assert not is_blocked_by_disconnect("http://8.8.8.8", ["facebook.com", "google.com"])
    disconnect_blocked_hosts = get_disconnect_blocked_hosts()
    assert is_blocked_by_disconnect("https://tps40.doubleverify.com/visit.js",
                                    disconnect_blocked_hosts)
    assert is_blocked_by_disconnect("https://pagead2.googlesyndication.com/bg/CI_hqThbQjBwoUSK10cIsovHByRI4InaU0wolTzGCLU.js",
                                    disconnect_blocked_hosts)
    assert not is_blocked_by_disconnect("http://bar-foo.com", ["foo.com"])
    assert not is_blocked_by_disconnect("http://oo.com", ["foo.com"])
    assert is_blocked_by_disconnect("http://bar.foo.com", ["foo.com"])
    assert is_blocked_by_disconnect("http://sub.bar.foo.com", ["foo.com"])
