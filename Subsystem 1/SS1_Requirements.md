# Requirements
| Code | Description | Value |
|------|------------|-------|
| 1.R1 | Upon detection of an overheight vehicle by US1, an alert is printed to the console. The alert should include the detected height of the vehicle, as well as the date/time of detection. | 5 |
| 1.R2 | Upon detection of an overheight vehicle by US1, the following sequence is triggered:<br><br>1.​ TL1 switches to yellow for 1s, then to red for 30s.<br>2.​ TL1 then turns back to green. | 5 |
| 1.R3 | Upon detection of an overheight vehicle by US2, the following sequence is triggered:<br><br>-​ If US1 did not detect an overheight vehicle, TL1 and TL2 immediately switch to yellow for 1s, then red for 30s before turning back to green.<br><br>-​ If US1 detected an overheight vehicle, then TL2 switches to yellow for 1s, then red for 30s before turning back to green.<br><br>You will need to calculate a reasonable threshold for determining if it’s the same vehicle based on the sensors being 500m apart for a heavy vehicle going at highway speeds. | 5 |
| 1.R4 | Upon system start-up, the user is prompted to enter the overheight limit configuration for the system. If the user hits enter without providing any input, it defaults to the system default value of 4.0 meters. This value should be used as a variable in the entire subsystem. | 5 |
| 1.G1 | Upon detection of an overheight vehicle by US1/US2, WL1 turns on and flashes each yellow LED in turn at 2-5 Hz so long as either TL1 or TL2 are not green. | 5 |
| 1.G4 | The data feed from ultrasonic sensor US1/US2 is filtered for noise appropriately using a moving average. | 5 |
