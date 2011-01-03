from nose.tools import *

from Cli import Cli
from Cli import CliParseError

class MyOptions(object):
   def getOption(self): pass
   def getMandatoryOption(self, mandatory): pass

class BadMandatoryOption(object):
   def getMandatoryOption(self, mandatory=True): pass

class TestCliWithMandatory(object):
   def testUnspecifiedNonMandatoryOptionReturnsNone(self):
      myOptions = Cli(MyOptions).parseArguments(['--mandatoryOption', 'value'])
      assert_true(myOptions.getOption() is None)

   def testUnspecifiedMandatoryOptionThrows(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['--option', 'value'])

   def testMandatoryOptionWithValueAgainstMandatoryAttributeThrows(self):
      assert_raises(CliParseError, Cli, BadMandatoryOption)

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
