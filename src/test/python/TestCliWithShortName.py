from nose.tools import *

from Cli import Cli
from Cli import CliParseError
from Cli import option

class MyOptions(object):
   @option(shortName='o')
   def getOptionWithShortName(self): pass

   @option(shortName='i')
   def isBooleanOptionWithShortName(self): pass

class BadNonStringShortName(object):
   @option(shortName=123)
   def getOption(self): pass

class BadDuplicateShortName(object):
   @option(shortName='a')
   def getOptionA(self): pass

   @option(shortName='a')
   def getOptionB(self): pass

class BadShortNameMatchingOwnLongName(object):
   @option(shortName='optionA')
   def getOptionA(self): pass

class BadShortNameMatchingOtherLongName(object):
   @option(shortName='a')
   def getOptionA(self): pass

   @option(shortName='optionA')
   def getOptionB(self): pass

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
