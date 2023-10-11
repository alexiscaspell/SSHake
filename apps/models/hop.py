from apps.models.tunnel import Tunnel,InvalidTunnelException
from typing import List, Dict
from enum import Enum
import os
import subprocess
from apps.utils.logger_util import get_logger

class SessionType(Enum):
    password = "password"
    key = "key"
    mixed = "mixed"
    none = "none"

logger = get_logger()

class Hop(object):
    def __init__(self, hop_spec: Dict):
        self.alias = list(hop_spec.keys())[0]

        hopinfo = hop_spec[self.alias]

        self.host = hopinfo['host']
        self.user = hopinfo['user']

        self.port = hopinfo.get('port', None)

        self.password = hopinfo.get('auth', {}).get("password",None)
        self.key = hopinfo.get('auth', {}).get("key",None)

        if self.password is not None and self.key is not None:
            self.type = SessionType.mixed
        else:
            self.type = SessionType.password if self.password is not None else SessionType.key

        self.type = SessionType.none if "auth" not in hopinfo else self.type

        self.tunnels = []

        for t in hopinfo["tunnels"]:
            try:
                self.tunnels.append(Tunnel(t))
            except InvalidTunnelException as e:
                logger.warning(e)

        self.next = None
        self.process = None

    def set_next(self, other_hop: 'Hop'):
        if self.next is None:
            self.next = other_hop
        else:
            self.next.set_next(other_hop)

    def get_all_port_mappings(self,mapped=True) -> List[str]:
        return self.get_port_mappings(mapped=mapped) + (self.next.get_all_port_mappings(mapped=mapped) if self.next is not None else [])

    def get_port_mappings(self,mapped=True) -> List[str]:
        return [tun.mapping if mapped else tun for tun in self.tunnels]

    def get_command(self):
        cmd = "ssh -tfN -o StrictHostKeyChecking=no -o ServerAliveInterval=15 -o ServerAliveCountMax=7 -g"

        if self.type==SessionType.key or self.type==SessionType.mixed:
            cmd+=f" -i {self.key.replace('~', os.path.expanduser('~'))}"

        if self.type==SessionType.password or self.type==SessionType.mixed:
            if os.path.isfile(self.password):
                cmd = f"sshpass -f '{self.password}' " + cmd
            else:
                cmd = f"sshpass -p '{self.password}' " + cmd

        cmd+=f" {self.user}@{self.host}"
        cmd+=f" -p {self.port}" if self.port is not None else ""

        cmd+=" -L "+' -L '.join(self.get_port_mappings())

        if self.next is not None:
            cmd+=" ; sleep 3; "+self.next.get_command()

        return cmd

    def connect(self) -> int:
        command = self.get_command()

        logger.debug(f"Executing command: {command}")

        with open('/tmp/sshtunnel.log', 'a+') as output:
            self.process = subprocess.Popen(command, shell=True, stdout=output,stderr=output, universal_newlines=True)
            logger.debug(f"Command returned: {output.read()}")

        return self.process.pid

    def get_jumps_str(self):
        if self.next is not None:
            return f"{self.alias} --> {self.next.get_jumps_str()}"
        else:
            return f"{self.alias}"

    def end_session(self):
        logger.info(f"Disconnecting from {self.get_jumps_str()}")

        self.process.kill()

    def get_pid(self):
        if self.process is not None:
            return self.process.pid
        return None