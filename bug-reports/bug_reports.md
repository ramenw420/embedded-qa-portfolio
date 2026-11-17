# Bug Reports — Embedded QA Portfolio

This document contains a summary of identified defects across testing cycles, along with detailed reports for critical issues.

## 1. Smart Gate Project

### Environment

* **MCU:** ESP32 DevKit v1
* **Platform:** Wokwi Simulator

### Summary Bug Log

| Bug ID    | Title                                                                            | Requirement | Severity     | Reproducibility | Evidence                                                                                                                                         |
| --------- | -------------------------------------------------------------------------------- | ----------- | ------------ | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **BUG01** | Open LED remains ON after STOP button is pressed                                 | R14         | Medium       | 5/5             | [smart_gate_project_bug_01.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/smart_gate_project_bug_01.png) |
| **BUG02** | System does not transition to ERROR state after 10-second timeout during OPENING | R9          | High         | 5/5             | N/A                                                                                                                                              |
| **BUG03** | Direct reversal between OPENING and CLOSING states allowed without STOP          | N/A         | **Critical** | 5/5             | [smart_gate_project_bug_03.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/smart_gate_project_bug_03.png) |

### Detailed Bug Report (Critical)

#### BUG03: Direct reversal between OPENING and CLOSING states allowed without STOP

* **Bug ID:** BUG03
* **Title:** Direct reversal between OPENING and CLOSING states allowed without STOP
* **Severity:** **Critical** 🔴
* **Reproducibility:** 5/5 (100%)

#### Preconditions

1. The Smart Gate system is powered ON.

#### Steps to Reproduce

1. Initiate opening sequence by triggering command `O` (State transitions: `CLOSED` -> `OPENING`).
2. While state is `OPENING`, immediately trigger opposing command `C` (Close).
3. Observe terminal output and relay behavior.
4. While state is `CLOSING`, immediately trigger opposing command `O` (Open).

#### Expected Result

* Direct state reversal between `OPENING` and `CLOSING` must be rejected or routed through a mandatory `STOP` phase.
* The system should ignore opposite directional commands during active movement to prevent mechanical and electric driver damage.

#### Actual Result

* The firmware immediately switches states back and forth without executing a stop sequence:
  * Log output: `STATE: OPENING -> CLOSING` on command `C`
  * Log output: `STATE: CLOSING -> OPENING` on command `O`

#### Evidence

[smart_gate_project_bug_03.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/smart_gate_project_bug_03.png)

---

## 2. Debounce Project

### Environment

* **MCU:** ESP32 DevKit v1
* **Platform:** Wokwi simulator

### Summary Bug Log

| Bug ID     | Title                                                                        | Requirement | Severity     | Reproducibility | Evidence                                                                                                                     |
| ---------- | ---------------------------------------------------------------------------- | ----------- | ------------ | --------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **BUG_01** | Short noise pulse triggers false logical event and action                    | R1          | High         | 5/5             | [debounce_bug_01.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/debounce_bug_01.png) |
| **BUG_02** | Noise during critical operation causes many false logical events and actions | R1          | **Critical** | 5/5             | [debounce_bug_02.jpg](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/debounce_bug_02.jpg) |

### Detailed Bug Report (Critical)

#### BUG_02: Noise during critical operation causes many false logical events and actions

* **Bug ID:** BUG_02
* **Title:** Noise during critical operation causes many false logical events and actions
* **Severity:** **Critical** 🔴
* **Requirement:** R1
* **Reproducibility:** 5/5

#### Preconditions

1. Simulation is up, system is IDLING

#### Steps to Reproduce

1. Click green button once (to generate an operation)
2. While critical operation is running hold red button to generate noise
3. Wait until operation is finished and observe terminal logs

#### Expected Result

System should generate one logical event and action as green button was pressed once

#### Actual Result

Noise during critical operation causes many false logical events and actions

#### Evidence

[debounce_bug_02.jpg](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/debounce_bug_02.jpg)

---

## 3. UART CLI Project

### Environment

* **MCU:** ESP32 DevKit v1
* **Interface:** UART Serial CLI
* **Platform:** Wokwi simulator

### Summary Bug Log

| Bug ID     | Title                                                                                                           | Requirement | Severity     | Reproducibility | Evidence                                                                                                                     |
| ---------- | --------------------------------------------------------------------------------------------------------------- | ----------- | ------------ | --------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **BUG-01** | No error displayed when speed limit is exceeded                                                                 | R3          | Mid          | 10/10           | [uart_cli_bug_01.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/uart_cli_bug_01.png) |
| **BUG-02** | No error displayed when timeout limit is exceeded                                                               | R5          | Medium       | 10/10           | [uart_cli_bug_02.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/uart_cli_bug_02.png) |
| **BUG-03** | Special characters are accepted with OK instead of unknown command error                                        | R7          | Low          | 10/10           | [uart_cli_bug_03.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/uart_cli_bug_03.png) |
| **BUG-04** | System executes command exceeding max length when padded with trailing spaces instead of returning length error | R10         | Low          | 10/10           | [uart_cli_bug_04.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/uart_cli_bug_04.png) |
| **BUG-05** | System is crashing with fault on buffer overflow when processing long input strings                             | R11         | **Critical** | 10/10           | N/A                                                                                                                          |

### Detailed Bug Report (Critical)

#### BUG-05: System is crashing with fault on buffer overflow when processing long input strings

* **Bug ID:** BUG-05
* **Title:** System is crashing with fault on buffer overflow when processing long input strings
* **Severity:** **Critical** 🔴
* **Requirement:** R11
* **Reproducibility:** 10/10

#### Preconditions

1. Simulation is running.

#### Steps to Reproduce

1. Run simulation
2. Enter a long string exceeding the buffer limit like: `helpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`
3. Observe logs

#### Expected Result

`ERROR: command too long` and remains stable without rebooting

#### Actual Result

System is rebooting

#### Evidence

N/A

---

## 4. I2C Protocol Project

### Environment

* **MCU:** ESP32 DevKit
* **Peripheral:** MPU6050 / 0x68
* **SDA/SCL:** GPIO21 / GPIO22
* **Capture:** i2c_trace.vcd
* **Build:** BUGGY

### Summary Bug Log

| Bug ID     | Title                                  | Requirement | Severity    | Reproducibility | Evidence                                                                                                                                                                                                                                                                                                                                         |
| ---------- | -------------------------------------- | ----------- | ----------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **BUG-01** | Firmware freezes upon NACK, no retry   | N/A         | **Highest** | 10/10           | [i2c_bug.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/i2c_bug.png), [i2c_trace.vcd](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/i2c_trace.vcd), [i2c_bug_2.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/i2c_bug_2.png) |
| **BUG-02** | Firmware won’t recover after FAULT OFF | N/A         | **Highest** | 10/10           | [i2c_bug.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/i2c_bug.png), [i2c_trace.vcd](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/i2c_trace.vcd), [i2c_bug_2.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/i2c_bug_2.png) |

### Detailed Bug Reports (Critical)

#### BUG-01: Firmware freezes upon NACK, no retry

* **Bug ID:** BUG-01
* **Title:** Firmware freezes upon NACK, no retry
* **Severity:** **Highest** 🔴
* **Reproducibility:** 10/10

#### Preconditions

System simulation is running

#### Steps to Reproduce

1. While simulation is running switch FAULT ON
2. Observe logs in terminal and data bus in pulse view

#### Expected Result

System should retry to connect, main loop should stay alive

#### Actual Result

System froze with `[  5519][E][Wire.cpp:499] requestFrom(): i2cWriteReadNonStop returned Error -1`, System’s main loop is no longer alive, retry isn’t happening

#### Evidence

* **Trace Evidence:** [i2c_bug.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/i2c_bug.png), [i2c_trace.vcd](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/i2c_trace.vcd)
* **Firmware Log Evidence:** [i2c_bug_2.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/i2c_bug_2.png)

#### BUG-02: Firmware won’t recover after FAULT OFF

* **Bug ID:** BUG-02
* **Title:** Firmware won’t recover after FAULT OFF
* **Severity:** **Highest** 🔴
* **Reproducibility:** 10/10

#### Preconditions

System simulation is running

#### Steps to Reproduce

1. While simulation is running switch FAULT ON
2. Wait a few seconds
3. Switch FAULT OFF
4. Observe logs in terminal and data bus in pulse view

#### Expected Result

System should continue working after FAULT is back OFF

#### Actual Result

System provides no recovery path after FAULT ON followed by FAULT OFF

#### Evidence

* **Trace Evidence:** [i2c_bug.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/i2c_bug.png), [i2c_trace.vcd](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/i2c_trace.vcd)
* **Firmware Log Evidence:** [i2c_bug_2.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/i2c_bug_2.png)

---

## 5. System Recovery & Watchdog Project

### Environment

* **MCU:** ESP32 DevKit V1
* **Sensor:** DHT22 GPIO15
* **Button:** GPIO4
* **LED:** GPIO2
* **Relay:** GPIO5
* **Serial:** 115200
* **Build:** BUGGY

### Summary Bug Log

| Bug ID     | Title                                                          | Requirement           | Severity     | Reproducibility | Evidence                                                                                                                             |
| ---------- | -------------------------------------------------------------- | --------------------- | ------------ | --------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Bug-01** | Single button press triggers multiple actions                  | Button R3             | Medium       | 3/5             | [recovery_bug_01.mp4](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/recovery_bug_01.mp4)         |
| **Bug-02** | Actuator remains ON after WDT reboot                           | R5 watchdog           | **Critical** | 10/10           | [recovery_bug_02.mp4](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/recovery_bug_02.mp4)         |
| **bug-03** | Device wakes up instantly from deep sleep ignoring sleep timer | R4 — Sleep / Wake     | High         | 10/10           | [recovery_bug_03.mp4](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/recovery_bug_03.mp4)         |
| **bug-04** | Incorrect counter displayed during powerloss                   | R6 — Interrupted save | High         | 10/10           | [recovery_bug_04.mp4.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/recovery_bug_04.mp4.png) |

### Detailed Bug Report (Critical)

#### Bug-02: Actuator remains ON after WDT reboot

* **Bug ID:** Bug-02
* **Title:** Actuator remains ON after WDT reboot
* **Severity:** **Critical** 🔴
* **Requirement:** R5 watchdog
* **Risk:** Led remains in wrong/unexpected state after WDT reboot
* **Reproducibility:** 10/10
* **Timing / Reset Reason:** int_wdt

#### Preconditions

Device is in active state

#### Steps to Reproduce

1. Turn Actuator ON
2. Execute hang
3. Execute status after reboot
4. Observe Actuator state

#### Expected Result

Actuator resets to OFF after WDT reboot

#### Actual Result

Actuator remains ON after WDT reboot

#### Evidence

[recovery_bug_02.mp4](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/recovery_bug_02.mp4)

---

## 6. Python Automation Project

### Environment

* **MCU:** ESP32 DevKit v1
* **Platform:** Wokwi Simulator (`rfc2217://localhost:4000`)
* **Framework:** Pytest, Python 3.14

### Summary Bug Log

| Bug ID     | Title                                                                                 | Category                 | Severity     | Reproducibility | Evidence                                                                                                                 |
| ---------- | ------------------------------------------------------------------------------------- | ------------------------ | ------------ | --------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **BUG-01** | PWM upper boundary value `100` rejected with `ERROR` instead of `OK`                  | Firmware / Requirement   | Medium       | 5/5             | [python_bug_01.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/python_bug_01.png) |
| **BUG-02** | State leakage on `RESET`: PWM remains at `255` instead of resetting to safe state `0` | Firmware Defect          | **Critical** | 5/5             | [python_bug_02.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/python_bug_02.png) |
| **BUG-03** | Temperature response JSON truncated mid-stream causing `JSONDecodeError`              | Communication / Firmware | **Critical** | 5/5             | [python_bug_03.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/python_bug_03.png) |
| **BUG-04** | Device fails to respond to `PING` command causing `TimeoutError`                      | Requirement / Firmware   | Medium       | 5/5             | [python_bug_04.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/python_bug_04.png) |

### Detailed Bug Reports (Critical)

#### BUG-02: State leakage on `RESET`: PWM remains at `255` instead of resetting to safe state `0`

* **Bug ID:** BUG-02
* **Title:** State leakage on `RESET`: PWM remains at `255` instead of resetting to safe state `0`
* **Category:** Firmware Defect
* **Severity:** **Critical** 🔴
* **Test File:** `automation/tests/test_relay.py` (`test_reset_restores_safe_state`)
* **Reproducibility:** 5/5

#### Preconditions

1. Simulation is running and serial connection via `rfc2217://localhost:4000` is established.

#### Steps to Reproduce

1. Turn the LED on by sending command `SET LED ON`.
2. Send command `RESET`.
3. Query the device status via command `STATUS`.
4. Check the `pwm` field value in the JSON response.

#### Expected Result

Command `RESET` restores all peripherals to a safe default state where `pwm == 0`.

#### Actual Result

The PWM subsystem retains an active value of `255` (`AssertionError: assert 255 == 0`).

#### Evidence

[python_bug_02.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/python_bug_02.png)

#### BUG-03: Temperature response JSON truncated mid-stream causing `JSONDecodeError`

* **Bug ID:** BUG-03
* **Title:** Temperature response JSON truncated mid-stream causing `JSONDecodeError`
* **Category:** Communication / Firmware Defect
* **Severity:** **Critical** 🔴
* **Test File:** `automation/tests/test_sensor.py` (`test_temperature_is_valid_json`)
* **Reproducibility:** 5/5

#### Preconditions

1. Simulation is running and serial connection via `rfc2217://localhost:4000` is established.

#### Steps to Reproduce

1. Send command `GET TEMP` to the device.
2. Read the raw serial line response (`ser.readline()`).
3. Attempt to parse the received payload using `json.loads()`.

#### Expected Result

Device transmits a complete, valid JSON object (e.g., `{"status":"OK","temperature":24.5}`).

#### Actual Result

The string is cut off before the closing brace (`'{"status":"OK","temperature":24.5'`), raising `JSONDecodeError`.

#### Evidence

[python_bug_03.png](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence/python_bug_03.png)

---

## 7. IoT Networking Project

### Environment

* **MCU:** ESP32 DevKit v1
* **Platform:** Wokwi Simulator / IoT Network Module

### Summary Bug Log

| Bug ID | Title                                                                          | Requirement | Severity | Reproducibility | Evidence                                                                                                                                 |
| ------ | ------------------------------------------------------------------------------ | ----------- | -------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **01** | Reconnect Storm & Immediate Retry Burst Failure                                | R2          | Critical | 5/5             | [iot_network_log_bug_01.txt](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/network-stress/iot_network_log_bug_01.txt)     |
| **02** | Offline Buffer Capacity Boundary Bypass & Element Drop Failure                 | R4          | Critical | 5/5             | [iot_network_log_bug_02_2.txt](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/network-stress/iot_network_log_bug_02_2.txt) |
| **03** | Message Duplication During Buffer Flush Upon Network Reconnection              | R6          | High     | 5/5             | [iot_network_log_bug_03_2.txt](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/network-stress/iot_network_log_bug_03_2.txt) |
| **04** | Dynamic Memory Leak and Heap Degradation Under Stress During Connection Outage | R7          | High     | 5/5             | [iot_network_log_bug_04_2.txt](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/network-stress/iot_network_log_bug_04_2.txt) |

### Detailed Bug Reports (Critical & High)

#### 01: Reconnect Storm & Immediate Retry Burst Failure

* **Bug ID:** 01
* **Title:** Reconnect Storm & Immediate Retry Burst Failure
* **Severity:** **Critical** 🔴
* **Requirement:** R2
* **Reproducibility:** 5/5

#### Preconditions

1. System is up and running in CONNECTED state.

#### Steps to Reproduce

1. Execute `NET DOWN` command to simulate connection loss.
2. Observe logs for backoff and retry behavior.

#### Expected Result

System should use an exponential backoff algorithm to prevent broker flooding.

#### Actual Result

`reconnect_attempts` happen rapidly with `backoff_ms=50`.

#### Evidence

[iot_network_log_bug_01.txt](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/network-stress/iot_network_log_bug_01.txt)

---

#### 02: Offline Buffer Capacity Boundary Bypass & Element Drop Failure

* **Bug ID:** 02
* **Title:** Offline Buffer Capacity Boundary Bypass & Element Drop Failure
* **Severity:** **Critical** 🔴
* **Requirement:** R4
* **Reproducibility:** 5/5

#### Preconditions

1. System is up and running in CONNECTED state.

#### Steps to Reproduce

1. Execute `NET DOWN` command to simulate connection loss.
2. Execute `SEND` more times than defined buffer capacity (10 or more times).
3. Execute `BUFFER` and `STATUS` during outage to check messages and dropped count.

#### Expected Result

Upon receiving the 9th and subsequent payloads, the `DROP_OLDEST` policy deletes the oldest items, setting `dropped: 2` while maintaining `buffer: 8`.

#### Actual Result

Buffer count exceeds max capacity (`buffer: 10`, `capacity: 8`) while dropped remains `0`.

#### Evidence

[iot_network_log_bug_02_2.txt](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/network-stress/iot_network_log_bug_02_2.txt)

---

#### 03: Message Duplication During Buffer Flush Upon Network Reconnection

* **Bug ID:** 03
* **Title:** Message Duplication During Buffer Flush Upon Network Reconnection
* **Severity:** **High** 🟠
* **Requirement:** R6
* **Reproducibility:** 5/5

#### Preconditions

1. System has messages in offline buffer.

#### Steps to Reproduce

1. Re-establish connection using `NET UP`.
2. Observe logs during `buffer_flush`.

#### Expected Result

Each buffered message is published to the broker exactly once.

#### Actual Result

Each message ID is published twice (duplicated IDs: `id-1`, `id-2`, `id-3`, `id-4`, `id-5`, `id-6`), and duplicate counters double the actual message count.

#### Evidence

[iot_network_log_bug_03_2.txt](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/network-stress/iot_network_log_bug_03_2.txt)

---

#### 04: Dynamic Memory Leak and Heap Degradation Under Stress During Connection Outage

* **Bug ID:** 04
* **Title:** Dynamic Memory Leak and Heap Degradation Under Stress During Connection Outage
* **Severity:** **High** 🟠
* **Requirement:** R7
* **Reproducibility:** 5/5

#### Preconditions

1. Device is running, state is CONNECTED, the broker is active, initial heap is recorded.

#### Steps to Reproduce

1. Execute `NET DOWN` followed by `STRESS 100` to simulate message burst during outage.
2. Execute `STATUS` and check heap state during connection outage.
3. Execute `NET UP` and wait until the buffer flush completes.
4. Execute `STATUS` and check heap state after `NET UP`.
5. Repeat the steps a few times and check/log heap every time.

#### Expected Result

Heap remains stable after buffer flushes, no memory drops are observed.

#### Actual Result

Free heap drops irreversibly, despite buffer flush after every `NET UP`.

* Initial heap: `350868`
* Heap during 1-st net down: `342868`
* Heap after 1-st net up: `342612`
* Heap during 2-nd net down: `334612`
* Heap after 2-nd net up: `334612`
* Heap during 3-rd net down: `326612`
* Heap after 3-rd net up: `326612`

#### Evidence

[iot_network_log_bug_04_2.txt](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/network-stress/iot_network_log_bug_04_2.txt)
