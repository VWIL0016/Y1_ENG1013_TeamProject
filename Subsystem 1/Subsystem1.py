# Version 3.0
# Author: Vivek Wilson

'''
Notes:
- Everything works (1.R1-1.R4, 1.G1)
-Waiting on confirmation before adding time-reset
'''

from pymata4 import pymata4 as pymata
import time

board = pymata.Pymata4()

# --- Approach Height Detection Subsystem Configuration ---

usSensorHeightCm = 800
defaultOverheightLimitM = 4.0
defaultOverheightLimitCm = defaultOverheightLimitM * 100
mainLoopIntervalS = .1

trafficLightPins = {
    1: {"red": 4, "yellow": 3, "green": 2},
    2: {"red": 7, "yellow": 6, "green": 5},
}

ultrasonicSensorPins = {
    1: (8, 9),
    2: (10, 11),
}

warningLightPins = (12, 13)

sonarPinToSensor = {
    ultrasonicSensorPins[1][0]: 1,
    ultrasonicSensorPins[1][1]: 1,
    ultrasonicSensorPins[2][0]: 2,
    ultrasonicSensorPins[2][1]: 2,
}


# --- Runtime State ---

latestSensorClearance = {
    1: None,
    2: None,
}

lastSensorTimestamp = {
    1: None,
    2: None,
}

lastProcessedSensorTimestamp = {
    1: None,
    2: None,
}

lastReportedDetection = {
    1: None,
    2: None,
}

trafficLightState = {
    1: "green",
    2: "green",
}

trafficLightTriggerTime = {
    1: None,
    2: None,
}

warningLightState = None

warningLightTriggerTime = None
warningLightPhaseDurationS = 0.5

decisionLoggingEnabled = False


# --- Hardware Setup ---

for lightPins in trafficLightPins.values(): #LED Setup
    for pin in lightPins.values():
        board.set_pin_mode_digital_output(pin)

for pin in warningLightPins:
    board.set_pin_mode_digital_output(pin)


def sonar_callback(data): 
    if len(data) < 3:
        return

    pin = data[1]
    clearanceCm = data[2]
    timestamp = data[3] if len(data) > 3 else time.time()
    sensorId = sonarPinToSensor.get(pin)

    if sensorId is None or clearanceCm is None:
        return

    latestSensorClearance[sensorId] = clearanceCm
    lastSensorTimestamp[sensorId] = timestamp


for triggerPin, echoPin in ultrasonicSensorPins.values():
    board.set_pin_mode_sonar(triggerPin, echoPin, callback=sonar_callback)


# --- Helper Functions ---

def human_readable_time(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


def cm_to_m(distanceCm):
    return distanceCm / 100


def format_distance_m(distanceCm):
    return f"{cm_to_m(distanceCm):.2f}m"


def log_decision(message):
    if decisionLoggingEnabled:
        print(f"[LOG] {message}")


def refresh_sonar_readings():
    for sensorId, pins in ultrasonicSensorPins.items():
        triggerPin = pins[0]
        clearanceCm, timestamp = board.sonar_read(triggerPin)

        if timestamp == 0 or clearanceCm is None:
            log_decision(f"US{sensorId}: sonar_read returned no new data.")
            continue

        latestSensorClearance[sensorId] = clearanceCm
        lastSensorTimestamp[sensorId] = timestamp
        log_decision(
            f"US{sensorId}: stored sonar reading clearance={format_distance_m(clearanceCm)} "
            f"timestamp={human_readable_time(timestamp)}."
        )


def read_vehicle_height(sensorId):
    clearanceCm = latestSensorClearance[sensorId]
    timestamp = lastSensorTimestamp[sensorId]

    if clearanceCm is None or timestamp is None:
        log_decision(f"US{sensorId}: no reading available to convert into vehicle height.")
        return None

    vehicleHeightCm = usSensorHeightCm - clearanceCm
    log_decision(
        f"US{sensorId}: converted clearance {format_distance_m(clearanceCm)} into "
        f"vehicle height {format_distance_m(vehicleHeightCm)}."
    )
    return vehicleHeightCm, timestamp


def is_overheight(reading, overheightLimitCm):
    return reading is not None and reading[0] > overheightLimitCm


def both_traffic_lights_green():
    return trafficLightState[1] == "green" and trafficLightState[2] == "green"


def set_warning_light_output(activePinIndex):
    for pinIndex, pin in enumerate(warningLightPins):
        board.digital_write(pin, 1 if pinIndex == activePinIndex else 0)


def initialise_traffic_light(trafficLightId):
    lightPins = trafficLightPins[trafficLightId]

    board.digital_write(lightPins["green"], 1)
    board.digital_write(lightPins["yellow"], 0)
    board.digital_write(lightPins["red"], 0)
    trafficLightState[trafficLightId] = "green"
    log_decision(f"Traffic light {trafficLightId}: initialised to green.")


def start_traffic_light_sequence(trafficLightId, triggerTimestamp):
    if trafficLightTriggerTime[trafficLightId] is None:
        trafficLightTriggerTime[trafficLightId] = triggerTimestamp
        log_decision(
            f"Traffic light {trafficLightId}: sequence started at "
            f"{human_readable_time(triggerTimestamp)}."
        )
    else:
        log_decision(
            f"Traffic light {trafficLightId}: sequence already active "
            f"while {trafficLightState[trafficLightId]}, trigger ignored."
        )


def update_traffic_light_sequence(trafficLightId, triggerTimestamp):
    lightPins = trafficLightPins[trafficLightId]
    elapsedTime = time.time() - triggerTimestamp
    log_decision(
        f"Traffic light {trafficLightId}: evaluating state from "
        f"{trafficLightState[trafficLightId]} at {elapsedTime:.2f}s elapsed."
    )

    if elapsedTime < 1:
        board.digital_write(lightPins["green"], 0)
        board.digital_write(lightPins["red"], 0)
        board.digital_write(lightPins["yellow"], 1)
        trafficLightState[trafficLightId] = "yellow"
        log_decision(f"Traffic light {trafficLightId}: set to yellow ({elapsedTime:.2f}s elapsed).")
        return

    if elapsedTime < 31:
        board.digital_write(lightPins["green"], 0)
        board.digital_write(lightPins["yellow"], 0)
        board.digital_write(lightPins["red"], 1)
        trafficLightState[trafficLightId] = "red"
        log_decision(f"Traffic light {trafficLightId}: set to red ({elapsedTime:.2f}s elapsed).")
        return

    board.digital_write(lightPins["red"], 0)
    initialise_traffic_light(trafficLightId)
    trafficLightTriggerTime[trafficLightId] = None
    log_decision(f"Traffic light {trafficLightId}: sequence finished and reset to green.")


def start_warning_light(triggerTimestamp):
    global warningLightTriggerTime
    if warningLightTriggerTime is None:
        warningLightTriggerTime = time.time()
        log_decision(
            f"Warning light: sequence started at "
            f"{human_readable_time(triggerTimestamp)}."
        )
    else:
        log_decision(f"Warning light: sequence already active")


def update_warning_light_sequence(triggerTimestamp):
    global warningLightState, warningLightTriggerTime
    elapsedTime = time.time() - triggerTimestamp
    log_decision(
        f"Warning light: evaluating state from "
        f"{warningLightState} at {elapsedTime:.2f}s elapsed."
    )
    if both_traffic_lights_green():
        warningLightState = None
        warningLightTriggerTime = None
        set_warning_light_output(None)
        log_decision(f"Warning light: both traffic lights green, sequence reset to OFF.")
        return

    activePinIndex = int(elapsedTime / warningLightPhaseDurationS) % len(warningLightPins)

    if warningLightState != activePinIndex:
        warningLightState = activePinIndex
        set_warning_light_output(activePinIndex)
        log_decision(
            f"Warning light: switched to LED {activePinIndex + 1} "
            f"({elapsedTime:.2f}s elapsed)."
        )


def report_overheight(sensorId, heightCm, detectedAt):
    print(
        f"Overheight detected at US{sensorId}: "
        f"{cm_to_m(heightCm):.2f}m at Time: {human_readable_time(detectedAt)}"
    )


def handle_us1_detection(reading, overheightLimitCm):
    if not is_overheight(reading, overheightLimitCm):
        log_decision(
            f"US1: vehicle height {format_distance_m(reading[0])} is not above the "
            f"{format_distance_m(overheightLimitCm)} threshold."
        )
        return

    detectedHeightCm, detectedAt = reading
    log_decision(
        f"US1: vehicle height {format_distance_m(detectedHeightCm)} exceeded the "
        f"{format_distance_m(overheightLimitCm)} threshold."
    )

    if detectedAt == lastReportedDetection[1]:
        log_decision("US1: duplicate timestamp detected, report skipped.")
        return

    lastReportedDetection[1] = detectedAt
    report_overheight(1, detectedHeightCm, detectedAt)
    start_traffic_light_sequence(1, detectedAt)
    start_warning_light(detectedAt)


def handle_us2_detection(reading, overheightLimitCm):
    if not is_overheight(reading, overheightLimitCm):
        log_decision(
            f"US2: vehicle height {format_distance_m(reading[0])} is not above the "
            f"{format_distance_m(overheightLimitCm)} threshold."
        )
        return

    detectedHeightCm, detectedAt = reading
    log_decision(
        f"US2: vehicle height {format_distance_m(detectedHeightCm)} exceeded the "
        f"{format_distance_m(overheightLimitCm)} threshold."
    )

    if detectedAt == lastReportedDetection[2]:
        log_decision("US2: duplicate timestamp detected, report skipped.")
        return

    lastReportedDetection[2] = detectedAt
    report_overheight(2, detectedHeightCm, detectedAt)
    log_decision("US2: same-vehicle matching disabled, triggering both traffic lights.")
    start_traffic_light_sequence(1, detectedAt)
    start_traffic_light_sequence(2, detectedAt)
    start_warning_light(detectedAt)


def prompt_overheight_limit_cm():
    while True:
        try:
            overheightLimitM = float(
                input(
                    "Enter overheight threshold in m\n"
                    "Default is 4.0m.\n"
                    "Press Enter to use default: "
                ) or defaultOverheightLimitM
            )
            return overheightLimitM * 100
        except ValueError:
            print("Invalid input. Please enter a valid number for the overheight threshold.")


def update_all_lights():
    for trafficLightId, triggerTimestamp in trafficLightTriggerTime.items():
        if triggerTimestamp is not None:
            log_decision(
                f"Traffic light {trafficLightId}: active trigger from "
                f"{human_readable_time(triggerTimestamp)}, updating sequence."
            )
            update_traffic_light_sequence(trafficLightId, triggerTimestamp)
    if warningLightTriggerTime is not None:
        update_warning_light_sequence(warningLightTriggerTime)
    else:
        log_decision(
            f"Warning light: no active trigger, staying "
            f"{warningLightState}."
        )


def prompt_run_mode():
    return (
        input(
            "Select mode:\n"
            "1. Logged overheight monitoring\n"
            "2. Full overheight monitoring\n"
            "Press Enter for full monitoring: "
        ).strip()
        or "2"
    )


def initialise_subsystem():
    for trafficLightId in trafficLightPins:
        initialise_traffic_light(trafficLightId)
    set_warning_light_output(None)


# --- Main Program ---
def main():
    global decisionLoggingEnabled
    runMode = prompt_run_mode()

    if runMode == "1":
        decisionLoggingEnabled = True
        print("Decision log mode enabled.")

    overheightLimitCm = prompt_overheight_limit_cm()
    initialise_subsystem()

    while True:
        try:
            refresh_sonar_readings()
            us1Reading = read_vehicle_height(1)
            us2Reading = read_vehicle_height(2)

            if us1Reading is not None and us1Reading[1] != lastProcessedSensorTimestamp[1]:
                lastProcessedSensorTimestamp[1] = us1Reading[1]
                handle_us1_detection(us1Reading, overheightLimitCm)

            if us2Reading is not None and us2Reading[1] != lastProcessedSensorTimestamp[2]:
                lastProcessedSensorTimestamp[2] = us2Reading[1]
                handle_us2_detection(us2Reading, overheightLimitCm)

            update_all_lights()
            time.sleep(mainLoopIntervalS)
        except KeyboardInterrupt:
            board.shutdown()
            quit()

if __name__ == "__main__":
    main()

board.shutdown()
quit()
