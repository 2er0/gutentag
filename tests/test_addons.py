import unittest
from pathlib import Path

import numpy as np

from gutenTAG import GutenTAG
from gutenTAG.addons import AddOnProcessContext
from gutenTAG.addons.timeeval import TimeEvalAddOn


class TestAddons(unittest.TestCase):
    def test_timeeval_addon_rmj(self):
        gutentag = GutenTAG.from_yaml(Path("tests/configs/example-config-rmj.yaml"), seed=42)
        gutentag.generate()
        addon = TimeEvalAddOn()
        addon.process(AddOnProcessContext(overview=gutentag._overview, datasets=gutentag._timeseries), gutentag)
        df = addon.df
        self.assertEqual(df["dataset_name"][0], "rmj.unsupervised")
        self.assertEqual(df["test_path"][0], "rmj/test.csv")
        self.assertEqual(df["input_type"][0], "multivariate")
        self.assertEqual(df["length"][0], 1000)
        self.assertEqual(df["dimensions"][0], 2)
        self.assertEqual(df["contamination"][0], 0.02)
        self.assertEqual(df["num_anomalies"][0], 1)
        self.assertEqual(df["min_anomaly_length"][0], 20)
        self.assertEqual(df["median_anomaly_length"][0], 20)
        self.assertEqual(df["max_anomaly_length"][0], 20, 2)
        self.assertEqual(df["train_type"][0], "unsupervised")
        self.assertAlmostEqual(df["mean"][0], -0.06, 2)
        self.assertAlmostEqual(df["stddev"][0], 0.02, 2)
        self.assertTrue(np.isnan(df["trend"][0]))
        self.assertEqual(df["period_size"][0], 20)

    def test_timeeval_addon_sine(self):
        gutentag = GutenTAG.from_yaml(Path("tests/configs/example-config-ecg.yaml"), seed=42)
        gutentag.generate()
        addon = TimeEvalAddOn()
        addon.process(AddOnProcessContext(overview=gutentag._overview, datasets=gutentag._timeseries), gutentag)
        df = addon.df
        self.assertEqual(df["dataset_name"][0], "ecg.unsupervised")
        self.assertEqual(df["test_path"][0], "ecg/test.csv")
        self.assertEqual(df["input_type"][0], "univariate")
        self.assertEqual(df["length"][0], 1000)
        self.assertEqual(df["dimensions"][0], 1)
        self.assertEqual(df["contamination"][0], 0.04)
        self.assertEqual(df["num_anomalies"][0], 1)
        self.assertEqual(df["min_anomaly_length"][0], 40)
        self.assertEqual(df["median_anomaly_length"][0], 40)
        self.assertEqual(df["max_anomaly_length"][0], 40, 2)
        self.assertEqual(df["train_type"][0], "unsupervised")
        self.assertAlmostEqual(df["mean"][0], 0.51, 2)
        self.assertAlmostEqual(df["stddev"][0], 0.00, 2)
        self.assertTrue(np.isnan(df["trend"][0]))
        self.assertEqual(df["period_size"][0], 10)

    def test_timeeval_addon_without_period(self):
        gutentag = GutenTAG.from_yaml(Path("tests/configs/example-config-rw.yaml"))
        gutentag.generate()
        addon = TimeEvalAddOn()
        addon.process(AddOnProcessContext(overview=gutentag._overview, datasets=gutentag._timeseries), gutentag)
        df = addon.df
        self.assertTrue(np.isnan(df["period_size"][0]))
