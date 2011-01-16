'''
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
'''
__VERSION__ = __version__ = "1.1.3"

import inspect
import os
import sys

def __digitStringValueFormatter(optionName, value):
   'Ensures value consists of just the digits 0 to 9.'
   if value.isdigit():
      return value
   else:
      raise CliParseError('Option %s has a value that contains non-digits: %s' % (optionName, value))

def __numericValueFormatter(optionName, value):
   '''Formats the value as an integer.
   Allows all standard Python forms for a numeric value, i.e.:
      12345     standard decimal value
      0x12abc   hexadecimal value
      0b10110   binary value
      076123    octal value
   '''
   if type(value) == int:
      return value

   if value[:2].lower() == '0x':         # hexadecimal
      radix = 16
   elif value[:2].lower() == '0b':       # binary
      radix = 2
      value = value[2:] or '0'           # have to remove "0b" prefix
   elif value[:1] == '0':                # octal
      radix = 8
   else:                                 # decimal
      radix = 10

   try:
      return int(value, radix)
   except BaseException as e:
      raise CliParseError('Option %s has a value that cannot be converted to a number: %s\n   caused by: %s' % (optionName, value, e))

STRING_VALUE_FORMATTER = lambda optionName, value: str(value)
DIGIT_STRING_VALUE_FORMATTER = __digitStringValueFormatter
NUMERIC_VALUE_FORMATTER = __numericValueFormatter

class CliError(Exception):
   'Base of all Cli Exceptions'
   def __init__(self, errorMessage):
      self.__errorMessage = errorMessage

   def __str__(self):
      return self.__errorMessage

class CliHelpError(CliError):
   'Error raised when help is requested'
   def __init__(self, helpText):
      CliError.__init__(self, helpText)
      self.__helpText = helpText

   @property
   def helpText(self):
      return self.__helpText

class CliParseError(CliError):
   'Error raised during parsing of the command line arguments'
   def __init__(self, errorMessage):
      CliError.__init__(self, errorMessage)

class positional(object):
   def __init__(self, relativePosition):
      self.__relativePosition = relativePosition

   def __call__(self, f):
      if type(self.__relativePosition) != int:
         raise CliParseError('Positional value for method "%s" must be an integer. Found "%s" of %s' % (f.__name__, self.__relativePosition, type(self.__relativePosition)))
      self.__f = f
      return self

   @property
   def relativePosition(self):
      return self.__relativePosition

   @property
   def wrappedMethod(self):
      return self.__f

class Cli(object):
   '''Provides access to command line arguments using the given
   "optionsClass" as a template for defining them.
   "prog" optional name of the program that is using these options (default os.path.basename(sys.argv[0]))
   "purpose" optional description of program that is included in the auto-generated help text.
   '''
   def __init__(self, optionsClass, prog=os.path.basename(sys.argv[0]), purpose=None):
      self.__optionsClass = optionsClass
      self.__options, self.__positionalArguments = Cli.__getSupportedOptions(optionsClass)
      self.__helpText = Cli.__constructHelpText(prog, purpose, self.__options, self.__positionalArguments)

   @classmethod
   def __getSupportedOptions(cls, optionsClass):
      '''Introspects the given "optionsClass" and uses all callable methods
      that start with either "get" or "is" to build up a list of supported
      options.
      '''
      supportedOptions = {}

      for methodName in dir(optionsClass):
         if methodName.startswith('get') or methodName.startswith('is'):
            method = getattr(optionsClass, methodName)
            if callable(method):
               if inspect.isclass(type(method)) and method.__class__.__name__ == 'positional':
                  position = method.relativePosition
                  method = method.wrappedMethod
               else:
                  position = None
               try:
                  methodArgs, varargs, varkw, defaults = inspect.getargspec(method) #@UnusedVariable
               except TypeError:
                  raise RuntimeError('Could not get argument specification for %r' % method)
               if inspect.ismethod(method) or position is not None:
                  methodArgs = methodArgs[1:]  # Skip 'self'
               supportedOptions[methodName] = _OptionDescription(optionsClass, methodName, methodArgs, defaults, position, method.__doc__)

      cls.__validateShortNames(supportedOptions)
      cls.__validatePositionalArguments(supportedOptions)

      options = {}
      positional = {}
      for option in supportedOptions.values():
         if option.hasPosition:
            positional[option.position] = option
         else:
            options[option.methodName] = option

      positions = positional.keys()[:]
      positions.sort()
      positionalArguments = []
      for position in positions:
         positionalArguments.append(positional[position])

      return options, positionalArguments

   @classmethod
   def __validateShortNames(cls, supportedOptions):
      '''Ensures that the short name for each option is unique and does not
      clash with any existing long names.
      '''
      optionsWithShortNames = {}
      for option in supportedOptions.values():
         if option.hasShortName:
            if type(option.shortName) != type(''):
               raise CliParseError('Option %s has a non-string shortName' % option)
            elif optionsWithShortNames.has_key(option.shortName):
               raise CliParseError('Option %s has a shortName that clashes with %s' % (option, optionsWithShortNames[option.shortName]))
            else:
               methodSuffix = option.shortName[0].upper() + option.shortName[1:]
               matchingLongNameOption = None
               if supportedOptions.has_key('is' + methodSuffix):
                  matchingLongNameOption = supportedOptions['is' + methodSuffix]
               elif supportedOptions.has_key('get' + methodSuffix):
                  matchingLongNameOption = supportedOptions['get' + methodSuffix]
               if matchingLongNameOption is not None:
                  raise CliParseError('Option %s has a shortName that clashes with the long name of %s' % (option, matchingLongNameOption))
               optionsWithShortNames[option.shortName] = option

   @classmethod
   def __validatePositionalArguments(cls, supportedOptions):
      'Ensures all positional arguments have a unique position'
      positionalArguments = {}
      for option in supportedOptions.values():
         if option.hasPosition:
            if positionalArguments.has_key(option.position):
               raise CliParseError('Positional argument %s has a position that clashes with %s' % (option, positionalArguments[option.position]))
            positionalArguments[option.position] = option

   @classmethod
   def __constructHelpText(cls, prog, purpose, options, positionalArguments):
      'Constructs the help text from the given options'
      usage = []
      maxLongNameLength = 0
      maxShortNameLength = 0
      maxValueLength = 0
      maxDefaultValueLength = 0
      containsBooleanOptions = False
      for option in options.values() + positionalArguments:
         helpTextComponents = option.helpTextComponents
         usage.append(helpTextComponents['usage'])
         maxLongNameLength = max(maxLongNameLength, len(helpTextComponents['longName']))
         maxShortNameLength = max(maxShortNameLength, len(helpTextComponents['shortName']))
         maxValueLength = max(maxValueLength, len(helpTextComponents['value']))
         maxDefaultValueLength = max(maxDefaultValueLength, len('%r' % helpTextComponents['default']))
         if option.isBoolean:
            containsBooleanOptions = True

      if maxShortNameLength > 0:
         format = '%-{longNameLength}s%-{shortNameLength}s %-{valueLength}s'.format(longNameLength=maxLongNameLength + 2, shortNameLength=maxShortNameLength, valueLength=maxValueLength)
      else:
         format = '%-{longNameLength}s%s %-{valueLength}s'.format(longNameLength=maxLongNameLength, valueLength=maxValueLength)

      defaultValueLength = maxDefaultValueLength + 11
      if containsBooleanOptions:
         defaultValueLength = max(defaultValueLength, len(' (True if specified, otherwise False)'))
      if maxDefaultValueLength > 0:
         format += '%-{defaultValueLength}s'.format(defaultValueLength=defaultValueLength)
      else:
         format += '%s'

      helpTextLines = []
      helpTextLines.append('Usage: %s %s' % (prog, ' '.join(usage)))
      if purpose:
         helpTextLines.append(purpose)
      helpTextLines.append('where:')
      for option in options.values() + positionalArguments:
         helpTextComponents = option.helpTextComponents
         if option.hasShortName:
            longName = helpTextComponents['longName'] + ', '
            shortName = helpTextComponents['shortName']
         else:
            longName = helpTextComponents['longName']
            shortName = ''

         if option.isBoolean:
            defaultValue = ' (True if specified, otherwise False)'
         elif option.hasDefault:
            defaultValue = ' (default=%r)' % helpTextComponents['default']
         else:
            defaultValue = ' '

         helpText = format % (longName, shortName, helpTextComponents['value'], defaultValue)
         if option.hasDocString():
            helpText += ' ' + helpTextComponents['docString']

         helpTextLines.append(helpText)

      return '\n'.join(helpTextLines)

   @property
   def helpText(self):
      'The help text'
      return self.__helpText

   def parseArguments(self, args=None):
      '''Parses the options specified within the optional arguments list.
      If "args" is omitted, then the options are picked up from sys.argv[1:].
      '''
      if args is None:
         return _ParsedOptions(self.__optionsClass, self.__helpText, self.__options, self.__positionalArguments, sys.argv[1:])
      else:
         return _ParsedOptions(self.__optionsClass, self.__helpText, self.__options, self.__positionalArguments, args[:])

class _OptionDescription(object):
   'Representation of a single option'
   def __init__(self, optionsClass, methodName, methodArgs, defaults, position, methodDocString):
      self.__optionsClass = optionsClass
      self.__methodName = methodName
      self.__defaults = defaults
      self.__position = position
      self.__methodDocString = methodDocString
      self.__isBooleanMethod = methodName.startswith('is')
      self.__isMandatory = 'mandatory' in methodArgs
      self.__isMultiValued = 'multiValued' in methodArgs
      self.__hasDefault = 'default' in methodArgs
      self.__hasShortName = 'shortName' in methodArgs
      self.__hasValueFormatter = 'valueFormatter' in methodArgs

      if self.__isBooleanMethod:
         methodSuffix = methodName[2:]
      else:
         methodSuffix = methodName[3:]

      self.__name = methodSuffix[0].lower() + methodSuffix[1:]
      self.__valueFormatter = STRING_VALUE_FORMATTER
      if self.__defaults is not None:
         defaultsOffset = len(methodArgs) - len(defaults)
      else:
         defaultsOffset = None
      self.__minCount = None
      self.__maxCount = None
      self.__methodArgs = []
      unrecognisedArgs = []
      for index in range(0, len(methodArgs)):
         methodArg = methodArgs[index]
         if methodArg == 'shortName':
            self.__shortName = self.__defaults[index - defaultsOffset]
            self.__methodArgs.append('%s=%r' % (methodArg, self.__shortName))
         elif methodArg == 'default':
            self.__defaultValue = defaults[index - defaultsOffset]
            self.__methodArgs.append('%s=%r' % (methodArg, self.__defaultValue))
         elif methodArg == 'valueFormatter':
            self.__valueFormatter = self.__defaults[index - defaultsOffset]
            self.__methodArgs.append('%s=%r' % (methodArg, self.__valueFormatter))
         elif methodArg == 'min':
            self.__minCount = self.__defaults[index - defaultsOffset]
            self.__methodArgs.append('%s=%r' % (methodArg, self.__minCount))
         elif methodArg == 'max':
            self.__maxCount = self.__defaults[index - defaultsOffset]
            self.__methodArgs.append('%s=%r' % (methodArg, self.__maxCount))
         elif methodArg != 'mandatory' and methodArg != 'multiValued':
            unrecognisedArgs.append(methodArg)
         else:
            self.__methodArgs.append(methodArg)

      self.__validate(methodArgs, unrecognisedArgs, defaultsOffset)

   def __validate(self, methodArgs, unrecognisedArgs, defaultsOffset):
      if len(unrecognisedArgs) > 0:
         raise CliParseError('Unrecognised arguments "%s" in %s' % (', '.join(unrecognisedArgs), self))

      if self.__position is not None:
         if self.__hasShortName:
            raise CliParseError('Positional argument %s cannot have a "shortName"' % self)
         elif self.__hasDefault:
            raise CliParseError('Positional argument %s cannot have a "default"' % self)
         elif self.__isMultiValued:
            raise CliParseError('Positional argument %s cannot be marked as "multiValued"' % self)
         elif self.__isMandatory:
            raise CliParseError('Positional argument %s cannot be marked as "mandatory"' % self)
         elif self.__minCount is not None:
            raise CliParseError('Positional argument %s cannot have "min" specified' % self)
         elif self.__maxCount is not None:
            raise CliParseError('Positional argument %s cannot have "max" specified' % self)

      if self.__isBooleanMethod:
         if self.__hasDefault:
            raise CliParseError('Boolean option %s cannot have a "default"' % self)
         elif self.__isMultiValued:
            raise CliParseError('Boolean option %s cannot be marked as "multiValued"' % self)
         elif self.__hasValueFormatter:
            raise CliParseError('Boolean option %s cannot have a "valueFormatter"' % self)

      if self.__hasDefault:
         if self.__isMandatory:
            raise CliParseError('Mandatory option %s cannot have "default" values' % self)
         elif not self.__isMultiValued and type(self.__defaultValue) == list and len(self.__defaultValue) > 1:
            raise CliParseError('Single-valued option %s cannot have multiple "default" values' % self)

      if not self.__isMultiValued:
         if self.__minCount is not None:
            raise CliParseError('Single-valued option %s cannot have "min" specified' % self)
         elif self.__maxCount is not None:
            raise CliParseError('Single-valued option %s cannot have "max" specified' % self)
      else:
         if self.__minCount is not None:
            if type(self.__minCount) != int:
               raise CliParseError('Multi-valued option %s has a non-numeric "min" value' % self)
            elif self.__minCount < 0:
               raise CliParseError('Multi-valued option %s cannot have "min" less than zero' % self)
         if self.__maxCount is not None:
            if type(self.__maxCount) != int:
               raise CliParseError('Multi-valued option %s has a non-numeric "max" value' % self)
            elif self.__maxCount < 2:
               raise CliParseError('Multi-valued option %s cannot have "max" less than two' % self)
            elif self.__minCount is not None and self.__maxCount < self.__minCount:
               raise CliParseError('Multi-valued option %s cannot have "max" less than "min"' % self)
         if self.__hasDefault:
            if type(self.__defaultValue) != list:
               raise CliParseError('Multi-valued option %s must have "default" values defined as a "list"' % self)
            defaultCount = len(self.__defaultValue)
            if self.__minCount is not None and defaultCount < self.__minCount:
               raise CliParseError('Multi-valued option %s must have at least %d "default" values' % (self, self.__minCount))
            elif self.__maxCount is not None and defaultCount > self.__maxCount:
               raise CliParseError('Multi-valued option %s must have at most %d "default" values' % (self, self.__maxCount))

      if not callable(self.__valueFormatter):
         raise CliParseError('Option %s has a non-callable valueFormatter.' % self)

      if defaultsOffset is not None:
         self.__validateMarkerAttribute('mandatory', methodArgs, defaultsOffset)
         self.__validateMarkerAttribute('multiValued', methodArgs, defaultsOffset)

   def __validateMarkerAttribute(self, attributeName, methodArgs, defaultsOffset):
      if attributeName in methodArgs:
         index = methodArgs.index(attributeName)
         if index >= defaultsOffset:
            raise CliParseError('Option %s has a badly formed "%s" marker (%s=%r). "%s" should not be assigned any value.' % (self, attributeName, attributeName, self.__defaults[index - defaultsOffset], attributeName))

   def formatValue(self, value):
      if type(value) == list:
         formattedList = []
         for item in value:
            formattedList.append(self.__valueFormatter('--' + self.__name, item))
         return formattedList
      else:
         return self.__valueFormatter('--' + self.__name, value)

   @property
   def isBoolean(self):
      return self.__isBooleanMethod

   @property
   def methodName(self):
      return self.__methodName

   @property
   def name(self):
      return self.__name

   @property
   def hasPosition(self):
      return self.__position is not None

   @property
   def position(self):
      return self.__position

   @property
   def isMandatory(self):
      return self.__isMandatory

   @property
   def isMultiValued(self):
      return self.__isMultiValued

   @property
   def hasMinCount(self):
      return self.__minCount is not None

   @property
   def minCount(self):
      return self.__minCount

   @property
   def hasMaxCount(self):
      return self.__maxCount is not None

   @property
   def maxCount(self):
      return self.__maxCount

   @property
   def hasDefault(self):
      return self.__hasDefault or self.__isBooleanMethod

   @property
   def default(self):
      return False if self.__isBooleanMethod else self.formatValue(self.__defaultValue)

   @property
   def hasShortName(self):
      return self.__hasShortName

   @property
   def shortName(self):
      return self.__shortName

   def hasDocString(self):
      return self.__methodDocString is not None

   @property
   def helpTextComponents(self):
      components = {}

      if self.hasPosition:
         usageText = self.__name
         components['longName'] = self.__name
         components['shortName'] = ''
         components['value'] = ''
      else:
         longName = '--' + self.__name
         components['longName'] = longName
         usageText = longName

         if self.hasShortName:
            shortName = '-' + self.shortName
            components['shortName'] = shortName
            usageText += ', ' + shortName
         else:
            components['shortName'] = ''

         if self.isBoolean:
            components['value'] = ''
         else:
            if self.isMultiValued:
               usageText += ' value1 ...'
               if self.hasMinCount or self.hasMaxCount:
                  minCount = 1
                  endValues = ['value2']
                  if self.hasMinCount:
                     minCount = self.minCount
                     endValues = []
                     if self.minCount == 1:
                        startValues = ['valueMin1']
                     elif self.minCount == 2:
                        startValues = ['value1', 'valueMin2']
                     else:
                        startValues = ['value1', '...', 'valueMin%d' % (self.minCount,)]
                  else:
                     startValues = ['value1']
                  if self.hasMaxCount:
                     if self.maxCount == minCount:
                        del startValues[-1]
                        endValues = ['valueMinMax%d' % minCount]
                     elif self.maxCount <= minCount + 1:
                        endValues = ['valueMax%d' % (minCount + 1,)]
                     else:
                        endValues = ['...', 'valueMax%d' % self.maxCount]
                  else:
                     endValues.append('...')
                  components['value'] = ' '.join(startValues + endValues)
               else:
                  components['value'] = 'value1 value2 ...'
            else:
               usageText += ' value'
               components['value'] = 'value'

      if self.hasDefault:
         components['default'] = self.default
      else:
         components['default'] = ''

      if self.hasDocString():
         components['docString'] = '%s' % self.__methodDocString
      else:
         components['docString'] = ''

      if self.isMandatory or (self.isMultiValued and self.hasMinCount) or self.hasPosition:
         components['usage'] = usageText
      else:
         components['usage'] = '[' + usageText + ']'

      return components

   def __str__(self):
      return '%s.%s(%s)' % (self.__optionsClass.__name__, self.__methodName, ', '.join(self.__methodArgs))

class _ParsedOptions(object):
   'Parses the command line options'
   def __init__(self, optionsClass, helpText, options, positionalArguments, args):
      self.__optionsClass = optionsClass
      self.__helpText = helpText
      self.__options = options.copy()
      for argument in positionalArguments:
         self.__options[argument.methodName] = argument

      context = _Context(optionsClass, helpText, options, positionalArguments)
      state = _StartState(context)
      argsLeft = len(args)
      for arg in args:
         argsLeft -= 1;
         state = state.process(arg, argsLeft)

      self.__parsedOptions = context.validateOptions()

   @property
   def helpText(self):
      'The help text'
      return self.__helpText

   def __getattr__(self, name):
      if self.__options.has_key(name):
         optionDescription = self.__options[name]
         if self.__parsedOptions.has_key(optionDescription.name):
            return _Option(self.__optionsClass, optionDescription, self.__parsedOptions[optionDescription.name])
         elif optionDescription.isBoolean:
            return _Option(self.__optionsClass, optionDescription, False)
         else:
            return _Option(self.__optionsClass, optionDescription)

      raise CliParseError('%s.%s() not defined' % (self.__optionsClass.__name__, name))

class _Context(object):
   'Context used to hold state information while parsing the command line'
   def __init__(self, optionsClass, helpText, options, positionalArguments):
      self.__optionsClass = optionsClass
      self.__helpText = helpText
      self.__options = options
      self.__positionalArguments = positionalArguments
      self.__positionalArgumentValues = []
      self.__shortOptions = {}

      for option in options.values():
         if option.hasShortName:
            self.__shortOptions[option.shortName] = option.name

      self.__parsedOptions = {}

   def addOption(self, optionName):
      if optionName == 'help':
         raise CliHelpError(self.__helpText)

      methodNameSuffix = optionName[0].upper() + optionName[1:]
      if self.__options.has_key('get' + methodNameSuffix):
         self.__option = self.__options['get' + methodNameSuffix]
         self.__parsedOptions[optionName] = []
      elif self.__options.has_key('is' + methodNameSuffix):
         self.__option = self.__options['is' + methodNameSuffix]
         self.__parsedOptions[optionName] = True
      else:
         raise CliParseError('Unrecognised option --%s' % optionName)

   def addShortOption(self, optionName):
      if optionName == '?':
         raise CliHelpError(self.__helpText)

      if self.__shortOptions.has_key(optionName):
         self.addOption(self.__shortOptions[optionName])
      else:
         raise CliParseError('Unrecognised short option -%s' % optionName)

   def appendOptionValue(self, value):
      if self.__option.isBoolean:
         raise CliParseError('Boolean option --%s cannot be followed by a value.\nFound unexpected value "%s" after this option.' % (self.__option.name, value))

      valueCount = len(self.__parsedOptions[self.__option.name])
      if self.__option.isMultiValued:
         if self.__option.hasMaxCount and valueCount == self.__option.maxCount:
            raise CliParseError('Multi-valued option --%s cannot have more than %d values' % (self.__option.name, self.__option.maxCount))
      elif valueCount > 0:
         raise CliParseError('Single-valued option --%s cannot have multiple values' % self.__option.name)
      self.__parsedOptions[self.__option.name].append(self.__option.formatValue(value))

   @property
   def numberOfPositionalArguments(self):
      return len(self.__positionalArguments)

   def addPositional(self, value):
      option = self.__positionalArguments[len(self.__positionalArgumentValues)]
      self.__positionalArgumentValues.append(option.formatValue(value))

   def validateOptions(self):
      for optionName in self.__parsedOptions.keys():
         methodNameSuffix = optionName[0].upper() + optionName[1:]
         if self.__options.has_key('get' + methodNameSuffix):
            option = self.__options['get' + methodNameSuffix]
            valueCount = len(self.__parsedOptions[optionName])
            if valueCount == 0:
               raise CliParseError('Missing value for option --%s' % optionName)
            elif option.isMultiValued:
               if option.hasMinCount and valueCount < option.minCount:
                  raise CliParseError('Multi-valued option --%s was given %d values - must have at least %d value(s)' % (optionName, valueCount, option.minCount))

      for option in self.__options.values():
         if option.isMandatory and option.name not in self.__parsedOptions:
            raise CliParseError('Missing mandatory option --%s' % option.name)
         elif option.isMultiValued and option.hasMinCount and option.minCount > 0 and option.name not in self.__parsedOptions:
            raise CliParseError('Multi-valued option --%s must be given with at least %d value(s)' % (option.name, option.minCount))

      numberOfMissingPositionalArguments = len(self.__positionalArguments) - len(self.__positionalArgumentValues)
      if numberOfMissingPositionalArguments > 1:
         raise CliParseError('Missing values for positional arguments: %s' % [option.name for option in self.__positionalArguments[len(self.__positionalArgumentValues):]])
      elif numberOfMissingPositionalArguments == 1:
         raise CliParseError('Missing value for last positional argument: %s' % [option.name for option in self.__positionalArguments[len(self.__positionalArgumentValues):]])
      else:
         for index in range(0, len(self.__positionalArguments)):
            option = self.__positionalArguments[index]
            value = self.__positionalArgumentValues[index]
            if option.isBoolean:
               if value.lower() not in ['true', 'false']:
                  raise CliParseError('Invalid boolean value "%s" for positional argument "%s". Must be "True" or "False" (case insensitive).' % (value, option.name))
               self.__parsedOptions[option.name] = value.lower() == 'true'
            else:
               self.__parsedOptions[option.name] = value

      return self.__parsedOptions

class _StartState(object):
   'The initial state during parsing of the command line'
   def __init__(self, context):
      self.__context = context

   def process(self, arg, argsLeft):
      if arg.startswith('-'):
         return _OptionState(self.__context, arg)
      elif argsLeft < self.__context.numberOfPositionalArguments:
         return _PositionalState(self.__context, arg)
      else:
         raise CliParseError('Expected option beginning with "-" or "--" but found: ' + arg)

class _OptionState(object):
   'We are processing an option in this state'
   def __init__(self, context, arg):
      self.__context = context
      if arg.startswith('--'):
         if len(arg) < 3:
            raise CliParseError('Missing option name after: ' + arg)
         elif arg[2] == '-':
            raise CliParseError('Too many -\'s in option: ' + arg)
         elif arg[2].lower() != arg[2]:
            raise CliParseError('Options must start with a lower case letter: ' + arg)
         context.addOption(arg[2:])
      elif len(arg) < 2:
         raise CliParseError('Missing option name after: ' + arg)
      elif arg[1].lower() != arg[1]:
         raise CliParseError('Short Options must start with a lower case letter: ' + arg)
      else: # startswith '-'
         context.addShortOption(arg[1:])

   def process(self, arg, argsLeft):
      if arg.startswith('-'):
         return _OptionState(self.__context, arg)
      elif argsLeft < self.__context.numberOfPositionalArguments:
         return _PositionalState(self.__context, arg)
      else:
         self.__context.appendOptionValue(arg)
         return self

class _PositionalState(object):
   'We are processing the positional arguments in this state'
   def __init__(self, context, arg):
      self.__context = context
      context.addPositional(arg)

   def process(self, arg, argsLeft):
      if arg.startswith('-'):
         raise CliParseError('Unexpected option "%s" found while processing positional arguments' % arg)
      else:
         self.__context.addPositional(arg)
         return self

class _Option(object):
   'Provides access to the value(s) of a parsed command line option'
   def __init__(self, optionsClass, optionDescription, values=None):
      self.__optionsClass = optionsClass
      self.__optionDescription = optionDescription
      self.__name__ = optionDescription.methodName

      if values is None:
         if optionDescription.hasDefault:
            self.__values = optionDescription.default
         else:
            self.__values = None
      elif type(values) is list:
         if len(values) == 0:
            self.__values = True
         elif len(values) == 1 and not optionDescription.isMultiValued:
            self.__values = values[0]
         else:
            self.__values = values
      else:
         self.__values = values

   def __call__(self, *params, **namedParams):
      return self.__values

   def __str__(self):
      return self.__optionDescription

   def __eq__(self, rhs):
      return (isinstance(rhs, _Option) and
              self.__optionsClass == rhs.__optionsClass and
              self.__name__ == rhs.__name__)

   def __ne__(self, rhs):
      return not self == rhs
