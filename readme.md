# Embedded and Hardware QA Portfolio — Embedded Systems Case Studies

## What this repository demonstrates

This repository demonstrates end-to-end quality assurance and robustness validation for embedded systems (ESP32-based platforms). It focuses on identifying critical firmware edge cases—such as unhandled bus faults, buffer overflows, memory leaks during network stress, and state machine race conditions—through automated PyTest suites, hardware simulation via Wokwi, logic analyzer signal capture, and systematic fault injection.

## System

The portfolio covers seven distinct embedded system environments and architectures:

- **Smart Gate & Debounce Controllers:** Finite state machines and physical interrupt noise filtering.
- **UART CLI & I2C Peripherals:** Command-line robustness, boundary limits, and sensor communication (MPU6050).
- **System Recovery & Watchdog (WDT):** Deep sleep management, power loss persistence, and crash recovery.
- **Python Automation Framework:** Automated black-box and integration testing via PyTest over `rfc2217`.
- **IoT Networking Module:** MQTT connection stress, offline buffering (`DROP_OLDEST`), and heap memory leak monitoring.

## Main quality risks

- **System Freezing & Deadlocks:** Complete firmware lockup upon unhandled I2C NACK events without automatic recovery.
- **Memory Corruption & Crashes:** Buffer overflow vulnerabilities on long serial input strings leading to unintended reboots.
- **State Machine Flaws:** Direct state reversals allowed without a mandatory stop phase, and state leakage on system resets (e.g., PWM retained at `255`).
- **Network & Dynamic Memory Degradation:** Reconnect storms bypassing exponential backoff, message duplication upon buffer flushes, and irreversible heap memory leaks during stress execution.

## Test strategy

Testing follows a structured verification approach combining functional requirement validation, boundary value analysis, fault injection, and hardware-in-the-loop simulation:

- Detailed test cases and execution matrices: [test-reports/test_reports.md](test-reports/test_reports.md)
- Defect tracking, reproduction steps, and evidence: [bug-reports/bug_reports.md](bug-reports/bug_reports.md)

## Key evidence

- **I2C Protocol Failure:** Logic analyzer captures and transaction logs showing system freeze upon `0x69` NACK (`pulseview/i2c_trace.vcd`).
- **Buffer Overflow Crash:** Serial execution traces showing device reboot upon receiving inputs exceeding 41 characters (`bug-reports/bug_reports.md`).
- **Heap Degradation Logs:** Step-by-step memory tracking showing progressive heap exhaustion during network stress (`network-stress/`).

## Key findings

- Firmware builds across critical subsystems (Networking, I2C, UART CLI, Watchdog) exhibit severe stability risks.
- Critical vulnerabilities such as unhandled protocol exceptions, incorrect buffer capacity enforcement, and memory leaks directly violate core reliability requirements.
- The system fails to guarantee safe operational states following automated resets or fault recovery cycles.

## Automation

Automated test suites are implemented using **PyTest (Python 3.14)** communicating with the ESP32 simulator via an RFC2217 serial bridge (`rfc2217://localhost:4000`).

- Located in the `pytest/` directory.

- Run tests locally by executing:
  
  ```bash
  pytest pytest/tests/ -v
  ```

## Limitations

- **Simulation Constraints:** Testing relies heavily on Wokwi Simulator environments and virtual serial bridges (`rfc2217`).
- **Hardware Dependencies:** Real-world power consumption, physical button contact bounce characteristics, and exact RF networking fluctuations require verification on physical hardware.

## Conclusion

Based on cumulative test evidence, defect severity, and unmitigated blocking risks (including memory leaks, unhandled protocol freezes, and data corruption during power loss), **current firmware builds are NOT recommended for release**. Mandatory fixes, boundary validation updates, and re-testing cycles must be completed before deployment.