Parametric Optics, Derivatives, and RDTs
========================================

For many advanced MAD-NG workflows, :literal:`twiss` is not used only to
produce a standard optics table. It is also used as a derivative engine.

This is a major practical reason to use MAD-NG. In practice, users rely on:

* :literal:`damap` to introduce parameter dependence
* :literal:`X0` to pass that DA state into :literal:`twiss`
* :literal:`trkopt` to request derivative-aware optics columns
* :literal:`trkrdt` to request resonance driving terms

The examples on this page were working for MAD-NG version
:literal:`1.1.13_P`. Matching runnable scripts are kept in this repository.

Why This Matters
----------------

The important distinction is that MAD-NG can propagate optics and normal-form
information with explicit dependence on user parameters. In practice, users do
this to:

* compute derivatives of optics functions with respect to knobs
* build Jacobians for matching and correction
* study chromatic and higher-order sensitivities
* extract resonance driving terms along a machine or a selected range

The basic pattern is:

1. build a DA map carrying the parameters of interest
2. promote selected strengths or knobs into that DA map
3. run :literal:`twiss` with :literal:`X0=<damap>`
4. request the extra outputs explicitly through :literal:`trkopt` or
   :literal:`trkrdt`

Parametric Optics with ``trkopt``
---------------------------------

Use :literal:`trkopt` when you want extra optics columns that carry parametric
dependence.

Minimal validated setup:

.. literalinclude:: ../../verified_examples/trkopt_minimal.mad
   :language: mad

What the pieces mean:

* :literal:`damap` defines the DA state, including the named parameters
* :literal:`pn={...}` names the parameter directions carried by the map
* promoting strengths with :literal:`+ x0.<name>` makes the optics depend on
  those parameters
* :literal:`trkopt` is an explicit request list; only requested quantities are
  added as extra output columns

In this minimal example, the returned columns provide first derivatives of tune
and beta-function quantities with respect to promoted PSB quadrupole strengths
from the loaded saved sequence.

What to look for in the output:

* derivative columns such as :literal:`mu1_10` and :literal:`beta11_10`
* base optics columns alongside those extra derivative columns

The exact suffix convention comes from the requested names. In practice, users
work by requesting the specific columns they need and then reading those
columns back from the output table.

RDTs with ``trkrdt``
--------------------

Use :literal:`trkrdt` when you want resonance driving terms included in the
:literal:`twiss` output.

Minimal validated setup:

.. literalinclude:: ../../verified_examples/trkrdt_minimal.mad
   :language: mad

Key points:

* :literal:`trkrdt` takes an explicit list of requested RDT names
* those names are expected to start with :literal:`f`
* :literal:`saveanf=true` saves the analysed normal form in the protected
  column :literal:`__nf`

In the validated minimal example, the important check is that the requested RDT
columns and the protected :literal:`__nf` column are present in the returned
table.

More advanced workflows, such as reusing :literal:`__nf` for a second ranged
:literal:`twiss` call, should only be documented once they have been verified
locally against a current example.

Practical Guidance
------------------

When documenting or using these workflows, keep the following rules in mind:

* :literal:`trkopt` and :literal:`trkrdt` are opt-in request lists
* :literal:`X0` is the entry point for DA-enabled work
* parameter names should be chosen deliberately because they become the knobs
  carried by the map
* table columns and protected columns such as :literal:`__nf` are part of the
  usable API for advanced workflows
* start with a minimal inline example before scaling up to large imported
  machines

See Also
--------

* :doc:`mad_cmd_twiss`
* :doc:`mad_cmd_track`
* :doc:`mad_mod_diffmap`
* :doc:`mad_mod_diffalg`
