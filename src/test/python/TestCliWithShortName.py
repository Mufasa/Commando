from nose.tools import *

from Cli import Cli
from Cli import CliParseError

class MyOptions(object):
   def getOptionWithShortName(self, shortName='o'): pass
   def isBooleanOptionWithShortName(self, shortName='i'): pass

class BadNonStringShortName(object):
   def getOption(self, shortName=123): pass

class BadDuplicateShortName(object):
   def getOptionA(self, shortName='a'): pass
   def getOptionB(self, shortName='a'): pass

class BadShortNameMatchingOwnLongName(object):
   def getOptionA(self, shortName='optionA'): pass

class BadShortNameMatchingOtherLongName(object):
   def getOptionA(self, shortName='a'): pass
   def getOptionB(self, shortName='optionA'): pass

class TestCliWithShortName(object):
   def testOptionWithShortNameCanBeSpecifiedUsingLongName(self):
      myOptions = Cli(MyOptions).parseArguments(['--optionWithShortName', 'abc'])
      assert_equals(myOptions.getOptionWithShortName(), 'abc')

   def testOptionWithShortNameCanBeSpecifiedUsingShortName(self):
      myOptions = Cli(MyOptions).parseArguments(['-o', 'abc'])
      assert_equals(myOptions.getOptionWithShortName(), 'abc')

   def testBooleanOptionWithShortNameCanBeSpecifiedUsingLongName(self):
      myOptions = Cli(MyOptions).parseArguments(['--booleanOptionWithShortName'])
      assert_true(myOptions.isBooleanOptionWithShortName())

   def testMissingBooleanOptionWithShortNameReturnsFalse(self):
      myOptions = Cli(MyOptions).parseArguments([])
      assert_false(myOptions.isBooleanOptionWithShortName())

   def testBooleanOptionWithShortNameCanBeSpecifiedUsingShortName(self):
      myOptions = Cli(MyOptions).parseArguments(['-i'])
      assert_true(myOptions.isBooleanOptionWithShortName())

   def testNonStringShortNameThrows(self):
      assert_raises(CliParseError, Cli, BadNonStringShortName)

   def testDuplicateShortNameThrows(self):
      assert_raises(CliParseError, Cli, BadDuplicateShortName)

   def testShortNameMatchingOwnLongNameThrows(self):
      assert_raises(CliParseError, Cli, BadShortNameMatchingOwnLongName)

   def testShortNameMatchingOtherLongNameThrows(self):
      assert_raises(CliParseError, Cli, BadShortNameMatchingOtherLongName)

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
