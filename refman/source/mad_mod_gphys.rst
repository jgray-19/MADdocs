Generic Physics
===============

The module :mod:`MAD.gphys` exports a mixed set of physics-oriented helper
functions from :literal:`MAD/src/madl_gphys.mad`.

The current implementation groups helpers for:

* converting between particle-like tables and numeric vectors
* sorting and post-processing tracking results
* checking and repairing linear maps before optics analysis
* extracting optics, chromatic, and normal-form data from maps
* estimating beam sizes from differential maps

The source implementation is in
:literal:`MAD/src/madl_gphys.mad`.

Where It Appears in Practice
----------------------------

The clearest direct consumers of :mod:`MAD.gphys` in the current code base are:

* :var:`cofind`, which uses :literal:`par2vec`, :literal:`vec2par`,
  :literal:`has_dpt`, and :literal:`msort`
* :var:`twiss`, which uses :literal:`normal`, :literal:`map2bet`,
  :literal:`bet2map`, :literal:`chr2bet`, :literal:`syn2bet`,
  :literal:`optfun`, and the optical-function name lists
* :var:`track` and tapering-related code, which use helpers such as
  :literal:`dp2pt`, :literal:`pt2dp`, and :literal:`bet2map`
* table post-processing workflows, which use :literal:`mchklost` and
  :literal:`melmcol`

This page is a guide to the exported helper surface, not a full derivation of
the underlying algorithms.

Particle and Orbit Helpers
--------------------------

The simplest entry points are the coordinate conversion helpers:

.. function:: par2vec(X, [V])

   Convert a particle-like object or coordinate table
   :literal:`{x, px, y, py, t, pt}` into a 6D vector. Missing coordinates are
   filled with zeros. If :var:`V` is provided, it is reused as the destination
   vector.

.. function:: vec2par(V, [X])

   Convert a 6D vector back to a particle-like table with the canonical fields
   :literal:`x`, :literal:`px`, :literal:`y`, :literal:`py`, :literal:`t`,
   :literal:`pt`. If :var:`X` is provided, it is reused as the destination
   table.

These functions are used directly by :var:`cofind`.

Example:

.. code-block:: mad

   local par2vec, vec2par in MAD.gphys

   local v  = par2vec { x=1e-3, px=2e-5 }
   local x0 = vec2par(v)

Momentum and Beta Conversions
-----------------------------

The module also provides compact helpers for converting longitudinal momentum
coordinates:

.. function:: dp2pt(dp, beta0)

   Convert relative momentum deviation :var:`dp` into canonical
   :literal:`pt`, using the reference relativistic :math:`\beta_0`.

.. function:: pt2dp(pt, beta0)

   Convert canonical :literal:`pt` back to relative momentum deviation
   :var:`dp`.

.. function:: pt2beta(pt, beta0)

   Convert canonical :literal:`pt` into the corresponding relativistic
   :math:`\beta`.

These helpers are used directly in the current source tree by tracking-related
code.

MTable and MFlow Helpers
------------------------

The module also exports helpers that operate on tracking tables and dynamic
map flows.

.. function:: mchklost(mtbl, ...)

   Return :var:`mtbl` if :literal:`mtbl.lost == 0`, otherwise return
   :const:`nil`. Any additional arguments are forwarded unchanged. This is a
   convenience helper for checking the :literal:`lost` header field.

.. function:: melmcol(mtbl, cols)

   Extend an :type:`mtable` with columns derived from the attached sequence.
   The table must carry the protected sequence handle :literal:`__seq` and the
   element-index column :literal:`eidx`, as produced for example by
   :var:`track` or :var:`twiss`.

   Standard element attributes such as :literal:`angle` or :literal:`tilt` can
   be copied directly. Integrated strengths such as :literal:`k1l`,
   :literal:`k2l`, :literal:`k1sl`, and similar names are also supported and
   are reconstructed from element length and local or packed strength data.

.. function:: msort(mflw, [cmp])

   Sort a dynamic map flow by status rank and particle id, then adjust
   :literal:`mflw.npar` to the number of still-trackable items. The default
   ordering is driven by the internal rank map
   :literal:`Xset/Mset/Aset/stable < unstable < singular < lost`.

For a worked example of :literal:`melmcol`, see :doc:`mad_gen_mtable`.

Example:

.. code-block:: mad

   local melmcol in MAD.gphys
   local tws = twiss { sequence=seq, method=4, cofind=true }

   melmcol(tws, {'angle', 'tilt', 'k1l', 'k2l'})

Linear Map Helpers
------------------

Several exported helpers operate on 4D or 6D matrices and on related eigensystem
objects:

.. function:: has_dpt(M)

   Check whether the input matrix or damap carries non-trivial
   longitudinal :literal:`pt` dependence according to the current tolerance
   test implemented in :mod:`gphys`.

.. function:: has_cpl(M, [tol])

   Check whether the transverse coupling blocks exceed the requested
   tolerance.

.. function:: is_eigsys(V, W, M, [tol])

   Check whether :var:`V` and :var:`W` form a consistent eigensystem of
   :var:`M` within the requested tolerance.

.. function:: get_eigval(M, V, W)

   Recover eigenvalue pairs :var:`W` from the eigenvector matrix :var:`V`.

.. function:: make_stable(M)

   Apply the implementation's stability check and optional small-coupling
   cleanup to the matrix :var:`M`.

.. function:: make_symp(M)

   Apply the implementation's symplectification step to :var:`M` when its
   symplectic deviation is within the accepted range.

.. function:: order_eigen(V, W)
              norml_eigen(A, W)
              phase_eigen(A)

   Reorder, normalize, and rephase eigensystem data according to the current
   implementation conventions.

These functions are used by the normal-form and optics code in the same module.

Normal Forms and Optics Extraction
----------------------------------

The module exports several functions that are used by the current
:var:`twiss` implementation:

.. function:: normal(m, [urdt])

   Build and analyse a normal-form object from a damap-like input. The exact
   internal structure is defined by the implementation in
   :literal:`madl_gphys.mad`.

.. function:: optfun(m, name, ...)

   Compute a named optics-related quantity from the normal-form machinery.
   This function is used internally by :literal:`twiss(trkopt=...)`.

.. function:: phasor(...)

   Export the phasor helper used by the normal-form code.

.. function:: bet2map(bb0, map, [sav])

   Convert a :type:`beta0` block into a damap with status
   :literal:`"Aset"` using the current implementation rules.

.. function:: map2bet(map, [rnk], [cpl], [beta], [dir])

   Extract or update a :type:`beta0` block from a damap.

.. function:: chr2bet(bb0, fdp, dpt)

   Update a :type:`beta0` block from a momentum-offset comparison block.

.. function:: syn2bet(bb0, mflw, elm)

   Update synchrotron-integral fields in a :type:`beta0` block using the
   current element and map-flow data.

These functions are closely tied to the current :var:`twiss` implementation.

Beam Size Estimates
-------------------

The module also exports beam-size helpers based on differential maps:

.. function:: beamsize(x, sig, [mo])

   Compute RMS beam-size estimates from a real TPSA :var:`x` and an iterable
   of sigma values. If :var:`mo` is omitted, the current implementation returns
   the result order by order up to the TPSA order.

.. function:: beamsize_tbl(m, sig, [p])

   Build an :type:`mtable` of beam-size estimates derived from the damap
   :var:`m`. If :var:`p` is truthy, momentum-related columns are included too.

The implementation comments reference Eq. 7 of
R. Tomas, "Nonlinear optimization of beam lines", Phys. Rev. Accel. Beams,
2006.

Tolerances and Name Lists
-------------------------

The module also exports:

* :literal:`MAD.gphys.tol`
* :literal:`MAD.gphys.ofname`
* :literal:`MAD.gphys.ofcname`
* :literal:`MAD.gphys.ofhname`
* :literal:`MAD.gphys.ofchname`

These are implementation-facing data tables used by the current optics code.

See Also
--------

* :doc:`mad_cmd_track`
* :doc:`mad_cmd_cofind`
* :doc:`mad_cmd_twiss`
* :doc:`mad_gen_mtable`
* :doc:`mad_gen_beta0`
* :doc:`mad_mod_diffmap`
