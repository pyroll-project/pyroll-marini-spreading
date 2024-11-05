import logging
import webbrowser
from pathlib import Path

from pyroll.core import Profile, Roll, ThreeRollPass, Transport, RoundGroove, CircularOvalGroove, PassSequence


def test_solve3(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")

    import pyroll.interface_friction
    import pyroll.marini_spreading

    in_profile = Profile.round(
        diameter=55e-3,
        temperature=1200 + 273.15,
        strain=0,
        material=["C45", "steel"],
        flow_stress=100e6,
        density=7.5e3,
        thermal_capacity=690,
    )

    sequence = PassSequence([
        ThreeRollPass(
            label="Oval I",
            roll=Roll(
                groove=CircularOvalGroove(
                    depth=8e-3,
                    r1=6e-3,
                    r2=40e-3,
                    pad_angle=30
                ),
                nominal_radius=160e-3,
                rotational_frequency=1
            ),
            gap=2e-3,
            coulomb_friction_coefficient=0.4,
        ),
        Transport(
            label="I => II",
            duration=1
        ),
        ThreeRollPass(
            label="Round II",
            roll=Roll(
                groove=RoundGroove(
                    r1=3e-3,
                    r2=25e-3,
                    depth=11e-3,
                    pad_angle=30
                ),
                nominal_radius=160e-3,
                rotational_frequency=1
            ),
            gap=2e-3,
            coulomb_friction_coefficient=0.4,
        ),
    ])

    try:
        sequence.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)

    try:
        import pyroll.report

        report = pyroll.report.report(sequence)

        report_file = tmp_path / "report.html"
        report_file.write_text(report, encoding="utf-8")
        print(report_file)
        webbrowser.open(report_file.as_uri())

    except ImportError:
        pass
