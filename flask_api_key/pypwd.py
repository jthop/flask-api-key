# -*- coding: utf-8 -*-
"""

genword(length, charset)

Our goal here is to be 100% compatible with passlib.pwd.genword

"""
import secrets
import string

DEFAULT_CHARSET = string.ascii_letters + string.digits
CHARSETS = {}
CHARSETS['ascii_62'] = string.ascii_letters + string.digits


##########################################


def genword(length=64, _charset='ascii_62'):
	"""Signature should be compatible with passlib.pwd.genword

	Args:
		length: Number of characters long the word will be
		charset: Choices of characters for use in the word

	Returns:
		Returns a random string of <length> made up of <charset>
	"""

	# obviously a defaultdict works here but it just isn't worth it
	charset = CHARSETS.get(_charset)
	if charset is None:
		charset = DEFAULT_CHARSET

	rando = ''.join(secrets.choice(charset) for i in range(length))

	return rando
