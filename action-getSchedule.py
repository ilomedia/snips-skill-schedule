#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"


class SnipsConfigParser(configparser.ConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.read_file(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()


def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)

    if intentMessage.asr_confidence < float(conf['global']['confidence_threshold']):
        hermes.publish_end_session(intentMessage.session_id)
    else:
        action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):

    sentence = "ce matin, promenade au marché et a 17 heure, cours de pilate sur la plage"

    hermes.publish_end_session(intentMessage.session_id, sentence)


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("duch:getSchedule", subscribe_intent_callback).start()
