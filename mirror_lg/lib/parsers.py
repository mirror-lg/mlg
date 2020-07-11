"""
Parser for shared library functions
"""

def parse_exploded_address(cidr: str) -> str:
    """remove cidr notation and return address as str"""
    exploded_ip_list = cidr.split('/')
    result = exploded_ip_list[0]

    return result
