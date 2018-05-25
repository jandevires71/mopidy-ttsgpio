import logging
import os
import time

logger = logging.getLogger(__name__)

music_level = 30

class TTS():
    def speak_text(self, text):
        logger.debug("TTSGPIO: speak text " + text)
        s='{0}'.format(text)
        os.system("echo " + s + "|/usr/bin/flite -voice kal16")
