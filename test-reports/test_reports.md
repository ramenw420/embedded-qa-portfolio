# Test Execution Reports — QA Portfolio

## 1. Smart Gate Project

### Environment

* **MCU:** ESP32 DevKit v1
* **Platform:** Wokwi Simulator

### Test Matrix

| TC ID    | Title                                                                                               | Precondition                                                     | Expected State | Actual Result                                                            | Status      |
|:-------- |:--------------------------------------------------------------------------------------------------- |:---------------------------------------------------------------- |:-------------- |:------------------------------------------------------------------------ |:-----------:|
| **TC01** | Correct state transition from CLOSED to OPENING after OPEN button is pressed                        | Controller is running; State = CLOSED; Open/Close Relays are OFF | OPENING        | OPEN relay = ON, Open LED = ON, CLOSE relay = OFF                        | **PASS**    |
| **TC02** | Correct state transition from OPENING to OPEN after LIMIT OPEN button is pressed                    | State = OPENING; Open Relay = ON; Open LED = ON                  | OPEN           | OPEN relay = OFF, Open LED = ON, CLOSE relay = OFF, State is not changed | **FAIL**    |
| **TC03** | Correct state transition from OPENING to STOPPED after STOP button is pressed                       | State = OPENING; Open Relay = ON; Open LED = ON                  | STOPPED        | OPEN relay = OFF, Open LED = ON                                          | **FAIL**    |
| **TC04** | Correct state transition from OPEN to CLOSING after CLOSE button is pressed                         | State = OPEN; Open Relay = OFF; Open LED = ON                    | CLOSING        | Close LED = ON, CLOSE relay = ON                                         | **BLOCKED** |
| **TC05** | Correct state transition from CLOSING to CLOSED after LIMIT CLOSE button is pressed                 | State = CLOSING; Close Relay = ON; Close LED = ON                | CLOSED         | Close relay = OFF, Close LED = OFF, CLOSE relay = OFF                    | **PASS**    |
| **TC06** | Correct state transition from CLOSING to STOPPED after STOP button is pressed                       | State = CLOSING; Close Relay = ON; Close LED = ON                | STOPPED        | Close relay = OFF, Open LED = ON                                         | **FAIL**    |
| **TC07** | Correct state transition from STOPPED to OPENING after OPEN button is pressed                       | State = STOPPED; Both Relays are OFF; Both LEDs = OFF            | OPENING        | OPEN relay = ON, Open LED = ON                                           | **PASS**    |
| **TC08** | Correct state transition from STOPPED to CLOSING after CLOSE button is pressed                      | State = STOPPED; Both Relays are OFF; Both LEDs = OFF            | CLOSING        | Close LED = ON, Close relay = ON                                         | **PASS**    |
| **TC09** | Correct system timeout transition for OPENING state if LIMIT OPEN is not triggered after 10 seconds | State = OPENING; Open Relay = ON; Open LED = ON                  | ERROR          | timeout error never arrived                                              | **FAIL**    |
| **TC10** | Correct system timeout transition for CLOSING state if LIMIT CLOSE is not triggered                 | State = CLOSING; Open Relay = ON; Open LED = ON                  | ERROR          | Close relay = OFF, Close LED = OFF, Error LED = ON                       | **PASS**    |
| **TC11** | Prevent direct reversal to/from CLOSING/OPENING state                                               | State = OPENING; Open Relay = ON; Open LED = ON                  | OPENING        | State is changed without errors                                          | **FAIL**    |
| **TC12** | Verify movement commands are blocked while in ERROR state                                           | State = ERROR; Open/Close Relays are OFF; Both LEDs = OFF        | ERROR          | OPEN relay = OFF, Close relay = OFF, Both LEDs = OFF                     | **PASS**    |

## 2. Debounce Project

### Environment

* **MCU:** ESP32 DevKit v1
* **Platform:** Wokwi simulator

### Acceptance Criteria

Valid physical presses = logical press events. RAW interrupts may be greater. Short unstable noise must not create a false logical press/action.

### Execution Log

| ID        | Scenario                        | Physical presses | RAW  | Logical | Actions | Expected | Actual | P/F      |
|:--------- |:------------------------------- |:----------------:|:----:|:-------:|:-------:|:--------:|:------:|:--------:|
| **TC-01** | Normal press                    | 1                | 153  | 1       | 1       | 1        | 1      | **PASS** |
| **TC-02** | Long press                      | 1                | 120  | 1       | 1       | 1        | 1      | **PASS** |
| **TC-03** | Rapid presses                   | 5                | 616  | 5       | 5       | 5        | 5      | **PASS** |
| **TC-04** | Short noise pulse               | 1                | 2    | 1       | 1       | 0        | 1      | **FAIL** |
| **TC-05** | Noise during critical operation | 1                | 1292 | 15      | 15      | 1        | 15     | **FAIL** |

### QA Conclusion

Based on test results the system correctly handles valid button interactions.

Still the system fails to filter noise interactions. Short ones trigger unauthorized actions. Noise during critical operation causes false events and actions multiplication executing few actions from one button interaction.

**Conclusion:** system is not ready for the release due to noise vulnerability, system should be fixed and retested afterwards.

## 3. UART CLI Project

### Environment

* **MCU:** ESP32 DevKit v1
* **Interface:** UART Serial CLI
* **Platform:** Wokwi simulator

### Objective

Find robustness defects without inspecting the source code first.

### Test Matrix

| TC ID     | Input / Sequence                                       | Technique                  | Expected                                          | Actual                                            | Result   | Bug ID     |
|:--------- |:------------------------------------------------------ |:-------------------------- |:------------------------------------------------- |:------------------------------------------------- |:--------:|:---------- |
| **TC-01** | `help`                                                 | valid                      | Commands list displayed                           | Commands list displayed                           | **PASS** | —          |
| **TC-02** | `status`                                               | valid                      | System current status displayed                   | System current status displayed                   | **PASS** | —          |
| **TC-03** | `Help`/`hElp`                                          | Invalid (Case sensitivity) | `ERROR: unknown command` displayed                | `ERROR: unknown command`                          | **PASS** | —          |
| **TC-04** | `set speed 0`                                          | Boundary min valid         | Speed is set to 0                                 | Speed is set to 0                                 | **PASS** | —          |
| **TC-05** | `set speed 255`                                        | Boundary max valid         | Speed is set to 255                               | Speed is set to 255                               | **PASS** | —          |
| **TC-06** | `set speed -1`                                         | Boundary min invalid       | `ERROR: speed out of range` displayed             | `ERROR: speed out of range` displayed             | **PASS** | —          |
| **TC-07** | `set speed 256`                                        | Boundary max invalid       | `ERROR: speed out of range` displayed             | `OK: speed=255` displayed                         | **FAIL** | **BUG-01** |
| **TC-08** | `set speed 255 10`                                     | invalid                    | `ERROR: unknown command` displayed                | `ERROR: unknown command` displayed                | **PASS** | —          |
| **TC-09** | `set timeout 1`                                        | Boundary min valid         | `OK: timeout=1`                                   | `OK: timeout=1`                                   | **PASS** | —          |
| **TC-10** | `set timeout 60`                                       | Boundary max valid         | `OK: timeout=60`                                  | `OK: timeout=60`                                  | **PASS** | —          |
| **TC-11** | `set timeout 0`                                        | Boundary min invalid       | `ERROR: timeout out of range` displayed           | `> OK: timeout=0`                                 | **FAIL** | **BUG-02** |
| **TC-12** | `set timeout 61`                                       | Boundary max invalid       | `ERROR: timeout out of range` displayed           | `ERROR: timeout out of range`                     | **PASS** | —          |
| **TC-13** | `set speed`/`set timeout`                              | invalid no value           | `ERROR: invalid speed` / `ERROR: invalid timeout` | `ERROR: invalid speed` / `ERROR: invalid timeout` | **PASS** | —          |
| **TC-14** | `%:?)(\*`                                              | invalid                    | `Error: unknown command` displayed                | `OK` displayed                                    | **FAIL** | **BUG-03** |
| **TC-15** | `set speed 1` + 29 spaces                              | Valid input length N       | Speed is set to 1                                 | Speed is set to 1                                 | **PASS** | —          |
| **TC-16** | `set speed 1` + 30 spaces                              | invalid input length N+1   | `ERROR: command too long`                         | Speed is set to 1                                 | **FAIL** | **BUG-04** |
| **TC-17** | `set speed 100` -> `set speed 300` -> `status`         | State                      | Previous value is not changed after error         | Previous value is not changed after error         | **PASS** | —          |
| **TC-18** | `helpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` | Buffer overflow            | `ERROR: command too long`                         | reboot                                            | **FAIL** | **BUG-05** |

### QA Conclusion

During system testing with functional, boundary and input length a few errors were found.

* **Critical:** Any string with more than 41 characters causes a buffer overflow, resulting in a system crash.
* **Medium:** The system handles parameter boundaries incorrectly: `set speed 256` cuts the value to 255 instead of returning an error, and `set timeout 0` accepts an invalid zero timeout as well.
* **Low:** System accepts invalid special character strings (`&(^`) with an OK response instead of rejecting them.

**Conclusion:** Current build is not recommended for the release, should be fixed and retested.

## 4. I2C Protocol Project

### Environment

* **MCU:** ESP32 DevKit
* **Peripheral:** MPU6050 / 0x68
* **SDA/SCL:** GPIO21 / GPIO22
* **Capture:** `i2c_trace.vcd`
* **Build:** BUGGY

### Transaction Log

| #     | Timestamp      | Address | R/W  | Data             | ACK/NACK | Expected | Observed |
|:-----:|:-------------- |:-------:|:----:|:---------------- |:--------:|:--------:|:--------:|
| **1** | `513.6102 ms`  | `0x68`  | W    | `6B; 00`         | ACK      | ACK      | ACK      |
| **2** | `514.1940 ms`  | `0x68`  | W->R | `W-41; R-EF, 5C` | ACK      | ACK      | ACK      |
| **3** | `1515.4753 ms` | `0x68`  | W->R | `W-41; R-EF, 5C` | ACK      | ACK      | ACK      |
| **4** | `2516.4753 ms` | `0x68`  | W->R | `W-41; R-EF, 5C` | ACK      | ACK      | ACK      |
| **5** | `3517.4753 ms` | `0x69`  | W    | `-`              | NACK     | ACK      | NACK     |

### Fault Timeline

| Event                   | Timestamp      | Trace Evidence                      |
|:----------------------- |:-------------- |:----------------------------------- |
| **Last successful ACK** | `2516.9000 ms` | `evidence/i2c_trace_evidence_1.png` |
| **First NACK**          | `3517.5650 ms` | `evidence/i2c_trace_evidence_2.png` |

### QA Conclusion

Testing revealed a critical system vulnerability: Fault simulation leads to system complete freezing upon first NACK, system is incapable of automatic recovery after fault condition is removed. Firmware is not recommended for the release and should be fixed and retested afterwards.

## 5. System Recovery & Watchdog Project

### Environment

* **MCU:** ESP32 DevKit V1
* **Sensor:** DHT22 (GPIO15)
* **Button:** GPIO4
* **LED:** GPIO2
* **Relay:** GPIO5
* **Serial:** 115200
* **Build:** BUGGY

### Test Matrix

| Scenario                                    | Risk                                                                         | Action                                                                                                                                           | Expected                                                                                                 | Actual                                                                               | P/F      |
|:------------------------------------------- |:---------------------------------------------------------------------------- |:------------------------------------------------------------------------------------------------------------------------------------------------ |:-------------------------------------------------------------------------------------------------------- |:------------------------------------------------------------------------------------ |:--------:|
| **Boot and reset reasons (R1)**             | Incorrect boot state or reset reason                                         | Start simulation -> observe log / do reboot via CLI -> observe log                                                                               | Device transitions to ACTIVE; correct reset reason displayed: "POWER_ON" / "SOFTWARE_RESET"              | Correct reason displayed                                                             | **PASS** |
| **Button (R3)**                             | Duplicate events / false triggers                                            | Click the button once / a few times -> observe log                                                                                               | 1 click = 1 action                                                                                       | 1 click = 2 actions                                                                  | **FAIL** |
| **Watchdog Trigger / No Boot Loop (R5)**    | Device or system freeze / boot loop                                          | Execute hang via CLI -> observe logs                                                                                                             | WDT triggers reset within 5s; WDT displayed as reset reason; system recovers to ACTIVE without boot loop | System hangs for around 5 sec, WDT triggers reset; System is rebooted                | **PASS** |
| **Post reboot Operability (R5)**            | Device remains unresponsive after WDT reboot                                 | Execute status/sensor commands after WDT reboot                                                                                                  | Device responds/operates after WDT reboot                                                                | Device responds/operates after WDT reboot                                            | **PASS** |
| **Actuator OFF after WDT reboot (R5)**      | Actuator is in a wrong state after WDT reboot                                | Turn Actuator ON -> execute hang -> execute status after reboot -> observe LED state                                                             | Actuator resets to OFF after WDT reboot                                                                  | Actuator remains ON after WDT reboot                                                 | **FAIL** |
| **Sleep Duration (R4)**                     | Failure to sleep / wake up after time is exceeded                            | Execute sleep N via CLI -> Observe system                                                                                                        | Device enters deep sleep and wakes up within N seconds                                                   | Device enters deep sleep and wakes up immediately after command is executed          | **FAIL** |
| **Post-Sleep Operability (R4)**             | Device remains unresponsive after deep sleep                                 | Execute status/sensor commands after Wake up                                                                                                     | Device responds/operates after Wake up; Deep sleep is displayed as reset reason                          | Device responds/operates after Wake up; Deep sleep is displayed as reset reason      | **PASS** |
| **Persistent data (R4)**                    | Data loss or corruption after deep sleep                                     | Execute a few commands so counter changes -> change relay state -> execute save -> execute sleep -> after wake up execute status -> observe logs | Data remains intact and matches pre-sleep values                                                         | Data remains intact and matches pre-sleep values                                     | **PASS** |
| **Data Integrity on Interrupted Save (R6)** | Data corruption due to power loss during saving                              | Execute a few commands so counter changes -> change relay state -> execute powerloss command -> execute status -> observe output                 | Device reboots with valid state and data; corrupted data is detected and rejected                        | System suffered data corruption during powerloss, counter value changed after reboot | **FAIL** |
| **Observable evidence (R7)**                | Missing fields prevent proper understanding of system current state for user | Execute status -> observe output                                                                                                                 | System should return: state, reset reason, relay state, event counter, free heap, sensor status.         | System returns all required fields.                                                  | **PASS** |

### Release Decision

| Decision                            | NO-GO / Action Required                                                                            |
|:----------------------------------- |:-------------------------------------------------------------------------------------------------- |
| **Blocking risks**                  | - Incorrect LED state after WDT reboot<br>- Data corruption on power loss<br>- Sleep timer ignored |
| **Tests required on real hardware** | - Physical button debounce<br>- Power consumption and sleep duration on physical device            |

## 6. Python Automation Project

### Environment

* **MCU:** ESP32 DevKit v1
* **Platform:** Wokwi Simulator (`rfc2217://localhost:4000`)
* **Framework:** Pytest, Python 3.14

### Automated Test Suite Execution

| Test ID   | Test File & Function                                               | Scenario / Parameters                                              | Expected Result                                              | Actual Result                                               | Status   | Bug ID     |
|:--------- |:------------------------------------------------------------------ |:------------------------------------------------------------------ |:------------------------------------------------------------ |:----------------------------------------------------------- |:--------:|:---------- |
| **AT-01** | `pytest/tests/test_boundaries.py`<br>`test_pwm_valid_boundaries`   | Set valid PWM boundary values: `[0, 1, 50, 99, 100]`               | Status `OK` and `pwm == value` for all inputs                | Upper boundary value `100` rejected with `ERROR`            | **FAIL** | **BUG-01** |
| **AT-02** | `pytest/tests/test_boundaries.py`<br>`test_pwm_invalid_boundaries` | Set invalid PWM boundary values: `[-1, 101, 999]`                  | Status `ERROR` with specific code `INVALID_VALUE`            | System returns generic `ERROR` without specific status/code | **FAIL** | —          |
| **AT-03** | `pytest/tests/test_relay.py`<br>`test_led_on_off`                  | Toggle LED state via `SET LED ON` / `SET LED OFF`                  | `led` state updates to `True` and `False` respectively       | LED toggles correctly                                       | **PASS** | —          |
| **AT-04** | `pytest/tests/test_relay.py`<br>`test_reset_restores_safe_state`   | Turn LED ON, execute `RESET`, then query `STATUS`                  | Peripherals reset to safe state (`pwm == 0`, `led is False`) | State leakage: `pwm` remains at `255` instead of `0`        | **FAIL** | **BUG-02** |
| **AT-05** | `pytest/tests/test_sensor.py`<br>`test_temperature_is_valid_json`  | Request temperature via `GET TEMP` and validate JSON               | Valid JSON payload with status `OK` and temp in `[-40, 80]`  | JSON payload truncated mid-stream (`JSONDecodeError`)       | **FAIL** | **BUG-03** |
| **AT-06** | `pytest/tests/test_status.py`<br>`test_ping`                       | Send `PING` command to device                                      | Status `OK` and `command == "PING"`                          | Device fails to respond to `PING`                           | **FAIL** | **BUG-04** |
| **AT-07** | `pytest/tests/test_status.py`<br>`test_status`                     | Query system telemetry via `STATUS` command                        | Status `OK` with `heap` and `pwm` fields present             | Telemetry fields returned in valid structure                | **PASS** | —          |
| **AT-08** | `pytest/tests/test_timeout.py`<br>`test_ping_response_time`        | Measure `PING` command execution time (`max_response_time = 1.0s`) | Device responds with `OK` within `<= 1.0s`                   | Response time exceeds `1.0s` limit (`TimeoutError`)         | **FAIL** | **BUG-04** |

### Test Summary & QA Conclusion

During testing some issues were found. The main issues are: valid PWM values like `100` throw error instead of being accepted, also the system shows Generic ERROR instead of specific statuses for unknown commands and invalid inputs. Additionally broken JSON payload on the temperature sensor and a timeout on `PING` were found.

**Conclusion:** The system is not ready for the release and needs to be fixed and retested afterwards.

## 7. IoT Networking Project

### Environment

* **MCU:** ESP32 DevKit v1
* **Platform:** Wokwi Simulator / IoT Network Module

### R1 Network States Model

| From State   | Trigger            | To State       | Expected Log Output                                                                                                                                                       |
|:------------ |:------------------ |:-------------- |:------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CONNECTED`  | `NET DOWN`         | `DISCONNECTED` | `[NET] state=DISCONNECTED`<br>`[NET] state=BACKOFF`                                                                                                                       |
| `BACKOFF`    | retry              | `CONNECTING`   | `[NET] state=BACKOFF`<br>`[NET] retry=1 backoff_ms=500`<br>`[NET] state=CONNECTING`                                                                                       |
| `CONNECTING` | `reconnect=FAILED` | `BACKOFF`      | `[NET] state=CONNECTING`<br>`[NET] reconnect=FAILED`<br>`[NET] state=BACKOFF`                                                                                             |
| `BACKOFF`    | `NET UP`           | `CONNECTED`    | `[NET] state=BACKOFF`<br>`[NET] retry=92 backoff_ms=50`<br>`[FAULT] network restored`<br>`[NET] state=CONNECTING`<br>`[NET] state=CONNECTED`<br>`[NET] reconnect=SUCCESS` |

### Risk Assessment & Test Matrix

| ID          | Risk                                                                              | Requirement | Consequence                                               | Verification | P/F      |
|:----------- |:--------------------------------------------------------------------------------- |:-----------:|:--------------------------------------------------------- |:------------ |:--------:|
| **RISK-01** | Node won’t recover after connection loss                                          | R2, R5      | Telemetry is not sent                                     | Scenario A   | **PASS** |
| **RISK-02** | Reconnect storm                                                                   | R2          | Broker flooding, device resource consumption              | Scenario B   | **FAIL** |
| **RISK-03** | Offline buffering failure, data loss or duplication                               | R3, R5, R6  | Data loss, messages duplication                           | Scenario C   | **FAIL** |
| **RISK-04** | Buffer overflow, `DROP_OLDEST` policy failure                                     | R4          | Data corruption, payload misorder, buffer boundary bypass | Scenario D   | **FAIL** |
| **RISK-05** | Memory leak and heap degradation during `STRESS` execution when network is lost   | R7          | Progressive memory decreasing leading to heap exhaustion  | Scenario E   | **FAIL** |
| **RISK-06** | Memory leak and heap degradation during `STRESS` execution when network is stable | R7          | Progressive memory decreasing leading to heap exhaustion  | Scenario F   | **FAIL** |

### Test Scenarios

#### Scenario A: Network Loss, Auto-Reconnect & Recovery (R2, R5)

* **Preconditions:** Device is running, state is `CONNECTED`, the broker is active.
* **Steps:**
  1. Execute `RESET STATS` to clear all counters. Record the initial state using the `STATUS` command.
  2. Execute `NET DOWN` to simulate connection loss.
  3. Observe the terminal logs for 10–20 seconds while `state = BACKOFF`, send `STATUS` command and check device response and stats.
  4. Execute `NET UP` to restore connection. Run `STATUS` and check device and stats after connection is restored. Compare stats before `NET DOWN` and after `NET UP`.
* **Expected Result:** After `NET UP`, device returns to the `CONNECTED` state, heap remains stable before and after the tests, `reconnect_attempts` number is increased, LED is on.

#### Scenario B: Reconnect Timing & Storm Verification (R2)

* **Preconditions:** Device is running, state is `CONNECTED`, the broker is active.
* **Steps:**
  1. Execute `NET DOWN` to simulate connection loss.
  2. Observe the terminal logs for 15–20 seconds, observe the `[NET] retry=... backoff_ms=...` sequence.
  3. Check time intervals between retry attempts to verify backoff scaling.
* **Expected Result:** Device should implement backoff logic increasing every other attempt.

#### Scenario C: Offline Buffering & Message Recovery (R3, R5, R6)

* **Preconditions:** Device is running, state is `CONNECTED`, the broker is active.
* **Steps:**
  1. Execute `RESET STATS` to clear all counters and `NET DOWN` to simulate connection loss.
  2. Execute `SEND` a few times.
  3. Execute `BUFFER` and verify queued messages count.
  4. Execute `NET UP` to restore connection.
  5. Observe `flush_start` logs.
  6. Execute `STATUS` and observe system state.
  7. Execute `BUFFER` and observe response.
* **Expected Result:** All queued messages are buffered correctly during connection loss. After `NET UP`, the device publishes all unique messages once without duplicates, `BUFFER` is cleared.

#### Scenario D: Boundary & Buffer Capacity Overflow Verification (R4)

* **Preconditions:** Device is running, state is `CONNECTED`, the broker is active.
* **Steps:**
  1. Execute `RESET STATS` to clear all counters and `NET DOWN` to simulate connection loss.
  2. Execute `SEND` more times than defined buffer capacity (10 or more).
  3. Execute `BUFFER` and `STATUS` during outage to check messages and dropped count.
  4. Execute `NET UP` to restore connection.
* **Expected Result:** Buffer count doesn’t exceed maximum capacity, device drops oldest messages, after `NET UP` only 8 newest messages are sent, the oldest are deleted.

#### Scenario E: Memory Stability & Stress Test During Outage (R7)

* **Preconditions:** Device is running, state is `CONNECTED`, the broker is active, initial heap is recorded.
* **Steps:**
  1. Execute `NET DOWN` followed by `STRESS 100` to simulate message burst during outage.
  2. Execute `STATUS` and check heap state during connection outage.
  3. Execute `NET UP` and wait until the buffer flush completes.
  4. Execute `STATUS` and check heap state after `NET UP`.
  5. Repeat the steps a few times and check/log heap every time.
* **Expected Result:** Heap remains stable after buffer flushes, no memory drops are observed.

#### Scenario F: Memory Leak & Heap Degradation During Stress When Network Is Stable (R7)

* **Preconditions:** Device is running, state is `CONNECTED`, the broker is active, initial heap is recorded.
* **Steps:**
  1. Execute `STRESS 100` to simulate message burst.
  2. Execute `STATUS` and check heap state.
  3. Repeat steps a few times.

##### Scenario F Execution Log

| Iteration | Action       | Network State | Buffer | Sent | Dropped | Duplicates | Free Heap | Notes         |
|:---------:|:------------ |:-------------:|:------:|:----:|:-------:|:----------:|:---------:|:------------- |
| **0**     | Baseline     | `CONNECTED`   | 0      | 0    | 0       | 0          | `350868`  | Initial state |
| **1**     | `STRESS 100` | `CONNECTED`   | 0      | 100  | 0       | 0          | `342604`  | heap `-8264`  |
| **2**     | `STRESS 100` | `CONNECTED`   | 0      | 200  | 0       | 0          | `334604`  | heap `-8000`  |
| **3**     | `STRESS 100` | `CONNECTED`   | 0      | 300  | 0       | 0          | `326612`  | heap `-7992`  |
| **4**     | `STRESS 100` | `CONNECTED`   | 0      | 400  | 0       | 0          | `318600`  | heap `-8012`  |
| **5**     | `STRESS 100` | `CONNECTED`   | 0      | 500  | 0       | 0          | `310600`  | heap `-8000`  |

##### Duplicates After Reconnect Log

| Message ID     | Publish Count | Expected | Result   |
|:-------------- |:-------------:|:--------:|:--------:|
| `publish id=1` | 2             | 1        | **FAIL** |
| `publish id=2` | 2             | 1        | **FAIL** |
| `publish id=3` | 2             | 1        | **FAIL** |
| `publish id=4` | 2             | 1        | **FAIL** |
| `publish id=5` | 2             | 1        | **FAIL** |
| `publish id=6` | 2             | 1        | **FAIL** |

### QA Summary

The current system build is **not recommended for release** due to critical defects affecting system stability, dynamic memory management, and core requirements compliance:

* Upon network loss, the system retries connection at fixed 50 ms intervals instead of applying a backoff logic.
* Offline queue exceeds maximum capacity limit. `DROP_OLDEST` policy is not applied; when connection is restored, every buffered message is sent twice.
* Stress testing with connection loss (as well as under stable connection) reveals a heap leak that is not restored after buffer flush.
