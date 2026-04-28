# ENG1013 — Engineering smart systems 

## 3​ Project Restrictions 

Your team has been asked to design, build, and demonstrate a simplified traffic control system in this project. 

Your system will consist of multiple subsystems, and the client has split these subsystems into groups of required features, general features and integration features. There is also an additional complete integration point value available. Most subsystems will contain multiple general and integration features which your team can choose to implement, which you can read about in the milestone deliverables section, and in the system features section below. Testing will only consider the case of a single vehicle passing through the system, which may or may not be overheight. Teams should select an appropriate scale for the project. 

The project is graded out of 260 points, with the final point value being scaled based on your individual contributions as a team member, and your final viva interview. Your mark is scaled according to the Weighted Scaling Factor to form 26% of your total mark for ENG1013. This project is not part of any hurdle requirement. 

You can find rubric feedback under the relevant link in Moodle under ‘Learning > Project Resources > Results’ which shows your team’s performance in each milestone against each assessed item.  

## 3.1​ Hardware Requirement  

You are permitted to use any and all of the hardware components provided in all of your team’s supplied kits (i.e. all 5 combined), plus single core wire and additional breadboards. However, you may use only ONE Arduino to attain maximum points for a fully integrated system. If your team isn’t aiming to attain points from the ‘integration features’, you can use multiple Arduinos - one for each subsystem - note that only one Arduino can be ‘active’ and running at once. You may not use any other hardware components. You may use more shift registers, op-amps, timers and MOSFETs than provided as long as they are the same component. 

## 3.2​ Software Requirements  

You may develop your software in any Integrated Development Environment (IDE); however, support will only be provided by demonstrators in VSCode. You may only use the following additional packages within Python 3.10.x: 

-​ Pymata4  
-​ Time  
-​ Math  
-​ Matplotlib  
-​ Random  

The following packages are permitted, but demonstrators will not provide support: 

-​ NumPy  
-​ CSV  

All other packages, Classes and assert statements are not to be used. If found, they will be commented out for marking.  

Students may use generative AI but must cite and provide a record of generative AI use (as a pdf) in their submission. 

## 3.3​ Academic Integrity Warning 

This is a team project. This means that all members of the team have equal responsibility to review work submitted, and ensure that all members comply with the academic standards required of you as a student of Monash University.  

You are permitted to: 

-​ Use generative AI to assist them in improving paragraphs of the report that is written by you (such as vocab, structure or grammar).  
-​ Use generative AI to assist them in code that is written by you (such as structure or standards), to understand circuit states (or debug), or verify calculations made. Students can use generative AI to understand how code syntax or a circuit works.  
-​ Work with your team-mates  
-​ Seek help from your team-mate  
-​ Seek help from unit staff in-class or via the ed forums  
-​ Use the Internet to look up resources. If you use work that isn’t your own, ensure that you provide a citation to the source. If you are unsure if you can use said work, please seek advice from the unit Chief Examiner before doing so. 

You are prohibited from: 

-​ Using generative AI to generate your entire (or the majority of your) work. The work submitted must be mostly original / written by the student.  
-​ Working with students not from your team  
-​ Working with friends  
-​ Working with family members  

You are reminded that any work submitted must: 

-​ represent a sincere demonstration of your human efforts, skills and subject knowledge that you will be accountable for.  
-​ adhere to the guidelines for AI use set for the assessment task.  
-​ reflect the University’s commitment to academic integrity and ethical behaviour.  

## 4​ System Overview 

This project is based on the Blackwall Tunnel (Southern Approach) which exists in the UK. We have simplified the actual system in reality to comprise of the A102, the freeway leading up to the tunnel entrance, and Tunnel Ave, the arterial road running parallel to A102 near the tunnel entrance. The main emphasis of the system is on traffic control and to prevent or minimize overheight vehicle collisions at the tunnel entrance, which only can accommodate up to 4.0m high vehicles. The system provides a overheight detection system on approach, a final overheight vehicle exit and a final overheight vehicle detection system just prior to the tunnel entrance. There are also systems in place to take control of the traffic should power fail in the area, which is run off backup batteries. You can find the feature and subsystem specifications under System Features which describes the system behaviour modelled below. US1/US2 should be capable of reading the actual vehicle height, whereas US3/US4/US4 are only required to detect an over-height vehicle passing. 

![Figure 1: Model of Traffic Control Safety System for the tunnel.](image_1.png)

## 7​ System Features 

This section outlines the functional requirements of the system, divided into five subsystems.  

The system should continue to run, uninterrupted, until the user chooses to exit (via KeyboardInterrupt).  
You must handle the KeyboardInterrupt and cleanly turn off all pins, then shutdown the Arduino.  

For your convenience, the features in each subsystem are color coded as follows: 

-​ Required features are shown in blue highlights.  
-​ General features are shown in normal text (no highlight).  
-​ Integration features are shown in yellow highlights.  

## 7.1​ Approach Height Detection Subsystem 

This is the primary overheight detection system, consisting of two sets of overheight detection ultrasonic sensor (US1, US2), two sets of red/yellow/green traffic lights (TL1, TL2) spaced 500m apart along the road, a speaker system (PA1) and a set of two yellow warning lights (WL1). The subsystem is the yellow highlighted section of the traffic control system prior to the over-height exit on the system overview.  

| Code | Description | Value |
|------|------------|-------|
| 1.R1 | Upon detection of an overheight vehicle by US1, an alert is printed to the console. The alert should include the detected height of the vehicle, as well as the date/time of detection. | 5 |
| 1.R2 | Upon detection of an overheight vehicle by US1, the following sequence is triggered:<br><br>1.​ TL1 switches to yellow for 1s, then to red for 30s.<br>2.​ TL1 then turns back to green. | 5 |
| 1.R3 | Upon detection of an overheight vehicle by US2, the following sequence is triggered:<br><br>-​ If US1 did not detect an overheight vehicle, TL1 and TL2 immediately switch to yellow for 1s, then red for 30s before turning back to green.<br><br>-​ If US1 detected an overheight vehicle, then TL2 switches to yellow for 1s, then red for 30s before turning back to green.<br><br>You will need to calculate a reasonable threshold for determining if it’s the same vehicle based on the sensors being 500m apart for a heavy vehicle going at highway speeds. | 5 |
| 1.R4 | Upon system start-up, the user is prompted to enter the overheight limit configuration for the system. If the user hits enter without providing any input, it defaults to the system default value of 4.0 meters. This value should be used as a variable in the entire subsystem. | 5 |
| 1.G1 | Upon detection of an overheight vehicle by US1/US2, WL1 turns on and flashes each yellow LED in turn at 2-5 Hz so long as either TL1 or TL2 are not green. | 5 |
| 1.G2 | Upon detection of an overheight vehicle by US1/US2, PA1 turns on and begins sounding a unique buzzer tone (400Hz - 800Hz). The buzzer tone must be generated using a 555 timer. PA1 turns off if TL1 and TL2 are no longer red. | 10 |
| 1.G3 | If US2 continues to detect an overheight vehicle, hold TL1/TL2 at red light. After 30s of TL2 at red, the buzzer tone on PA1 changes to a higher frequency tone (2kHz - 4kHz). The buzzer tone must be generated using a 555 timer. | 10 |
| 1.G4 | The data feed from ultrasonic sensor US1/US2 is filtered for noise appropriately using a moving average. | 5 |
| 1.I1 | This feature requires integration with subsystem three.<br><br>This feature overrides the default behaviour above.<br>When TL1 and TL2 turn red as controlled by US1/US2, they will stay red until US5 detects an overheight vehicle passing (hence exiting the system), and US1/US2 and US5 no longer detect an overheight vehicle. Then, set TL1 and TL2 back to green, and turn off WL1 and PA1. | 10 |

## 7.2 Tunnel Ave Control Subsystem
This subsystem contains a major road, the Tunnel Ave with a minor controlled junction that turns into it via controlled Traffic Lights (TL4/TL5). It has a pedestrian crossing with its associated red/green pedestrian lights (PL1/PL2) and pair of pedestrian crossing push buttons (PB1/PB2) on the Tunnel Ave arterial road. DS2 is a LDR that controls the traffic light timing for day/night cycles. This subsystem is highlighted in pink on the system overview.

| Category | Description | Value |
|----------|------------|-------|
| 2.R1 | If the pedestrian push button PB1/PB2 is pressed, the following sequence should be triggered after a two second wait.<br><br>If TL5 is currently not red, TL5 goes yellow for 3s, then red. Otherwise, TL4 turns yellow for 3 seconds, then red.<br><br>1.​ Then, PL1/PL2 turns green for 3s, then flashing red for 2s before resetting to solid red.<br>2.​ Then, TL4 turns back to green. | 10 |
| 2.R2 | If the pedestrian push button PB1/PB2 is pressed, show this information on the console once (until the sequence 2.R1 is run). (i.e. you should ensure that holding down or spamming the push button does not trigger multiple console prints). | 5 |
| 2.R3 | TL4 and TL5 operate on a 20-10 second cycle. That is, after 20 seconds on green, TL4 will turn yellow (3s), then red. When TL4 turns red, TL5 turns green for 10 seconds, then yellow (3s), then red, and the cycle repeats with TL4 turning green. | 5 |
| 2.G1 | After PB1/PB2 is pressed and 2.R1 runs, enforce a minimum wait of 30s before running 2.R1 again.<br><br>The pedestrian push button PB1/PB2 is explicitly debounced using hardware components such that a clear signal is sent. | 5 |
| 2.G2 | The frequency of flashing of PL1/PL2 red light is generated using a single 555 timer. | 5 |
| 2.G3 | LDR DS2 is used to detect if it’s currently day or night. If it’s night-time, then the traffic light timings for TL4 and TL5 are overridden as follows:<br><br>-​ TL4 green cycle is now 30s.<br>-​ TL5 green cycle is now 5s.<br>-​ If PB1/PB2 is triggered during any cycle, both TL4 and TL5 will follow their respective timings and stop at red for 5s to allow PL1/PL2 to follow their pedestrian cycle of green/flashing red. | 5 |
| 2.I1 | This feature requires integration with subsystem three.<br><br>This feature overrides the default behaviour.<br>Upon detection of a vehicle by US5, if TL4 is currently not red, it should turn yellow (3s) then red. If TL5 is currently not red, it should turn yellow, then red. Then, PL1/PL2 turns green.<br><br>When a vehicle is no longer detected by US5, the following sequence should execute:<br><br>-​ PL1/PL2 should turn flashing red for 2s before resetting to solid red.<br>-​ Then, TL4 should turn green.<br>-​ TL4/TL5 should then resume the normal 2.R3 cycle. | 10 |

## 7.3 Over-height Exit Subsystem
This is the subsystem controlling the set of the red/yellow/green traffic lights (TL6), a light dependent resistor
for detecting day/night (DS1), a set of two floodlights (white LEDs) (FL1, FL2) as well as the vehicle presence
detection ultrasonic sensor (US5) on the over-height exit off the A102. This subsystem is highlighted in purple
on the system overview.

| Category | Description | Value |
|----------|------------|-------|
| 3.R1 | Upon detection of an overheight vehicle by US5, the following sequence should trigger to allow the vehicle to exit:<br><br>1.​ TL6 turns green for 5s<br>2.​ TL6 then turns yellow for 3s<br>3.​ TL6 then turns back to red | 10 |
| 3.R2 | If the ultrasonic sensor US5 continues to detect an overheight vehicle after TL6 has been green for 5s, TL6 continues to stay green until US5 no longer detects a vehicle. | 5 |
| 3.G1 | If the ultrasonic sensor US5 continues to detect an overheight vehicle after TL6 has stayed green for at least 5s, the following sequence runs instead:<br><br>1.​ TL6 flashes green at 2-5 Hz continuously until US5 no longer detects an overheight vehicle<br><br>2.​ TL6 turns back to red (otherwise (1) will continue).<br><br>The frequency of flashing green of TL6 at 2-5Hz is generated using a 555 timer. | 10 |
| 3.G2 | The data feed from ultrasonic sensor US5 is filtered for noise appropriately using a moving average. | 3 |
| 3.G3 | If the ultrasonic sensor US5 detects an overheight vehicle and the LDR DS1 detects that it is night time, the following events occur:<br><br>1.​ Turn FL1 and FL2 on and this stays on while US5 detects an overheight vehicle<br><br>2.​ Turn FL1 and FL2 off afterwards/after the condition is cleared | 5 |
| 3.G4 | If the LDR DS1 detects that it is night time, the base green timing for TL6 is changed from 5s to 10s. This affects all triggers relying on TL6 green such as in 3.R2 and 3.G1. | 5 |
| 3.I1 | This feature requires integration with subsystem two.<br><br>This feature overrides the default behaviour.<br>Upon detection of an overheight vehicle by US5, 3.R1 sequence is delayed by a minimum of 3s (upper limit delay for TL6 is determined by the time needed for TL4/TL5 to complete sequences and turn red) to allow for the Tunnel Ave traffic lights to turn red before allowing the exit traffic to move. | 5 |

## 7.4 Tunnel Height Detection Subsystem
This is the “last chance” overheight detection system, consisting of a set of overheight detection ultrasonic sensor (US3/US4), a set of red/green traffic lights (TL3), and two sets of two red warning lights (WL2) which are used to indicate tunnel closure when flashing. This subsystem is highlighted in green on the system overview.

| Category | Description | Value |
|----------|------------|-------|
| 4.R1 | Upon detection of an overheight vehicle by US3, TL3 should turn from green to red immediately. The system can only reset to ‘normal state’ if an overheight vehicle is no longer detected by US3. (i.e. TL3 turns back to green) | 5 |
| 4.R2 | The ultrasonic sensor US4 is used to verify data read by US3. US3 is only triggered if US4 reads the same value (within an acceptable error range). | 5 |
| 4.R3 | Upon system start-up, the user is prompted to enter the overheight limit configuration for the system. If the user hits enter without providing any input, it defaults to the system default value of 4.0 meters. This value should be used as a variable in the entire subsystem. | 5 |
| 4.G1 | Upon detection of an overheight vehicle by US3, WL2 turns on and flashes each red LED in turn at 2-5 Hz so long as US3/US4 detects an overheight vehicle. The pattern of flashing is XOXO then OXOX where WL2 is configured as two pairs of red LEDs. | 5 |
| 4.G2 | (Must implement 4.G1) WL2 flashing red frequency is generated electrically using a 555 timer. | 5 |
| 4.I1 | This feature requires integration with subsystem one.<br><br>This feature overrides the default behaviour from subsystem 1.<br>Upon detection of an overheight vehicle by US3/US4, execute the following sequences until US3/US4 no longer detects an overheight vehicle:<br><br>-​ TL1 and TL2 turns red<br>-​ PA1 starts sounding a unique tone between 4kHz and 6kHz. This frequency is generated using a 555 timer.<br>-​ WL1 turns on and flashes each yellow LED in turn at 5-10 Hz | 10 |
| 4.I2 | This feature requires integration with subsystem two.<br><br>This feature overrides the default behaviour from subsystem 2.<br>Upon detection of an overheight vehicle by US3/US4, execute the following sequences until US3/US4 no longer detects an overheight vehicle:<br><br>-​ TL4/TL5 turns red (overriding any existing state temporarily). | 5 |
| 4.I3 | This feature requires integration with subsystem one, subsystem two and subsystem three.<br><br>This feature overrides the default behaviour from subsystems 1, 2 and 3.<br>Upon detection of an overheight vehicle by US3/US4, execute the following alternate behaviour:<br><br>-​ The system reset to ‘normal state’ now relies on:<br>○​ US5 detecting an overheight vehicle exiting<br>○​ US1/US2/US3/US4/US5 no longer detecting an overheight vehicle | 10 |

## 7.5 Failure Alert Subsystem (Advanced)
This is the subsystem that operates in case of power failure to the Tunnel Height Detection Subsystem in order to shut down the tunnel for safety reasons. It consists primarily of a backup battery pack, an override switch (OS1), a speaker system (PA2), and has overarching control of all the red traffic lights on the A102. This system must be built entirely in hardware and is electrically controlled (i.e. no software). This subsystem is highlighted in orange on the system overview. Note for testing: We will not test ‘resumption’ of existing states on power restoration.
The general/integration features (anything above 5.R1) of this subsystem are significantly more difficult to implement than all the others, and should only be attempted by students that have mastered the electrical content. You will need to have completed the last week of lab activities. This subsystem is only worth 10 (required) + 20 (general+integration) = 30 points, so you can attain these marks alternatively by completing the Practical Learning Competencies during the bonus mark periods

| Category | Description | Value |
|----------|------------|-------|
| 5.R1 | This subsystem is powered by an external battery supply and must not be powered by the Arduino’s pins. Upon detecting a loss of power to the Tunnel Height Detection Subsystem’s Arduino (by monitoring the Arduino’s power pins), PA2 should start sounding an alert tone between 500Hz and 2kHz immediately. A 555 timer must be used to generate the tone. The alert tone should be clearly audible (not soft) but not excessive (not too loud). | 10 |
| 5.G1 | The subsystem maintains the alert tone for 3s after power is restored, after a power outage has occurred. (This means the tone should continue to sound for 3s after power is restored after a power outage, and not impact the immediate start of the alert tone upon detection of a power outage). | 5 |
| 5.G2 | If the override switch OS1 has been turned on, enable the Failure Alert subsystem (act as if a power outage has been detected). The override switch OS1 is debounced using hardware components such that a clear signal is sent. | 2 |
| 5.G3 | The detection circuit (monitoring power loss from the Arduino) is done by implementing a comparator op-amp. | 5 |
| 5.I1 | This feature requires integration with subsystem one.<br><br>This feature overrides the default behaviour.<br>If the Failure Alert subsystem is triggered (on a power outage), run:<br><br>-​ TL1 and TL2 turns red until power is restored (this interrupts any existing sequence).<br><br>-​ On power restoration, resume the original sequence. | 8 |
| 5.I2 | This feature requires integration with subsystem four.<br><br>This feature overrides the default behaviour.<br>If the Failure Alert subsystem is triggered (on a power outage), run:<br><br>-​ TL3 turns red until power is restored<br>-​ (Must implement 4.G1) WL2 turns on and flashes each red LED in turn at 5-10 Hz using a 555 timer to generate the flashing signal until power is restored.<br><br>-​ On power restoration, resume the original sequence. | 8 |