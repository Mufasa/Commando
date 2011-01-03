from nose.tools import *

from Cli import Cli
from Cli import CliParseError

class MyOptions(object):
   def isDeleteFiles(self): pass
   def getSimpleOption(self): pass

class TestSimpleCli(object):
   def testNonBooleanOptionWithSingleValueReturnsSpecifiedValue(self):
      myOptions = Cli(MyOptions).parseArguments(['--simpleOption', 'valueA'])
      assert_equals(myOptions.getSimpleOption(), 'valueA')

   def testNonBooleanOptionWithoutValueThrows(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['--simpleOption'])

   def testUnspecifiedNonBooleanOptionWithNoDefaultReturnsNone(self):
      myOptions = Cli(MyOptions).parseArguments([])
      assert_true(myOptions.getSimpleOption() is None)

   def testMissingBooleanOptionReturnsFalse(self):
      myOptions = Cli(MyOptions).parseArguments([])
      assert_false(myOptions.isDeleteFiles())

   def testPresentBooleanOptionReturnsTrue(self):
      myOptions = Cli(MyOptions).parseArguments(['--deleteFiles'])
      assert_true(myOptions.isDeleteFiles())

   def testBooleanOptionWithValueThrows(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['--deleteFiles', 'True'])

   def testOptionMissingFromInterfaceThrows(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['--missingFromInterface'])

   def testInvalidOptionFormatThrows(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['-'])
      assert_raises(CliParseError, cli.parseArguments, ['--'])
      assert_raises(CliParseError, cli.parseArguments, ['---simpleOption'])
      assert_raises(CliParseError, cli.parseArguments, ['-simpleOption', 'valueA'])
      assert_raises(CliParseError, cli.parseArguments, ['simpleOption', 'valueA'])
      assert_raises(CliParseError, cli.parseArguments, ['--SimpleOption'])
      assert_raises(CliParseError, cli.parseArguments, ['-O'])

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
