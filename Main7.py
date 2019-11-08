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
import time
import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
import spidev
import os
from time import sleep
from pidev.stepper import stepper

spi = spidev.SpiDev()
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'Main7'
ADMIN_SCREEN_NAME = 'admin'
direction = 0
speed = 0
s = Slider(min=0, max=500, value=200)

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)
cyprus.initialize()


# if it is 50:1, multiply steps_per_unit by 50

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
            # global direction
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

    def exit_program():
        s0.free_all()
        spi.close()
        GPIO.cleanup()
        cyprus.close()
        quit()

    def thatDoesStuff(self):
        # print(position)

        position = s0.get_position_in_units()
        self.ids.buttonThatDoesStuffLabel.text = "Position = " + str(position)

        # t = int(6400 + position)

        s0.set_speed(1)
        s0.start_relative_move(-15)

        position = s0.get_position_in_units()
        self.ids.buttonThatDoesStuffLabel.text = "Position = " + str(position)
        # self.ids.buttonThatDoesStuffLabel.text = str(position)

        time.sleep(10)
        s0.set_speed(5)
        s0.start_relative_move(10)

        position = s0.get_position_in_units()
        self.ids.buttonThatDoesStuffLabel.text = "Position = " + str(position)

        time.sleep(8)
        s0.goHome()
        time.sleep(30)

        position = s0.get_position_in_units()
        self.ids.buttonThatDoesStuffLabel.text = "Position = " + str(position)

        s0.set_speed(8)
        s0.start_relative_move(-100)

        position = s0.get_position_in_units()
        self.ids.buttonThatDoesStuffLabel.text = "Position = " + str(position)

        time.sleep(10)
        s0.goHome()

        position = s0.get_position_in_units()
        self.ids.buttonThatDoesStuffLabel.text = "Position = " + str(position)

        # s0.goHome()

    # servo functions
    def servoMotorBinaryState(self):
        cyprus.initialize()
        cyprus.setup_servo(2)

        while True:
            if cyprus.read_gpio() & 0b0001:
                cyprus.set_servo_position(2, 0)  # close gate
                sleep(1)
            else:
                cyprus.set_servo_position(2, .7)  # open gate
                sleep(1)

    def talonDCMotor(self):
        cyprus.initialize()
        cyprus.setup_servo(1)

        cyprus.set_servo_position(1, 1)
        sleep(5)
        cyprus.set_servo_position(1, 0.5)
        sleep(5)
        cyprus.set_servo_position(1, 0)
        sleep(5)
        cyprus.set_servo_position(1, 0.5)

    def talonDCMotorSpeedUp(self):
        # cyprus.initialize()
        cyprus.setup_servo(1)
        cyprus.set_servo_position(1, 0.5)

        for i in range(60, 100, 1):
            cyprus.set_servo_position(1, i / 100.0)
            sleep(0.5)

        cyprus.set_servo_position(1, 0.5)

    def talonDCMotorFullSpeedWhenPressed(self):  # talon motor is in 1 (port 4)
        cyprus.setup_servo(1)
        cyprus.set_servo_position(1, 0.5)

        while True:
            if cyprus.read_gpio() & 0b0001:
                sleep(0.05)
                if cyprus.read_gpio() & 0b0001:
                    cyprus.set_servo_position(1, 0.5)
            else:
                cyprus.set_servo_position(1, 1)

    def cytronControllerFN(self):
        cyprus.setup_servo(1)
        # cyprus.set_servo_position(1, 0.5)

        cyprus.set_pwm_values(1, period_value=100000, compare_value=50000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        sleep(5)
        cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        sleep(5)

    def proximitySensorCytronController(self):
        cyprus.setup_servo(1)
        # cyprus.set_servo_position(1, 0.5)
        print("function is working")

        while True:
            if cyprus.read_gpio() & 0b0010:  # HIGH (True) means not detecting metal
                sleep(1)
                if cyprus.read_gpio() & 0b0010:
                    print("Metal not detected")
                    cyprus.set_pwm_values(1, period_value=100000, compare_value=50000,
                                          compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            if not (cyprus.read_gpio() & 0b0010):
                sleep(1)
                if not (cyprus.read_gpio() & 0b0010):
                    cyprus.set_pwm_values(1, period_value=100000, compare_value=0,
                                          compare_mode=cyprus.LESS_THAN_OR_EQUAL)
                    print("Metal detected")

        # while cyprus.read_gpio() & 0b0010:
        # cyprus.set_pwm_values(1, period_value=100000, compare_value=50000,
        # compare_mode=cyprus.LESS_THAN_OR_EQUAL)


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
