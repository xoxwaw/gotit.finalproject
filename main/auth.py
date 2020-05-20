import json
import logging
import re
import base64

import six

__author__ = 'roland'

logger = logging.getLogger(__name__)

class Invalid(Exception):
    """The JWT is invalid."""

class BadSyntax(Invalid):
    """The JWT could not be parsed because the syntax is invalid."""
    def __init__(self, value, msg):
        self.value = value
        self.msg = msg

    def __str__(self):
        return "%s: %r" % (self.msg, self.value)



def split_token(token):
    if not token.count(b"."):
        raise BadSyntax(token,
                        "expected token to contain at least one dot")
    return tuple(token.split(b"."))


def b64e(b):
    u"""Base64 encode some bytes.
    Uses the url-safe - and _ characters, and doesn't pad with = characters."""
    return base64.urlsafe_b64encode(b).rstrip(b"=")

_b64_re = re.compile(b"^[A-Za-z0-9_-]*$")
def b64d(b):
    u"""Decode some base64-encoded bytes.
    Raises BadSyntax if the string contains invalid characters or padding."""

    # Python's base64 functions ignore invalid characters, so we need to
    # check for them explicitly.
    if not _b64_re.match(b):
        raise BadSyntax(b, "base64-encoded data contains illegal characters")

    # add padding chars
    m = len(b) % 4
    if m == 1:
        # NOTE: for some reason b64decode raises *TypeError* if the
        # padding is incorrect.
        raise BadSyntax(b, "incorrect padding")
    elif m == 2:
        b += b"=="
    elif m == 3:
        b += b"="
    return base64.urlsafe_b64decode(b)


def b2s_conv(item):
    if isinstance(item, bytes):
        return item.decode("utf-8")
    elif item is None or isinstance(item, (six.string_types, int, bool)):
        return item
    elif isinstance(item, list):
        return [b2s_conv(i) for i in item]
    elif isinstance(item, dict):
        return dict([(k, b2s_conv(v)) for k, v in item.items()])

    raise ValueError("Can't convert {}.".format(repr(item)))


def b64encode_item(item):
    if isinstance(item, bytes):
        return b64e(item)
    elif isinstance(item, str):
        return b64e(item.encode("utf-8"))
    elif isinstance(item, int):
        return b64e(item)
    else:
        return b64e(json.dumps(b2s_conv(item),
                               separators=(",", ":")).encode("utf-8"))


class JWT(object):
    def __init__(self, **headers):
        if not headers.get("alg"):
            headers["alg"] = None
        self.headers = headers
        self.b64part = [b64encode_item(headers)]
        self.part = [b64d(self.b64part[0])]

    def unpack(self, token):
        """
        Unpacks a JWT into its parts and base64 decodes the parts
        individually
        :param token: The JWT
        """
        if isinstance(token, six.string_types):
            try:
                token = token.encode("utf-8")
            except UnicodeDecodeError:
                pass

        part = split_token(token)
        self.b64part = part
        self.part = [b64d(p) for p in part]
        self.headers = json.loads(self.part[0].decode())
        return self

    def pack(self, parts=None, headers=None):
        """
        Packs components into a JWT
        :param returns: The string representation of a JWT
        """
        if not headers:
            if self.headers:
                headers = self.headers
            else:
                headers = {'alg': 'none'}

        logging.debug('JWT header: {}'.format(headers))

        if not parts:
            return ".".join([a.decode() for a in self.b64part])

        self.part = [headers] + parts
        _all = self.b64part = [b64encode_item(headers)]
        _all.extend([b64encode_item(p) for p in parts])

        return ".".join([a.decode() for a in _all])

    def payload(self):
        _msg = as_unicode(self.part[1])

        # If not JSON web token assume JSON
        if "cty" in self.headers and self.headers["cty"].lower() != "jwt":
            pass
        else:
            try:
                _msg = json.loads(_msg)
            except ValueError:
                pass

        return _msg


def as_unicode(b):
    """
    Convert a byte string to a unicode string
    :param b: byte string
    :return: unicode string
    """
    try:
        b = b.decode()
    except (AttributeError, UnicodeDecodeError):
        pass
    return b