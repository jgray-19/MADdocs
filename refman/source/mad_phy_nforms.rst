.. _ch.phy.nform:

Normal Forms
============

MAD-NG computes a Birkhoff normal form from a one-turn damap to extract tunes,
chromaticities, anharmonicities, and resonance driving terms.  The result is
stored in a *normal form* (nform) table.

Source: :file:`src/madl_gphys.mad` (functions :literal:`normal_init`,
:literal:`normal`, :literal:`normal_a0`, :literal:`normal_a1`,
:literal:`normal_c`).

Normal form object
------------------

A normal form object is produced by calling :literal:`MAD.gphys.normal(m)`
where :literal:`m` is an :literal:`Xset` or :literal:`Mset` damap from
:literal:`twiss` or :literal:`track` with :literal:`mapdef=true`.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Field
     - Description
   * - :literal:`nn`
     - Total number of GTPSA variables + parameters.
   * - :literal:`nv`
     - Number of phase-space variables.
   * - :literal:`rk`
     - Rank of the phase-space variables (4 for coasting, 6 otherwise).
   * - :literal:`it`
     - Index of the :math:`t` variable (5 for coasting beams, 0 otherwise).
   * - :literal:`ipt`
     - Index of the :math:`p_t` variable (0 for 6D, 5 for 5D, 6 for 56D).
   * - :literal:`a`
     - Normalising map :math:`A` (set by :literal:`normal`).
   * - :literal:`a_0`
     - Closed-form (fixed-point) map :math:`A_0`.
   * - :literal:`a_1`
     - Courant–Snyder map :math:`A_1`.
   * - :literal:`a_2`
     - Full nonlinear normalising map :math:`A_2`.
   * - :literal:`c`, :literal:`ci`
     - Action–angle basis map and its inverse.
   * - :literal:`lam`
     - Eigenvalues (eigentunes).
   * - :literal:`anh`
     - Anharmonicity TPSA table (indexed by monomial strings).
   * - :literal:`gnf`
     - Generating function RDTs (set by :literal:`analyse`).
   * - :literal:`ham`
     - Hamiltonian terms (set by :literal:`analyse`).

Normal form methods
-------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Method
     - Description
   * - :literal:`nf:q1()`, :literal:`nf:q2()`, :literal:`nf:q3()`
     - Tunes of modes 1, 2, 3.
   * - :literal:`nf:dq1()`, :literal:`nf:dq2()`, :literal:`nf:dq3()`
     - First-order chromaticities :math:`\xi_i = \partial Q_i / \partial \delta`.
   * - :literal:`nf:anhx(ord)`
     - Detuning with amplitude :math:`\partial Q / \partial J_x` at order
       :literal:`ord`.
   * - :literal:`nf:anhy(ord)`
     - Detuning with amplitude :math:`\partial Q / \partial J_y`.
   * - :literal:`nf:anht(ord)`
     - Detuning with amplitude :math:`\partial Q / \partial J_t`.
   * - :literal:`nf:gnfu(ms)`
     - Value of the generating function RDT at monomial string :literal:`ms`.
   * - :literal:`nf:haml(ms)`
     - Value of the Hamiltonian term at monomial string :literal:`ms`.
   * - :literal:`nf:copy(a_)`
     - Returns a copy of the normal form, optionally replacing the
       normalising map with :literal:`a_`.
   * - :literal:`nf:analyse()`
     - Computes RDTs (:literal:`gnf`) and Hamiltonian terms (:literal:`ham`).

Variable index conventions
--------------------------

The phase-space variables are indexed as:

.. list-table::
   :header-rows: 1
   :widths: 10 15 75

   * - Index
     - Variable
     - Notes
   * - 1
     - :math:`x`
     -
   * - 2
     - :math:`p_x`
     -
   * - 3
     - :math:`y`
     -
   * - 4
     - :math:`p_y`
     -
   * - 5
     - :math:`t` or :math:`p_t`
     - :math:`t` for 6D / 56D; :math:`p_t` for 5D; absent for 4D.
   * - 6
     - :math:`p_t`
     - 6D only.

Parameters (knobs) follow the phase-space variables starting at index
:literal:`nv+1`.

Monomial strings
----------------

Anharmonicities and RDTs are indexed by *monomial strings* — compact
representations of polynomial orders.  For example, :literal:`"200000"` means
one power of :math:`x`, :literal:`"020000"` means one power of :math:`p_x`,
and :literal:`"110010"` means one :math:`x \cdot p_x \cdot t`.

See Also
--------

* :doc:`mad_phy_optics` — optical functions returned by twiss
* :doc:`parametric_optics_and_rdts` — derivative-aware optics and RDTs
* :doc:`mad_cmd_twiss` — :literal:`mapdef`, :literal:`norms` options
