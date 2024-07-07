import pytest
from mase_components.synth_runner import run_synth


@pytest.mark.vivado
def test_synth_float_arithmetic():
    run_synth("float_arithmetic")


if __name__ == "__main__":
    test_synth_float_arithmetic()
