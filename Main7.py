import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton

from kivy.uix.slider import Slider
from kivy.animation import Animation
from threading import Thread

import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers

spi = spidev.SpiDev()

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'Main7'
ADMIN_SCREEN_NAME = 'admin'
direction = 0
speed = 0
s = Slider(min=0, max=500, value=200)

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=1000, speed=8)


#  Line above:port=1 sets the port


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (.4, .4, 1, 1)


class MainScreen(Screen):

    def turnOnMotor(self, val):
        global direction
        global speed
        speed = self.ids.sliderForMotorSpeed.value
        # speed = 700
        if val == "On":  # Run Motor, change text
            s0.run(direction, speed)
            self.ids.turnOnMotorButton.text = "Off"
        if val == "Off":  # Stop Motor, change text
            s0.softStop()
            s0.softFree()
            self.ids.turnOnMotorButton.text = "On"

    def changeMotorDirection(self, val):
        if val == "clockWise":  # changes text, switches direction
            global direction  # global dir declared at top
            direction = 0
            self.turnOnMotor(self.ids.turnOnMotorButton.text)
            self.turnOnMotor(self.ids.turnOnMotorButton.text)
            return "counterClockWise"
        if val == "counterClockWise":
            global direction
            direction = 1
            self.turnOnMotor(self.ids.turnOnMotorButton.text)
            self.turnOnMotor(self.ids.turnOnMotorButton.text)
            return "clockWise"
        ###

    def changeSpeed(self, val):
        if val == "Speed1":
            global speed
            speed = self.ids.sliderForMotorSpeed.value
            self.turnOnMotor(self.ids.turnOnMotorButton.text)
            self.turnOnMotor(self.ids.turnOnMotorButton.text)
            sleep(.1)
            return "Speed2"
        # if val == "Speed2":
        # global speed
        # speed = self.ids.sliderForMotorSpeed.value
        # self.turnOnMotor(self.ids.turnOnMotor.text)
        # self.turnOnMotor(self.ids.turnOnMotor.text)
        # return "Speed1"

    def start_joy_thread(self):
        x = Thread(target=self.changeSpeed)
        x.start()

    def thatDoesStuff(self):
        # s0.start_relative_move(15)
        s0.goHome()
        self.ids.buttonThatDoesStuffLabel.text = str(s0.get_position_in_units)

    def exit_program():
        s0.free_all()
        spi.close()
        GPIO.cleanup()
        quit()


Builder.load_file('Main7.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
