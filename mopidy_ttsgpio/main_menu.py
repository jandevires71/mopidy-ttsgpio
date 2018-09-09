import logging
import os
import socket
from datetime import datetime

from .on_off_configuration import OnOffConfiguration
from .playlist_menu import PlaylistMenu

logger = logging.getLogger(__name__)

class MainMenu():
    def __init__(self, frontend):
        logger.debug("TTSGPIO: mainmenu init")
        self.current = 0
        self.frontend = frontend
        self.main_menu = False
        self.elements = [PlaylistMenu(frontend), 'exit mopidy']
        self.elements.append(OnOffConfiguration('random'))
        self.elements.append('shutdown')
        self.elements.append('reboot')
        self.elements.append('check i p')
        self.elements.append('what time is it')

    def reset(self):
        self.current = 0
        self.say_current_element()
        self.main_menu = True

    def input(self, input_event):
        if self.main_menu:
            if input_event['key'] == 'next':
                self.change_current(1)
            elif input_event['key'] == 'previous':
                self.change_current(-1)
            elif input_event['key'] == 'main':
                if isinstance(self.elements[self.current], str):
                    self.item_selected(self.elements[self.current])
                else:
                    self.main_menu = False
                    self.elements[self.current].reset()
        else:
            self.elements[self.current].input(input_event)

    def item_selected(self, item):
        if item == 'exit mopidy':
            os.system("pkill mopidy")
        elif item == 'shutdown':
            os.system("shutdown now -h")
        elif item == 'reboot':
            os.system("shutdown -r now")
        elif item == 'check i.p.':
            self.check_ip()
        elif item == 'what time is it':
            self.tell_time()

    def change_current(self, move):
        self.current += move
        if self.current < 0:
            self.current = len(self.elements) - 1
        elif self.current >= len(self.elements):
            self.current = 0
        self.say_current_element()

    def say_current_element(self):
        is_playing = self.frontend.is_playing()
        if (is_playing):
            self.frontend.core.playback.pause()
        self.frontend.tts.speak_text(str(self.elements[self.current]))
        if (is_playing):
            self.frontend.core.playback.play()

    def repeat(self):
        if self.main_menu:
            self.say_current_element()
        else:
            self.elements[self.current].repeat()

    def check_ip(self):
        is_playing = self.frontend.is_playing()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            if (is_playing):
                self.frontend.core.playback.pause()
            self.frontend.tts.speak_text("Your I.P. is: " + ip)
            if (is_playing):
                self.frontend.core.playback.play()
        except socket.error:
            s.close()
            if (is_playing):
                self.frontend.core.playback.pause()
            self.frontend.tts.speak_text("No internet connection found")
            if (is_playing):
                self.frontend.core.playback.play()

    def tell_time(self):
        is_playing = self.frontend.is_playing()
        mytime = datetime.now().strftime("%B %d, %Y the time is %H hours %M minutes")
        if (is_playing):
            self.frontend.core.playback.pause()
        self.frontend.tts.speak_text(mytime)
        if (is_playing):
            self.frontend.core.playback.play()
