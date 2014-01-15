import youtube_dl
import youtube_dl.utils
from youtube_dl import YoutubeDL

from MediaFormat import MediaFormat


class YoutubeDLEngine(YoutubeDL):

    def __init__(self, params=None):
        """Initialize a YoutubeDLEngine.

        Calls the super's initializer, but also adds the default
        InfoExtractors.
        """
        super(YoutubeDLEngine, self).__init__(params)

        self.add_default_info_extractors()

    # Intercept messages to the screen
    def to_stdout(self, message, skipe_eol=False, check_quiet=False):
        """Intercepts the messages to the stdout"""

    def to_stderr(self, message):
        """Intercecpts the message to the stderr"""

    def to_console_title(self, message):
        """Don't touch the console title"""

    # Retreive information about the video
    def getVideoInformation(self, url):
        """Returns an information dictionary about a video.

        Raises exceptions when an error occurs:
          - UnsupportedURLError: the url provided is not supported
          - other: errors thrown by the youtube-dl source code
        """
        try:
            return self.extract_info(url, False)
        except (youtube_dl.DownloadError,
                youtube_dl.utils.compat_urllib_error.URLError):
            raise UnsupportedURLError(url)

    def extractAvailableFormatsFromInfo(self, info_dict):
        """Extracts the available format from a video information dictionary.

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

### Exceptions ###
class UnsupportedURLError(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return "unsupported url: '" + self.url + "'"
            
        
