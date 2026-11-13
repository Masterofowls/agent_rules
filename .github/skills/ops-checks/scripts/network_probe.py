"""Isolated network probes so the parent timeout also bounds DNS resolution."""

import argparse
import json
import socket
import ssl
import sys
import time
from datetime import datetime, timezone

from checks import CheckError, bounded_integer, host_name, nonnegative_number, ssh_port


def probe(args: argparse.Namespace) -> dict:
    if not args.authorized:
        raise CheckError("Explicit target authorization required (--authorized)", 2)
    host = host_name(args.host)
    if args.task == "check-dns":
        addresses = {
            (family, address[0])
            for family, _, _, _, address in socket.getaddrinfo(
                host, None, type=socket.SOCK_STREAM
            )
        }
        if not addresses:
            raise CheckError("DNS lookup returned no addresses")
        return {
            "resolved": True,
            "ipv4_count": sum(family == socket.AF_INET for family, _ in addresses),
            "ipv6_count": sum(family == socket.AF_INET6 for family, _ in addresses),
        }
    context = ssl.create_default_context()
    with (
        socket.create_connection((host, args.port), timeout=args.timeout) as connection,
        context.wrap_socket(connection, server_hostname=host) as secured,
    ):
        certificate = secured.getpeercert()
    expiry = certificate.get("notAfter") if isinstance(certificate, dict) else None
    if not isinstance(expiry, str):
        raise CheckError("Verified certificate has no expiry time")
    expires_at = ssl.cert_time_to_seconds(expiry)
    days_remaining = (expires_at - time.time()) / 86400
    if days_remaining < args.min_days:
        raise CheckError(
            f"TLS certificate expires below the {args.min_days:g}-day threshold"
        )
    return {
        "verified": True,
        "expires_at": datetime.fromtimestamp(expires_at, timezone.utc).isoformat(),
        "days_remaining": round(days_remaining, 3),
        "minimum_days": args.min_days,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", choices=("check-dns", "check-tls"))
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=ssh_port, default=443)
    parser.add_argument("--timeout", type=bounded_integer, default=15)
    parser.add_argument("--min-days", type=nonnegative_number, default=14)
    parser.add_argument("--authorized", action="store_true")
    args = parser.parse_args()
    try:
        result = probe(args)
    except CheckError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return exc.code
    except (ssl.SSLError, socket.gaierror, TimeoutError, OSError, ValueError):
        print(
            json.dumps(
                {"error": "DNS, TLS verification, or network connection failed"}
            ),
            file=sys.stderr,
        )
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
