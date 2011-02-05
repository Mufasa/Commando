from nose.tools import *

from Cli import Cli
from Cli import CliParseError
from Cli import option

class MyOptions(object):
   @option
   def getSingleValuedOption(self): pass

   @option(multiValued=True, default=['abc', 'def'])
   def getMultiValuedOption(self): pass

class OptionWithMin(object):
   @option(multiValued=True, min=1)
   def getOption(self): pass

class OptionWithMax(object):
   @option(multiValued=True, max=3)
   def getOption(self): pass

class BadSingleValuedOption(object):
   @option(default=['x', 'y'])
   def getSingleValuedOption(self): pass

class BadMultiValuedDefaultOption(object):
   @option(multiValued=True, default='abc')
   def getOption(self): pass

class BadMultiValuedBoolenOption(object):
   @option(multiValued=True)
   def isSomething(self): pass

class BadMinUsageOnNonMultiValuedOption(object):
   @option(min=1)
   def getOption(self): pass

class BadMaxUsageOnNonMultiValuedOption(object):
   @option(max=1)
   def getOption(self): pass

class BadMinLessThanZeroOption(object):
   @option(multiValued=True, min= -1)
   def getOption(self): pass

class BadMaxLessThanTwoOption(object):
   @option(multiValued=True, max=1)
   def getOption(self): pass

class BadMaxLessThanMinOption(object):
   @option(multiValued=True, min=3, max=2)
   def getOption(self): pass

class BadDefaultLessThanMinOption(object):
   @option(multiValued=True, min=2, default=[123])
   def getOption(self): pass

class BadDefaultMoreThanMaxOption(object):
   @option(multiValued=True, max=2, default=[1, 2, 3])
   def getOption(self): pass

class TestCliWithMultiValued(object):
   def testUnspecifiedMultiValuedOptionReturnsDefaults(self):
      myOptions = Cli(MyOptions).parseArguments([])
      assert_equals(myOptions.getMultiValuedOption(), ['abc', 'def'])

   def testMultiValuedOptionWithJustOneValueSpecifiedReturnsItAsAList(self):
      myOptions = Cli(MyOptions).parseArguments(['--multiValuedOption', 'one'])
      assert_equals(myOptions.getMultiValuedOption(), ['one'])

   def testMultiValuedOptionReturnsAllSpecifiedValues(self):
      myOptions = Cli(MyOptions).parseArguments(['--multiValuedOption', 'one', 'two', 'three'])
      assert_equals(myOptions.getMultiValuedOption(), ['one', 'two', 'three'])

   def testSingleValuedOptionThrowsIfMultipleDefaultValuesSpecified(self):
      assert_raises(CliParseError, Cli, BadSingleValuedOption)

   def testMultiValuedOptionThrowsIfDefaultIsNotAList(self):
      assert_raises(CliParseError, Cli, BadMultiValuedDefaultOption)

   def testMultiValuedBoolenOptionThrows(self):
      assert_raises(CliParseError, Cli, BadMultiValuedBoolenOption)

   def testSingleValuedOptionThrowsIfMultipleValuesSpecified(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['--singleValuedOption', 'a', 'b'])

   def testMultiValuedWithMinOptionThrowsIfLessThanMinValuesGiven(self):
      cli = Cli(OptionWithMin)
      assert_raises(CliParseError, cli.parseArguments, [])

   def testMultiValuedWithMinOptionDoesNotThrowsIfAtLeastMinValuesGiven(self):
      cli = Cli(OptionWithMin)
      options = cli.parseArguments(['--option', 'blue'])
      assert_equals(options.getOption(), ['blue'])

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
      try:
         class BadMinDataTypeOption(object):
            @option(multiValued=True, min='a')
            def getOption(self): pass
      except:
         return

      assert False, 'Non int data type for "min" parameter value should not be allowed'

   def testMaxOptionLessThanTwoThrows(self):
      assert_raises(CliParseError, Cli, BadMaxLessThanTwoOption)

   def testNonNumericMaxOptionThrows(self):
      try:
         class BadMaxDataTypeOption(object):
            @option(multiValued=True, max='a')
            def getOption(self): pass
      except:
         return

      assert False, 'Non int data type for "max" parameter value should not be allowed'

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
