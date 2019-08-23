"""Contains the AppInsights Telemetry collection.

This module is intended to be used as a singleton.
"""
import os
import functools
from applicationinsights import TelemetryClient
from timeit import default_timer
from weakref import WeakValueDictionary


MAIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
APP_INSIGHTS_KEY = 'a4f5caaa-ba76-4759-af36-7ff1ba52d0de'


class Singleton(type):
    """Singleton metaclass.

    All classes affected by this metaclass have the property that only one instance
    is created for each set of arguments passed to the class constructor.
    """

    _instances = WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        """Override __call__ magic function."""
        if cls not in cls._instances:
            # This variable declaration is required to force a
            # strong reference on the instance.
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Telemetry(metaclass=Singleton):
    """Singleton class that handles telemetry sending to AppInsights."""

    def __init__(self, toggle):
        """Initialize Telemetry instance."""
        self._toggle = toggle
        if self._toggle:
            self._telemetry_client = TelemetryClient(APP_INSIGHTS_KEY)
            self._telemetry_channel = self._setup_telemetry_channel()
            print("Telemetry enabled.")
        else:
            self._telemetry_client = None
            self._telemetry_channel = None
            print("Telemetry disabled.")

    def track_event(self, name, properties=None, measurements=None):
        """Track a telemetry event."""
        try:
            self._telemetry_client.track_event(name, properties, measurements)
        except AttributeError:
            print(f"Telemetry Disabled: Event Name: {name}")
            print(f"properties: {properties}")
            print(f"measurements: {measurements}")

    def track_metric(self, name, value, type=None, count=None, min=None, max=None,
                     std_dev=None, properties=None):
        """Track a telemetry metric."""
        try:
            self._telemetry_client.track_metric(name, value, type, count, min, max,
                                                std_dev, properties)
        except AttributeError:
            print(f"Telemetry Disabled: Metric Name: {name}")
            print(f"value: {value}")
            if type:
                print(f"type: {type}")
            if count:
                print(f"count: {count}")
            if min:
                print(f"min: {min}")
            if max:
                print(f"max: {max}")
            if std_dev:
                print(f"std_dev: {std_dev}")
            if properties:
                print(f"properties: {properties}")

    def flush(self):
        """Flush the telemetry client info to AppInsights."""
        try:
            self._telemetry_client.flush()
        except AttributeError:
            pass

    def _setup_telemetry_channel(self):
        """Create telemetry_channel object.

        Instantiates a telemetry channel that collects unhandled exceptions.

        Return:
            telemetry_channel

        """
        from applicationinsights.exceptions import enable
        from applicationinsights import channel

        # set up channel with context
        telemetry_channel = channel.TelemetryChannel()
        telemetry_channel.context.application.ver = get_version()
        # set up exception capture
        telemetry_channel.context.properties['capture'] = 'exceptions'
        enable(APP_INSIGHTS_KEY, telemetry_channel=telemetry_channel)

        return telemetry_channel


def get_version():
    """Read and return the version of Hydrate."""
    with open(os.path.join(MAIN_DIRECTORY, 'VERSION')) as version_file:
        version = version_file.read().strip()
    return version


def timeit_telemetry(func):
    """Time and send telemetry decorator.

    Uses timeit.default_timer(), measured values are based on wall time.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = default_timer()
        result = func(*args, **kwargs)
        runtime = default_timer() - start_time
        TELEMETRY = Telemetry(None)
        TELEMETRY.track_metric(f"func:{func.__name__} runtime in seconds",
                               runtime)
        return result
    return wrapper
