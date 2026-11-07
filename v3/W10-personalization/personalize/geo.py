"""Coarse geography from ZIP3 prefixes only. Straight-line miles between centroids, NOT drive time.

The centroid table is a small hand-keyed approximation covering only ZIP3s that appear in the
W7 pilot (Denver metro + Colorado Springs). Unknown ZIP3 -> distance None (never invented).
Values are approximate city-area centers, flagged as such; replace with a licensed/open table
(e.g. Census ZCTA) before any production use.
"""
from math import radians, sin, cos, asin, sqrt

# zip3 -> (lat, lon), approximate area centers. UNVERIFIED approximations for prototype only.
ZIP3_CENTROIDS = {
    "802": (39.74, -104.99),  # Denver
    "801": (39.60, -104.85),  # Aurora/Centennial/Parker area (approx)
    "804": (39.75, -105.22),  # Golden
    "809": (38.83, -104.82),  # Colorado Springs
    "803": (40.02, -105.27),  # Boulder
}


def miles(a_zip3, b_zip3):
    a, b = ZIP3_CENTROIDS.get(a_zip3), ZIP3_CENTROIDS.get(b_zip3)
    if not a or not b:
        return None
    la1, lo1, la2, lo2 = map(radians, (a[0], a[1], b[0], b[1]))
    h = sin((la2 - la1) / 2) ** 2 + cos(la1) * cos(la2) * sin((lo2 - lo1) / 2) ** 2
    return round(3958.8 * 2 * asin(sqrt(h)), 1)


def band(m):
    if m is None:
        return "unknown"
    return "local" if m <= 15 else "metro" if m <= 40 else "regional" if m <= 100 else "far"
