.. _ch.phy.geomap:

Geometric Maps
==============

MAD-NG computes the 3D layout of a sequence using *geometric maps* — functions
that propagate a position vector :math:`V` and orientation matrix :math:`W`
through each element.  These maps are used exclusively by the
:literal:`survey` command.

Source: :file:`src/madl_geomap.mad`.

Tracking frame
--------------

Each geomap function receives and updates a *mflow* table with the fields:

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Field
     - Description
   * - :literal:`V`
     - 3-vector: global Cartesian position of the reference point :math:`(X, Y, Z)`.
   * - :literal:`W`
     - 3×3 rotation matrix: orientation of the local frame in the global frame.
   * - :literal:`sdir`
     - Tracking direction along :math:`s` (:literal:`+1` forward, :literal:`-1` backward).
   * - :literal:`edir`
     - Element direction (:literal:`seq.dir`).
   * - :literal:`ang`
     - Accumulated bending angle from element :literal:`angle` attribute.
   * - :literal:`tlt`
     - Tilt from element :literal:`tilt` attribute.

Direction conventions
---------------------

* :literal:`edir` is taken from :literal:`seq.dir` and affects curvatures.
* :literal:`sdir` is taken from :literal:`cmd.dir` and affects element lengths.
* :literal:`tdir = edir × sdir` affects angles.

Patch maps
----------

Patch elements transform :math:`V` and :math:`W` without advancing :math:`s`.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Map
     - Description
   * - :literal:`xrotation`
     - Rotation :math:`R_x(\Delta\phi)` about the :math:`x`-axis (pitch).
   * - :literal:`yrotation`
     - Rotation :math:`R_y(\Delta\theta)` about the :math:`y`-axis (yaw).
   * - :literal:`srotation`
     - Rotation :math:`R_z(\Delta\psi)` about the :math:`s`-axis (roll).
   * - :literal:`translate`
     - Translation :math:`V \mathrel{+}= W \cdot (dx, dy, ds)^T`.
   * - :literal:`changeref`
     - Combined translation and rotation patch.  Forward: first translate then
       rotate (:literal:`TR`); backward: rotate then translate (:literal:`RT`).
   * - :literal:`changedir`
     - Reverses element direction :literal:`edir`.
   * - :literal:`changenrj`
     - No-op for survey (energy change does not affect 3D geometry).
   * - :literal:`misalign`
     - Applies the element misalignment table at entry or exit.

Misalignment in survey
----------------------

The :literal:`misalign` geomap applies translational and rotational offsets
from the element :literal:`misalign` table in the global frame.  The forward
entry transformation is:

.. math::

   W' = W \cdot R, \quad V' = V + W \cdot T

where :math:`T = (dx, dy, ds)` and :math:`R` is built from
:math:`(d\theta, d\phi, d\psi)`.  The exit applies the inverse.

See Also
--------

* :doc:`mad_cmd_survey` — survey command reference
* :doc:`mad_phy_alignments` — misalignment attribute definitions
