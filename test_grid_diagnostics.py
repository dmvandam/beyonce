from tkinter import Grid
from GridDiagnostics import GridDiagnostics
from GridParameters import GridParameters
import pytest
import numpy as np
import os
import shutil

from errors import LoadError

GRID_PARAMETERS = GridParameters(
    min_x = 0, 
    max_x = 1, 
    num_x = 2, 
    min_y = 0, 
    max_y = 1,
    num_y = 2,
    max_rf = 2, 
    num_rf = 1
)

def test_repr() -> None:
    diag = GridDiagnostics(GRID_PARAMETERS)
    repr_string = diag.__repr__()
    assert repr_string == ("\nGrid Diagnostics\n----------------------------"
        "\ndiagnostics saved: 0")


def test_repr_with_diagnostics() -> None:
    diag = GridDiagnostics(GRID_PARAMETERS)
    diag.save_diagnostic(0, 0, np.zeros(1), np.ones(1))
    repr_string = diag.__repr__()
    assert repr_string == ("\nGrid Diagnostics\n----------------------------"
        "\ndiagnostics saved: 1")


def test_str() -> None:
    diag = GridDiagnostics(GRID_PARAMETERS)
    str_string = diag.__str__()
    assert str_string == ("\nGrid Diagnostics\n----------------------------"
        "\ndiagnostics saved: 0")


def test_str_with_diagnostics() -> None:
    diag = GridDiagnostics(GRID_PARAMETERS)
    diag.save_diagnostic(0, 0, np.zeros(1), np.ones(1))
    str_string = diag.__str__()
    assert str_string == ("\nGrid Diagnostics\n----------------------------"
        "\ndiagnostics saved: 1")


def test_generate_key_none() -> None:
    diag = GridDiagnostics(GRID_PARAMETERS)
    key = diag._generate_key(1, 0)
    assert key == "(1, 0)"


def test_generate_key_valid() -> None:
    diag = GridDiagnostics(GRID_PARAMETERS)
    key = diag._generate_key(0, 1)
    assert key == "(0, 1)"


def test_generate_key_y_invalid() -> None:
    diag = GridDiagnostics(GRID_PARAMETERS)
    with pytest.raises(ValueError) as ERROR:
        diag._generate_key(2, 0)

    error_message = "The y argument must be less than or equal to 1.0000"
    assert str(ERROR.value) == error_message


def test_generate_key_x_invalid() -> None:
    diag = GridDiagnostics(GRID_PARAMETERS)
    with pytest.raises(ValueError) as ERROR:
        diag._generate_key(0, 2)

    error_message = "The x argument must be less than or equal to 1.0000"
    assert str(ERROR.value) == error_message


def test_generate_key_both_invalid() -> None:
    diag = GridDiagnostics(GRID_PARAMETERS)
    with pytest.raises(ValueError) as ERROR:
        diag._generate_key(10, 10)

    error_message = "The y argument must be less than or equal to 1.0000"
    assert str(ERROR.value) == error_message


def test_save_diagnostic() -> None:
    fy = np.linspace(0, 1, 3)
    disk_radius = np.ones_like(fy)

    diag = GridDiagnostics(GRID_PARAMETERS)
    diag.save_diagnostic(1, 0, fy, disk_radius)

    key = diag._generate_key(1, 0)
    assert np.all(diag._fy_dict[key] == fy)
    assert np.all(diag._disk_radius_dict[key] == disk_radius)


def test_save_diagnostic_valid_with_allowed() -> None:
    fy = np.linspace(0, 1, 3)
    disk_radius = np.ones_like(fy)

    diag = GridDiagnostics(GRID_PARAMETERS)
    diag.save_diagnostic(1, 0, fy, disk_radius)

    key = diag._generate_key(1, 0)
    assert np.all(diag._fy_dict[key] == fy)
    assert np.all(diag._disk_radius_dict[key] == disk_radius)


def test_get_diagnostic_valid() -> None:
    fy = np.linspace(0, 1, 3)
    disk_radius = np.ones_like(fy)

    diag = GridDiagnostics(GRID_PARAMETERS)
    diag.save_diagnostic(1, 0, fy, disk_radius)

    fy_get, disk_radius_get = diag.get_diagnostic(1, 0)

    assert np.all(fy_get == fy)
    assert np.all(disk_radius_get == disk_radius)

def test_get_diagnostic_invalid() -> None:
    fy = np.linspace(0, 1, 3)
    disk_radius = np.ones_like(fy)

    diag = GridDiagnostics(GRID_PARAMETERS)
    diag.save_diagnostic(1, 0, fy, disk_radius)

    with pytest.raises(KeyError) as ERROR:
        diag.get_diagnostic(0, 1)

    assert str(ERROR.value) == "'(0, 1)'"


def test_save_without_allowed() -> None:
    directory = "test_data"

    fy = np.linspace(0, 1, 3)
    disk_radius = np.ones_like(fy)

    diag = GridDiagnostics(GRID_PARAMETERS)
    diag.save_diagnostic(1, 0, fy, disk_radius)
    diag.save(f"{directory}")

    fy_saved: dict = np.load(f"{directory}/fy_dict.npy", 
        allow_pickle=True).item()
    disk_radius_saved: dict = np.load(f"{directory}/disk_radius_dict.npy", 
        allow_pickle=True).item()

    shutil.rmtree(f"{directory}")

    for key, value in fy_saved.items():
        assert np.all(value == diag._fy_dict[key])

    for key, value, in disk_radius_saved.items():
        assert np.all(value == diag._disk_radius_dict[key])


def test_save_with_allowed() -> None:
    directory = "test_data"
    fy = np.linspace(0, 1, 3)
    disk_radius = np.ones_like(fy)

    diag = GridDiagnostics(GRID_PARAMETERS)
    diag.save_diagnostic(1, 0, fy, disk_radius)
    diag.save(f"{directory}")

    fy_saved: dict = np.load(f"{directory}/fy_dict.npy", 
        allow_pickle=True).item()
    disk_radius_saved: dict = np.load(f"{directory}/disk_radius_dict.npy",
        allow_pickle=True).item()

    shutil.rmtree(f"{directory}")

    for key, value in fy_saved.items():
        assert np.all(value == diag._fy_dict[key])

    for key, value, in disk_radius_saved.items():
        assert np.all(value == diag._disk_radius_dict[key])


def test_extend() -> None:
    diag = GridDiagnostics(GRID_PARAMETERS)
    diag.extend()
    assert diag._extended == True


def test_extended_save() -> None:
    diag = GridDiagnostics(GRID_PARAMETERS)
    diag.extend()

    with pytest.raises(RuntimeError) as ERROR:
        diag.save_diagnostic(0, 0, np.zeros(1), np.ones(1))

    error_message = "diagnostics have been extended and can not be changed"
    assert str(ERROR.value) == error_message


def test_generate_key_extended_invalid() -> None:
    diag = GridDiagnostics(GRID_PARAMETERS)
    diag.save_diagnostic(0, 0, np.zeros(1), np.ones(1))
    diag.extend()
    
    with pytest.raises(KeyError) as ERROR:
        diag.get_diagnostic(0, 0)
    
    assert str(ERROR.value) == "'(2, 2)'"


def test_generate_key_extended_valid() -> None:
    diag = GridDiagnostics(GRID_PARAMETERS)
    diag.save_diagnostic(1, 1, np.zeros(1), np.ones(1))
    diag.extend()

    key = diag._generate_key(0, 0)
    assert key == "(2, 2)"


def test_load_invalid() -> None:
    directory = "invalid"
    
    with pytest.raises(LoadError) as ERROR:
        GridDiagnostics.load(directory)
    
    error_message = f"failed to load grid diagnostics from {directory}"
    assert str(ERROR.value) == error_message


def test_load_valid() -> None:
    directory = "test_data"
    os.mkdir(directory)
    fy_dict = {"(1, 0)": np.zeros(2)}
    disk_radius_dict = {"(1, 0)": np.ones(2)}
    max_x = 2
    max_y = 3
    max_yx = np.array([max_y, max_x])
    np.save(f"{directory}/fy_dict", fy_dict)
    np.save(f"{directory}/disk_radius_dict", disk_radius_dict)
    np.save(f"{directory}/max_yx", max_yx)
    
    diag = GridDiagnostics.load(directory)
    
    shutil.rmtree(directory)

    for key, value in fy_dict.items():
        assert np.all(value == diag._fy_dict[key])

    for key, value, in disk_radius_dict.items():
        assert np.all(value == diag._disk_radius_dict[key])

    assert np.all(diag._max_x == max_x)
    assert np.all(diag._max_y == max_y)

    
