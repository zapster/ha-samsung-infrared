# Samsung Infrared for Home Assistant

Custom Home Assistant integration for Samsung TV IR control using the
first-class `infrared` entity platform introduced in Home Assistant 2026.4.

This integration uses a custom Samsung IR protocol encoder and code set
instead of the upstream `infrared-protocols` library, to support TVs that
require a different protocol variant.

## Installation

Use HACS as a custom integration repository, or copy
`custom_components/samsung_infrared` into your Home Assistant
`custom_components` directory.

Restart Home Assistant, then add **Samsung Infrared** from **Settings >
Devices & services > Add integration**.

Looking for Pioneer receiver support? See [ha-pioneer-infrared](https://github.com/zapster/ha-pioneer-infrared).

## Development

Local checks that do not require a Home Assistant checkout:

```bash
python -m compileall custom_components tests
```

The test suite expects Home Assistant 2026.4 or newer and the
`infrared-protocols` package.
