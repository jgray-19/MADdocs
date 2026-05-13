.. _ch.phy.dynmap:

Dynamic Maps
============

MAD-NG integrates particle motion through each element using a catalog of
*dynamic maps* — one per element kind, covering both particle (orbit) and
damap (optics) tracking.  The same map functions work for both modes
simultaneously.

Source: :file:`src/madl_dynmap.mad`.

Direction conventions
---------------------

Three independent direction signs govern each tracking step.

.. list-table::
   :header-rows: 1
   :widths: 12 20 68

   * - Variable
     - Default
     - Meaning
   * - :literal:`edir`
     - :literal:`seq.dir`
     - Element direction.  Affects curvatures.
   * - :literal:`sdir`
     - :literal:`cmd.dir`
     - Tracking (s) direction.  Affects element lengths.
   * - :literal:`tdir`
     - :literal:`edir × sdir`
     - Time direction.  Affects angles and energy.

Patch maps
----------

Patch elements apply a rigid-body transformation to the tracking frame without
magnetic kicks.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Map
     - Description
   * - :literal:`xrotation`
     - Rotation about the :math:`x`-axis (pitch, :math:`R_x(\Delta\phi)`).
   * - :literal:`yrotation`
     - Rotation about the :math:`y`-axis (yaw, :math:`R_y(\Delta\theta)`).
   * - :literal:`srotation`
     - Rotation about the :math:`s`-axis (roll, :math:`R_z(\Delta\psi)`).
   * - :literal:`translate`
     - Translation by :math:`(dx, dy, ds)`.
   * - :literal:`changeref`
     - Generic combined translation + rotation patch (:literal:`RT` forward,
       :literal:`TR` backward).
   * - :literal:`changedir`
     - Reverses the element direction :literal:`edir`.
   * - :literal:`changenrj`
     - Changes the reference frame energy (e.g. at RF cavities).
   * - :literal:`misalign`
     - Applies the element misalignment at entry (:literal:`lw>0`) or exit
       (:literal:`lw<0`).
   * - :literal:`tilt`
     - Applies the element :literal:`tilt` attribute as an :math:`s`-rotation.

DKD maps (straight elements)
-----------------------------

Used for the :literal:`'DKD'` integration model on straight elements.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Map
     - Description
   * - :literal:`strex_drift`
     - Exact straight drift.
   * - :literal:`strex_kick`
     - Combined multipole kick on a straight element (:literal:`INTER_STREX`).
   * - :literal:`strex_fringe`
     - Fringe-field kick for straight elements.
   * - :literal:`strex_kickhs`
     - Combined kick with hard-edge solenoid fringe.

TKT maps (curved elements — sbend / rbend)
------------------------------------------

Used for the :literal:`'TKT'` integration model on bending magnets.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Map
     - Description
   * - :literal:`sbend_thick`
     - Thick sector-bend map (:literal:`INTER_TEAPOT`, :literal:`SSEC`).
   * - :literal:`sbend_kick`
     - Kick step for :literal:`sbend` (wraps :literal:`curex_kick`).
   * - :literal:`rbend_thick`
     - Thick rectangular-bend map (:literal:`INTER_STREX`, :literal:`SPAR`).
   * - :literal:`rbend_kick`
     - Kick step for :literal:`rbend` (wraps :literal:`strex_kick`).
   * - :literal:`dipeg_fringe`
     - Dipole-edge fringe field for curved magnets.

TKT maps (quadrupoles)
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Map
     - Description
   * - :literal:`quad_thick`
     - Thick quadrupole matrix (:literal:`INTER_TKTF`, normal orientation).
   * - :literal:`quad_thicks`
     - Thick quad matrix with solenoid coupling.
   * - :literal:`quad_thickh`
     - Thick quad matrix with dipole term (:math:`k_0 \neq 0`).
   * - :literal:`quad_kick`
     - Quadrupole kick (wraps :literal:`quad_kick_`).
   * - :literal:`quad_kicks`
     - Quadrupole kick with solenoid coupling.
   * - :literal:`quad_kickh`
     - Quadrupole kick with dipole term.

Other element maps
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Map
     - Element
   * - :literal:`solen_thick`, :literal:`solen_fringe`
     - Solenoid (:literal:`INTER_SOL5`).
   * - :literal:`sept_thick`, :literal:`sept_kick`
     - Electrostatic septum (:literal:`SEPTTRACK`).
   * - :literal:`rfcav_kick`
     - RF cavity (:literal:`INTER_CAV4`).
   * - :literal:`acdip_kick`, :literal:`acqd_kick`
     - AC dipole / AC Dipole as a thin quadrupole.
   * - :literal:`wire_kick`
     - Wire element.
   * - :literal:`beambeam_kick`
     - Beam–beam thin-lens kick.
   * - :literal:`nllens_kick`
     - Nonlinear lens.
   * - :literal:`linmap_thick`
     - Generic linear map (from :literal:`matrix` attribute).
   * - :literal:`genmap_kick`
     - Generic nonlinear map (from :literal:`map` attribute).

Fringe-field maps
-----------------

Fringe maps are stored in :literal:`M.fringe` and dispatched per element kind.
They are applied at element entry and exit by the integrator.  Available
entries cover: :literal:`quadrupole`, :literal:`sextupole`, :literal:`solenoid`,
:literal:`rfcavity`, :literal:`dipole_edge`, :literal:`bend` (entrance/exit
pole-face rotation), and :literal:`elseparator`.

See Also
--------

* :doc:`mad_phy_integrators` — integration models and methods
* :doc:`mad_cmd_track` — :literal:`model`, :literal:`method`, :literal:`nslice`
* :doc:`mad_cmd_twiss`
