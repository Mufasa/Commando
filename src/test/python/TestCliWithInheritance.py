from nose.tools import *

from Cli import Cli
from Cli import option

class ParentOptions(object):
   @option
   def isDeleteFiles(self): pass

class MyOptions(ParentOptions):
   @option
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
