# Master Test Plan — ESP32 Firmware Quality

## 1. Document Purpose

This Master Test Plan establishes the formal quality assurance, verification, and risk-based validation strategy for the ESP32 DevKit v1 IoT controller firmware. It supports the formal release decision by validating 7 core functional modules (Smart Gate controller, debouncing, UART CLI, I2C MPU6050 sensor, system recovery/WDT, Python automation, and IoT networking) under simulated fault and stress conditions without initial source code access (black-box approach).

## 2. System Overview

- **Hardware:** ESP32 DevKit v1, DHT22 sensor, MPU6050 sensor (0x68), peripheral relays, LEDs, push buttons, limit switches.
- **Firmware:** Custom C/C++ ESP32 firmware (`homework_buggy`), including CLI parser, finite state machines, Watchdog (WDT), offline queuing buffers, and NVS persistence.
- **Interfaces:** UART Serial CLI (115200 baud), I2C (GPIO21 / GPIO22), GPIO lines, Wi-Fi / MQTT networking stack.
- **External Dependencies:** Wokwi Simulator, MQTT Broker, Python 3.14 PyTest framework, PulseView logic analyzer.
- **Critical Data / Actuators:** Relay state, PWM levels, system configuration parameters (`speed`, `timeout`), unique message counters, free heap memory.

## 3. Quality Objectives

- Ensure strict functional compliance with state transition requirements and boundary limits.
- Guarantee memory safety, preventing buffer overflows and handling long-run heap degradation.
- Validate robust error recovery upon protocol communication faults (I2C NACK) and system hangs (WDT).
- Verify reliable offline message buffering (`DROP_OLDEST` policy) and network auto-reconnection behavior.

## 4. Scope

Black-box functional, boundary, fault-injection, and stress testing across all 7 embedded modules, supported by automated PyTest regression scripts and logic analyzer trace evidence.

## 5. Out of Scope

- Physical electrical power consumption spikes, RF interference, and deep-sleep current draw measurements on real hardware.
- Security penetration testing, OTA firmware updates, and SPI bus protocol verification.

## 6. Assumptions / Constraints

- Testing is primarily conducted within the Wokwi Simulator environment and via virtual serial bridges (`rfc2217://localhost:4000`).
- Simulation timing may not reflect exact real-world network propagation delays or physical button debounce physics.
- The firmware builds evaluated are intentionally buggy (`BUGGY`) to simulate real-world defect injection.

## 7. Quality Risks

| Risk ID | Risk                                                             | Impact | Probability | Priority     | Mitigation / Test                                   |
| ------- | ---------------------------------------------------------------- | ------ | ----------- | ------------ | --------------------------------------------------- |
| **R01** | Uncontrolled motor state transitions & direct reversal           | High   | High        | **Critical** | Functional state transition test (Smart Gate)       |
| **R02** | Noise pulse creates duplicate actions during critical operations | High   | High        | **Critical** | Debounce pulse injection test                       |
| **R03** | UART input buffer overflow on long strings causing reboots       | High   | High        | **Critical** | CLI boundary and buffer overflow testing            |
| **R04** | I2C bus lock upon NACK without automatic recovery                | High   | High        | **Critical** | I2C fault injection & PulseView trace analysis      |
| **R05** | Unsafe actuator states (relay/PWM) retained after WDT/reset      | High   | High        | **Critical** | Watchdog trigger and post-reset state verification  |
| **R06** | Network reconnection storm bypassing exponential backoff         | Medium | High        | **High**     | Network down/up retry timing observation            |
| **R07** | Offline buffer capacity bypass & silent data duplication/loss    | High   | High        | **Critical** | Buffer capacity overflow & reconnection flush tests |
| **R08** | Progressive heap degradation (memory leak) during stress         | High   | High        | **Critical** | Repeated stress cycles with heap tracking           |

## 8. Test Levels

- **Component / Firmware Function:** Individual command parsers, sensor readouts, and boundary values.
- **Interface / Protocol:** UART CLI input validation, I2C transaction framing and NACK handling.
- **System:** Smart Gate state machine sequences, button debouncing, and status reporting.
- **Recovery / Fault Injection:** Watchdog (WDT) triggers, deep sleep, and power-loss save interruptions.
- **Network:** MQTT connection drops, offline buffering, and stress message bursts.
- **Regression:** Automated PyTest execution suite over virtual serial ports.

## 9. Test Types

| Type                    | Example from the practices                                                                                                                                                                            |
|:----------------------- |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Functional**          | Valid CLI commands (`help`, `status`), Smart Gate state transitions (`OPEN`, `CLOSE`, `STOP`, limit switches), LED toggling (`SET LED ON/OFF`)                                                        |
| **Boundary / negative** | `speed` `0..255` (invalid `-1`, `256`), `timeout` `1..60` (invalid `0`, `61`), input length `41` vs overflow (`>41` chars), PWM `0..100` (invalid `-1`, `101`, `999`), special characters (`%:?)(\*`) |
| **Protocol**            | I2C ACK/NACK (`0x68` vs `0x69` fault), JSON payload structure validation (`GET TEMP` truncation)                                                                                                      |
| **Reliability**         | Button debounce under short noise pulses and noise during critical operations (`RAW` vs `Logical` events), `PING` response time (`<= 1.0s`)                                                           |
| **Recovery**            | Watchdog reset after `hang` (`int_wdt`), deep sleep wake-up (`sleep N`), I2C `FAULT ON -> OFF` recovery, network reconnect (`NET DOWN -> NET UP`)                                                     |
| **Persistence**         | `save` -> `sleep` -> `status` (pre-sleep values check); `powerloss` during `save` (counter corruption check)                                                                                          |
| **Network stress**      | `SEND` burst exceeding buffer capacity (`10` messages vs capacity `8`, `DROP_OLDEST` policy), message deduplication on flush, `STRESS 100`                                                            |
| **Memory stability**    | Heap tracking across `STRESS 100` ×5 iterations (`350868` -> `310600` bytes, ~8 KB leak per iteration)                                                                                                |
| **Automation**          | 8 PyTest automated tests (`test_boundaries`, `test_relay`, `test_sensor`, `test_status`, `test_timeout`): 2 passed, 6 failed                                                                          |

## 10. Test Environment

| Environment         | Purpose                                           | Tools                                              |
| ------------------- | ------------------------------------------------- | -------------------------------------------------- |
| **Wokwi**           | Firmware and system simulation                    | ESP32 simulator, virtual serial bridge (`rfc2217`) |
| **Logic analysis**  | Protocol evidence & transaction verification      | PulseView / logic analyzer (`.vcd` capture)        |
| **Host automation** | Automated regression test execution               | Python 3.14 / PyTest                               |
| **Real hardware**   | Electrical and physical validation (future phase) | Haven't used physical devices so far               |

## 11. Entry Criteria

- Simulation environment (`Wokwi`) successfully initialized and running the target firmware build.
- Requirements and expected behaviour are documented
- Critical interfaces are observable: UART/CLI, I2C, network states, logs.

## 12. Exit Criteria

- 100% execution of planned test scenarios across all 7 project modules.
- All critical and high-priority risks covered by verifiable evidence.
- Defect reports logged with exact reproduction steps, logs, and evidence links.

## 13. Regression Strategy

- Run the core PyTest automated test suite (`pytest pytest/tests/ -v`) after any firmware change.
- Perform smoke tests verifying boot sequence, `help`, `status`, sensor readout, BVA and network connection status.

## 14. Evidence Strategy

- **Logs:** Terminal execution logs and error outputs ([bug-reports](https://github.com/ramenw420/embedded-qa-portfolio/blob/main/bug-reports/bug_reports.md)), [network-stress](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/network-stress)).
- **Traces:** Logic analyzer captures and protocol dumps ([PulseView i2c_trace.vcd](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/network-stress)).
- **Screenshots:** Visual proof of state failures and simulation states ([evidence](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports/evidence)).
- **Reports:** Detailed execution matrices and bug logs ([Test Reports](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/test-reports), [Bug Reports](https://github.com/ramenw420/embedded-qa-portfolio/tree/main/bug-reports)).

## 15. Defect Management

- **Severity:** Classified into Critical, High, Medium, and Low based on system stability and data integrity impact.
- **Reproducibility:** Tested across multiple iterations (e.g., 5/5 or 10/10 consistency).
- **Evidence:** Must include matching log output, trace file, or screenshot reference.
- **Retest:** Mandatory verification cycle following developer fixes.

## 16. Residual Risks

- Wokwi simulation does not capture real physical contact bounce characteristics, RF noise, or hardware power supply fluctuations.
- Long-term memory exhaustion thresholds are extrapolated from simulation stress cycles and require physical soak testing.

## 17. Release Recommendation

### **NO-GO (Not Recommended for Release)**

**Argumentation:** The firmware violates critical reliability requirements, exhibiting unhandled buffer overflows causing reboots (UART CLI), permanent bus lockups on I2C NACK errors, state leakage on resets (PWM remaining at 255), failure of offline buffer capacity limits (`DROP_OLDEST`), message duplication upon reconnection, and irreversible heap memory leaks during stress. Deployment without remediation presents severe stability risks.