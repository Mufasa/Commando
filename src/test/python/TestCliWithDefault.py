from nose.tools import *

from Cli import Cli
from Cli import CliParseError

class MyOptions(object):
   def getOptionWithDefault(self, default='123'): pass

class BooleanOptionWithDefaultSpecified(object):
   def isBadOption(self, default=True): pass

class TestCliWithDefault(object):
   def testUnspecifiedNonBooleanOptionWithDefaultReturnsDefault(self):
      myOptions = Cli(MyOptions).parseArguments([])
      assert_equals(myOptions.getOptionWithDefault(), '123')

   def testNonBooleanOptionWithDefaultWithSingleValueReturnsSpecifiedValue(self):
      myOptions = Cli(MyOptions).parseArguments(['--optionWithDefault', '567'])
      assert_equals(myOptions.getOptionWithDefault(), '567')

   def testBooleanOptionWithDefaultThrows(self):
      assert_raises(CliParseError, Cli, BooleanOptionWithDefaultSpecified)

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
