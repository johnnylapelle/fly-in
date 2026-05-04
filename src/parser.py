from .zone import Zone
from .connection import Connection
from .drone import Drone
from .exception import ConfigFileError, ParameterError


class Parser():
    def __init__(self, file: str):
        self.file = file
        self.nb_drones: int = 0
        self.is_start_hub = False
        self.is_end_hub = False
        self.is_hub = False
        self.is_connection = False
        self.zones: dict[str, Zone] = {}
        self.connections: dict[str, Connection] = {}
        self.valid_zone_type = [
            "normal", "blocked", "restricted", "priority"
        ]
        self.lineno = 0

    def parse(self) -> None:
        self._parse_args()
        self._parse_map()
        self._validate()

        for zone in self.zones.values():
            print(zone)
            print()

        for co in self.connections.values():
            print(co)
            print()

    def _parse_args(self):
        pass

    def _parse_map(self):
        try:
            with open(self.file, 'r') as f:
                for line in f:
                    self.lineno += 1

                    # get rid of \n and espace
                    line = line.strip()

                    # ignore the comments
                    if line.startswith('#'):
                        continue

                    # ignore empty line
                    if len(line) <= 0:
                        continue

                    # get the nb of drones
                    if line.startswith('nb_drones:'):
                        self._parse_nb_drones(line)

                    # get the start_hub data
                    elif line.startswith('start_hub:'):
                        if self.is_start_hub is True:
                            raise ConfigFileError(
                                f"line {self.lineno} - "
                                "start_hub found multiple times.")
                        self.is_start_hub = True
                        self._parse_hub(line, 'start_hub')

                    # get the hub data
                    elif line.startswith('hub:'):
                        self.is_hub = True
                        self._parse_hub(line, 'hub')

                    # get the end_hub data
                    elif line.startswith('end_hub'):
                        if self.is_end_hub is True:
                            raise ConfigFileError(
                                f"line {self.lineno} - "
                                "end_hub found multiple times")
                        self.is_end_hub = True
                        self._parse_hub(line, 'end_hub')

                    # get the connections data
                    elif line.startswith("connection:"):
                        self._parse_connection(line)
                        self.is_connection = True

                    # raise error if any other line
                    else:
                        raise ConfigFileError(f"line {self.lineno} -"
                                              f" Line - '{line}' not valid.")

        except ConfigFileError as e:
            print(f"ConfigFileError: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def _parse_nb_drones(self, line: str) -> None:
        # get the nb of drones
        if (self.is_start_hub or self.is_end_hub
           or self.is_hub or self.is_connection):
            raise ConfigFileError(
                f"line {self.lineno} - "
                "The first line must define the number "
                "of drones using:\n"
                "   nb_drones: <positive_integer>.")

        try:
            nb_drones_data = line.split(':')
            nb_drones = nb_drones_data[1].strip()
            self.nb_drones = int(nb_drones)
        except Exception:
            raise ConfigFileError(
                f"line {self.lineno} - "
                f"(nb_drones) '{nb_drones}' is not a valid int.")

    def _parse_hub(self, line: str, hub_type: str) -> None:
        # check if arg len is > 4
        hub_data = line.split()
        if len(hub_data) < 4:
            raise ConfigFileError(
                f"line {self.lineno} - "
                "Zone definition must be:\n    hub: <name> <x> <y> [metadata].")

        # get the name and validate it
        hub_name = hub_data[1]
        if '-' in hub_name:
            raise ConfigFileError(
                f"line {self.lineno} - "
                f"Invalid name '{hub_name}'.\n"
                "The connection syntax forbids dashes in zone names.")

        # get the x
        try:
            hub_x = hub_data[2]
            hub_x_int = int(hub_x)
        except Exception:
            raise ConfigFileError(
                f"line {self.lineno} - "
                f"(start_hub 'x' value) '{hub_x}' is not a valid int.")

        # get the y
        try:
            hub_y = hub_data[3]
            hub_y_int = int(hub_y)
        except Exception:
            raise ConfigFileError(
                f"line {self.lineno} - "
                f"(start_hub 'y' value) '{hub_y}' is not a valid int.")

        # get the hub metadatas
        hub_metadatas = self._parse_metadatas(line)

        # get the known metadata
        try:
            zone_type = hub_metadatas.get('zone', 'normal')
            color = hub_metadatas.get('color', None)
            max_drones_str = hub_metadatas.get('max_drones', 1)
            max_drones_int = int(max_drones_str)
        except ValueError:
            raise ConfigFileError(
                f"line {self.lineno} - "
                f"(max_drones) '{max_drones_str}' is not a valid int.")

        if zone_type not in self.valid_zone_type:
            raise ConfigFileError(
                f"line {self.lineno} - "
                f"Zone type '{zone_type}' invalid.")

        # get the type
        is_start = hub_type == 'start_hub'
        is_end = hub_type == 'end_hub'

        # instantiate the zone
        zone = Zone(
            name=hub_name,
            x=hub_x_int,
            y=hub_y_int,
            is_start=is_start,
            is_end=is_end,
            color=color,
            zone_type=zone_type,
            max_drones=max_drones_int
        )

        # add to the dict
        if zone.name in self.zones:
            raise ConfigFileError(
                f"line {self.lineno} - "
                f"Zone '{zone.name}' already exists.")
        self.zones[zone.name] = zone

    def _parse_connection(self, line: str):
        # get the datas
        connection_datas = line.split()

        # get the zone's names
        connection_zones = connection_datas[1].split('-')

        try:
            zone_a = self.zones[connection_zones[0]]
        except KeyError:
            raise ConfigFileError(
                f"line {self.lineno} - "
                f"'{connection_zones[0]}' don't exists.")

        try:
            zone_b = self.zones[connection_zones[1]]
        except KeyError:
            raise ConfigFileError(
                f"line {self.lineno} - "
                f"'{connection_zones[1]}' don't exists.")

        # get the connection metadatas
        co_metadatas = self._parse_metadatas(line)

        # get the known metadata
        try:
            max_link_cap_str = co_metadatas.get('max_link_capacity', 1)
            max_link_cap_int = int(max_link_cap_str)
        except ValueError:
            raise ConfigFileError(
                f"line {self.lineno} - "
                f"(max_drones) '{max_link_cap_str}' is not a valid int.")

        # add and create a connection instance
        key = '-'.join(sorted([zone_a.name, zone_b.name]))
        if key in self.connections:
            raise ConfigFileError(
                f"line {self.lineno} - "
                "The same connection must not appear more than once "
                "(e.g., a-b and b-a are considered duplicates).")
        else:
            self.connections[key] = Connection(
                zone_a=zone_a,
                zone_b=zone_b,
                max_capacity=max_link_cap_int
            )

    def _parse_metadatas(self, line) -> dict[str, str]:
        # get the metadatas
        metadatas: dict[str, str] = {}
        try:
            if '[' in line:
                metadatas_str = line.split('[')[1].strip(']')
                metadatas_list = metadatas_str.split()
                for data in metadatas_list:
                    current_key_value = data.split('=')
                    metadatas[current_key_value[0]] = current_key_value[1]
        except (ValueError, IndexError) as e:
            raise ConfigFileError(e)

        return metadatas

    def _validate(self):
        """
        1. nb_drones > 0
        2. start_hub existe, end_hub existe
        3. les zones dans les connections ont été définies avant
        4. pas de connection en double (a-b et b-a)
        5. les capacity values sont des entiers positifs
        6. les zone types sont valides (normal/blocked/restricted/priority)
        7. un chemin existe entre start et end (pas de graph déconnecté)
        """

        if self.is_start_hub is False:
            raise ConfigFileError(
                f"line {self.lineno} - "
                "start_hub is mandatory.")
        if self.is_end_hub is False:
            raise ConfigFileError(
                f"line {self.lineno} - "
                "end_hub is mandatory.")
        if self.nb_drones <= 0:
            raise ConfigFileError(
                f"line {self.lineno} - "
                "nb_drones muste be greater than 0.")
