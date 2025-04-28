import pytest
from television import *


class Test:
    def setup_method(self):
        self.tv1 = Television()
        self.tv2 = Television(status=True, channel=2, volume=1)

        self.tv3 = Television(muted=True)
        self.tv4 = Television(muted=True, volume=1)

    def teardown_method(self):
        del self.tv1
        del self.tv2
        del self.tv3
        del self.tv4

    def test__init__(self):
        assert self.tv1.__str__() == 'Power = False, Channel = 0, Volume = 0'
        assert self.tv2.__str__() == 'Power = True, Channel = 2, Volume = 1'

        # These values technically shouldn't be possible (TV muted but has volume), but because there are no
        # getters/setters, can't account for them if the user decides to change some of the default values in an odd way.
        assert self.tv3.__str__() == 'Power = False, Channel = 0, Volume = 0'
        assert self.tv4.__str__() == 'Power = False, Channel = 0, Volume = 1'

    def test_power(self):
        self.tv1.power()
        assert self.tv1.__str__() == 'Power = True, Channel = 0, Volume = 0'  # off > on
        assert self.tv2.__str__() == 'Power = True, Channel = 2, Volume = 1'  # control

        self.tv2.power()
        assert self.tv1.__str__() == 'Power = True, Channel = 0, Volume = 0'  # control
        assert self.tv2.__str__() == 'Power = False, Channel = 2, Volume = 1'  # on > off

        self.tv1.power()
        self.tv2.power()
        assert self.tv1.__str__() == 'Power = False, Channel = 0, Volume = 0'  # on > off
        assert self.tv2.__str__() == 'Power = True, Channel = 2, Volume = 1'  # off > on

    def test_mute(self):
        self.tv1.power()
        self.tv1.volume_up()
        assert self.tv1.__str__() == 'Power = True, Channel = 0, Volume = 1'  # brief test to make sure volume_up works
        self.tv1.mute()
        assert self.tv1.__str__() == 'Power = True, Channel = 0, Volume = 0'  # TV muted while on

        self.tv1.mute()
        self.tv1.__str__() == 'Power = True, Channel = 0, Volume = 1'  # TV unmuted while on

        self.tv1.power()
        self.tv1.mute()
        assert self.tv1.__str__() == 'Power = False, Channel = 0, Volume = 1'  # muted while off

        self.tv1.mute()
        assert self.tv1.__str__() == 'Power = False, Channel = 0, Volume = 1'  # unmuted while off

        assert self.tv2.__str__() == 'Power = True, Channel = 2, Volume = 1'  # control

    def test_channel_up(self):
        self.tv1.channel_up()
        assert self.tv1.__str__() == 'Power = False, Channel = 0, Volume = 0'  # channel up while off

        self.tv1.power()
        self.tv1.channel_up()
        assert self.tv1.__str__() == 'Power = True, Channel = 1, Volume = 0'  # channel up while on

        self.tv1.channel_up()
        self.tv1.channel_up()
        self.tv1.channel_up()  # exceeds max value (3)
        assert self.tv1.__str__() == 'Power = True, Channel = 0, Volume = 0'  # channel exceeding max

        assert self.tv2.__str__() == 'Power = True, Channel = 2, Volume = 1'  # control

    def test_channel_down(self):
        self.tv1.channel_down()
        assert self.tv1.__str__() == 'Power = False, Channel = 0, Volume = 0'  # channel down while off

        self.tv1.power()
        self.tv1.channel_down()  # exceeds min
        assert self.tv1.__str__() == 'Power = True, Channel = 3, Volume = 0'  # channel down exceeds min while on

        self.tv1.channel_down()
        assert self.tv1.__str__() == 'Power = True, Channel = 2, Volume = 0'  # channel down while on

        assert self.tv2.__str__() == 'Power = True, Channel = 2, Volume = 1'  # control

    def test_volume_up(self):
        self.tv1.volume_up()
        assert self.tv1.__str__() == 'Power = False, Channel = 0, Volume = 0'  # volume up while off

        self.tv1.power()
        self.tv1.volume_up()
        assert self.tv1.__str__() == 'Power = True, Channel = 0, Volume = 1'  # volume up while on

        self.tv1.mute()
        self.tv1.volume_up()
        assert self.tv1.__str__() == 'Power = True, Channel = 0, Volume = 2'  # volume up while muted

        self.tv1.volume_up()  # exceeds max
        assert self.tv1.__str__() == 'Power = True, Channel = 0, Volume = 2'  # volume up exceeds max

        assert self.tv2.__str__() == 'Power = True, Channel = 2, Volume = 1'  # control

    def test_volume_down(self):
        self.tv1.volume_down()
        assert self.tv1.__str__() == 'Power = False, Channel = 0, Volume = 0'  # volume down while off

        self.tv1.power()
        self.tv1.volume_up()
        self.tv1.volume_up()
        self.tv1.volume_down()
        assert self.tv1.__str__() == 'Power = True, Channel = 0, Volume = 1'  # volume down while on

        self.tv1.volume_up()
        self.tv1.mute()
        self.tv1.volume_down()
        assert self.tv1.__str__() == 'Power = True, Channel = 0, Volume = 1'  # volume down while muted

        self.tv1.volume_down()
        self.tv1.volume_down()
        assert self.tv1.__str__() == 'Power = True, Channel = 0, Volume = 0'  # volume down exceeds min

        assert self.tv2.__str__() == 'Power = True, Channel = 2, Volume = 1'  # control
