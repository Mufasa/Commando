from nose.tools import *

from Cli import Cli
from Cli import CliHelpError

class MyOptions(object):
   def isDeleteFiles(self): pass
   def getSimpleOption(self): pass
   def getOptionWithDefault(self, default='123'): pass
   def getOptionWithDefaultList(self, multiValued, default=['123', '456']): pass
   def getOptionWithShortName(self, shortName='o'): pass
   def isBooleanOptionWithShortName(self, shortName='i'): pass
   def getOptionWithDefaultAndShortName(self, default=999, shortName='t'): pass

class TestCliWithDefaultHelp(object):
   def testCanRequestHelpTextFromCliInstance(self):
      self.__checkHelpText(Cli(MyOptions).helpText)

   def testCanRequestHelpTextFromParsedArguments(self):
      self.__checkHelpText(Cli(MyOptions).parseArguments([]).helpText)

   def testMinusMinusHelpGeneratesHelpText(self):
      try:
         Cli(MyOptions).parseArguments(['--help'])
         assert False
      except CliHelpError as e:
         self.__checkHelpText(e.helpText)

   def testMinusQuestionMarkGeneratesHelpText(self):
      try:
         Cli(MyOptions).parseArguments(['-?'])
         assert False
      except CliHelpError as e:
         self.__checkHelpText(e.helpText)

   def __checkHelpText(self, helpText):
      assert_true(helpText.startswith('Usage: TestCliWithDefaultHelp.py [--optionWithShortName, -o value] [--optionWithDefaultList value1 value2 ...] [--optionWithDefaultAndShortName, -t value] [--deleteFiles] [--optionWithDefault value] [--booleanOptionWithShortName, -i] [--simpleOption value]\n'))
      assert_true(helpText.find('where:\n') != -1)
      assert_true(helpText.find('--deleteFiles                                         (True if specified, otherwise False)') != -1)
      assert_true(helpText.find('--simpleOption                      value') != -1)
      assert_true(helpText.find('--optionWithDefault                 value             (default=\'123\')') != -1)
      assert_true(helpText.find('--optionWithDefaultList             value1 value2 ... (default=[\'123\', \'456\'])') != -1)
      assert_true(helpText.find('--optionWithShortName,           -o value') != -1)
      assert_true(helpText.find('--booleanOptionWithShortName,    -i                   (True if specified, otherwise False)') != -1)
      assert_true(helpText.find('--optionWithDefaultAndShortName, -t value             (default=\'999\')') != -1)

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
