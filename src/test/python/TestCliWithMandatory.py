from nose.tools import *

from Cli import Cli
from Cli import CliParseError
from Cli import option

class MyOptions(object):
   @option
   def getOption(self): pass

   @option(mandatory=True)
   def getMandatoryOption(self): pass

class BadMandatoryWithDefaultOption(object):
   @option(mandatory=True, default=123)
   def getOption(self): pass

class TestCliWithMandatory(object):
   def testUnspecifiedNonMandatoryOptionReturnsNone(self):
      myOptions = Cli(MyOptions).parseArguments(['--mandatoryOption', 'value'])
      assert_true(myOptions.getOption() is None)

   def testUnspecifiedMandatoryOptionThrows(self):
      cli = Cli(MyOptions)
      assert_raises(CliParseError, cli.parseArguments, ['--option', 'value'])

   def testMandatoryOptionWithDefaultValueThrows(self):
      assert_raises(CliParseError, Cli, BadMandatoryWithDefaultOption)

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
