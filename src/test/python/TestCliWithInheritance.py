from nose.tools import *

from Cli import Cli

class ParentOptions(object):
   def isDeleteFiles(self): pass

class MyOptions(ParentOptions):
   def getSimpleOption(self): pass

class TestCliWithInheritance(object):
   def testInheritedOptionIsParsedCorrectly(self):
      myOptions = Cli(MyOptions).parseArguments(['--simpleOption', 'valueA', '--deleteFiles'])
      assert_equals(myOptions.getSimpleOption(), 'valueA')
      assert_true(myOptions.isDeleteFiles())

if __name__ == '__main__':
   import sys, inspect, nose

   sys.argv = ['', inspect.getmodulename(__file__)]
   nose.main()
