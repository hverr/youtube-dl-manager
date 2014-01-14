from Preferences import Preferences
from SourceCodeManager import SourceCodeManager

def main():
    prefs = Preferences()
    prefs.readPreferences()
    scm = SourceCodeManager(prefs)

    scm.downloadYoutubeDL()

if __name__ == "__main__":
    main()

