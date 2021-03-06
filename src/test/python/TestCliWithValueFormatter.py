from nose.tools import *

from Cli import Cli
from Cli import CliParseError
from Cli import option
from Cli import positional
from Cli import DIGIT_STRING_VALUE_FORMATTER
from Cli import NUMERIC_VALUE_FORMATTER
from Cli import STRING_VALUE_FORMATTER

class MyOptions(object):
   @option
   def getSimpleOption(self): pass

   @option(default=123)
   def getSimpleWithDefaultOption(self): pass

   @option(multiValued=True, default=[123, '456'])
   def getSimpleWithDefaultListOption(self): pass

   @option(valueFormatter=STRING_VALUE_FORMATTER)
   def getStringOption(self): pass

   @option(valueFormatter=DIGIT_STRING_VALUE_FORMATTER)
   def getDigitStringOption(self): pass

   @option(multiValued=True, valueFormatter=NUMERIC_VALUE_FORMATTER)
   def getNumericOption(self): pass

class MyPositionalArguments(object):
   @positional(1, valueFormatter=NUMERIC_VALUE_FORMATTER)
   def getSize(self): pass

class TestCliWithValueFormatter(object):
   def testNoValueFormatterSpecifiedReturnsStringType(self):
      myOptions = Cli(MyOptions).parseArguments(['--simpleOption', '123'])
      assert_equals(myOptions.getSimpleOption(), '123')

   def testNoValueFormatterSpecifiedWithNonStringDefaultReturnsStringType(self):
      myOptions = Cli(MyOptions).parseArguments([])
      assert_equals(myOptions.getSimpleWithDefaultOption(), '123')

   def testNoValueFormatterSpecifiedWithNonStringDefaultListReturnsListOfStringType(self):
      myOptions = Cli(MyOptions).parseArguments([])
      assert_equals(myOptions.getSimpleWithDefaultListOption(), ['123', '456'])

   def testStringValueFormatterReturnsStringType(self):
      myOptions = Cli(MyOptions).parseArguments(['--stringOption', '123'])
      assert_equals(myOptions.getStringOption(), '123')

   def testDigitStringValueFormatterReturnsStringType(self):
      myOptions = Cli(MyOptions).parseArguments(['--digitStringOption', '0123'])
      assert_equals(myOptions.getDigitStringOption(), '0123')

   def testDigitStringValueFormatterThrowsOnNonDigits(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['--digitStringOption', 'abc'])

   def testNumericValueFormatterReturnsDecimalNumberAsNumberType(self):
      myOptions = Cli(MyOptions).parseArguments(['--numericOption', '123'])
      assert_equals(myOptions.getNumericOption(), [123])

   def testNumericValueFormatterThrowsOnInvalidDecimalNumber(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['--numericOption', '12a'])

   def testNumericValueFormatterReturnsHexadecimalNumberAsNumberType(self):
      myOptions = Cli(MyOptions).parseArguments(['--numericOption', '0xff', '0xEE'])
      assert_equals(myOptions.getNumericOption(), [0xff, 0xee])

   def testNumericValueFormatterThrowsOnInvalidHexadecimalNumber(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['--numericOption', '0xgg'])

   def testNumericValueFormatterReturnsOctalNumberAsNumberType(self):
      myOptions = Cli(MyOptions).parseArguments(['--numericOption', '017'])
      assert_equals(myOptions.getNumericOption(), [017])

   def testNumericValueFormatterThrowsOnInvalidOctalNumber(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['--numericOption', '0888'])

   def testNumericValueFormatterReturnsBinaryNumberAsNumberType(self):
      myOptions = Cli(MyOptions).parseArguments(['--numericOption', '0b1010'])
      assert_equals(myOptions.getNumericOption(), [0b1010])

   def testNumericValueFormatterThrowsOnInvalidBinaryNumber(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['--numericOption', '0b222'])

   def testPositionalArgumentsCanHaveValueFormatter(self):
      myPositionalArguments = Cli(MyPositionalArguments).parseArguments(['1024'])
      assert_equals(myPositionalArguments.getSize(), 1024)

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
