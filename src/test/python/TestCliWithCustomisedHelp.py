from nose.tools import *

from Cli import Cli
from Cli import positional

PURPOSE = 'This is where you would describe the purpose of the program using these options'

class MyOptions(object):
   def isDeleteFiles(self):
      'do you want to delete files'
      pass
   def getSimpleOption(self): pass
   def getOptionWithDefault(self, default='123'): pass
   def getOptionWithDefaultList(self, multiValued, default=['123', '456']): pass
   def getOptionWithShortName(self, shortName='o'): pass
   def isBooleanOptionWithShortName(self, shortName='i'): pass
   def getOptionWithDefaultAndShortName(self, default='999', shortName='t'):
      'specific help on this option'
      pass

   @positional(1)
   def getArgumentA(self):
      'help for argumentA'
      pass

   @positional(2)
   def getArgumentB(self): pass

class TestCliWithCustomisedHelp(object):
   def testSpecifiedHelpStringsAppearInHelpText(self):
      self.__checkHelpText(Cli(MyOptions).helpText, 'TestCliWithCustomisedHelp.py')

   def testSpecifiedProgramAppearsInHelpText(self):
      self.__checkHelpText(Cli(MyOptions, prog='MyApp.py').helpText, 'MyApp.py')

   def testSpecifiedPurposeAppearsInHelpText(self):
      self.__checkHelpText(Cli(MyOptions, purpose=PURPOSE).helpText, 'TestCliWithCustomisedHelp.py', PURPOSE)

   def __checkHelpText(self, helpText, prog, purpose=None):
      helpLines = helpText.splitlines()
      usage = helpLines[0]
      assert_true(usage.startswith('Usage: %s' % prog))
      assert_true(usage.find('[--deleteFiles]') != -1)
      assert_true(usage.find('[--simpleOption value]') != -1)
      assert_true(usage.find('[--optionWithDefault value]') != -1)
      assert_true(usage.find('[--optionWithDefaultList value1 ...]') != -1)
      assert_true(usage.find('[--optionWithShortName, -o value]') != -1)
      assert_true(usage.find('[--booleanOptionWithShortName, -i]') != -1)
      assert_true(usage.find('[--optionWithDefaultAndShortName, -t value]') != -1)
      assert_true(usage.endswith('argumentA argumentB\n') != -1)

      if purpose:
         assert_true(helpText.find('%s\n' % PURPOSE) != -1)
      else:
         assert_equals(helpText.find('%s\n' % PURPOSE), -1)

      assert_true(helpText.find('where:\n') != -1)
      assert_true(helpText.find('--deleteFiles                                         (True if specified, otherwise False) do you want to delete files') != -1)
      assert_true(helpText.find('--simpleOption                      value') != -1)
      assert_true(helpText.find('--optionWithDefault                 value             (default=\'123\')') != -1)
      assert_true(helpText.find('--optionWithDefaultList             value1 value2 ... (default=[\'123\', \'456\'])') != -1)
      assert_true(helpText.find('--optionWithShortName,           -o value') != -1)
      assert_true(helpText.find('--booleanOptionWithShortName,    -i                   (True if specified, otherwise False)') != -1)
      assert_true(helpText.find('--optionWithDefaultAndShortName, -t value             (default=\'999\')                      specific help on this option') != -1)
      assert_true(helpText.find('argumentA                                                                                  help for argumentA') != -1)
      assert_equals([arg.strip() for arg in helpLines[-1:]], ['argumentB'])

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
