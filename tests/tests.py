#!/usr/bin/env python3
import sys
from pathlib import Path
from collections import OrderedDict
import unittest
from array import array

thisFile = Path(__file__).absolute()
thisDir = thisFile.parent.absolute()
repoMainDir = thisDir.parent.absolute()
sys.path.append(str(repoMainDir))

dict = OrderedDict

from AnyVer import _AnyVer, AnyVer, parseVersionComponents


class SimpleTests(unittest.TestCase):
	def setUp(self) -> None:
		self.maxDiff = None

	pairs = {
		"0.1.2.3": ({'format': '{0}.{1}.{2}.{3}', 'parsed': [0, 1, 2, 3], 'hash': '', 'suffixFormat': ''}, _AnyVer(array('B', (0, 1, 2, 3)))),
		"0-1-2-3": ({'format': '{0}-{1}-{2}-{3}', 'parsed': [0, 1, 2, 3], 'hash': '', 'suffixFormat': ''}, _AnyVer(array('B', (0, 1, 2, 3)), format="{0}-{1}-{2}-{3}")),
		"0-1.2 3": ({'format': '{0}-{1}.{2} {3}', 'parsed': [0, 1, 2, 3], 'hash': '', 'suffixFormat': ''}, _AnyVer(array('B', (0, 1, 2, 3)), format="{0}-{1}.{2} {3}")),
		"20190405ubuntu1": ({'format': '{0}ubuntu{1}', 'parsed': [20190405, 1], 'hash': '', 'suffixFormat': ''}, _AnyVer(array('L', (20190405, 1)), format="{0}ubuntu{1}")),
		"3build1": ({'format': '{0}build{1}', 'parsed': [3, 1], 'hash': '', 'suffixFormat': ''}, _AnyVer(array('B', (3, 1)), format="{0}build{1}")),
		"2019-10-16 0A7FF": ({'format': '{0}-{1}-{2}', 'parsed': [2019, 10, 16], 'hash': '0A7FF', 'suffixFormat': ' {hash}'}, _AnyVer(array('H', (2019, 10, 16)), hash="0A7FF", format="{0}-{1}-{2}", suffixFormat=" {hash}")),
		"1.6.2+git20170426.d24a630-2ubuntu1": ({'format': '{0}.{1}.{2}+git{3}', 'parsed': [1, 6, 2, 20170426], 'hash': 'd24a630', 'suffixFormat': '.{hash}-2ubuntu1'}, _AnyVer(array('L', (1, 6, 2, 20170426)), hash="0A7FF", format='{0}.{1}.{2}+git{3}', suffixFormat=".{hash}-2ubuntu1")),
		
	}
	
	def testIdentitiesParsing(self) -> None:
		for (c, (parsingDict, r)) in self.__class__.pairs.items():
			with self.subTest(c=c, r=r):
				self.assertEqual(parseVersionComponents(c), parsingDict)
	
	
	def testHashability(self) -> None:
		for (c, (parsingDict, r)) in self.__class__.pairs.items():
			with self.subTest(c=c, r=r):
				p = AnyVer(c)
				self.assertEqual(hash(p), hash(r))
	
	
	def testTypeCheck(self) -> None:
		with self.assertRaises(ValueError):
			AnyVer(None)
	
	def testUnparseableVersion(self) -> None:
		with self.assertRaises(ValueError):
			AnyVer("fffffuuuu")
	
	
	def testRepr(self) -> None:
		self.assertEqual(repr(_AnyVer(array('H', (2019, 10, 16)), hash="F2BFA", format="{0}-{1}-{2}", suffixFormat=" {hash}")), "_AnyVer(array('H', [2019, 10, 16]), 'F2BFA', format='{0}-{1}-{2}', suffixFormat=' {hash}')")
		self.assertEqual(repr(AnyVer("2019-10-16 F2BFA")), "AnyVer('2019-10-16 F2BFA')")

	
	def testGt(self):
		self.assertGreater(AnyVer("2019-10-17 F2BFA"), AnyVer("2019-10-16 F2BFA"))
	
	
	def testLt(self):
		self.assertLess(AnyVer("2019-10-16 F2BFA"), AnyVer("2019-10-17 F2BFA"))
	
	
	def testCloning(self) -> None:
		a = AnyVer("0-1.2 3-F2BFA")
		b = AnyVer(a)
		self.assertEqual(a, b)
	
	def testToStringConversion(self) -> None:
		etalonStr = "0-1-2-3"
		a = _AnyVer((0, 1, 2, 3), format="{0}-{1}-{2}-{3}")
		
		self.assertEqual(str(a), etalonStr)
		self.assertEqual(a + "b", etalonStr + "b")
		self.assertEqual("b" + a, "b" + etalonStr)

	def testIdentities(self) -> None:
		for (c, (parsingDict, r)) in self.__class__.pairs.items():
			with self.subTest(c=c, r=r):
				p = AnyVer(c)
				self.assertEqual(p, r)
				self.assertEqual(p.suffixFormat, r.suffixFormat)
	
	def testRoundTrip(self) -> None:
		for (c, (parsingDict, r)) in self.__class__.pairs.items():
			with self.subTest(c=c, r=r):
				self.assertEqual(str(AnyVer(c)), c)
	
	def testEditing(self) -> None:
		a = AnyVer("0-1.2 3-F2BFA")
		b = _AnyVer(array('B', (1, 2, 3, 4)), hash="F2BFA", format="{0}-{1}.{2} {3}")
		for i in range(4):
			a[i] += 1
		self.assertEqual(a, b)
		self.assertEqual(str(a), str(b))
	
	def testNamedComponents(self) -> None:
		a = AnyVer("0-1.2 3-F2BFA")
		self.assertEqual(a.major, 0)
		self.assertEqual(a.minor, 1)
		self.assertEqual(a.patch, 2)
		self.assertEqual(a.tweak, 3)
		
		a.major=3
		a.minor=2
		a.patch=1
		a.tweak=0
		self.assertEqual(tuple(a), (3, 2, 1, 0))


if __name__ == "__main__":
	unittest.main()
