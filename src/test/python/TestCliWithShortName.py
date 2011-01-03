from nose.tools import *

from Cli import Cli

class MyOptions(object):
   def getOptionWithShortName(self, shortName='o'): pass
   def isBooleanOptionWithShortName(self, shortName='i'): pass

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

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
