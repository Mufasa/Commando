from nose.tools import *

from Cli import Cli
from Cli import CliParseError
from Cli import NUMERIC_VALUE_FORMATTER
from Cli import positional

class MyOptions(object):
   def getOptionalA(self): pass
   def getOptionalB(self): pass

   @positional(1)
   def getPositionalArgumentA(self): pass

   @positional(2)
   def getPositionalArgumentB(self): pass

class RandomPositionsOptions(object):
   @positional(8)
   def getPositionalArgument8(self, valueFormatter=NUMERIC_VALUE_FORMATTER): pass

   @positional(12)
   def getPositionalArgument12(self, valueFormatter=NUMERIC_VALUE_FORMATTER): pass

   @positional(-1)
   def getPositionalArgumentMinus1(self, valueFormatter=NUMERIC_VALUE_FORMATTER): pass

class MultiValuedAndPositionalOptions(object):
   def getOption(self, multiValued): pass

   @positional(1)
   def getPositionalArgumentA(self): pass

   @positional(2)
   def getPositionalArgumentB(self): pass

class BadDuplicatePosition(object):
   @positional(1)
   def getPositionalArgumentA(self): pass

   @positional(1)
   def getPositionalArgumentB(self): pass

class BadShortName(object):
   @positional(1)
   def getPositionalArgumentA(self, shortName='a'): pass

class BadDefault(object):
   @positional(1)
   def getPositionalArgumentA(self, default=1): pass

class BadMultiValued(object):
   @positional(1)
   def getPositionalArgumentA(self, multiValued): pass

class BadMin(object):
   @positional(1)
   def getPositionalArgumentA(self, min=1): pass

class BadMax(object):
   @positional(1)
   def getPositionalArgumentA(self, max=1): pass

class BadMandatory(object):
   @positional(1)
   def getPositionalArgumentA(self, mandatory): pass

class TestCliWithPositional(object):
   def testMissingPositionalArgumentsThrows(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['--optionalA', 'A', '--optionalB', 'B'])

   def testInsufficientPositionalArgumentsThrows(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['pA'])

   def testPositionalArgumentsAloneRetrievedCorrectly(self):
      myOptions = Cli(MyOptions).parseArguments(['pA', 'pB'])
      assert_equals(myOptions.getPositionalArgumentA(), 'pA')
      assert_equals(myOptions.getPositionalArgumentB(), 'pB')

   def testPositionalArgumentsAfterOptionalRetrievedCorrectly(self):
      myOptions = Cli(MyOptions).parseArguments(['--optionalA', 'A', '--optionalB', 'B', 'pA', 'pB'])
      assert_equals(myOptions.getOptionalA(), 'A')
      assert_equals(myOptions.getOptionalB(), 'B')
      assert_equals(myOptions.getPositionalArgumentA(), 'pA')
      assert_equals(myOptions.getPositionalArgumentB(), 'pB')

   def testPositionalArgumentsWithRandomPositionValuesRetrievedInCorrectOrder(self):
      myOptions = Cli(RandomPositionsOptions).parseArguments(['1', '2', '3'])
      assert_equals(myOptions.getPositionalArgumentMinus1(), 1)
      assert_equals(myOptions.getPositionalArgument8(), 2)
      assert_equals(myOptions.getPositionalArgument12(), 3)

   def testPositionalArgumentsAfterMultiValuedOptionalRetrievedCorrectly(self):
      myOptions = Cli(MultiValuedAndPositionalOptions).parseArguments(['--option', 'A', 'B', 'C', 'pA', 'pB'])
      assert_equals(myOptions.getOption(), ['A', 'B', 'C'])
      assert_equals(myOptions.getPositionalArgumentA(), 'pA')
      assert_equals(myOptions.getPositionalArgumentB(), 'pB')

   def testDuplicatePositionsThrows(self):
      assert_raises(CliParseError, Cli, BadDuplicatePosition)

   def testShortNameOnPositionalArgumentThrows(self):
      assert_raises(CliParseError, Cli, BadShortName)

   def testDefaultOnPositionalArgumentThrows(self):
      assert_raises(CliParseError, Cli, BadDefault)

   def testMultiValuedOnPositionalArgumentThrows(self):
      assert_raises(CliParseError, Cli, BadMultiValued)

   def testMandatoryOnPositionalArgumentThrows(self):
      assert_raises(CliParseError, Cli, BadMandatory)

   def testMinOnPositionalArgumentThrows(self):
      assert_raises(CliParseError, Cli, BadMin)

   def testMaxOnPositionalArgumentThrows(self):
      assert_raises(CliParseError, Cli, BadMax)

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()