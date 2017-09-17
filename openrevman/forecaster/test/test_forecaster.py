from unittest import TestCase

from openrevman.forecaster.forecaster import Forecaster


class TestForecaster(TestCase):
    def test_solver_simple_od_leg_better(self):
        forecaster = Forecaster()
        forecaster.fit_parameters()
        forecaster.update_parameter()
