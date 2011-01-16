from nose.tools import *

from Cli import Cli
from Cli import CliHelpError
from Cli import positional

class MyOptions(object):
   def isDeleteFiles(self): pass
   def getSimpleOption(self): pass
   def getOptionWithDefault(self, default='123'): pass
   def getOptionWithDefaultList(self, multiValued, default=['123', '456']): pass
   def getOptionWithShortName(self, shortName='o'): pass
   def isBooleanOptionWithShortName(self, shortName='i'): pass
   def getOptionWithDefaultAndShortName(self, default=999, shortName='t'): pass
   def getOptionWithMin1(self, multiValued, min=1): pass
   def getOptionWithMin2(self, multiValued, min=2): pass
   def getOptionWithMin3(self, multiValued, min=3): pass
   def getOptionWithMax2(self, multiValued, max=2): pass
   def getOptionWithMax3(self, multiValued, max=3): pass
   def getOptionWithMin1Max2(self, multiValued, min=1, max=2): pass
   def getOptionWithMin1Max3(self, multiValued, min=1, max=3): pass
   def getOptionWithMin2Max2(self, multiValued, min=2, max=2): pass
   def getOptionWithMin2Max3(self, multiValued, min=2, max=3): pass
   def getOptionWithMin2Max4(self, multiValued, min=2, max=4): pass
   def getOptionWithMin3Max3(self, multiValued, min=3, max=3): pass
   def getOptionWithMin3Max4(self, multiValued, min=3, max=4): pass
   def getOptionWithMin3Max5(self, multiValued, min=3, max=5): pass

   @positional(1)
   def getArgumentA(self): pass
   @positional(2)
   def getArgumentB(self): pass

class TestCliWithDefaultHelp(object):
   def testCanRequestHelpTextFromCliInstance(self):
      self.__checkHelpText(Cli(MyOptions).helpText)

   def testCanRequestHelpTextFromParsedArguments(self):
      self.__checkHelpText(Cli(MyOptions).parseArguments(['--optionWithMin1', '1',
                                                          '--optionWithMin2', '1', '2',
                                                          '--optionWithMin3', '1', '2', '3',
                                                          '--optionWithMin1Max2', '1',
                                                          '--optionWithMin1Max3', '1',
                                                          '--optionWithMin2Max2', '1', '2',
                                                          '--optionWithMin2Max3', '1', '2',
                                                          '--optionWithMin2Max4', '1', '2',
                                                          '--optionWithMin3Max3', '1', '2', '3',
                                                          '--optionWithMin3Max4', '1', '2', '3',
                                                          '--optionWithMin3Max5', '1', '2', '3',
                                                          'positionalA', 'positionalB']).helpText)

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
      helpLines = helpText.splitlines()
      usage = helpLines[0]
      assert_true(usage.startswith('Usage: TestCliWithDefaultHelp.py '))
      assert_true(usage.find('[--deleteFiles]') != -1)
      assert_true(usage.find('[--simpleOption value]') != -1)
      assert_true(usage.find('[--optionWithDefault value]') != -1)
      assert_true(usage.find('[--optionWithDefaultList value1 ...]') != -1)
      assert_true(usage.find('[--optionWithShortName, -o value]') != -1)
      assert_true(usage.find('[--booleanOptionWithShortName, -i]') != -1)
      assert_true(usage.find('[--optionWithDefaultAndShortName, -t value]') != -1)
      assert_true(usage.find('--optionWithMin1 value1 ...') != -1)
      assert_true(usage.find('--optionWithMin2 value1 ...') != -1)
      assert_true(usage.find('--optionWithMin3 value1 ...') != -1)
      assert_true(usage.find('[--optionWithMax2 value1 ...]') != -1)
      assert_true(usage.find('[--optionWithMax3 value1 ...]') != -1)
      assert_true(usage.find('--optionWithMin1Max2 value1 ...') != -1)
      assert_true(usage.find('--optionWithMin1Max3 value1 ...') != -1)
      assert_true(usage.find('--optionWithMin2Max2 value1 ...') != -1)
      assert_true(usage.find('--optionWithMin2Max3 value1 ...') != -1)
      assert_true(usage.find('--optionWithMin2Max4 value1 ...') != -1)
      assert_true(usage.find('--optionWithMin3Max3 value1 ...') != -1)
      assert_true(usage.find('--optionWithMin3Max4 value1 ...') != -1)
      assert_true(usage.find('--optionWithMin3Max5 value1 ...') != -1)
      assert_true(usage.endswith('argumentA argumentB\n') != -1)

      assert_true(helpText.find('where:\n') != -1)
      assert_true(helpText.find('--deleteFiles                                                          (True if specified, otherwise False)') != -1)
      assert_true(helpText.find('--simpleOption                      value') != -1)
      assert_true(helpText.find('--optionWithDefault                 value                              (default=\'123\')') != -1)
      assert_true(helpText.find('--optionWithDefaultList             value1 value2 ...                  (default=[\'123\', \'456\'])') != -1)
      assert_true(helpText.find('--optionWithShortName,           -o value') != -1)
      assert_true(helpText.find('--booleanOptionWithShortName,    -i                                    (True if specified, otherwise False)') != -1)
      assert_true(helpText.find('--optionWithDefaultAndShortName, -t value                              (default=\'999\')') != -1)
      assert_true(helpText.find('--optionWithMin1                    valueMin1 ...') != -1)
      assert_true(helpText.find('--optionWithMin2                    value1 valueMin2 ...') != -1)
      assert_true(helpText.find('--optionWithMin3                    value1 ... valueMin3 ...') != -1)
      assert_true(helpText.find('--optionWithMax2                    value1 valueMax2') != -1)
      assert_true(helpText.find('--optionWithMax3                    value1 ... valueMax3') != -1)
      assert_true(helpText.find('--optionWithMin1Max2                valueMin1 valueMax2') != -1)
      assert_true(helpText.find('--optionWithMin1Max3                valueMin1 ... valueMax3') != -1)
      assert_true(helpText.find('--optionWithMin2Max2                value1 valueMinMax2') != -1)
      assert_true(helpText.find('--optionWithMin2Max3                value1 valueMin2 valueMax3') != -1)
      assert_true(helpText.find('--optionWithMin2Max4                value1 valueMin2 ... valueMax4') != -1)
      assert_true(helpText.find('--optionWithMin3Max3                value1 ... valueMinMax3') != -1)
      assert_true(helpText.find('--optionWithMin3Max4                value1 ... valueMin3 valueMax4') != -1)
      assert_true(helpText.find('--optionWithMin3Max5                value1 ... valueMin3 ... valueMax5') != -1)
      assert_equals([arg.strip() for arg in helpLines[-2:]], ['argumentA', 'argumentB'])

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
