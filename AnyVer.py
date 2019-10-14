__all__ = ("AnyVer",)

"""This module is meant to allow you to parse, compare and edit an any version string containing numbers in the order `major version` `minor version` `patch version`. Major version can be a year.
"""

import typing
import re
from array import array

defaultSeparator = "."
defaultSuffixFormat = "-{hash}"
specifiers2Try = "BHLQ"


class _AnyVer:
	"""This class contains the functionality to store and compare version numbers."""

	__slots__ = ("format", "parsed", "hash", "suffixFormat")

	def __init__(self, parsed: typing.Iterable[int], hash: typing.Optional[str] = None, *, format=None, suffixFormat="") -> None:  # pylint: disable=W0622
		for s in specifiers2Try:
			try:
				parsed = array(s, parsed)
				break
			except OverflowError:
				continue
		self.parsed = parsed
		self.hash = hash
		if format is None:
			format = defaultSeparator.join("{" + str(i) + "}" for i in range(len(parsed)))
		self.format = format

		if not suffixFormat and hash:
			suffixFormat = defaultSuffixFormat
		self.suffixFormat = suffixFormat

	def __iter__(self) -> typing.Iterator[int]:
		yield from self.parsed

	def __len__(self) -> int:
		return len(self.parsed)

	def __getitem__(self, k: int) -> int:
		return self.parsed[k]

	def __setitem__(self, k: int, v: int) -> None:
		self.parsed[k] = v

	def __repr__(self) -> str:
		return self.__class__.__name__ + "(" + ", ".join((repr(self.parsed), repr(self.hash), "format=" + repr(self.format), "suffixFormat=" + repr(self.suffixFormat))) + ")"

	def __str__(self) -> str:
		return self.format.format(*self.parsed) + self.suffixFormat.format(hash=self.hash)

	def __eq__(self, other: typing.Union["_AnyVer", typing.Iterable[int]]) -> bool:
		if not self.format == other.format:
			print(repr(self.format), repr(other.format))
		return tuple(self) == tuple(other) and ((self.format == other.format) if isinstance(other, __class__) else True)

	def __hash__(self):
		return hash(tuple(self) + (self.format,))

	def __gt__(self, other) -> bool:
		return tuple(self) > tuple(other)

	def __lt__(self, other) -> bool:
		return tuple(self) < tuple(other)

	def __radd__(self, other: str) -> str:
		if isinstance(other, str):
			return other + str(self)
		raise NotImplementedError()
		if isinstance(other, _AnyVer):
			return _AnyVer()

	def __add__(self, other: str) -> str:
		if isinstance(other, str):
			return str(self) + other
		raise NotImplementedError()
		if isinstance(other, _AnyVer):
			return _AnyVer()

	@property
	def major(self) -> typing.Optional[int]:
		if len(self) < 1:
			raise AttributeError()
		return self.parsed[0]

	@major.setter
	def major(self, v) -> None:
		if len(self) < 1:
			raise AttributeError()
		self.parsed[0] = v

	@property
	def minor(self) -> typing.Optional[int]:
		if len(self) < 2:
			raise AttributeError()
		return self.parsed[1]

	@minor.setter
	def minor(self, v) -> None:
		if len(self) < 2:
			raise AttributeError()
		self.parsed[1] = v

	@property
	def patch(self) -> typing.Optional[int]:
		if len(self) < 3:
			raise AttributeError()
		return self.parsed[2]

	@patch.setter
	def patch(self, v) -> None:
		if len(self) < 3:
			raise AttributeError()
		self.parsed[2] = v

	@property
	def tweak(self) -> typing.Optional[int]:
		if len(self) < 4:
			raise AttributeError()
		return self.parsed[3]

	@tweak.setter
	def tweak(self, v) -> None:
		if len(self) < 4:
			raise AttributeError()
		self.parsed[3] = v


numberRx = re.compile("(\\b|(?<=\\w))\\d+(\\b|(?=\\w))", re.I)
hexRx = re.compile("\\b([\\da-f]+[a-f][\\da-f]*|[\\da-f]*[a-f][\\da-f]+)\\b", re.I)


def parseVersionComponents(ver: str) -> typing.Dict[str, typing.Union[typing.Optional[str], typing.List[int]]]:
	ver1 = ver.replace("}", "}}").replace("{", "{{")
	
	hash = ""  # pylint: disable=W0622
	maxPos = 0
	def replacerHash(m):
		nonlocal hash, maxPos
		hash = m.group(0)[::-1]  # pylint: disable=W0622
		maxPos = len(ver1) - m.span()[1]
		return "{hash}"[::-1]
	
	ver2 = hexRx.sub(replacerHash, ver1[::-1])[::-1]
	if maxPos:
		maxPos += len(ver2) - len(ver1)
		suffix = ver2[maxPos:]
		ver2 = ver2[:maxPos]  # pylint: disable=W0622
	else:
		ver2 = ver1
		suffix = ""
	

	parsed = []
	maxPos = 0
	def replacerVersion(m):
		nonlocal parsed, maxPos
		idx = len(parsed)
		maxPos = max(m.span()[1], maxPos)
		parsed.append(int(m.group(0)))
		return "{" + str(idx) + "}"

	rr = numberRx.subn(replacerVersion, ver2)
	if not rr[1]:
		if not hash:
			raise ValueError("Version is not parsed: " + repr(ver))
	ver3 = rr[0]
	maxPos += len(ver3) - len(ver2)

	format = ver3[:maxPos]  # pylint: disable=W0622
	suffix = ver3[maxPos:] + suffix
	res = {"format": format, "parsed": parsed, "hash": hash, "suffixFormat": suffix}
	return res


class AnyVer(_AnyVer):
	__slots__ = ()

	def __init__(self, ver: str) -> None:
		if isinstance(ver, _AnyVer):
			super().__init__(ver.parsed, ver.hash, format=ver.format, suffixFormat=ver.suffixFormat)
		elif isinstance(ver, str):
			super().__init__(**parseVersionComponents(ver))
		else:
			raise ValueError("Incorrect type for `ver` argument: " + repr(type(ver)))

	def __repr__(self) -> str:
		return self.__class__.__name__ + "(" + repr(str(self)) + ")"
