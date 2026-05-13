.. _ch.phy.radia:

Radiation
=========

MAD-NG simulates synchrotron radiation energy loss and quantum excitation during
:literal:`track` via the :literal:`radiate` attribute.  The implementation is
adapted from MAD-X.

Source: :file:`src/madl_synrad.mad`, :file:`src/madl_track.mad`.

Enabling radiation
------------------

Pass :literal:`radiate` to :literal:`track`:

.. code-block:: mad

   trk = track { sequence=seq, radiate="damping", ... }

A boolean :const:`true` is treated as :literal:`"damp"`.

Radiation modes
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Description
   * - :literal:`false` or :literal:`nil`
     - No radiation (default).
   * - :literal:`"damping"` / :literal:`"damp"`
     - Classical radiation damping only.  Energy loss per slice is computed
       analytically from the local curvature and field.
   * - :literal:`"quantum"` / :literal:`"quan"`
     - Quantum excitation: energy loss is distributed over a random number of
       photons drawn from a Poisson distribution, with individual photon
       energies sampled from the synchrotron radiation spectrum.
   * - :literal:`"photon"` / :literal:`"phot"`
     - Same as :literal:`"quantum"`, but the emitted photons are also tracked
       as separate particles appended to the mflow.

Appending :literal:`"+"` to any mode (e.g. :literal:`"damping+"`) activates
the *double-pass* (symmetric-pass) integration which evaluates radiation at
both entry and exit of each slice for better accuracy.

Element radiation length
-------------------------

Radiation is only applied to elements with a non-zero :literal:`lrad` attribute.
By default :literal:`lrad` equals the element length :literal:`l`.  Set
:literal:`lrad=0` to suppress radiation for a specific element.

Radiation integrals
-------------------

The synchrotron radiation integrals :math:`I_1` through :math:`I_8` are
computed by :literal:`twiss` and returned as header fields
:literal:`synch_1` … :literal:`synch_8` of the mtable.  These are available
without enabling :literal:`radiate`; they are computed from the linear optics.

See Also
--------

* :doc:`mad_cmd_track` — :literal:`radiate`, :literal:`taper` attributes
* :doc:`mad_phy_optics` — :literal:`synch_1` … :literal:`synch_8` header fields
