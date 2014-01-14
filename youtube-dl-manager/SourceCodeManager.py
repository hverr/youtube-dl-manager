import urllib.request
import tempfile
import tarfile
import shutil
import os

class SourceCodeManager(object):
    YOUTUBE_DL_MASTER = "https://raw.github.com/rg3/youtube-dl/master"
    YOUTUBE_DL_VERSION_URL = YOUTUBE_DL_MASTER + "/youtube_dl/version.py"

    GITHUB_REPOS_API = "https://api.github.com/repos"
    YOUTUBE_DL_TARBALL_URL = GITHUB_REPOS_API + "/rg3/youtube-dl/tarball"

    BLOCKING_TIMEOUT = 5
    def __init__(self, prefs):
        """
        prefs - An instance of Preference
        """
        self._preferences = prefs

    def youtubeDLSourceFolder(self):
        return self._preferences.sourcepath + "/youtube-dl"
    
    def currentYoutubeDLVersion(self):
        """Returns the version of youtube-dl installed in the system"""

    def checkForYoutubeDLUpdates(self):
        """Checks for updates only when enabled in the preferences.

        Raises exceptions on error:
          - urllib.request.URLError
          - ExtractionError: unable to extract the version string
        """
        if self._preferences.autoupdates == False:
            return

        # check for youtube-dl updates
        fh = urllib.request.urlopen(self.YOUTUBE_DL_VERSION_URL, timeout=5)
        try:
            html = fh.read().decode().strip()
            s = re.search('((?:\d+\.){2}\d+)',html)
            if s == None:
                raise ExtractionError()
            
        finally:
            fh.close()
        return html

    def downloadYoutubeDL(self):
        """Downloads and updates the youtube-dl source code on the system

        Raises exceptions on error:
          - urllib.request.URLError
        """

        # download to tmp file
        tmp = tempfile.mkstemp()[1]
        fh = open(tmp, 'wb')
        try:
            req = urllib.request.urlopen(self.YOUTUBE_DL_TARBALL_URL, timeout=5)
            chunkSize = 256*10240
            while True:
                chunk = req.read(chunkSize)
                if not chunk:
                    break
                fh.write(chunk)


        except Exception as e:
            fh.close()
            os.remove(tmp)
            raise e

        # read in tarball
        try:
            tf = tarfile.open(name=tmp)
            extractDir = tempfile.mkdtemp()
            tf.extractall(path=extractDir)

            newCode = extractDir + "/" + tf.getmembers()[0].name
            tf.close()
        finally:
            os.remove(tmp)

        # delete the previous code and move the new code
        oldCode = self.youtubeDLSourceFolder()
        try:
            shutil.rmtree(oldCode)
        except FileNotFoundError:
            pass
        shutil.move(newCode, oldCode)
        


### Exceptions ###
class ExtractionError(Exception):
    def __init__(self):
        super(Exception, self).__init__("could not extract version")
        
