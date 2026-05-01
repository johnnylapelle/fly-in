from .connection import Connection
from .exception import ConfigFileError, ParameterError
from .zone import Zone


class MapLoader():
    def __init__(self, file: str):
        self._file = file
        self._nb_drones: int = 0
        self._is_start_hub = False
        self._is_end_hub = False
        self._is_hub = False
        self._is_connection = False
        self._zones: dict[str, Zone] = {}
        self._connections: dict[str, Connection] = {}
        self._valid_zone_type = [
            "normal", "blocked", "restricted", "priority"]
        self._valid_metadatas_co = [
            "max_link_capacity"]
        self._valid_metadatas_hub = [
            "color", "zone", "max_drones"]
        self._lineno = 0

    @property
    def zones(self) -> dict[str, Zone]:
        return self._zones

    @property
    def connections(self) -> dict[str, Connection]:
        return self._connections

    @property
    def nb_drones(self) -> int:
        return self._nb_drones

    def parse(self) -> None:
        self._parse_args()
        self._parse_map()
        self._validate()
        self._lineno = 0

        for zone in self._zones.values():
            print(zone)
            print()

        for co in self._connections.values():
            print(co)
            print()

    def _parse_args(self):
        pass

    def _parse_map(self):
        with open(self._file, 'r') as f:
            for line in f:
                self._lineno += 1

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
                    if self._is_start_hub is True:
                        raise ConfigFileError(
                            f"line {self._lineno} - "
                            "start_hub found multiple times.")
                    self._is_start_hub = True
                    self._parse_hub(line, 'start_hub')

                # get the hub data
                elif line.startswith('hub:'):
                    self._is_hub = True
                    self._parse_hub(line, 'hub')

                # get the end_hub data
                elif line.startswith('end_hub'):
                    if self._is_end_hub is True:
                        raise ConfigFileError(
                            f"line {self._lineno} - "
                            "end_hub found multiple times.")
                    self._is_end_hub = True
                    self._parse_hub(line, 'end_hub')

                # get the connections data
                elif line.startswith("connection:"):
                    self._parse_connection(line)
                    self._is_connection = True

                # raise error if any other line
                else:
                    raise ConfigFileError(
                        f"line {self._lineno} -"
                        f" Line - '{line}' not valid.")

    def _parse_nb_drones(self, line: str) -> None:
        # check if the nb_drones is the very first line
        if (self._is_start_hub or self._is_end_hub
           or self._is_hub or self._is_connection):
            raise ConfigFileError(
                f"line {self._lineno} - "
                "The first line must define the number "
                "of drones using:\n"
                "   nb_drones: <number>")

        if self.nb_drones != 0:
            raise ConfigFileError(
                f"line {self._lineno} - "
                "nb_drones found multiple times."
            )

        # get and validate the nb_drones
        try:
            nb_drones_data = line.split(':')
            nb_drones = nb_drones_data[1].strip()
            self._nb_drones = int(nb_drones)
        except Exception:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"(nb_drones) '{nb_drones}' is not a valid int.")
        if self._nb_drones <= 0:
            raise ConfigFileError(
                f"line {self._lineno} - "
                "(nb_drones) must be a valid positive int."
            )

    def _parse_hub(self, line: str, hub_type: str) -> None:
        # check if arg len is >= 5
        hub_data = line.split()
        if (len(hub_data) < 4 or
           (len(hub_data) >= 5
           and not hub_data[4].startswith('['))):
            raise ConfigFileError(
                f"line {self._lineno} - "
                "Zone definition must be:\n"
                "   hub: <name> <x> <y> [metadata]")

        # get the name and validate it
        hub_name = hub_data[1]
        if '-' in hub_name:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"Invalid name '{hub_name}'.\n"
                "The connection syntax forbids dashes in zone names.")

        # get the x
        try:
            hub_x = hub_data[2]
            hub_x_int = int(hub_x)
        except ValueError:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"(hub_type 'x' value) '{hub_x}' is not a valid int.")

        # get the y
        try:
            hub_y = hub_data[3]
            hub_y_int = int(hub_y)
        except ValueError:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"(hub_type 'y' value) '{hub_y}' is not a valid int.")

        # get the metadatas
        hub_metadatas = self._parse_metadatas(
            line, self._valid_metadatas_hub)

        # get the known metadata
        try:
            zone_type = hub_metadatas.get('zone', 'normal')
            color = hub_metadatas.get('color', None)
            max_drones_str = hub_metadatas.get('max_drones', 1)
            max_drones_int = int(max_drones_str)
        except ValueError:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"(max_drones) '{max_drones_str}' is not a valid int.")

        # validate the zone_type
        if zone_type not in self._valid_zone_type:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"Zone type '{zone_type}' invalid.")

        if max_drones_int <= 0:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"(max_drones) is not a valid positive int.")

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
        if zone.name in self._zones:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"Zone '{zone.name}' already exists.")
        else:
            self._zones[zone.name] = zone

    def _parse_connection(self, line: str):
        # get the datas and check the format
        if not self._is_start_hub or not self._is_end_hub:
            raise ConfigFileError(
                f"line {self._lineno} - "
                "All hubs must be defined before connections.")

        connection_datas = line.split()
        if len(connection_datas) < 2 or len(connection_datas) > 3:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"Connections must follow the format:\n"
                "   connection: <zone1>-<zone2>")

        if (len(connection_datas) == 3
           and not connection_datas[2].startswith('[')):
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"Connections must follow the format:\n"
                "   connection: <zone1>-<zone2>")

        # get the zone's names
        connection_zones = connection_datas[1].split('-')
        if len(connection_zones) != 2:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"Connections must follow the format:\n"
                "   connection: <zone1>-<zone2>")

        # check if the zones name exists
        try:
            zone_a = self._zones[connection_zones[0]]
        except KeyError:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"Zone '{connection_zones[0]}' doesn't exists.")
        try:
            zone_b = self._zones[connection_zones[1]]
        except KeyError:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"Zone '{connection_zones[1]}' doesn't exists.")

        # check if no duplicate
        if zone_a == zone_b:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"Zone '{zone_a.name}' and '{zone_b.name}' "
                "must be two different zones."
            )

        # get the connection metadatas
        co_metadatas = self._parse_metadatas(
            line, self._valid_metadatas_co)

        # get the known metadata
        try:
            max_link_cap_str = co_metadatas.get('max_link_capacity', 1)
            max_link_cap_int = int(max_link_cap_str)
        except ValueError:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"(max_drones) '{max_link_cap_str}' is not a valid int.")
        if max_link_cap_int <= 0:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"(max_link_capacity) must be a valid positive int."
            )

        # add and create a connection instance
        key = '-'.join(sorted([zone_a.name, zone_b.name]))
        if key in self._connections:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"Connection '{key}' appear more than once.\n"
                "The same connection must not appear more than once "
                "(e.g., a-b and b-a are considered duplicates).")
        else:
            self._connections[key] = Connection(
                zone_a=zone_a,
                zone_b=zone_b,
                max_capacity=max_link_cap_int
            )

    def _parse_metadatas(self, line,
                         valid_keys: list[str]) -> dict[str, str]:
        # parse the metadatas and check if they are valid
        metadatas: dict[str, str] = {}
        try:
            if '[' in line:
                metadatas_str = line.split('[')[1].strip(']')
                metadatas_list = metadatas_str.split()
                for data in metadatas_list:
                    current_key_value = data.split('=')
                    key = current_key_value[0]
                    value = current_key_value[1]
                    if key not in valid_keys:
                        raise ConfigFileError(
                            f"line {self._lineno} - "
                            f"Invalid metadata '{key}'.")
                    metadatas[key] = value
        except IndexError:
            raise ConfigFileError(
                f"line {self._lineno} - "
                f"Invalid line '{line}'."
            )

        return metadatas

    def _validate(self):
        # check if there is one start_hub/end_hub
        if self._is_start_hub is False:
            raise ConfigFileError(
                "start_hub parameter is mandatory:\n"
                "   start_hub: <name> <x> <y> [metadatas]")
        if self._is_end_hub is False:
            raise ConfigFileError(
                "end_hub parameter is mandatory:\n"
                "   end_hub: <name> <x> <y> [metadatas]")
        if self._nb_drones == 0:
            raise ConfigFileError(
                "nb_drones parameter is mandatory:\n"
                "   nb_drones: <number>")
