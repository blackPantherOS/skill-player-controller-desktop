import sys
import dbus
import os
import time
import subprocess
from traceback import print_exc
from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'blackPantherOS.eu'

LOGGER = getLogger(__name__)

class PlayerControllerDesktopSkill(MycroftSkill):

    def __init__(self):
        super(PlayerControllerDesktopSkill, self).__init__(name="PlayerControllerDesktopSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))

        playercontroll_playing_skill_intent = IntentBuilder("PlayerControllPlayKeywordIntent").\
            require("PlayerControllDesktopPlayKeyword").build()
        self.register_intent(playercontroll_playing_skill_intent, self.handle_playercontroll_playing_skill_intent)

        playercontroll_pause_skill_intent = IntentBuilder("PlayerControllPauseKeywordIntent").\
            require("PlayerControllDesktopPauseKeyword").build()
        self.register_intent(playercontroll_pause_skill_intent, self.handle_playercontroll_playing_skill_intent)

        playercontroll_stop_skill_intent = IntentBuilder("PlayerControllStopKeywordIntent").\
            require("PlayerControllDesktopStopKeyword").build()
        self.register_intent(playercontroll_stop_skill_intent, self.handle_playercontroll_stop_skill_intent)

        playercontroll_next_skill_intent = IntentBuilder("PlayerControllNextKeywordIntent").\
            require("PlayerControllDesktopNextKeyword").build()
        self.register_intent(playercontroll_next_skill_intent, self.handle_playercontroll_next_skill_intent)

        playercontroll_previous_skill_intent = IntentBuilder("PlayerControllPreviousKeywordIntent").\
            require("PlayerControllDesktopPreviousKeyword").build()
        self.register_intent(playercontroll_previous_skill_intent, self.handle_playercontroll_previous_skill_intent)

        playercontroll_seekfw_skill_intent = IntentBuilder("PlayerControllSeekFwKeywordIntent").\
            require("PlayerControllDesktopSeekFwKeyword").build()
        self.register_intent(playercontroll_seekfw_skill_intent, self.handle_playercontroll_seekfw_skill_intent)

        playercontroll_seekbw_skill_intent = IntentBuilder("PlayerControllSeekBwKeywordIntent").\
            require("PlayerControllDesktopSeekBwKeyword").build()
        self.register_intent(playercontroll_seekbw_skill_intent, self.handle_playercontroll_seekbw_skill_intent)

    def handle_check_player(func):

        def wrapper(*args, **kwargs):
            global playerRunning, playerName
            playerRunning = False

            for service in dbus.SessionBus().list_names():
                if service.startswith("org.mpris.MediaPlayer2"):
                    services = service.startswith("org.mpris.MediaPlayer2")
                    playerName = service.split("2.")[1]
                    playerRunning = playerName in ['clementine','smplayer']
                    if playerRunning:
                        break

            return func(*args, **kwargs)

        return wrapper

    @handle_check_player
    def handle_playercontroll_playing_skill_intent(self, message):

        self.speak_dialog("player.play")
        if playerRunning == False:
       	   def runprocandplay():
           	bus = dbus.SessionBus()
           	subprocess.Popen(["clementine"])
           	time.sleep(1)
           	remote_object = bus.get_object("org.mpris.MediaPlayer2.clementine","/org/mpris/MediaPlayer2")
           	remote_object.Play(dbus_interface = "org.mpris.MediaPlayer2.Player")
           runprocandplay()
        else:
       	   def runplay():
           	bus = dbus.SessionBus()
           	cmd = ['qdbus org.mpris.MediaPlayer2.'+playerName+' /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause']
           	get_state =  subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
           runplay()

    @handle_check_player
    def handle_playercontroll_stop_skill_intent(self, message):
        cmd = ['qdbus org.mpris.MediaPlayer2.'+playerName+' /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Stop']
        get_state =  subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    @handle_check_player
    def handle_playercontroll_next_skill_intent(self, message):
        cmd = ['qdbus org.mpris.MediaPlayer2.'+playerName+' /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next']
        get_state =  subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    @handle_check_player
    def handle_playercontroll_previous_skill_intent(self, message):
        cmd = ['qdbus org.mpris.MediaPlayer2.'+playerName+' /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous']
        get_state =  subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    @handle_check_player
    def handle_playercontroll_seekfw_skill_intent(self, message):
        cmd = ['qdbus org.mpris.MediaPlayer2.'+playerName+' /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Seek "5000000"']
        get_state =  subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    @handle_check_player
    def handle_playercontroll_seekbw_skill_intent(self, message):
        cmd = ['qdbus org.mpris.MediaPlayer2.'+playerName+' /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Seek "-5000000"']
        get_state =  subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    def stop(self):
        pass

def create_skill():
    return PlayerControllerDesktopSkill()
