from nose.tools import *

from Cli import Cli
from Cli import CliParseError

class MyOptions(object):
   def getSingleValuedOption(self): pass
   def getMultiValuedOption(self, multiValued, default=['abc', 'def']): pass

class OptionWithMin(object):
   def getOption(self, multiValued, min=1): pass

class OptionWithMax(object):
   def getOption(self, multiValued, max=3): pass

class BadSingleValuedOption(object):
   def getSingleValuedOption(self, default=['x', 'y']): pass

class BadMultiValuedBoolenOption(object):
   def isSomething(self, multiValued): pass

class BadMultiValuedOption(object):
   def getMultiValuedOption(self, multiValued=True): pass

class BadMinUsageOnNonMultiValuedOption(object):
   def getOption(self, min=1): pass

class BadMaxUsageOnNonMultiValuedOption(object):
   def getOption(self, max=1): pass

class BadMinLessThanZeroOption(object):
   def getOption(self, multiValued, min= -1): pass

class BadMinDataTypeOption(object):
   def getOption(self, multiValued, min='a'): pass

class BadMaxLessThanTwoOption(object):
   def getOption(self, multiValued, max=1): pass

class BadMaxDataTypeOption(object):
   def getOption(self, multiValued, max='a'): pass

class BadMaxLessThanMinOption(object):
   def getOption(self, multiValued, min=3, max=2): pass

class BadDefaultLessThanMinOption(object):
   def getOption(self, multiValued, min=2, default=123): pass

class BadDefaultMoreThanMaxOption(object):
   def getOption(self, multiValued, max=2, default=[1, 2, 3]): pass

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

   def testMultiValuedWithMinOptionThrowsIfLessThanMinValuesGiven(self):
      cli = Cli(OptionWithMin)
      assert_raises(CliParseError, cli.parseArguments, [])

   def testMultiValuedWithMinOptionDoesNotThrowsIfAtLeastMinValuesGiven(self):
      cli = Cli(OptionWithMin)
      options = cli.parseArguments(['--option', 'blue'])
      assert_equals(options.getOption(), 'blue')

   def testMultiValuedWithMaxOptionThrowsIfMoreThanMaxValuesGiven(self):
      cli = Cli(OptionWithMax)
      assert_raises(CliParseError, cli.parseArguments, ['--option', 'a', 'b', 'c', 'd'])

   def testMultiValuedWithMaxOptionDoesNotThrowsIfLessThanMaxValuesGiven(self):
      cli = Cli(OptionWithMax)
      options = cli.parseArguments(['--option', 'a', 'b'])
      assert_equals(options.getOption(), ['a', 'b'])

   def testMinOnNonMultiValuedOptionThrows(self):
      assert_raises(CliParseError, Cli, BadMinUsageOnNonMultiValuedOption)

   def testMaxOnNonMultiValuedOptionThrows(self):
      assert_raises(CliParseError, Cli, BadMaxUsageOnNonMultiValuedOption)

   def testMinOptionLessThanZeroThrows(self):
      assert_raises(CliParseError, Cli, BadMinLessThanZeroOption)

   def testNonNumericMinOptionThrows(self):
      assert_raises(CliParseError, Cli, BadMinDataTypeOption)

   def testMaxOptionLessThanTwoThrows(self):
      assert_raises(CliParseError, Cli, BadMaxLessThanTwoOption)

   def testNonNumericMaxOptionThrows(self):
      assert_raises(CliParseError, Cli, BadMaxDataTypeOption)

   def testOptionWithMaxLessThanMinThrows(self):
      assert_raises(CliParseError, Cli, BadMaxLessThanMinOption)

   def testOptionWithMinAndInsufficientDefaultValuesThrows(self):
      assert_raises(CliParseError, Cli, BadDefaultLessThanMinOption)

   def testOptionWithMaxAndTooManyDefaultValuesThrows(self):
      assert_raises(CliParseError, Cli, BadDefaultMoreThanMaxOption)

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
