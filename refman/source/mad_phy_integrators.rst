.. _ch.phy.intrg:

Integrators
===========

MAD-NG integrates the equations of motion through each element by splitting it
into a sequence of *drift* and *kick* sub-steps.  The integrator scheme is
selected by the :literal:`model` and :literal:`method` attributes of
:literal:`track` and :literal:`twiss`.

Source: :file:`src/madl_symint.mad`.

Slice index convention
----------------------

Every element is broken into slices.  Each slice has an integer index that
identifies its position within the element.  This index appears in the
:literal:`slc` column of the output mtable and is used by the
:literal:`save`, :literal:`aper`, and action hook attributes to select
*when* a callback or save fires.

.. list-table::
   :header-rows: 1
   :widths: 12 88

   * - Index
     - Meaning
   * - :const:`-3`
     - **Beginning patch** — geometry/energy patch applied before element entry
       (e.g. :literal:`changeref`, :literal:`changedir`).
   * - :const:`-1`
     - **Entry** — the element entry boundary, after beginning patches.
   * - :const:`0`
     - **First body slice** (the first drift/kick sub-step of the body).
   * - :const:`1` … :const:`N-1`
     - **Intermediate body slices**.
   * - :const:`N` (= :literal:`nslice`)
     - **Last body slice** (final sub-step of the body).
   * - :const:`-4`
     - **Ending patch** — geometry/energy patch applied after element exit.
   * - :const:`-2`
     - **Exit** — the element exit boundary, before ending patches.

The default :literal:`save=true` fires at index :const:`-2` (exit).

Slice selectors (:literal:`save`, :literal:`aper`, hooks)
----------------------------------------------------------

The :literal:`save`, :literal:`aper`, :literal:`atentry`, :literal:`atslice`,
:literal:`atexit`, and all other action attributes accept either a *boolean*
or one of the following *string keys* from :literal:`MAD.symint.slcsel`.

Source: :file:`src/madl_symint.mad`, table :literal:`M.slcsel`.

**Single-position selectors**

.. list-table::
   :header-rows: 1
   :widths: 18 12 70

   * - String
     - :literal:`slc`
     - Fires at
   * - :literal:`"atbegin"`
     - :const:`-3`
     - Beginning patch only.
   * - :literal:`"atentry"`
     - :const:`-1`
     - Element entry only.
   * - :literal:`"atfirst"`
     - :const:`0`
     - First body slice only.
   * - :literal:`"atmid"`
     - :math:`\lceil N/2 \rceil`
     - Middle body slice (rounded up for even :literal:`nslice`).
   * - :literal:`"atlast"`
     - :const:`N`
     - Last body slice only.
   * - :literal:`"atend"`
     - :const:`-4`
     - Ending patch only.
   * - :literal:`"atexit"`
     - :const:`-2`
     - Element exit only.  **This is the default** (:literal:`save=true`).

**Multi-position selectors**

.. list-table::
   :header-rows: 1
   :widths: 18 70

   * - String
     - Fires at
   * - :literal:`"atslice"`
     - All body slices :const:`0` … :const:`N`.
   * - :literal:`"atslicel"`
     - Body slices :const:`1` … :const:`N` (excludes first).
   * - :literal:`"atslicer"`
     - Body slices :const:`0` … :const:`N-1` (excludes last).
   * - :literal:`"atcore"`
     - Body slices :const:`1` … :const:`N-1` (excludes both endpoints).
   * - :literal:`"atbody"`
     - Like :literal:`"atcore"` but guarantees at least one slice when
       :literal:`nslice=1`.
   * - :literal:`"atborder"`
     - Body slice endpoints: :const:`0` and :const:`N`.
   * - :literal:`"atentex"`
     - Entry and exit: :const:`-1` and :const:`-2`.
   * - :literal:`"atpatch"`
     - Patch positions only: :const:`-3` and :const:`-4`.
   * - :literal:`"atenbeex"`
     - All non-body positions: :const:`-3`, :const:`-1`, :const:`-4`,
       :const:`-2`.
   * - :literal:`"atbound"`
     - Border slices + entry + exit: :const:`0`, :const:`N`, :const:`-1`,
       :const:`-2`.
   * - :literal:`"atsample"`
     - Middle body slice + border slices + entry + exit.
   * - :literal:`"atfull"`
     - All body slices + exit: :const:`0` … :const:`N`, :const:`-2`.
   * - :literal:`"atstd"`
     - Core body slices + exit: :const:`1` … :const:`N-1`, :const:`-2`.
   * - :literal:`"atstd1"`
     - Body slices + exit (like :literal:`"atstd"` with :literal:`nslice=1`
       guarantee).
   * - :literal:`"atfront"`
     - Odd-indexed positions: entry + beginning patches (positions where
       :literal:`i % 2 == 1`).
   * - :literal:`"atback"`
     - Even-indexed positions: exit + ending patches (positions where
       :literal:`i % 2 == 0`).
   * - :literal:`"atall"`
     - Every position.
   * - :literal:`"atnone"`
     - No positions.  Equivalent to :const:`false`.

**Boolean shortcuts**

.. list-table::
   :header-rows: 1
   :widths: 18 82

   * - Value
     - Equivalent
   * - :const:`true`
     - :literal:`"atexit"` — save at element exit.
   * - :const:`false`
     - :literal:`"atnone"` — never fire / no output table.

Curved multipole expansion (:literal:`secnmul`)
-----------------------------------------------

When tracking through a bending magnet that is integrated in a curved frame
(:literal:`sbend`, fake :literal:`rbend`) that carries higher-order multipole
components (:literal:`knl`, :literal:`ksl`), the kick field in the curved
reference frame differs from the straight-element case.  MAD-NG expands the
exact curved-frame kick as a polynomial in :math:`(x, y)` using pre-computed
coefficients.  The maximum polynomial order of this expansion is controlled
by :literal:`secnmul`.

Source: :file:`src/madl_curvmul.mad` (:literal:`getanbnr`),
:file:`src/madl_etrck.mad`.

The expansion is computed from the normal and skew multipole strengths
:literal:`knl[i]`, :literal:`ksl[i]` and the curvature :math:`h = \theta/L`,
with coefficients derived from the PTC curved-bend potential.  The result is
stored in the :literal:`bfx`, :literal:`bfy` arrays (length
:math:`(snm+1)(snm+2)/2`), which are evaluated by :literal:`bxbyh` inside each
kick step.

:literal:`secnmul` values
~~~~~~~~~~~~~~~~~~~~~~~~~~

The :literal:`secnmul` attribute is accepted by :literal:`track` and
:literal:`twiss` as a command-level default, and can also be set on individual
elements as :literal:`elm.secnmul` (takes precedence over the command default).

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Behaviour
   * - :const:`false` / :const:`0`
     - **Disabled** (default).  No curved-multipole expansion; the bend body
       uses the straight-element kick :literal:`strex_kick` / :literal:`curex_kick`
       with only the :math:`k_0` dipole curvature built into the drift.
   * - :const:`-1` — automatic
     - :math:`snm = \max(damo+1,\; nmul+2)`, where :literal:`damo` is the
       maximum DA order of any tracked damap and :literal:`nmul` is the number of
       non-zero multipole orders on the element.  This is the recommended
       automatic strategy: the expansion order adapts to both the element
       content and the DA tracking order, ensuring the kick is exact up to the
       requested polynomial order.
   * - :const:`-2` — automatic (broader)
     - :math:`snm = damo+1 + nmul`.  A wider expansion that sums both
       contributions.  Use when cross-terms between the curvature and high-order
       multipoles are important.
   * - positive integer :math:`N`
     - Exactly :math:`N` terms, capped at :const:`22` (the hard limit
       :literal:`nmul_max`).  Useful for fixed reproducible benchmarks.

.. note::

   The curved-multipole expansion is skipped entirely when the element has only
   a pure dipole (:literal:`nmul=1`, :literal:`ksl[1]=0`), or when the element
   flag :literal:`kill_body` is set.  In those cases :literal:`snm` is forced to
   :const:`0` regardless of :literal:`secnmul`.

Element-level override
~~~~~~~~~~~~~~~~~~~~~~

Setting :literal:`elm.secnmul` on an individual element overrides the
command-level :literal:`secnmul` for that element only:

.. code-block:: mad

   local sbend in MAD.element
   local mb = sbend 'MB' { l=14.3, angle=0.1, knl={0, 0, 1e-3},
                            secnmul=-1 }  -- automatic expansion for this bend

When neither the element nor the command sets :literal:`secnmul`, the default
is effectively ``-1`` for sbends with higher-order multipoles encountered during
damap tracking, and :const:`0` otherwise.

Practical guidance
~~~~~~~~~~~~~~~~~~

* For pure dipoles without higher-order components, :literal:`secnmul` has no
  effect.
* For bends with sextupole or higher components in DA (optics/RDT) workflows,
  set :literal:`secnmul=-1` to ensure exact kicks up to the DA order.
* For particle tracking only (no damap), :literal:`secnmul=nmul+2` is
  sufficient.
* The expansion cost scales as :math:`O(snm^2)` per kick step.  Keep
  :literal:`secnmul` as small as needed.

Integration models
------------------

The :literal:`model` attribute selects the type of map used for each sub-step.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - model
     - Description
   * - :literal:`'TKT'`
     - **Thick-Kick-Thick** (default).  The drift sub-steps use *exact thick
       maps* for each element kind (quadrupole matrix, solenoid matrix, …).
       Combines with the Yoshida or Boole splitting coefficients.
   * - :literal:`'DKD'`
     - **Drift-Kick-Drift**.  The drift sub-steps use an exact straight or
       curved drift map.  Kicks use a generic multipole kick.  Equivalent to
       a standard thin-lens integration model.
   * - :literal:`'KMK'`
     - **Kick-Matrix-Kick** (Boole's rule).
       Used internally for elements with a 2nd-order thick map such as
       quadrupoles and electrostatic separators.  Exposed via the
       :literal:`'collim'` method string.

Integration orders
------------------

The :literal:`method` attribute selects the order of integration, from
:const:`1` to :const:`8`.  Odd values are rounded up to the next even order.

It should be noted that an increase in the level of integration order results in
an equivalent increase of 10 times slicing uniformly. For example, a 4th-order
integrator with :literal:`nslice=10` is roughly equivalent to a 2nd-order
integrator with :literal:`nslice=100` in terms of accuracy, but the former is
much faster. Therefore it is generally recommended to use higher-order integrators
with fewer slices for better performance without sacrificing accuracy.

.. list-table::
   :header-rows: 1
   :widths: 10 20 70

   * - method
     - Steps per slice
     - Notes
   * - 1, 2
     - 1 kick, 2 drifts
     - 2nd-order Leapfrog / Yoshida (eq. 2.10) — fast, low accuracy
   * - 3, 4
     - 3 kicks, 4 drifts
     - 4th-order Yoshida (eq. 2.11)
   * - 5, 6
     - 7 kicks, 8 drifts
     - 6th-order Yoshida (table 1, variant A)
   * - 7, 8
     - 15 kicks, 16 drifts
     - 8th-order Yoshida (table 2, variant D)

Named method strings
--------------------

In addition to numeric orders, :literal:`method` accepts the following strings.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - String
     - Equivalent
   * - :literal:`'simple'`
     - :literal:`DKD` order 2 (2nd-order Leapfrog).
   * - :literal:`'collim'`
     - :literal:`KMK` order 2 (2nd-order Boole collimation scheme).
   * - :literal:`'teapot'`
     - Teapot splitting order 2 (n=2).
   * - :literal:`'teapot2'`
     - Teapot splitting n=2: 2 kicks, 3 drifts.
   * - :literal:`'teapot3'`
     - Teapot splitting n=3: 3 kicks, 4 drifts.
   * - :literal:`'teapot4'`
     - Teapot splitting n=4: 4 kicks, 5 drifts.

Teapot splitting uses non-uniform drift fractions based on [Burkhardt13]
table 1, optimised for accuracy in bending magnets.

Practical guidance
------------------

* The default :literal:`method=4` (:literal:`TKT`, 4th-order Yoshida) is a
  good balance between accuracy and speed for most workflows.
* Increase :literal:`method` to 6 or 8 for high-precision studies or large
  :literal:`nslice`.
* Use :literal:`model='DKD'` only when thin-lens compatibility with MAD-X or
  PTC is needed; otherwise :literal:`TKT` is preferable.
* Set :literal:`save="atslice"` (or :literal:`"atbody"`) to record
  intermediate positions inside an element — useful for phase-space portraits
  or verifying per-slice coordinates.
* The Yoshida coefficients and scheme structure are taken from [Yoshida90].

See Also
--------

* :doc:`mad_cmd_track` — :literal:`method`, :literal:`model`, :literal:`nslice`,
  :literal:`save`, :literal:`aper`
* :doc:`mad_cmd_twiss`
* :doc:`mad_cmd_survey`
