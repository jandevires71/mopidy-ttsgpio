import logging

logger = logging.getLogger(__name__)


class PlaylistMenu():

    def __init__(self, frontend):
        self.frontend = frontend
        self.playlists = None
        self.selected = None
        self.reload_playlists()

    def __str__(self):
        return "playlists"

    def speak_current(self):
        if self.selected < len(self.playlists):
            self.frontend.tts.speak_text(self.playlists[self.selected].name)
        else:
            self.frontend.tts.speak_text("No playlists found")

    def reload_playlists(self):
        self.playlists = []
        logger.debug("TTSGPIO: load playlists")
        for playlist in self.frontend.core.playlists.playlists.get():
            self.playlists.append(playlist)
        logger.debug("TTSGPIO: playlists loaded")
        self.selected = 0

    def reset(self):
        self.selected = 0
        self.speak_current()

    def change_current(self, change):
        self.selected += change
        if self.selected < 0:
            self.selected = len(self.playlists) - 1
        if self.selected >= len(self.playlists):
            self.selected = 0
        self.speak_current()

    def input(self, input_event):
        logger.debug("TTSGPIO: playlist '" + input_event['key'] + "'")
        if input_event['key'] == 'next':
            logger.debug("TTSGPIO: playlist next")
            self.change_current(1)
        if input_event['key'] == 'previous':
            logger.debug("TTSGPIO: playlist prev")
            self.change_current(-1)
        if input_event['key'] == 'main':
            logger.debug("TTSGPIO: playlist main")
            core = self.frontend.core
            core.tracklist.clear()

            playlist = core.playlists.lookup(self.playlists[self.selected]).get()

            core.tracklist.add(playlist.tracks)
            core.tracklist.consume = False
            core.tracklist.single = False
            core.tracklist.repeat = True

            core.playback.play()
            self.frontend.exit_menu()

    def repeat(self):
        self.speak_current()
