class InvalidTunnelException(Exception):
    pass
class Tunnel(object):
    def __init__(self, mapping):
        m = mapping.split(":")
        self.mapping = mapping

        if len(m)==4:
            self.local_host=m[0]
            self.local_port = m[1]
            self.remote_host = m[2]
            self.remote_port = m[3]

        elif len(m)<=2:
            raise InvalidTunnelException(f"Imposible mapear tunel {m}")
        else:
            self.local_port = m[0]
            self.remote_host = m[1]
            self.remote_port = m[2]
            self.local_host="localhost"

    def __str__(self):
        return f"{self.local_host}:{self.local_port} --> {self.remote_host}:{self.remote_port}"

    def set_local_port(self, new_port):
        self.local_port = new_port
        self.update_mapping()

    def set_remote_host(self, new_host):
        self.remote_host = new_host
        self.update_mapping()

    def get_localhost_mapping(self):
        return f"{self.local_port}:localhost:{self.local_port}"

    def update_mapping(self):
        self.mapping = f"{self.local_host}:{self.local_port}:{self.remote_host}:{self.remote_port}"
