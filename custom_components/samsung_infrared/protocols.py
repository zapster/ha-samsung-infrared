"""Samsung IR protocol encoder."""

from __future__ import annotations

from typing import override

from infrared_protocols.commands import Command

SAMSUNG_MODULATION = 38000
SAMSUNG_HEADER_HIGH_US = 4500
SAMSUNG_HEADER_LOW_US = 4500
SAMSUNG_BIT_HIGH_US = 560
SAMSUNG_BIT_ONE_LOW_US = 1690
SAMSUNG_BIT_ZERO_LOW_US = 560
SAMSUNG_FOOTER_HIGH_US = 560
SAMSUNG_FOOTER_LOW_US = 560

DEFAULT_REPEAT_TIMES = 1
DEFAULT_REPEAT_WAIT_US = 10000


def _append_repeats(
    timings: list[int], frame: list[int], repeat_count: int, repeat_wait_us: int,
) -> None:
    for repeat_index in range(repeat_count + 1):
        current_frame = list(frame)
        if repeat_index < repeat_count:
            if current_frame[-1] < 0:
                current_frame[-1] -= repeat_wait_us
            else:
                current_frame.append(-repeat_wait_us)
        timings.extend(current_frame)


class SamsungCommand(Command):
    """Samsung IR command matching ESPHome's transmit_samsung encoder."""

    def __init__(
        self,
        *,
        data: int,
        nbits: int = 32,
        modulation: int = SAMSUNG_MODULATION,
        repeat_count: int = DEFAULT_REPEAT_TIMES - 1,
        repeat_wait_us: int = DEFAULT_REPEAT_WAIT_US,
    ) -> None:
        """Initialize a Samsung IR command."""
        super().__init__(modulation=modulation, repeat_count=repeat_count)
        self.data = data
        self.nbits = nbits
        self.repeat_wait_us = repeat_wait_us

    @override
    def get_raw_timings(self) -> list[int]:
        frame: list[int] = [SAMSUNG_HEADER_HIGH_US, -SAMSUNG_HEADER_LOW_US]

        for bit in range(self.nbits, 0, -1):
            low_us = (
                SAMSUNG_BIT_ONE_LOW_US
                if (self.data >> (bit - 1)) & 1
                else SAMSUNG_BIT_ZERO_LOW_US
            )
            frame.extend([SAMSUNG_BIT_HIGH_US, -low_us])

        frame.extend([SAMSUNG_FOOTER_HIGH_US, -SAMSUNG_FOOTER_LOW_US])

        timings: list[int] = []
        _append_repeats(timings, frame, self.repeat_count, self.repeat_wait_us)
        return timings
