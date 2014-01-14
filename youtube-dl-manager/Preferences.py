import configparser
from configparser import SafeConfigParser


class Preferences(object):
    DEFAULT_FILE = "/etc/youtube-dl-manager.ini"
    
    def __init__(self, inifile=DEFAULT_FILE):
        self._file = inifile

        self.sourcepath = None
        self.autoupdates = None # != False !!!!

    def readPreferences(self):
        """Reads in the preference file.

        This method will throw exceptions when errors occur:
          - FileReadException: unable to parse the configuraiton file
          - SectionNotFoundException: unable to locate a required section
          - OptionNotFoundException: unable to locate a required option
          - UnkownOptionException: unkown option encountered
          - InvalidOptionException: option has wrong value

        For the configuration file format look at the bottom of this file.
        """
        parser = SafeConfigParser()
        if len(parser.read([self._file])) != 1:
            raise FileReadException(self._file)


        try:
            # source
            sn = 'source'
            kvp = parser.items(sn)
            self.__parseSourceSection(sn, kvp)

        except (configparser.NoSectionError):
            raise SectionNotFoundException(self._file, sn)

    def __parseSourceSection(self, sn, keyValuePairs):
        f = self._file
        for option, value in keyValuePairs:
            if option == "sourcepath":
                self.sourcepath = value

            elif option == "autoupdates":
                if value == "1":
                    self.autoupdates = True
                elif value == "0":
                    self.autoupdates = False
                else:
                    e = "value must be 0 or 1"
                    raise InvalidOptionException(f, sn, option, value, e)

            else:
                raise UnkownOptionException(f, sn, option)

        if self.sourcepath == None:
            raise OptionNotFoundException(f, sn, 'sourcepath')
        elif self.autoupdates == None:
            raise OptionNotFoundException(f, sn, 'autoupdates')
            

### Exceptions ###       
class PreferencesException(Exception):
    """Generic preference exception"""
    

class FileReadException(PreferencesException):
    def __init__(self, file):
        s = super(PreferencesException, self)
        s.__init__("could not read '" + str(file) + "'")
        self.file = file

class SectionNotFoundException(PreferencesException):
    def __init__(self, file, section):
        s = super(PreferencesException, self)
        e =  "section not found: section '" + section
        e += "' not found in preferences file '"
        e += file + "'"
        s.__init__(e)
        self.file = file
        self.section = section

class OptionNotFoundException(PreferencesException):
    def __init__(self, file, section, option):
        s = super(PreferencesException, self)
        e =  "option not found: option '" + option + "' of section '"
        e += section
        e += "' not found in preferences file '" + file + "'"
        s.__init__(e)
        self.file = file
        self.section = section
        self.option = option

class UnkownOptionException(PreferencesException):
    def __init__(self, file, section, option):
        s = super(PreferencesException, self)
        e =  "unkown option: option '" + option + "' in section '" + section
        e += "' in preferences file '" + file + "' is unkown"
        s.__init__(e)
        self.file = file
        self.section = section
        self.option = option

class InvalidOptionException(PreferencesException):
    def __init__(self, file, section, option, value, err):
        s = super(PreferencesException, self)
        e =  "invalid option: option '" + option + "' in section '" + section
        e += "' in preferences file '" + file + "' has an invalid value '"
        e += str(value) + "': " + err
        s.__init__(e)
        self.file = file
        self.section = section
        self.option = option
        self.error = err

### CONFIGURATION FNILE FORMAT ###
#
# The configuration file has the ini format with following sections and
# options:
#
# [source]
# ; Where the source files are located. This is used to initialize the
# ; program and update the youtube-dl source code.
# sourcepath=/usr/share/youtube-dl-manager
#
# ; Wether or not the program should check for updates on startup. Can
# ; be either 1 or 0.
# autoupdates=1
#
#
#



