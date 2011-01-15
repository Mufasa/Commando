from nose.tools import *

from Cli import Cli
from Cli import NUMERIC_VALUE_FORMATTER

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

class MyOptions2(object):
   def getInputFiles(self, multiValued, mandatory, shortName='f'):
      'List of input files to process'
      pass
   def getOutputFile(self, shortName='o', default='output.csv'):
      'Output filename'
      pass
   def isReplace(self, shortName='r'):
      'Do you want to replace the output file if it already exists'
      pass
   def getMaxOutputSize(self, shortName='m', default=1024, valueFormatter=NUMERIC_VALUE_FORMATTER):
      'Maximum size to limit the output file to'
      pass

class TestCliWithCustomisedHelp(object):
   def testX(self):
      print Cli(MyOptions2).helpText
      assert False

   def testSpecifiedHelpStringsAppearInHelpText(self):
      self.__checkHelpText(Cli(MyOptions).helpText, 'TestCliWithCustomisedHelp.py')

   def testSpecifiedProgramAppearsInHelpText(self):
      self.__checkHelpText(Cli(MyOptions, prog='MyApp.py').helpText, 'MyApp.py')

   def testSpecifiedPurposeAppearsInHelpText(self):
      self.__checkHelpText(Cli(MyOptions, purpose=PURPOSE).helpText, 'TestCliWithCustomisedHelp.py', PURPOSE)

   def __checkHelpText(self, helpText, prog, purpose=None):
      assert_true(helpText.find('Usage: %s [--optionWithShortName, -o value] [--optionWithDefaultList value1 ...] [--optionWithDefaultAndShortName, -t value] [--deleteFiles] [--optionWithDefault value] [--booleanOptionWithShortName, -i] [--simpleOption value]\n' % prog) != -1)

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

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
