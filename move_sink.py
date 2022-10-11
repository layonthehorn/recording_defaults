#!/usr/bin/env python3

import os


def move_sinks(sink_name="game_sink", application_name="wine64-preloader"):
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

    :param sink_name: Name of your sink
    :param application_name: Name of the application binary to move.
    :return:
    """

    path = f"{os.path.expanduser('~')}/.config/"

    os.system(f"pactl list sink-inputs >> {path}in.txt")

    with open(f"{path}in.txt", "r") as file:
        inputs = file.read()

    # get sinks
    os.system(f"pactl list sinks >> {path}sink.txt")

    with open(f"{path}sink.txt", "r") as file:
        sinks = file.read()

    input_list = []

    sink_number = 0
    input_number = 0

    for item in sinks.splitlines():
        if item.startswith("Sink #"):
            sink_number = (item.split("#"))[-1]

        if item.endswith(sink_name):
            # We are doing looking when we find the sink name we want.
            break
    else:
        print("Found no matching sinks!")

    for item in inputs.splitlines():

        if item.startswith("Sink Input #"):
            input_number = (item.split("#"))[-1]

        if item.endswith(f"{application_name}\""):
            input_list.append(input_number)

    if len(input_list) > 0:
        for number in input_list:
            os.system(f"pactl move-sink-input {number} {sink_number}")

    else:
        print("Found no wine applications!")

    os.remove(f"{path}in.txt")
    os.remove(f"{path}sink.txt")


if __name__ == '__main__':
    move_sinks()
