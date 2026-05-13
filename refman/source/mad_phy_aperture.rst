.. _ch.phy.aper:

Aperture
========

MAD-NG checks particle positions against element aperture definitions during
tracking.  A particle whose transverse position falls outside the aperture is
tagged :literal:`"lost"` and removed from the tracked set.

Source: :file:`src/madl_aper.mad`.

Aperture check control
----------------------

Aperture checking is enabled by the :literal:`aper` attribute of
:literal:`track` (default :const:`true`, checked at element exit).

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Effect
   * - :const:`true`
     - Check at last slice (just before exit). Default.
   * - :const:`false`
     - No aperture check.
   * - :literal:`"atentry"`
     - Check at element entry.
   * - :literal:`"atexit"`
     - Check at element exit (same as :const:`true`).
   * - :literal:`"atslice"`
     - Check after every integration slice.
   * - :literal:`"atbody"`
     - Check after every non-entry slice.
   * - :literal:`"atbound"`
     - Check at entry and exit.
   * - :literal:`"atall"`
     - Check at entry, every slice, and exit.

Aperture models
---------------

An element's aperture is specified by the :literal:`aperture` attribute, a table
with a mandatory :literal:`kind` field.  Parameters follow :literal:`kind` as
positional entries.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - kind
     - Parameters
     - Description
   * - :literal:`'circle'`
     - :literal:`{r}`
     - Circular aperture of radius :math:`r`.
   * - :literal:`'ellipse'`
     - :literal:`{a, b}`
     - Elliptical aperture with semi-axes :math:`a` (x) and :math:`b` (y).
   * - :literal:`'square'`
     - :literal:`{h}`
     - Square aperture of half-side :math:`h`.
   * - :literal:`'rectangle'`
     - :literal:`{hx, hy}`
     - Rectangular aperture with half-widths :math:`hx`, :math:`hy`.
   * - :literal:`'rectcircle'`
     - :literal:`{hx, hy, r}`
     - Intersection of a rectangle and a circle.
   * - :literal:`'rectellipse'`
     - :literal:`{hx, hy, a, b}`
     - Intersection of a rectangle and an ellipse.
   * - :literal:`'racetrack'`
     - :literal:`{hx, hy, rx, ry}`
     - Rectangle with elliptical rounded corners.
   * - :literal:`'octagon'`
     - :literal:`{hx, hy, cx}`
     - Rectangle clipped at 45-degree corners.
   * - :literal:`'polygon'`
     - :literal:`{vx=..., vy=...}`
     - Arbitrary closed polygon defined by vertex vectors :literal:`vx`, :literal:`vy`.
   * - :literal:`'bbox'`
     - :literal:`{hx, hpx, hy, hpy}`
     - Phase-space bounding box on :math:`(x, p_x, y, p_y)`.

All models except :literal:`'polygon'` and :literal:`'bbox'` support optional
:literal:`tilt`, :literal:`xoff`, and :literal:`yoff` fields to rotate and shift
the acceptance boundary.

Example
-------

.. code-block:: mad

   local sbend in MAD.element
   local mb = sbend 'MB' { l=14.3, angle=0.1, aperture={kind='circle', 0.055} }

Defining a default aperture for all elements that lack their own:

.. code-block:: mad

   trk = track {
     sequence = seq,
     aperture = { kind='circle', 0.055 },
   }

Lost particles
--------------

When a particle is lost:

* Its :literal:`status` is set to :literal:`"lost"`.
* Its :literal:`spos` and :literal:`turn` are recorded at the loss point.
* It is removed from the active tracking list.
* The :literal:`lost` counter in the mtable header is incremented.
* With :literal:`info >= 1`, a summary line is printed to the console.

The :literal:`apersel` attribute on :literal:`track` is a predicate callable
that can suppress the default aperture check for selected elements.

See Also
--------

* :doc:`mad_cmd_track` — :literal:`aper`, :literal:`aperture`, :literal:`apersel`, :literal:`ataper`
* :doc:`mad_phy_alignments`
