#!/usr/bin/env python3

import argparse
import os
import signal
import time

import yaml
from yaml import SafeLoader

from apps.models.hop import Hop
from apps.utils.logger_util import get_logger, set_metadata, colored_message, GREEN,bold_message

logger = get_logger()


def load_config(c: str):

    logger.debug(f'Using: {c}')

    with open(c) as f:
        config = yaml.load(f, Loader=SafeLoader)

    return config


def main(args):
    config = load_config(args.config)

    if "logging" in config:
        dir = config.get("logging").get("dir")
        level = config.get("logging").get("level")

        set_metadata(log_directory=dir, log_level=level)

        logger = get_logger(rebuild=True)

    base_hop = None

    for h in config["hops"]:
        hop = Hop(h)
        if base_hop is None:
            base_hop = hop
        else:
            base_hop.set_next(hop)

    base_hop.connect()

    logger.info('Tunneling done:')

    actual_hop = base_hop

    line_length = 70

    while(actual_hop is not None):
        logger.info(colored_message(f"#"*line_length, GREEN))
        logger.info(colored_message("#", GREEN)+" " * int((line_length-2-len(actual_hop.alias))/2) +
                    bold_message(actual_hop.alias.upper())+" " * int((line_length-2-len(actual_hop.alias))/2)+colored_message("#", GREEN))
        logger.info(colored_message(f"#"*line_length, GREEN))

        for pm in actual_hop.get_port_mappings(mapped=False):
            logger.info(pm)

        actual_hop = actual_hop.next

    if config.get("mode", {}).get("background", False):
        time.sleep(config.get("mode", {}).get("timeout", 10))
    else:
        try:
            input("Press ENTER to disconnect")
            print()
        except KeyboardInterrupt:
            print()
            logger.error('Getting out of here!')

    try:
        r = base_hop.end_session()

    except KeyboardInterrupt:
        logger.warning("Hurrying up.")

    logger.info('Disconnected')

    try:
        os.kill(base_hop.get_pid(), signal.SIGKILL)
        logger.warning('Killed off remaining SSH process')
    except ProcessLookupError:
        pass

    logger.info('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config', default='config.yml',
                        help='Configuration file to use')

    main(parser.parse_args())
