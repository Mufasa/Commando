from nose.tools import *

from Cli import Cli
from Cli import CliParseError
from Cli import option
from Cli import positional

class MyOptions(object):
   @option
   def getOptionalA(self): pass

   @option
   def getOptionalB(self): pass

   @positional(1)
   def getPositionalArgumentA(self): pass

   @positional(2)
   def getPositionalArgumentB(self): pass

class BooleanPositionalOptions(object):
   @positional(1)
   def isTest(self): pass

class SinglePositionalOptions(object):
   @positional(1)
   def getPositionalArgumentA(self): pass

class RandomPositionsOptions(object):
   @positional(8)
   def getPositionalArgument8(self): pass

   @positional(12)
   def getPositionalArgument12(self): pass

   @positional(-1)
   def getPositionalArgumentMinus1(self): pass

class MultiValuedAndPositionalOptions(object):
   @option(multiValued=True)
   def getOption(self): pass

   @positional(1)
   def getPositionalArgumentA(self): pass

   @positional(2)
   def getPositionalArgumentB(self): pass

class BadDuplicatePosition(object):
   @positional(1)
   def getPositionalArgumentA(self): pass

   @positional(1)
   def getPositionalArgumentB(self): pass

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

   def testBooleanPositionalArgumentAllowsTrue(self):
      cli = Cli(BooleanPositionalOptions)

      myOptions = cli.parseArguments(['true'])
      assert_true(myOptions.isTest())

      myOptions = cli.parseArguments(['True'])
      assert_true(myOptions.isTest())

      myOptions = cli.parseArguments(['tRue'])
      assert_true(myOptions.isTest())

      myOptions = cli.parseArguments(['TRUE'])
      assert_true(myOptions.isTest())

   def testBooleanPositionalArgumentAllowsFalse(self):
      cli = Cli(BooleanPositionalOptions)

      myOptions = cli.parseArguments(['false'])
      assert_false(myOptions.isTest())

      myOptions = cli.parseArguments(['False'])
      assert_false(myOptions.isTest())

      myOptions = cli.parseArguments(['fAlse'])
      assert_false(myOptions.isTest())

      myOptions = cli.parseArguments(['FALSE'])
      assert_false(myOptions.isTest())

   def testBooleanPositionalArgumentThrowsIfNotTrueOrFalse(self):
      cli = Cli(BooleanPositionalOptions)
      assert_raises(CliParseError, cli.parseArguments, ['wibble'])

   def testSinglePositionalArgumentRetrievedAsAValue(self):
      myOptions = Cli(SinglePositionalOptions).parseArguments(['pA'])
      assert_equals(myOptions.getPositionalArgumentA(), 'pA')

   def testPositionalArgumentsWithRandomPositionValuesRetrievedInCorrectOrder(self):
      myOptions = Cli(RandomPositionsOptions).parseArguments(['1', '2', '3'])
      assert_equals(myOptions.getPositionalArgumentMinus1(), '1')
      assert_equals(myOptions.getPositionalArgument8(), '2')
      assert_equals(myOptions.getPositionalArgument12(), '3')

   def testPositionalArgumentsAfterMultiValuedOptionalRetrievedCorrectly(self):
      myOptions = Cli(MultiValuedAndPositionalOptions).parseArguments(['--option', 'A', 'B', 'C', 'pA', 'pB'])
      assert_equals(myOptions.getOption(), ['A', 'B', 'C'])
      assert_equals(myOptions.getPositionalArgumentA(), 'pA')
      assert_equals(myOptions.getPositionalArgumentB(), 'pB')

   def testNonIntPositionalDataTypeThrows(self):
      try:
         class BadPositionalDataType(object):
            @positional('1')
            def getPositionalArgument(self): pass
      except:
         return

      assert False, 'Non int data type for @positional value should not be allowed'

   def testDuplicatePositionsThrows(self):
      assert_raises(CliParseError, Cli, BadDuplicatePosition)

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
