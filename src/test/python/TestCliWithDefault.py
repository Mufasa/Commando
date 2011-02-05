from nose.tools import *

from Cli import Cli
from Cli import CliParseError
from Cli import option

class MyOptions(object):
   @option(default='123')
   def getOptionWithDefault(self): pass

class BooleanOptionWithDefaultSpecified(object):
   @option(default=True)
   def isBadOption(self): pass

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
