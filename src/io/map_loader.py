from ..core.connection import Connection
from ..core.drone import Drone
from ..core.exception import ConfigFileError
from ..core.zone import Zone


class MapLoader():
    """
    Parses a map file and builds the zones, connections, and drones.

    Map files are plain text with one directive per line. Supported
    directives are: nb_drones, start_hub, hub, end_hub, and connection.
    Lines starting with # are treated as comments and ignored.
    """

    def __init__(self) -> None:
        """Initializes an empty MapLoader ready to parse a file."""

        self._nb_drones = 0
        self._is_start_hub = False
        self._is_end_hub = False
        self._is_hub = False
        self._is_connection = False
        self._drones: list[Drone] = []
        self._zones: dict[str, Zone] = {}
        self._connections: dict[str, Connection] = {}
        self._valid_zone_type = [
            "normal", "blocked", "restricted", "priority"]
        self._valid_metadatas_co = [
            "max_link_capacity"]
        self._valid_metadatas_zone = [
            "color", "zone", "max_drones"]
        self._lineno = 0

    @property
    def zones(self) -> dict[str, Zone]:
        """All zones parsed from the last call to parse(), keyed by name."""

        return self._zones

    @property
    def connections(self) -> dict[str, Connection]:
        """All connections parsed from the last call
        to parse(), keyed by key."""

        return self._connections

    @property
    def drones(self) -> list[Drone]:
        """All drones instantiated from the last call to parse()."""

        return self._drones

    @property
    def nb_drones(self) -> int:
        """Number of drones defined in the last parsed map."""

        return self._nb_drones

    @nb_drones.setter
    def nb_drones(self, n: int) -> None:
        self._nb_drones = n

    def parse(self, file: str) -> None:
        """
        Parses a map file and populates zones, connections, and drones.

        Resets internal state before parsing, so calling parse() multiple
        times on the same instance is safe.

        Args:
            file: Path to the map file to parse.
        """

        self._reset()

        self._parse_map(file)
        self._validate()
        self._lineno = 0

    def _parse_map(self, file: str) -> None:
        """
        Parses a map file and populates zones, connections, and drones.

        Resets internal state before parsing, so calling parse() multiple
        times on the same instance is safe.

        Args:
            file: Path to the map file to parse.
        """

        with open(file, 'r') as f:
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
                            f"Line {self._lineno} - "
                            "start_hub found multiple times.")
                    self._is_start_hub = True
                    self._parse_zone(line, 'start_hub')

                # get the hub data
                elif line.startswith('hub:'):
                    self._is_hub = True
                    self._parse_zone(line, 'hub')

                # get the end_hub data
                elif line.startswith('end_hub'):
                    if self._is_end_hub is True:
                        raise ConfigFileError(
                            f"Line {self._lineno} - "
                            "end_hub found multiple times.")
                    self._is_end_hub = True
                    self._parse_zone(line, 'end_hub')

                # get the connections data
                elif line.startswith("connection:"):
                    self._parse_connection(line)
                    self._is_connection = True

                # raise error if any other line
                else:
                    raise ConfigFileError(
                        f"Line {self._lineno} -"
                        f" line - '{line}' not valid.")

    def _parse_nb_drones(self, line: str) -> None:
        """
        Parses the nb_drones directive and instantiates the drones.

        Must be the first directive in the file. Raises if nb_drones
        appears more than once or after any other directive.

        Args:
            line: The raw line containing the nb_drones directive.
        """

        # check if the nb_drones is the very first line
        if (self._is_start_hub or self._is_end_hub
           or self._is_hub or self._is_connection):
            raise ConfigFileError(
                f"Line {self._lineno} - "
                "The first line must define the number "
                "of drones using:\n"
                "   nb_drones: <number>")

        if self.nb_drones != 0:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                "nb_drones found multiple times."
            )

        # get and validate the nb_drones
        try:
            nb_drones_data = line.split(':')
            nb_drones = nb_drones_data[1].strip()
            self._nb_drones = int(nb_drones)
        except Exception:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"(nb_drones) '{nb_drones}' is not a valid int.")
        if self._nb_drones <= 0:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                "(nb_drones) must be a valid positive int.")

        # instantiate the drones
        for i in range(self._nb_drones):
            drone = Drone(i + 1)
            self._drones.append(drone)

    def _parse_zone(self, line: str, hub_type: str) -> None:
        """
        Parses the nb_drones directive and instantiates the drones.

        Must be the first directive in the file. Raises if nb_drones
        appears more than once or after any other directive.

        Args:
            line: The raw line containing the nb_drones directive.
        """

        # check if arg len is >= 5
        zone_data = line.split()
        if (len(zone_data) < 4 or
           (len(zone_data) >= 5
           and not zone_data[4].startswith('['))):
            raise ConfigFileError(
                f"Line {self._lineno} - "
                "Zone definition must be:\n"
                "   hub: <name> <x> <y> [metadata]")

        # get the name and validate it
        zone_name = zone_data[1]
        if '-' in zone_name:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"Invalid name '{zone_name}'.\n"
                "The connection syntax forbids dashes in zone names.")

        # get the x
        try:
            zone_x = zone_data[2]
            zone_x_int = int(zone_x)
            # if hub_x_int < 0:
            #     raise ValueError
        except ValueError:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"({hub_type} 'x' value) '{zone_x}' is not a valid int.")

        # get the y
        try:
            zone_y = zone_data[3]
            zone_y_int = int(zone_y)
            # if hub_y_int < 0:
            #     raise ValueError
        except ValueError:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"({hub_type} 'y' value) '{zone_y}' is not a valid int.")

        # get the metadatas
        zone_metadatas = self._parse_metadatas(
            line, self._valid_metadatas_zone)

        # get the known metadata
        try:
            zone_type = zone_metadatas.get('zone', 'normal')
            color = zone_metadatas.get('color', None)
            max_drones_str = zone_metadatas.get('max_drones', 1)
            max_drones_int = int(max_drones_str)
        except ValueError:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"(max_drones) '{max_drones_str}' is not a valid int.")

        # validate the zone_type
        if zone_type not in self._valid_zone_type:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"Zone type '{zone_type}' invalid.")

        if max_drones_int <= 0:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"(max_drones) is not a valid positive int.")

        # get the type
        is_start = hub_type == 'start_hub'
        is_end = hub_type == 'end_hub'

        if is_start or is_end:
            if zone_type == "blocked":
                raise ConfigFileError(
                    f"Line {self._lineno} - "
                    f"Start and end zones cannot be blocked.")

        for zone in self._zones.values():
            if zone.x == zone_x_int and zone.y == zone_y_int:
                raise ConfigFileError(
                    f"Line {self._lineno} - "
                    f"Zone '{zone.name} and {zone_name}' "
                    "cannot be at the same position.")

        # instantiate the zone
        zone = Zone(
            name=zone_name,
            x=zone_x_int,
            y=zone_y_int,
            is_start=is_start,
            is_end=is_end,
            color=color,
            zone_type=zone_type,
            max_drones=max_drones_int
        )

        # add to the dict
        if zone.name in self._zones:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"Zone '{zone.name}' already exists.")
        else:
            self._zones[zone.name] = zone

    def _parse_connection(self, line: str) -> None:
        """
        Parses the nb_drones directive and instantiates the drones.

        Must be the first directive in the file. Raises if nb_drones
        appears more than once or after any other directive.

        Args:
            line: The raw line containing the nb_drones directive.

        Raises:
            ConfigFileError: If the value is missing, not a positive
                integer, or appears out of order.
        """

        # get the datas and check the format
        if not self._is_start_hub or not self._is_end_hub:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                "Start and end hubs must be defined before connections.")

        connection_datas = line.split()
        if len(connection_datas) < 2 or len(connection_datas) > 3:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"Connections must follow the format:\n"
                "   connection: <zone1>-<zone2>")

        if (len(connection_datas) == 3
           and not connection_datas[2].startswith('[')):
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"Connections must follow the format:\n"
                "   connection: <zone1>-<zone2>")

        # get the zone's names
        connection_zones = connection_datas[1].split('-')
        if len(connection_zones) != 2:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"Connections must follow the format:\n"
                "   connection: <zone1>-<zone2>")

        # check if the zones name exists
        try:
            zone_a = self._zones[connection_zones[0]]
        except KeyError:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"Zone '{connection_zones[0]}' doesn't exists.")
        try:
            zone_b = self._zones[connection_zones[1]]
        except KeyError:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"Zone '{connection_zones[1]}' doesn't exists.")

        # check if no duplicate
        if zone_a == zone_b:
            raise ConfigFileError(
                f"Line {self._lineno} - "
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
                f"Line {self._lineno} - "
                f"(max_drones) '{max_link_cap_str}' is not a valid int.")
        if max_link_cap_int <= 0:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"(max_link_capacity) must be a valid positive int."
            )

        # add and create a connection instance
        key = '-'.join(sorted([zone_a.name, zone_b.name]))
        if key in self._connections:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"Connection '{key}' appear more than once.\n"
                "The same connection must not appear more than once "
                "(e.g., a-b and b-a are considered duplicates).")
        else:
            self._connections[key] = Connection(
                key=key,
                zone_a=zone_a,
                zone_b=zone_b,
                max_capacity=max_link_cap_int,
                is_restricted=(zone_a.type == "restricted"
                               or zone_b.type == "restricted")
            )

    def _parse_metadatas(self, line: str,
                         valid_keys: list[str]) -> dict[str, str]:
        """
        Extracts key=value metadata from the bracketed section of a line.

        Args:
            line: The full raw line, optionally containing [...] metadata.
            valid_keys: The list of accepted metadata keys.

        Returns:
            A dictionary of metadata key-value pairs. Empty if no
            metadata block is present.
        """

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
                            f"Line {self._lineno} - "
                            f"Invalid metadata '{key}'.")
                    metadatas[key] = value
        except IndexError:
            raise ConfigFileError(
                f"Line {self._lineno} - "
                f"Invalid line '{line}'."
            )

        return metadatas

    def _validate(self) -> None:
        """
        Extracts key=value metadata from the bracketed section of a line.

        Args:
            line: The full raw line, optionally containing [...] metadata.
            valid_keys: The list of accepted metadata keys.

        Returns:
            A dictionary of metadata key-value pairs. Empty if no
            metadata block is present.
        """

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

    def _reset(self) -> None:
        """Resets all internal state in preparation for a new parse."""

        self._nb_drones = 0
        self._is_start_hub = False
        self._is_end_hub = False
        self._is_hub = False
        self._is_connection = False
        self._drones = []
        self._zones = {}
        self._connections = {}
        self._lineno = 0
