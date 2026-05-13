"""
Minimal pymadng example: load the PSB sequence, run twiss, retrieve the result.

Run from the MADdocs repository root:
    python verified_examples/pymadng_minimal.py
"""
import sys

from pymadng import MAD

with MAD() as mad:
    mad.send("""
    local beam, twiss in MAD
    MADX:load("doc_sequences/psb3_saved.seq",
              "doc_sequences/psb3_saved.mad")
    local psb3 in MADX
    psb3.beam = beam { particle="proton", energy=1.098 }
    local tw = twiss { sequence=psb3 }
    py:send(tw)
    """)
    tw = mad.recv("tw")

assert tw is not None, "did not receive twiss table"
assert hasattr(tw, "q1"),     "missing q1"
assert hasattr(tw, "beta11"), "missing beta11 column"

print(f"q1={tw.q1:.6f}  q2={tw.q2:.6f}")
print(f"nrows={len(tw.s)}")
