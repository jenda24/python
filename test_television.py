from television import Television


def test_initial_state():
    tv = Television()
    assert str(tv) == "Power = False, Channel = 0, Volume = 0"


def test_power():
    tv = Television()
    tv.power()
    assert "Power = True" in str(tv)
    tv.power()
    assert "Power = False" in str(tv)

    tv.mute()  # TV is off
    assert str(tv) == "Power = False, Channel = 0, Volume = 0"

    tv.mute()  # Still off
    tv.mute()  # Try to unmute while still off
    assert str(tv) == "Power = False, Channel = 0, Volume = 0"


def test_mute_and_unmute():
    tv = Television()
    tv.power()
    tv.volume_up()         # volume should now be 1
    tv.mute()              # mute sets volume to 0
    assert "Volume = 0" in str(tv)

    tv.mute()              # unmute, should restore to 1
    assert "Volume = 1" in str(tv)

    tv.mute()  # mute sets volume to 0
    tv.mute()  # unmute (should restore volume)
    tv.mute()  # mute again, volume = 0
    tv.volume_up()  # should unmute and go to 2
    assert "Volume = 2" in str(tv)


def test_channel_up_wrapping():
    tv = Television()
    tv.power()
    tv.channel_up()  # from 0 to 1
    assert "Channel = 1" in str(tv)

    # Go to max channel
    for x in range(Television.MAX_CHANNEL):
        tv.channel_up()
    assert f"Channel = {Television.MIN_CHANNEL}" in str(tv)  # wraps around

    for _ in range(Television.MAX_CHANNEL + 1):  # go past the max
        tv.channel_up()
    assert f"Channel = {Television.MIN_CHANNEL}" in str(tv)


def test_channel_down_wrapping():
    tv = Television()
    tv.power()
    tv.channel_down()  # from 0 to 3
    assert f"Channel = {Television.MAX_CHANNEL}" in str(tv)


def test_volume_up_normal_and_muted():
    tv = Television()
    tv.power()
    tv.volume_up()  # should be 1
    assert "Volume = 1" in str(tv)

    tv.mute()       # muted → volume = 0
    assert "Volume = 0" in str(tv)

    tv.volume_up()  # should unmute and go to 2
    assert "Volume = 2" in str(tv)

    for x in range(Television.MAX_VOLUME + 1):  # intentionally go beyond max
        tv.volume_up()
    assert f"Volume = {Television.MAX_VOLUME}" in str(tv)


def test_volume_down_normal_and_muted():
    tv = Television()
    tv.power()
    tv.volume_down()  # already at 0
    assert f"Volume = {Television.MIN_VOLUME}" in str(tv)

    tv.volume_up()      # 1
    tv.volume_up()      # 2
    tv.mute()           # muted → 0

    tv.volume_down()    # unmuted → back to 2, then down to 1
    assert "Volume = 1" in str(tv)

    tv.volume_down()    # down to 0
    assert "Volume = 0" in str(tv)


def test_does_not_change_when_off():
    tv = Television()

    # doesn't change volume
    tv.volume_up()
    assert "Volume = 0" in str(tv)
    tv.volume_down()
    assert "Volume = 0" in str(tv)

    #doesn't change channel
    tv.channel_up()
    assert "Channel = 0" in str(tv)
    tv.channel_down()
    assert "Channel = 0" in str(tv)