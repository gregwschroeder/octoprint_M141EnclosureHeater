# OctoPrint-M141EnclosureHeater

This plugin listens for the M141 G-code command. When it detects an M141 command, it extracts the temperature from the S parameter and sends an HTTP POST with the payload:

```json
{
  "setpoint": <temperature>,
  "HeaterArmed": true
}
