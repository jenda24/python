class Television:
    # initialize class variables
    MIN_VOLUME = 0
    MAX_VOLUME = 2
    MIN_CHANNEL = 0
    MAX_CHANNEL = 3

    def __init__(self):
        # set default instance variables (all private)
        self.__status = False  # tv off
        self.__muted = False  # tv unmuted
        self.__volume = self.MIN_VOLUME  # initial volume is min (0)
        self.__channel = self.MIN_CHANNEL  # initial channel is min (0)

    def power(self):
        # turn the TV on or off by changing the status variable
        self.__status = not self.__status

    def mute(self):
        # mute or unmute the TV by changing the muted variable.
        # Only works when the TV is on
        if self.__status:  # only works when TV is on
            self.__muted = not self.__muted

    def channel_up(self):
        # increase the TV channel by 1 when the TV is on
        # if at maximum channel, wraps around to minimum channel.

       if self.__status:  # only works if TV is on
            if self.__channel == self.MAX_CHANNEL:
                self.__channel = self.MIN_CHANNEL  # wrap around to minimum
            else:
                self.__channel += 1

    def channel_down(self):
        # decrease the TV channel by 1 when the TV is on
        # if at min channel, wraps around to max channel

        if self.__status:  # only works if TV is on
            if self.__channel == self.MIN_CHANNEL:
                self.__channel = self.MAX_CHANNEL  # wrap around to maximum
            else:
                self.__channel -= 1

    def volume_up(self):
        # increase the TV volume by 1 when the TV is on
        # If at max volume, stays at max
        # if TV is muted, unmutes it

        if self.__status:  # Only works if TV is on
            if self.__muted:
                self.__muted = False  # unmute if currently muted

            if self.__volume < self.MAX_VOLUME:
                self.__volume += 1
            # if already at maximum, it stays there

    def volume_down(self):
        # decrease the TV volume by 1 when the TV is on
        # if at minimum volume, stays at minimum
        # if TV is muted, unmutes it

        if self.__status:  # only works if TV is on
            if self.__muted:
                self.__muted = False  # unmute if currently muted

            if self.__volume > self.MIN_VOLUME:
                self.__volume -= 1
            # if already at min, it stays there

    def __str__(self):
        # return string representation of the tv's current state
        # Format: Power = [status], Channel = [channel], Volume = [volume]
        # if muted, volume displays as 0 regardless of actual volume setting.

        # Get display volume (0 if muted, actual volume otherwise)
        display_volume = 0 if self.__muted and self.__status else self.__volume

        return f"Power = {self.__status}, Channel = {self.__channel}, Volume = {display_volume}"