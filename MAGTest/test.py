import paho.mqtt.client as mqtt
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import *
from MAGLabPyLib import MAGDaemon
import logging, traceback
from pathlib import Path

class TEST_CLASS(MAGDaemon):
    @dataclass_json
    @dataclass
    class Config(MAGDaemon.Config):
        secret: str
        loglevel: Optional[str] = None
    def __init__(self):
        long_name = "maglaboratory_daemon_tester"
        cfg_file_name = "test"
        """ the name "logger" is reserved in the parent class for derived use """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG) # just for development
        self.set_config(long_name, cfg_file_name)
        super().__init__(long_name, cfg_file_name)
        self.config_log()
        self.logger.debug("Exiting init function")

    def on_message(self, client, userdata, message):
        if message.topic in self.config.mqtt.data_sources:
            if message.topic.endswith("checkup_req"):
                self.logger.info("Received checkup")
            else:
                try:
                    decoded = message.payload.decode('utf-8')
                    self.logger.debug(decoded)

                except Exception as err:
                    tb = traceback.format_exc()
                    self.logger.warning(f"L{sys._getframe().f_back.f_lineno} Caught exception: {err}\nTraceback:\n{tb}")
        else:
            self.logger.warning("Message not in data sources")


    def main(self):
        self.logger.debug("Calling super main")
        super().main()
        self.logger.info("Starting main loop")
        while not self.exit_evt.is_set():
            self.loop()

        
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test = TEST_CLASS()
    test.main()            
