# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
import requests

class M141EnclosureHeaterPlugin(octoprint.plugin.StartupPlugin,
                                  octoprint.plugin.SettingsPlugin,
                                  octoprint.plugin.TemplatePlugin):

    def process_gcode(self, comm, line):
        stripped = line.strip()
        if stripped.startswith("M141"):
            self._logger.info("M141 command detected: %s", stripped)
            try:
                # Default: extract the temperature from the S parameter
                setpoint = None
                parts = stripped.split()
                for part in parts:
                    if part.startswith("S"):
                        try:
                            setpoint = float(part[1:])
                        except ValueError:
                            self._logger.error("Invalid temperature value in M141 command: %s", part)
                        break

                if setpoint is None:
                    self._logger.warn("M141 detected but no valid S parameter found; skipping API call.")
                else:
                    # Build the payload: include both the extracted temperature and HeaterArmed flag.
                    payload = {
                        "setpoint": int(setpoint),  # or use float(setpoint) if desired
                        "HeaterArmed": True
                    }
                    # Get API URL from settings; defaults to our endpoint.
                    api_url = self._settings.get(["api_url"], "http://fileserver5.localnet:1880/api/v1/enclosureheater/setparams")
                    self._logger.info("Sending API request to %s with payload: %s", api_url, payload)
                    response = requests.post(api_url, json=payload, timeout=5)
                    self._logger.info("API response: %s %s", response.status_code, response.text)
            except Exception as e:
                self._logger.error("Error processing M141 command: %s", e)
        return line

    ##-- SettingsPlugin mixin: provide default settings.
    def get_settings_defaults(self):
        return {
            "api_url": "http://fileserver5.localnet:1880/api/v1/enclosureheater/setparams"
        }

    ##-- TemplatePlugin mixin: expose settings UI.
    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    ##-- StartupPlugin mixin: log plugin startup.
    def on_after_startup(self):
        self._logger.info("M141 Enclosure Heater Plugin started")

    ##-- Software Update Information (optional)
    def get_update_information(self):
        return {
            "m141enclosureheater": {
                "displayName": "M141 Enclosure Heater Plugin",
                "displayVersion": self._plugin_version,
                "type": "github_release",
                "user": "your_github_username",      # Replace with your GitHub username
                "repo": "OctoPrint-M141EnclosureHeater",  # Replace with your repository name
                "current": self._plugin_version,
                "pip": "https://github.com/your_github_username/OctoPrint-M141EnclosureHeater/archive/{target_version}.zip"
            }
        }

__plugin_name__ = "M141 Enclosure Heater Plugin"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = M141EnclosureHeaterPlugin()

__plugin_hooks__ = {
    "octoprint.comm.protocol.gcode.process": __plugin_implementation__.process_gcode
}
