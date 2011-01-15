******************
Python Cli Library
******************

What is it?
===========
A Python Command Line Interface (Cli) Library.

How do I install it?
====================
Just copy the Cli.py module into your Python site-packages folder.

Copyright & License?
====================
(c) Anjum Naseer <open-cli@anjum.otherinbox.com> 2nd January 2011
Licensed under the (GPL-compatible) MIT License:
http://www.opensource.org/licenses/mit-license.php

Developer Information
=====================
This version was built and tested using Python v2.6.
The unit tests make use of the Python nosetools v1.0.0 library (http://packages.python.org/nose/index.html).

Developed using Eclipse IDE (Build id: 20100218-1602) with following plugins:
   - PyDev v1.6.4 (http://pydev.org/updates)

Each unit test was run within Eclipse by selecting it and then picking Run As -> Python Run 

Eclipse Project Structure
-------------------------
   - ReadMe.txt                                 this file
   - Changes.txt                                list of what has changed in each release of the Cli library
   - .project                                   Eclipse project information file
   - .pydevproject                              Eclipse PyDev Plugin project file
   - .gitignore                                 list of files to ignore when working with GIT
   - src
      |
      +- main
      |    |
      |    +- python
      |         |
      |         +- Cli.py                       Cli source code
      +- test
           |
           +- python
                |
                +- Test*.py                     Unit tests for the Cli library

How do I use it?
================
The Command Line Interface (Cli) Library allows you to both define and
access command line arguments via a user-defined Python interface. As
Python does not have the ability to define an interface, this is achieved
here by using the "pass" keyword to define a standard Python class where
every method is a NOP, e.g.:
     class MyOptions(object):
        def getFilePath(self): pass
        def isRecursive(self): pass

This library was inspired by both Pythons built-in optparse module and the
JewelCli Java library at:
     http://jewelcli.sourceforge.net/index.html

The Cli library has the following features:
     - Ability to define an inheritance hierarchy of options (to aid re-use)
     - Ability define a short name for each option
     - Ability to define default value for each option
     - Ability to mark options as mandatory
     - Ability to mark an option as multi-valued (with optional min/max values)
     - Auto-generates help text based on the interface
     - Ability to define additional custom help text for each option
     - Ability to define custom value formatters for each option
       The library comes with the following pre-built formatters:
          - String (default)
          - Digits-only String
          - Numeric (allows decimal, hexadecimal, binary, octal integers)
     - Ability to specify positional arguments

Every option is defined by a method whose name either starts with "get" or "is".
Methods that start with "is" represent boolean options. "is" methods will return
True if that option was specified, and will return False otherwise.

The interface MyOptions defined above would be populated as follows:
     - No command line arguments specified:   getFilePath() == None,              isRecursive() == False
     - --filePath C:\Some\Folder:             getFilePath() == r'C:\Some\Folder', isRecursive() == False
     - --filePath C:\Some\Folder --recursive: getFilePath() == r'C:\Some\Folder', isRecursive() == True

The library is best documented by examining its test cases which are split by feature:
     - TestSimpleCli.py                    This represents the simplest usage
     - TestCliWithInheritance.py           This shows how options can be inherited
     - TestCliWithDefault.py               This shows how default values can be specified
     - TestCliWithMandatory.py             This shows how to specify an option as being mandatory
     - TestCliWithMultiValued.py           This shows how to specify an option with multiple values
     - TestCliWithShortName.py             This shows how each option can be given a short name
     - TestCliWithDefaultHelp.py           This shows to access the default help text
     - TestCliWithCustomisedHelp.py        This shows how to enhance the help text
     - TestCliWithValueFormatter.py        This shows how the option values can be formatted to suit your needs
     - TestCliWithPositional.py            This shows how to specify positional arguments
     
Typical Usage
=============
MyApp.py:
   from Cli import Cli
   from Cli import NUMERIC_VALUE_FORMATTER

   class MyOptions(object):
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

   if __name__ == '__main__':
      myOptions = Cli(MyOptions).parseArguments()
      outFile = open(myOptions.getOutputFile(), 'w' if myOptions.isReplace() else 'a')
      for inputFilename in myOptions.getInputFiles():
         inFile = open(inputFilename, 'r')
         ...

The above code could be invoked with the following command line arguments:
   python MyApp.py -f File1.txt File2.txt -o Result.txt --replace
   
Help text for this would be invoked by --help (or -?) and displayed as follows:
   python MyApp.py --help

   Output
   ------
   Usage: TestCliWithCustomisedHelp.py --inputFiles, -f value1 ... [--outputFile, -o value] [--maxOutputSize, -m value] [--replace, -r]
   where:
   --inputFiles,    -f value1 value2 ...                                      List of input files to process
   --outputFile,    -o value             (default='output.csv')               Output filename
   --maxOutputSize, -m value             (default=1024)                       Maximum size to limit the output file to
   --replace,       -r                   (True if specified, otherwise False) Do you want to replace the output file if it already exists
