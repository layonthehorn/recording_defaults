#!/usr/bin/env python3

import subprocess


def get_sink_number(sink_name):
    sink_number = None
    temp = subprocess.Popen(["pactl", 'list', "sinks"], stdout=subprocess.PIPE)
    output = str(temp.communicate()[0])
    output_cleaned = (output.replace(r"\t", ""))[2:-1]
    results_list = output_cleaned.split(r"\n")

    for item in results_list:
        if item.startswith("Sink #"):
            sink_number = (item.split("#"))[-1]

        if item.endswith(sink_name):
            # We are doing looking when we find the sink name we want.
            return sink_number
    else:
        print("Found no matching sink names!")


def get_stream_numbers(application_list):
    temp = subprocess.Popen(["pactl", 'list', "sink-inputs"], stdout=subprocess.PIPE)
    output = str(temp.communicate()[0])
    output_cleaned = (output.replace(r"\t", ""))[2:-1]
    results_list = output_cleaned.split(r"\n")

    input_list = []
    input_number = 0

    for item in results_list:

        if item.startswith("Sink Input #"):
            input_number = (item.split("#"))[-1]

        for app in application_list:
            if item.endswith(f"{app}\""):
                input_list.append(input_number)

    return input_list


# Adding applications to the tuple to move things not running in Wine.
# because of the tuple you will need at least 2 items in the list.
# I have gone with Wine and FMOD due to the high number of games using either on Linux.
def move_sinks(sink_name="game_sink", application_list=("wine64-preloader","FMOD Ex App")):
    """
    Best used with applications that the audio stream goes away from when alt-tabbing.
    Works with all wine applications no matter how many output streams they use.

    Get the application from: pactl list sink-inputs
        client.api = "pipewire-pulse"
		pulse.server.type = "unix"
		pipewire.access.portal.app_id = "io.freetubeapp.FreeTube"
		pipewire.client.access = "flatpak"
		application.name = "Chromium" <----- This is the application name.
		application.process.id = "157"
		application.process.user = USERNAME
		application.process.host = HOSTNAME
		application.process.binary = "freetube"



    Get the sink_name from: pactl list sinks
Sink #36
	State: IDLE
	Name: game_sink <----- This is your sink name. Yours will be whatever you specified in your pipewire config.
	Description: Virtual game sink
	Driver: PipeWire
	Sample Specification: float32le 2ch 48000Hz
	Channel Map: front-left,front-right
	Owner Module: 4294967295
	Mute: no

    :param application_list: Tuple of applications to move the sound output on,
    :param sink_name: Name of your sink

    :return:
    """

    # Getting ID of the applications
    input_list = get_stream_numbers(application_list)

    # Getting the ID of the sink
    sink_number = get_sink_number(sink_name)

    if len(input_list) > 0:
        for number in input_list:
            subprocess.Popen(["pactl", 'move-sink-input', f"{number}", f"{sink_number}"], stdout=subprocess.PIPE)

    else:
        print("Found no wine applications!")


if __name__ == '__main__':
    move_sinks()
