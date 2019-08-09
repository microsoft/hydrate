"""Test suite for telemetry.py."""
import pytest

from hydrate.telemetry import Singleton
from hydrate.telemetry import Telemetry
from hydrate.telemetry import get_version
from hydrate.telemetry import timeit_telemetry


class TestTelemetry:
    """Test suite for the Telemetry class."""
    @pytest.mark.parametrize("tst_toggle", [(True), (False)])
    def test_init(self, mocker, tst_toggle):
        # Setup Test
        # Call Function
        tst_tele = Telemetry(tst_toggle)
        # Assert Results
        if tst_toggle:
            assert tst_tele._telemetry_client is not None
            assert tst_tele._telemetry_channel is not None
        else:
            assert tst_tele._telemetry_channel is None
            assert tst_tele._telemetry_client is None
        # Delete Telemetry Instance
        del tst_tele

    test_event_name_1 = "test-event"
    test_event_prop_1 = {"test-prop-key": "test-prop-value"}
    test_event_meas_1 = {"test-meas-key": "test-meas-value"}
    @pytest.mark.parametrize("tst_event_name, tst_event_props, tst_event_meas",
                             [(test_event_name_1, test_event_prop_1, test_event_meas_1)])
    def test_track_event(self, mocker,
                         tst_event_name, tst_event_props, tst_event_meas):
        # Setup Test
        tst_tele = Telemetry(True)
        tst_tele._telemetry_client.track_event = mocker.MagicMock()
        # Call Function
        tst_tele.track_event(tst_event_name, tst_event_props, tst_event_meas)
        # Assert Results
        tst_tele._telemetry_client.track_event.assert_called_with(tst_event_name,
                                                                  tst_event_props,
                                                                  tst_event_meas)
        # Delete Telemetry Instance
        del tst_tele

    test_metric_name = "test-metric"
    test_metric_value = 350
    test_metric_type = "test-type"
    test_metric_count = 100
    test_metric_min = 0
    test_metric_max = 100
    test_metric_std_dev = 10
    test_metric_properties = {"test-prop-key": "test-prop-value"}
    @pytest.mark.parametrize("""tst_name, tst_value, tst_type, tst_count, tst_min,
                                tst_max, tst_std_dev, tst_properties""",
                                [(test_metric_name, test_metric_value, test_metric_type,
                                  test_metric_count, test_metric_min, test_metric_max,
                                  test_metric_std_dev, test_metric_properties)])
    def test_track_metric(self, mocker,
                          tst_name, tst_value, tst_type, tst_count, tst_min, tst_max,
                          tst_std_dev, tst_properties):
        # Setup Test
        tst_tele = Telemetry(True)
        tst_tele._telemetry_client.track_metric = mocker.MagicMock()
        # Call Function
        tst_tele.track_metric(tst_name, tst_value, tst_type, tst_count,
                              tst_min, tst_max, tst_std_dev, tst_properties)
        # Assert Results
        tst_tele._telemetry_client.track_metric.assert_called_with(tst_name, tst_value,
                                                                   tst_type, tst_count,
                                                                   tst_min, tst_max,
                                                                   tst_std_dev,
                                                                   tst_properties)
        # Delete Telemetry Instance
        del tst_tele

    def test_flush(self, mocker):
        # Setup Test
        tst_tele = Telemetry(True)
        tst_tele._telemetry_client.flush = mocker.MagicMock()
        # Call Function
        tst_tele.flush()
        # Assert Results
        tst_tele._telemetry_client.flush.assert_called_once()
        # Delete Telemetry Instance
        del tst_tele

    def test_setup_telemetry_channel(self, mocker):
        # Setup Test
        # Call Function
        # Assert Results
        # Delete Telemetry Instance
        pass

def test_get_version():
    # Setup Test
    # Call Function
    # Assert Results
    pass


def test_timeit_telemetry():
    # Setup Test
    # Call Function
    # Assert Results
    pass