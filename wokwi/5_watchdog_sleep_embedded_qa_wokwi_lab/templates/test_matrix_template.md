# Test Matrix Template

| ID | Risk | Test / Scenario | Precondition | Action | Expected | Evidence | Result |
|---|---|---|---|---|---|---|---|
| T01 | Invalid sensor data | Sensor unavailable | Device ACTIVE | Disconnect DHT | Explicit sensor error | Serial log | |
| T02 | Button bounce | Duplicate event | Device ACTIVE | Press button 20 times | Exactly 20 events | Counter + video | |
| T03 | Sleep timing | Wrong state timing | Device ACTIVE | `sleep 5` | Wake in 4.25–5.75 s | Timestamped log | |
| T04 | Firmware hang | Device unavailable | Device ACTIVE | `hang` | WDT reset ≲5 s | Reset log | |
| T05 | Unsafe recovery | Unsafe actuator state | Relay ON | `hang` | After WDT relay OFF | Video + status | |
| T06 | Interrupted save | Corrupted persistent state | Known state | `powerloss` | Old or new valid state only | Before/after status | |
| T07 | Recovery stability | Boot loop | Device ACTIVE | hang/recovery ×10 | Returns ACTIVE each time | Serial log | |
