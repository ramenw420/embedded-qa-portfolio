# Embedded QA Portfolio Case Study:

## 1. Project Overview

A comprehensive QA portfolio case study focused on verification, validation, and stress-testing of firmware for the **ESP32 DevKit v1** microcontrolled ecosystem. The project spans 7 core modules: Smart Gate control, hardware debouncing, UART CLI, I2C protocol analysis (MPU6050 sensor), system recovery & watchdog mechanisms, Python/PyTest automation, and IoT networking with offline buffering.

---

## 2. My QA Goal

To evaluate system stability, boundary limits, noise resilience, fault recovery mechanisms, and compliance with core reliability requirements using black-box and grey-box testing methodologies (without initial source code inspection), backed by automated regression scripts.

---

## 3. System Architecture & Tech Stack

| Component                    | Specification / Technology                                                |
|:---------------------------- |:------------------------------------------------------------------------- |
| **Target MCU**               | ESP32 DevKit v1                                                           |
| **Simulation Platform**      | Wokwi Simulator, PulseView (`i2c_trace.vcd`), `rfc2217://localhost:4000`  |
| **Languages & Frameworks**   | Python 3.14, PyTest, C/C++ (Firmware)                                     |
| **Interfaces & Peripherals** | UART Serial CLI, I2C (GPIO21/GPIO22), GPIO (Buttons, Relays, LEDs, DHT22) |

---

## 4. Critical Engineering Risks

| Risk ID     | Module       | Risk Description                                       | Potential Impact                                      |
|:----------- |:------------ |:------------------------------------------------------ |:----------------------------------------------------- |
| **RISK-01** | Smart Gate   | Uncontrolled motor state transitions & direct reversal | Mechanical/electrical driver damage                   |
| **RISK-02** | Debounce     | Noise vulnerability during critical operations         | Multiplied false triggers & unauthorized actions      |
| **RISK-03** | UART CLI     | Input buffer overflow on long strings                  | Kernel panic, complete system crash and reboot        |
| **RISK-04** | I2C Protocol | Bus lock upon NACK without retry logic                 | Total freeze of the main firmware loop                |
| **RISK-05** | Recovery     | State leakage and unsafe actuator states post-WDT      | Unintended physical output activation                 |
| **RISK-06** | IoT Network  | Reconnect storms, buffer bypass, & heap leaks          | Broker flooding, data corruption, & memory exhaustion |

---

## 5. Test Strategy & Coverage

| Test Level                | Scope & Method                                                     | Environment                               |
|:------------------------- |:------------------------------------------------------------------ |:----------------------------------------- |
| **Unit & Integration**    | Automated test suites (`pytest`) for CLI, boundaries, and sensors  | Python + Wokwi Virtual Serial (`rfc2217`) |
| **Black-box System**      | Functional and boundary value testing across all 7 modules         | Wokwi Simulator UI                        |
| **Fault Injection**       | Simulating I2C NACK, power loss, network drop, and buffer overflow | CLI Commands & Wokwi Fault Switches       |
| **Bus & Signal Analysis** | Capturing and decoding physical protocol traces                    | PulseView (`.vcd` logic analyzer)         |

---

## 6. Key Test Scenarios

1. **Smart Gate Transitions:** Validating state sequences (`CLOSED -> OPENING -> OPEN -> CLOSING`) and handling 10-second timeout errors.
2. **Noise Immunity:** Injecting short pulses and high-frequency noise during button operations to catch action multiplication bugs.
3. **CLI Boundary Check:** Feeding out-of-range parameters (`set speed 256`, `set timeout 0`) and extreme string lengths.
4. **I2C Fault Injection:** Switching fault state (`FAULT ON`) during MPU6050 polling to test error handling and recovery.
5. **WDT & Deep Sleep Recovery:** Triggering system hangs and power loss during saves to verify reset reasons and state restoration.
6. **IoT Outage & Buffering:** Simulating `NET DOWN`, overflowing the capacity-8 offline buffer, and testing data deduplication upon `NET UP`.

---

## 7. Test Automation (Python / PyTest)

* **Framework:** PyTest with parameterized boundary testing.
* **Covered Modules (`pytest/tests/`):**
  * `test_boundaries.py`: PWM upper/lower boundaries validation.
  * `test_relay.py`: LED toggling and safe state verification on `RESET`.
  * `test_sensor.py`: JSON response integrity and range checks (`GET TEMP`).
  * `test_status.py`: Telemetry structure validation and `PING` execution.
  * `test_timeout.py`: Performance benchmarking (`max_response_time <= 1.0s`).

---

## 8. Fault Injection & Recovery Results

| Injection Type                     | Target Module   | Observed Behavior                         | Recovery Status             |
|:---------------------------------- |:--------------- |:----------------------------------------- |:--------------------------- |
| **I2C Address Shift (NACK)**       | I2C Protocol    | Main loop freezes completely              | **FAIL** (No recovery path) |
| **Long String Input (>41 chars)**  | UART CLI        | Buffer overflow triggers reboot           | **FAIL** (System crash)     |
| **Network Loss + Stress Burst**    | IoT Networking  | Heap decreases irreversibly across cycles | **FAIL** (Memory leak)      |
| **Power Interruption During Save** | System Recovery | Counter value changed after reboot        | **FAIL** (Data corruption)  |

---

## 9. Key Findings & Critical Defects

| Bug ID       | Project      | Defect Summary                                                          | Severity     |
|:------------ |:------------ |:----------------------------------------------------------------------- |:------------ |
| **BUG-03**   | Smart Gate   | Direct reversal between OPENING and CLOSING allowed without STOP        | **Critical** |
| **BUG-02_1** | Debounce     | Noise during critical operation causes multiple false actions           | **Critical** |
| **BUG-05**   | UART CLI     | Buffer overflow on input strings >41 chars causes system crash/reboot   | **Critical** |
| **BUG-01_1** | I2C Protocol | Firmware freezes upon first NACK with error `-1` and no retry           | **Highest**  |
| **BUG-02_2** | Python/Relay | State leakage on `RESET`: PWM remains at `255` instead of `0`           | **Critical** |
| **BUG-01_1** | IoT Network  | Reconnect burst uses fixed 50ms interval instead of exponential backoff | **Critical** |
| **BUG-04**   | IoT Network  | Progressive heap degradation (memory leak) under stress test            | **High**     |

---

## 10. Release & Quality Conclusion

> **Decision: NO-GO (Not Recommended for Release)**

**Justification:** The firmware exhibits severe stability and safety defects. Critical vulnerabilities include unhandled buffer overflows causing reboots, permanent bus lockups on I2C communication errors, state leakage on resets, memory leaks during network stress, and missing offline buffer capacity limits (`DROP_OLDEST` failure).

---

## 11. Recommendations for Next Iteration

1. Implement safe memory copy routines (e.g., `snprintf`) to prevent UART CLI buffer overflows.
2. Add bus timeout and automatic recovery/retry handlers for I2C master requests.
3. Fix peripheral state clearing routines to ensure all actuators reset safely upon `RESET` commands.
4. Refactor dynamic memory allocation inside the IoT queuing layer to eliminate heap fragmentation and leaks.
5. Introduce hardware-in-the-loop (HIL) verification for physical button debounce and power management on real ESP32 hardware.
