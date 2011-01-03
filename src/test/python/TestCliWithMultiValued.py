from nose.tools import *

from Cli import Cli
from Cli import CliParseError

class MyOptions(object):
   def getSingleValuedOption(self): pass
   def getMultiValuedOption(self, multiValued, default=['abc', 'def']): pass

class BadSingleValuedOption(object):
   def getSingleValuedOption(self, default=['x', 'y']): pass

class BadMultiValuedBoolenOption(object):
   def isSomething(self, multiValued): pass

class BadMultiValuedOption(object):
   def getMultiValuedOption(self, multiValued=True): pass

class TestCliWithMultiValued(object):
   def testUnspecifiedMultiValuedOptionReturnsDefaults(self):
      myOptions = Cli(MyOptions).parseArguments([])
      assert_equals(myOptions.getMultiValuedOption(), ['abc', 'def'])

   def testMultiValuedOptionReturnsAllSpecifiedValues(self):
      myOptions = Cli(MyOptions).parseArguments(['--multiValuedOption', 'one', 'two', 'three'])
      assert_equals(myOptions.getMultiValuedOption(), ['one', 'two', 'three'])

   def testSingleValuedOptionThrowsIfMultipleDefaultValuesSpecified(self):
      assert_raises(CliParseError, Cli, BadSingleValuedOption)

   def testMultiValuedBoolenOptionThrows(self):
      assert_raises(CliParseError, Cli, BadMultiValuedBoolenOption)

   def testSingleValuedOptionThrowsIfMultipleValuesSpecified(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['--singleValuedOption', 'a', 'b'])

   def testMultiValuedOptionWithValueAgainstMultiValuedAttributeThrows(self):
      assert_raises(CliParseError, Cli, BadMultiValuedOption)

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
