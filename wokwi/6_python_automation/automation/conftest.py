import os
import pytest
from device import Device


@pytest.fixture
def device():

  port = os.getenv("DEVICE_PORT")
  if not port:
    pytest.skip(
        "Set DEVICE_PORT, e.g. COM5, /dev/ttyUSB0 or rfc2217://localhost:4000"
        " (Wokwi)"
    )


  dev = Device(port, timeout=1.0)

  try:

    res_led = dev.command("SET LED OFF")
    assert (
        res_led.get("status") == "OK"
    ), f"Не вдалося вимкнути LED перед тестом: {res_led}"

    res_pwm = dev.command("SET PWM 0")
    assert (
        res_pwm.get("status") == "OK"
    ), f"Не вдалося обнулити PWM перед тестом: {res_pwm}"


    status = dev.command("STATUS")
    assert status.get("status") == "OK"
    assert status.get("led") is False, (
        f"Стан протікає: LED залишився увімкненим ({status})"
    )
    assert status.get("pwm") == 0, f"Стан протікає: PWM не обнулився ({status})"

    yield dev

  finally:

    try:
      dev.command("SET LED OFF")
      dev.command("SET PWM 0")
    except Exception:
      pass
    dev.close()
