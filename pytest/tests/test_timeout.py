import time
import pytest


def test_ping_response_time(device):
    max_response_time = 1.0

    start_time = time.perf_counter()
    r = device.command("PING")
    elapsed = time.perf_counter() - start_time

    assert r["status"] == "OK"
    assert r["command"] == "PING"
    assert elapsed <= max_response_time, (
        f"Час відповіді на PING ({elapsed:.3f} с) перевищив ліміт {max_response_time} с"
    )
