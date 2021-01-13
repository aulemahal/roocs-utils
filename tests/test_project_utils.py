import os

import pytest
import xarray as xr

from ._common import TESTS_HOME
from roocs_utils.project_utils import DatasetMapper
from roocs_utils.project_utils import derive_dset
from roocs_utils.project_utils import dset_to_filepaths
from roocs_utils.project_utils import get_project_base_dir
from roocs_utils.project_utils import get_project_name
from roocs_utils.project_utils import switch_dset


def test_get_project_name():
    dset = "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    project = get_project_name(dset)
    assert project == "cmip5"

    dset = "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc"
    project = get_project_name(dset)
    assert project == "cmip5"

    dset = "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc"
    project = get_project_name(dset)
    assert project == "cmip5"

    dset = "CMIP6.CMIP.NCAR.CESM2.historical.r1i1p1f1.SImon.siconc.gn.latest"
    project = get_project_name(dset)
    assert project == "cmip6"

    ds = xr.open_mfdataset(
        os.path.join(
            TESTS_HOME,
            "mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical"
            "/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        ),
        use_cftime=True,
        combine="by_coords",
    )
    project = get_project_name(ds)
    assert project == "cmip5"

    ds = xr.open_mfdataset(
        os.path.join(
            TESTS_HOME,
            "mini-esgf-data/test_data/badc/cmip6/data/CMIP6/CMIP/NCAR/CESM2/historical/r1i1p1f1"
            "/SImon/siconc/gn/latest/*.nc",
        ),
        use_cftime=True,
        combine="by_coords",
    )
    project = get_project_name(ds)
    assert project == "cmip6"

    # tests default for cmip6 path is c3s-cmip6
    dset = "/badc/cmip6/data/CMIP6/CMIP/MIROC/MIROC6/historical/r1i1p1f1/SImon/siconc/gn/latest/*.nc"
    project = get_project_name(dset)
    assert project == "c3s-cmip6"


def test_get_project_base_dir():
    cmip5_base_dir = get_project_base_dir("cmip5")
    assert cmip5_base_dir == "/badc/cmip5/data/cmip5"

    c3s_cordex_base_dir = get_project_base_dir("c3s-cordex")
    assert c3s_cordex_base_dir == "/gws/nopw/j04/cp4cds1_vol1/data/c3s-cordex"

    with pytest.raises(Exception) as exc:
        get_project_base_dir("test")
        assert exc.value == "The project supplied is not known."


class TestDatasetMapper:
    dset = "CMIP6.CMIP.NCAR.CESM2.historical.r1i1p1f1.SImon.siconc.gn.latest"
    dm = DatasetMapper(dset)

    def test_raw(self):
        assert (
            self.dm.raw
            == "CMIP6.CMIP.NCAR.CESM2.historical.r1i1p1f1.SImon.siconc.gn.latest"
        )

    def test_data_path(self):
        assert (
            self.dm.data_path
            == "/badc/cmip6/data/CMIP6/CMIP/NCAR/CESM2/historical/r1i1p1f1/SImon/siconc/gn/latest"
        )

    def test_ds_id(self):
        assert (
            self.dm.ds_id
            == "CMIP6.CMIP.NCAR.CESM2.historical.r1i1p1f1.SImon.siconc.gn.latest"
        )

    def test_base_dir(self):
        assert self.dm.base_dir == "/badc/cmip6/data/CMIP6"

    def test_files(self):
        assert self.dm.files == [
            "/badc/cmip6/data/CMIP6/CMIP/NCAR/CESM2/historical/r1i1p1f1/SImon/siconc/gn/latest"
            "/siconc_SImon_CESM2_historical_r1i1p1f1_gn_185001-201412.nc"
        ]


def test_get_filepaths():
    dset = "c3s-cmip6.CMIP.MIROC.MIROC6.historical.r1i1p1f1.SImon.siconc.gn.latest"

    files = dset_to_filepaths(dset)
    assert files == [
        "/badc/cmip6/data/CMIP6/CMIP/MIROC/MIROC6/historical/r1i1p1f1/SImon/siconc"
        "/gn/latest/siconc_SImon_MIROC6_historical_r1i1p1f1_gn_185001-194912.nc",
        "/badc/cmip6/data/CMIP6/CMIP/MIROC/MIROC6/historical/r1i1p1f1/SImon/siconc"
        "/gn/latest/siconc_SImon_MIROC6_historical_r1i1p1f1_gn_195001-201412.nc",
    ]

    dset = "c3s-cmip6.CMIP.MIROC.MIROC6.historical.r1i1p1f1.SImon.siconc.gn.latest"

    files_force = dset_to_filepaths(dset, force=True)
    assert files_force == [
        "/badc/cmip6/data/CMIP6/CMIP/MIROC/MIROC6/historical/r1i1p1f1/SImon/siconc"
        "/gn/latest/siconc_SImon_MIROC6_historical_r1i1p1f1_gn_185001-194912.nc",
        "/badc/cmip6/data/CMIP6/CMIP/MIROC/MIROC6/historical/r1i1p1f1/SImon/siconc"
        "/gn/latest/siconc_SImon_MIROC6_historical_r1i1p1f1_gn_195001-201412.nc",
    ]

    dset = "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc"

    files = dset_to_filepaths(dset)
    assert (
        "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon"
        "/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_217412-219911.nc"
        in files
    )

    dset = "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc"

    files_force = dset_to_filepaths(dset, force=True)
    assert (
        "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon"
        "/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_217412-219911.nc"
        in files_force
    )


def test_derive_dset():

    dset = "c3s-cmip6.CMIP.MIROC.MIROC6.historical.r1i1p1f1.SImon.siconc.gn.latest"
    ds_id = derive_dset(dset)

    assert (
        ds_id
        == "/badc/cmip6/data/CMIP6/CMIP/MIROC/MIROC6/historical/r1i1p1f1/SImon/siconc/gn/latest"
    )

    dset = "cmip5.output1.ICHEC.EC-EARTH.historical.day.atmos.day.r1i1p1.tas.v20131231"
    ds_id = derive_dset(dset)

    assert (
        ds_id
        == "/badc/cmip5/data/cmip5/output1/ICHEC/EC-EARTH/historical/day/atmos/day/r1i1p1/tas/v20131231"
    )


def test_switch_dset():

    dset = "/badc/cmip6/data/CMIP6/CMIP/MIROC/MIROC6/historical/r1i1p1f1/SImon/siconc/gn/latest/*.nc"
    ds_id = switch_dset(dset)

    assert (
        ds_id
        == "c3s-cmip6.CMIP.MIROC.MIROC6.historical.r1i1p1f1.SImon.siconc.gn.latest"
    )


def test_unknown_fpath_force():
    dset = "/tmp/tmpxi6d78ng/subset_tttaum9d/rlds_Amon_IPSL-CM6A-LR_historical_r1i1p1f1_gr_19850116-20141216.nc"

    dm_force = DatasetMapper(dset, force=True)

    assert dm_force.files == [
        "/tmp/tmpxi6d78ng/subset_tttaum9d/"
        "rlds_Amon_IPSL-CM6A-LR_historical_r1i1p1f1_gr_19850116-20141216.nc"
    ]
    assert dm_force.data_path == "/tmp/tmpxi6d78ng/subset_tttaum9d"
    assert dm_force.ds_id is None

    dm = DatasetMapper(dset)

    assert dm.files == []
    assert dm.data_path is None
    assert dm.ds_id is None

    files = dset_to_filepaths(dset, force=True)
    assert files == [
        "/tmp/tmpxi6d78ng/subset_tttaum9d/"
        "rlds_Amon_IPSL-CM6A-LR_historical_r1i1p1f1_gr_19850116-20141216.nc"
    ]
