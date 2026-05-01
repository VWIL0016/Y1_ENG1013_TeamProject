# Version 1.0
# Author: Vivek Wilson

'''
Notes from testing: US1&2 work
TL1&2 Need work. Get stuck on yellow, barely any green. No red
WL1 Pending
More notes pending.
'''

from pymata4 import pymata4 as pymata
import time

board = pymata.Pymata4()

# --- Approach Height Detection Subsystem Configuration ---

usSensorHeightCm = 400
defaultOverheightLimitM = 4.0
defaultOverheightLimitCm = defaultOverheightLimitM * 100

sameSensorWindowS = 1.0
us1ToUs2ToleranceS = 2.0
heightMatchToleranceCm = 20.0
vehicleRetentionWindowS = 35.0

vehicleSpeedKmh = 100
distanceUs1ToUs2M = 5.0

trafficLightPins = {
    1: {"yellow": 2, "red": 3, "green": 4},
    2: {"yellow": 5, "red": 6, "green": 7},
}

ultrasonicSensorPins = {
    1: (8, 9),
    2: (10, 11),
}

sonarPinToSensor = {
    ultrasonicSensorPins[1][0]: 1,
    ultrasonicSensorPins[1][1]: 1,
    ultrasonicSensorPins[2][0]: 2,
    ultrasonicSensorPins[2][1]: 2,
}


def calc_delta_time_us1_to_us2(vehicleSpeedKmh, sensorDistanceM):
    metresPerSecond = vehicleSpeedKmh * (1000 / 3600)
    return sensorDistanceM / metresPerSecond


expectedUs1ToUs2TimeS = calc_delta_time_us1_to_us2(
    vehicleSpeedKmh,
    distanceUs1ToUs2M,
)


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

lastReportedClearance = {
    1: None,
    2: None,
}

lastNoDataReportTime = {
    1: 0,
    2: 0,
}

trafficLightState = {
    1: "green",
    2: "green",
}

trafficLightTriggerTime = {
    1: None,
    2: None,
}

overheightVehicles = []


# --- Hardware Setup ---

for lightPins in trafficLightPins.values():
    for pin in lightPins.values():
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


def refresh_sonar_readings():
    for sensorId, pins in ultrasonicSensorPins.items():
        triggerPin = pins[0]
        clearanceCm, timestamp = board.sonar_read(triggerPin)

        if timestamp == 0 or clearanceCm is None:
            continue

        latestSensorClearance[sensorId] = clearanceCm
        lastSensorTimestamp[sensorId] = timestamp


def report_sonar_configuration():
    print("Sonar configuration:")
    for sensorId, pins in ultrasonicSensorPins.items():
        triggerPin, echoPin = pins
        print(
            f"US{sensorId}: trigger pin {triggerPin}, echo pin {echoPin}, "
            f"registered={triggerPin in board.active_sonar_map}"
        )


def read_vehicle_height(sensorId):
    clearanceCm = latestSensorClearance[sensorId]
    timestamp = lastSensorTimestamp[sensorId]

    if clearanceCm is None or timestamp is None:
        return None

    vehicleHeightCm = usSensorHeightCm - clearanceCm
    return vehicleHeightCm, timestamp


def is_overheight(reading, overheightLimitCm):
    return reading is not None and reading[0] > overheightLimitCm


def both_traffic_lights_green():
    return trafficLightState[1] == "green" and trafficLightState[2] == "green"


def clear_finished_vehicle_entries():
    if not both_traffic_lights_green():
        return

    currentTime = time.time()
    overheightVehicles[:] = [
        vehicle
        for vehicle in overheightVehicles
        if currentTime - vehicle["last_seen"] <= vehicleRetentionWindowS
    ]


def get_latest_active_vehicle(sensorId):
    for vehicle in reversed(overheightVehicles):
        if vehicle["sensor"] == sensorId and vehicle["active"]:
            return vehicle
    return None


def within_same_sensor_window(previousTimestamp, currentTimestamp):
    if previousTimestamp is None:
        return False
    return currentTimestamp - previousTimestamp <= sameSensorWindowS


def store_vehicle_sample(sensorId, reading):
    vehicleHeightCm, timestamp = reading
    vehicle = get_latest_active_vehicle(sensorId)

    if vehicle is None or not within_same_sensor_window(vehicle["last_seen"], timestamp):
        vehicle = {
            "sensor": sensorId,
            "detected_at": timestamp,
            "last_seen": timestamp,
            "height_samples_cm": [vehicleHeightCm],
            "active": True,
            "matchedToUs2": False,
            "matchedUs1Detection": None,
        }
        overheightVehicles.append(vehicle)
        return vehicle

    if vehicle["last_seen"] != timestamp:
        vehicle["height_samples_cm"].append(vehicleHeightCm)
        vehicle["last_seen"] = timestamp

    return vehicle


def moving_average_height(vehicle):
    heightSamples = vehicle["height_samples_cm"]
    return sum(heightSamples) / len(heightSamples)


def find_matching_us1_vehicle(us2Timestamp, us2HeightCm):
    bestMatch = None
    bestTimeError = None

    for vehicle in overheightVehicles:
        if vehicle["sensor"] != 1 or not vehicle["active"] or vehicle["matchedToUs2"]:
            continue

        us1Timestamp = vehicle["detected_at"]
        timeDifference = us2Timestamp - us1Timestamp
        timeError = abs(timeDifference - expectedUs1ToUs2TimeS)

        if timeError > us1ToUs2ToleranceS:
            continue

        us1AverageHeightCm = moving_average_height(vehicle)
        heightError = abs(us2HeightCm - us1AverageHeightCm)

        if heightError > heightMatchToleranceCm:
            continue

        if bestMatch is None or timeError < bestTimeError:
            bestMatch = vehicle
            bestTimeError = timeError

    return bestMatch


def is_same_vehicle(us1Timestamp, us2Timestamp):
    if us1Timestamp is None:
        return False

    timeDifference = us2Timestamp - us1Timestamp
    return abs(timeDifference - expectedUs1ToUs2TimeS) <= us1ToUs2ToleranceS


def initialise_traffic_light(trafficLightId):
    lightPins = trafficLightPins[trafficLightId]

    board.digital_write(lightPins["green"], 1)
    board.digital_write(lightPins["yellow"], 0)
    board.digital_write(lightPins["red"], 0)
    trafficLightState[trafficLightId] = "green"


def start_traffic_light_sequence(trafficLightId, triggerTimestamp):
    if trafficLightTriggerTime[trafficLightId] is None:
        trafficLightTriggerTime[trafficLightId] = triggerTimestamp


def update_traffic_light_sequence(trafficLightId, triggerTimestamp):
    lightPins = trafficLightPins[trafficLightId]
    elapsedTime = time.time() - triggerTimestamp

    if elapsedTime < 1:
        board.digital_write(lightPins["green"], 0)
        board.digital_write(lightPins["red"], 0)
        board.digital_write(lightPins["yellow"], 1)
        trafficLightState[trafficLightId] = "yellow"
        return

    if elapsedTime < 31:
        board.digital_write(lightPins["green"], 0)
        board.digital_write(lightPins["yellow"], 0)
        board.digital_write(lightPins["red"], 1)
        trafficLightState[trafficLightId] = "red"
        return

    board.digital_write(lightPins["red"], 0)
    initialise_traffic_light(trafficLightId)
    trafficLightTriggerTime[trafficLightId] = None

    if both_traffic_lights_green():
        for vehicle in overheightVehicles:
            vehicle["active"] = False


def report_overheight(sensorId, averageHeightCm, detectedAt):
    print(
        f"Overheight detected at US{sensorId}: "
        f"{cm_to_m(averageHeightCm):.2f}m at Time: {human_readable_time(detectedAt)}"
    )


def report_live_sensor_reading(sensorId):
    clearanceCm = latestSensorClearance[sensorId]
    timestamp = lastSensorTimestamp[sensorId]

    if clearanceCm is None or timestamp is None:
        return

    if lastReportedClearance[sensorId] == timestamp:
        return

    lastReportedClearance[sensorId] = timestamp
    vehicleHeightCm = usSensorHeightCm - clearanceCm
    print(
        f"US{sensorId} raw clearance: {format_distance_m(clearanceCm)} | "
        f"calculated vehicle height: {format_distance_m(vehicleHeightCm)} | "
        f"time: {human_readable_time(timestamp)}"
    )


def report_no_data_status(sensorId):
    currentTime = time.time()

    if currentTime - lastNoDataReportTime[sensorId] < 1:
        return

    triggerPin = ultrasonicSensorPins[sensorId][0]
    clearanceCm, timestamp = board.sonar_read(triggerPin)
    lastNoDataReportTime[sensorId] = currentTime

    print(
        f"US{sensorId} no data yet | trigger pin: {triggerPin} | "
        f"raw sonar_read: [{clearanceCm}, {timestamp}]"
    )


def run_live_test_mode():
    print("Live sonar test mode started. Press Ctrl+C to stop.")
    report_sonar_configuration()

    while True:
        try:
            refresh_sonar_readings()
            report_live_sensor_reading(1)
            report_live_sensor_reading(2)
            if lastSensorTimestamp[1] is None:
                report_no_data_status(1)
            if lastSensorTimestamp[2] is None:
                report_no_data_status(2)
            time.sleep(0.1)
        except KeyboardInterrupt:
            break


def handle_us1_detection(reading, overheightLimitCm):
    if not is_overheight(reading, overheightLimitCm):
        return

    vehicle = store_vehicle_sample(1, reading)
    averageHeightCm = moving_average_height(vehicle)
    detectedAt = vehicle["detected_at"]

    if detectedAt == lastReportedDetection[1]:
        return

    lastReportedDetection[1] = detectedAt
    report_overheight(1, averageHeightCm, detectedAt)
    start_traffic_light_sequence(1, detectedAt)


def handle_us2_detection(reading, overheightLimitCm):
    if not is_overheight(reading, overheightLimitCm):
        return

    vehicle = store_vehicle_sample(2, reading)
    averageHeightCm = moving_average_height(vehicle)
    detectedAt = vehicle["detected_at"]

    if detectedAt == lastReportedDetection[2]:
        return

    lastReportedDetection[2] = detectedAt

    matchingUs1Vehicle = find_matching_us1_vehicle(detectedAt, averageHeightCm)

    if matchingUs1Vehicle is None:
        start_traffic_light_sequence(1, detectedAt)
    else:
        matchingUs1Vehicle["matchedToUs2"] = True
        vehicle["matchedUs1Detection"] = matchingUs1Vehicle["detected_at"]

    report_overheight(2, averageHeightCm, detectedAt)
    start_traffic_light_sequence(2, detectedAt)


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


def update_all_traffic_lights():
    for trafficLightId, triggerTimestamp in trafficLightTriggerTime.items():
        if triggerTimestamp is not None:
            update_traffic_light_sequence(trafficLightId, triggerTimestamp)


def prompt_run_mode():
    return (
        input(
            "Select mode:\n"
            "1. Live sonar test\n"
            "2. Full overheight monitoring\n"
            "Press Enter for full monitoring: "
        ).strip()
        or "2"
    )


def initialise_subsystem():
    for trafficLightId in trafficLightPins:
        initialise_traffic_light(trafficLightId)


# --- Main Program ---
def main():
    runMode = prompt_run_mode()

    if runMode == "1":
        run_live_test_mode()
        return

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

            update_all_traffic_lights()
            clear_finished_vehicle_entries()
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()

board.shutdown()
quit()
