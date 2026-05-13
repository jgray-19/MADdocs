.. _ch.phy.align:

Misalignments
=============

MAD-NG supports element-level misalignments: translations and rotations of the
element reference frame relative to the nominal sequence geometry.

There are two kinds of misalignment:

* **Permanent misalignment** — stored in the :literal:`misalign` attribute of
  the element itself (``elm.misalign``).  Applied unconditionally whenever the
  element is tracked, regardless of the :literal:`misalign` command flag.
* **Error misalignment** — stored in the sequence via :literal:`seq:ealign()`.
  Applied only when the command attribute :literal:`misalign=true` is set.

Neither kind affects :literal:`survey`, which always uses the ideal geometry.

Source: :file:`src/madl_etrck.mad`, function :literal:`get_algn`.

Misalignment attributes
-----------------------

Misalignments are stored on elements in a :literal:`misalign` table with the
following fields.

.. list-table::
   :header-rows: 1
   :widths: 15 20 65

   * - Field
     - Unit
     - Description
   * - :literal:`dx`
     - m
     - Horizontal translation (transverse :math:`x`).
   * - :literal:`dy`
     - m
     - Vertical translation (transverse :math:`y`).
   * - :literal:`ds`
     - m
     - Longitudinal translation along the element axis.
   * - :literal:`dtheta`
     - rad
     - Rotation about the vertical axis (yaw / azimuthal).
   * - :literal:`dphi`
     - rad
     - Rotation about the horizontal axis (pitch / elevation).
   * - :literal:`dpsi`
     - rad
     - Rotation about the longitudinal axis (roll).

Setting permanent misalignments
--------------------------------

Set the :literal:`misalign` table directly on an element.  This misalignment
is always active during tracking:

.. code-block:: mad

   seq["QF1"].misalign = { dx=1e-4, dy=-5e-5 }

Setting error misalignments
----------------------------

Error misalignments are set on the sequence and are only applied when
:literal:`misalign=true` is passed to the command:

.. code-block:: mad

   seq:misalign("QF1", { dx=2e-4 })  -- store error misalignment
   trk = track { sequence=seq, X0={x=0}, misalign=true }

Without :literal:`misalign=true`, error misalignments from :literal:`seq:ealign`
are ignored.  Permanent element-level misalignment (:literal:`elm.misalign`) is
always applied regardless.

Element tilt
------------

The :literal:`tilt` attribute on an element is a rotation about the longitudinal
axis applied to the element body maps.  It is distinct from the :literal:`dpsi`
misalignment:

* :literal:`tilt` is **always** applied, regardless of the :literal:`misalign`
  flag.
* :literal:`dpsi` in a :literal:`misalign` table is only applied when
  :literal:`misalign=true`.

.. code-block:: mad

   seq["QS"].tilt = pi/4  -- 45-degree skew quad tilt, always active

Implementation
--------------

When :literal:`misalign=true` is active, the integrator wraps each element body
with a :literal:`misalign` patch (translation + rotation) at entry and its
inverse at exit.  The patches combine the element's permanent
:literal:`.misalign` table and any additional error misalignment from the
sequence :literal:`:ealign` method.

See Also
--------

* :doc:`mad_cmd_track` — :literal:`misalign` attribute
* :doc:`mad_cmd_twiss`
* :doc:`mad_cmd_survey`