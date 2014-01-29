import youtube_dl
import youtube_dl.utils
from youtube_dl import YoutubeDL

from MediaFormat import MediaFormat


class MediaObject(YoutubeDL):

    def __init__(self, url):
        """Initialize a MediaObject.

        Calls the super's initializer, but also adds the default
        InfoExtractors and stores the url.
        """
        super(MediaObject, self).__init__(None)

        self.add_default_info_extractors()

        self.url = url

    # Intercept messages to the screen
    def to_stdout(self, message, skip_eol=False, check_quiet=False):
        """Intercepts the messages to the stdout"""
        pass

    def to_stderr(self, message):
        """Intercecpts the message to the stderr"""
        pass

    def to_console_title(self, message):
        """Don't touch the console title"""

    def trouble(self, message=None, tb=None):
        """This method is called when trouble occurs."""
        try:
            super(MediaObject, self).trouble(message, tb)
        except:
            pass

    # Retreive information about the video
    def getMediaInformation(self):
        """Returns an information dictionary about the media.

        Raises exceptions when an error occurs:
          - UnsupportedURLError: the url provided is not supported
          - other: errors thrown by the youtube-dl source code
        """
        url = self.url
        try:
            return self.extract_info(url, download=False)
        except (youtube_dl.DownloadError,
                youtube_dl.utils.compat_urllib_error.URLError):
            raise UnsupportedURLError(url)

    def extractAvailableFormatsFromInfo(self, info_dict):
        """Extracts the available format from a media information dictionary.

        This method will probably operate on the return value of
        getVideoInformation.

        Returns a list of MediaFormat instances.
        """
        formats = info_dict.get('formats', [info_dict])
        l = [MediaFormat(f) for f in formats]
        if len(l) > 1:
            l[0].quality = MediaFormat.QUALITY_WORST
            l[-1].quality = MediaFormat.QUALITY_BEST
        return l

    def downloadMedia(self, filename, formatID=None):
        """Downloads the media at url to filename.

        Returns True on succes, false if an error occurred.

        """
        url = self.url
        self.params['outtmpl'] = filename
        if formatID != None:
            self.params['format'] = str(formatID)

        return self.download([url]) == 0
        

### Exceptions ###
class UnsupportedURLError(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return "unsupported url: '" + self.url + "'"
            
        
