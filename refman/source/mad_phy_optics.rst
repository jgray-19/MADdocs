.. _ch.phy.optic:

Optics
======

The :literal:`twiss` command computes linear optical functions by propagating a
normalised one-turn map through the lattice.  This page documents the optical
function names, their organisation into modes, and the additional columns
available with :literal:`chrom` and :literal:`coupling`.

Source: :file:`src/madl_gphys.mad` (optical function name tables
:literal:`gphys.ofname`, :literal:`gphys.ofcname`, :literal:`gphys.ofhname`).

Coordinate and mode convention
-------------------------------

MAD-NG uses the Courant-Snyder normal-mode basis.  Three modes are defined:

* **Mode 1** — primarily horizontal (:math:`x, p_x` plane for uncoupled
  machines).
* **Mode 2** — primarily vertical (:math:`y, p_y` plane for uncoupled
  machines).
* **Mode 3** — longitudinal (:math:`t, p_t` plane).

Column names use a double-index suffix: the first digit identifies the mode,
the second digit identifies the coordinate within that mode.  For example,
:literal:`beta11` is the beta function of mode 1, coordinate 1 (:math:`x`).

Standard optics columns
-----------------------

These columns are always present in the :literal:`twiss` mtable.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Column
     - Description
   * - :literal:`beta11`
     - :math:`\beta` function of mode 1 [m].
   * - :literal:`alfa11`
     - :math:`\alpha` function of mode 1.
   * - :literal:`gama11`
     - :math:`\gamma` function of mode 1 [:math:`\mathrm{m}^{-1}`].
   * - :literal:`mu1`
     - Phase advance of mode 1 from the start of the range [rad/2π].
   * - :literal:`dx`
     - Horizontal dispersion function :math:`D_x` [m].
   * - :literal:`dpx`
     - Dispersion of :math:`p_x`.
   * - :literal:`beta22`
     - :math:`\beta` function of mode 2 [m].
   * - :literal:`alfa22`
     - :math:`\alpha` function of mode 2.
   * - :literal:`gama22`
     - :math:`\gamma` function of mode 2 [:math:`\mathrm{m}^{-1}`].
   * - :literal:`mu2`
     - Phase advance of mode 2 [rad/2π].
   * - :literal:`dy`
     - Vertical dispersion function :math:`D_y` [m].
   * - :literal:`dpy`
     - Dispersion of :math:`p_y`.
   * - :literal:`beta33`
     - :math:`\beta` function of mode 3 [m].
   * - :literal:`alfa33`
     - :math:`\alpha` function of mode 3.
   * - :literal:`gama33`
     - :math:`\gamma` function of mode 3 [:math:`\mathrm{m}^{-1}`].
   * - :literal:`mu3`
     - Phase advance of mode 3 [rad/2π].

Summary scalar fields
---------------------

Header fields on the returned mtable, not per-element columns.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Field
     - Description
   * - :literal:`q1`, :literal:`q2`, :literal:`q3`
     - Tunes of modes 1, 2, 3.
   * - :literal:`alfap`
     - Momentum compaction factor :math:`\alpha_p`.
   * - :literal:`etap`
     - Phase slip factor :math:`\eta_p = \alpha_p - 1/\gamma^2`.
   * - :literal:`gammatr`
     - Transition gamma :math:`\gamma_{\text{tr}} = 1/\sqrt{\alpha_p}`.
   * - :literal:`synch_1` … :literal:`synch_8`
     - Synchrotron radiation integrals :math:`I_1` through :math:`I_8`.

Chromatic functions (:literal:`chrom=true`)
--------------------------------------------

When :literal:`chrom=true`, an extra tracking pass at :math:`\delta_p = 10^{-6}`
provides first-order chromatic derivatives by finite difference.

Additional header fields:

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Field
     - Description
   * - :literal:`dq1`, :literal:`dq2`, :literal:`dq3`
     - Chromaticities :math:`\xi = \partial Q / \partial \delta_p`.

Additional columns:

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Column
     - Description
   * - :literal:`dmu1`, :literal:`dmu2`
     - Chromatic derivative of the phase advance.
   * - :literal:`ddx`, :literal:`ddpx`
     - :math:`\partial D_x/\partial\delta_p`, :math:`\partial D_{px}/\partial\delta_p`.
   * - :literal:`ddy`, :literal:`ddpy`
     - :math:`\partial D_y/\partial\delta_p`, :math:`\partial D_{py}/\partial\delta_p`.
   * - :literal:`wx`, :literal:`phix`
     - Chromatic amplitude and phase functions of mode 1 (W function).
   * - :literal:`wy`, :literal:`phiy`
     - Chromatic amplitude and phase functions of mode 2.

Coupling functions (:literal:`coupling=true`)
----------------------------------------------

When :literal:`coupling=true`, the full 6D normal-mode decomposition is used and
off-diagonal coupling functions are computed for all mode pairs.

Off-diagonal column names follow the same suffix convention:
:literal:`alfa12`, :literal:`beta12`, :literal:`gama12` are the coupling
functions from mode 1 to mode 2; :literal:`alfa21`, :literal:`beta21`,
:literal:`gama21` are the reverse, and so on for all six off-diagonal pairs.

Additional columns include the Edwards–Teng parameterisation:
:literal:`betx`, :literal:`bety`, :literal:`alfx`, :literal:`alfy`,
:literal:`kpa`, :literal:`r11`, :literal:`r12`, :literal:`r21`, :literal:`r22`,
and the linear resonance driving terms :literal:`f1010`, :literal:`f1001`.

See Also
--------

* :doc:`mad_cmd_twiss` — full twiss command reference
* :doc:`parametric_optics_and_rdts` — derivative-aware optics and RDTs
* :doc:`mad_phy_nforms` — normal forms