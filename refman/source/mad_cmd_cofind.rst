Cofind
======
.. _ch.cmd.cofind:

The :var:`cofind` command (i.e. closed orbit finder) provides a simple interface to find a closed orbit using the Newton algorithm on top of the :var:`track` command.

Command synopsis
----------------

.. code-block:: lua
    :caption: Synopsis of the :var:`cofind` command with default setup.
    :name: fig-cofind-synop

    mtbl, mflw = cofind {
        sequence=sequ,  -- sequence (required)
        beam=nil,       -- beam (or sequence.beam, required)
        range=nil,      -- range of tracking (or sequence.range)
        dir=nil,        -- s-direction of tracking (1 or -1)
        s0=nil,         -- initial s-position offset [m]
        X0=nil,         -- initial coordinates (or damap, or beta block)
        O0=nil,         -- initial coordinates of reference orbit
        deltap=nil,     -- initial deltap(s)
        nturn=nil,      -- number of turns to track
        nslice=nil,     -- number of slices (or weights) for each element
        method=nil,     -- method or order for integration (1 to 8)
        model=nil,      -- model for integration ('DKD' or 'TKT')
        mapdef=true,    -- setup for damap (or list of, true => {})
        secnmul=nil,    -- curved-multipole expansion for bends
        implicit=nil,   -- slice implicit elements too (e.g. plots)
        misalign=nil,   -- consider misalignment
        aperture=nil,   -- default aperture
        fringe=nil,     -- enable fringe fields (see element.flags.fringe)
        frngmax=nil,    -- maximum multipole fringe field order
        radiate=nil,    -- radiate at slices
        nocavity=nil,   -- disable rfcavities
        totalpath=nil,  -- variable 't' is the totalpath
        cmap=nil,       -- use C/C++ maps when available
        ptcmodel=nil,   -- nil=MADNG, true=PTC, false=MADX
        save=false,     -- create mtable and save results
        aper=nil,       -- check for aperture
        observe=nil,    -- save only in observed elements (every n turns)
        savesel=nil,    -- save selector (predicate)
        savemap=nil,    -- save damap in the column __map
        atentry=nil,    -- action called when entering an element
        atslice=nil,    -- action called after each element slices
        atexit=nil,     -- action called when exiting an element
        ataper=nil,     -- action called when checking for aperture
        atsave=nil,     -- action called when saving in mtable
        atdebug=nil,    -- action called when debugging the element maps
        apersel=nil,    -- aperture selector (predicate)
        coitr=25,       -- maximum number of iterations
        cotol=1e-8,     -- closed orbit tolerance (i.e.|dX|)
        costp=1e-8,     -- finite-difference scale for the Jacobian
        O1=0,           -- optional final coordinates translation
        info=nil,       -- information level (output on terminal)
        debug=nil,      -- debug information level (output on terminal)
        usrdef=nil,     -- user defined data attached to the mflow
        mflow=nil,      -- mflow, exclusive with other attributes
    }

The :var:`cofind` command format is summarized in :numref:`fig-cofind-synop`, including the default setup of the attributes. Most of these attributes are set to :const:`nil` by default, meaning that :var:`cofind` relies on the :var:`track` command defaults.

**Sequence and beam**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`sequence`
     - *required*
     - Sequence to search for a closed orbit.
     - ``sequence = lhcb1``
   * - :literal:`beam`
     - :const:`nil`
     - Reference beam (or :literal:`seq.beam`). [#f1]_
     - ``beam = mybeam``
   * - :literal:`range`
     - :const:`nil`
     - Sub-range of the sequence (or :literal:`seq.range`).
     - ``range = "IP1/IP5"``
   * - :literal:`dir`
     - :const:`nil`
     - Tracking direction: :const:`1` forward, :const:`-1` backward.
     - ``dir = -1``
   * - :literal:`s0`
     - :const:`nil`
     - Initial :math:`s`-position offset [m].
     - ``s0 = 5000``

**Initial conditions**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`X0`
     - :const:`nil`
     - Starting-guess coordinates :literal:`{x,px,y,py,t,pt}`, damap, or beta block.
     - ``X0 = {x=1e-3}``
   * - :literal:`O0`
     - :const:`nil`
     - Reference orbit coordinates.
     - ``O0 = {x=1e-4}``
   * - :literal:`deltap`
     - :const:`nil`
     - Initial :math:`\delta_p` offset(s) added to :literal:`pt`.
     - ``deltap = 1e-3``
   * - :literal:`nturn`
     - :const:`nil`
     - Number of turns per Newton iteration.
     - ``nturn = 2``
   * - :literal:`nslice`
     - :const:`nil`
     - Slices per element: number, list, or callable :literal:`(elm,mflw,lw)`.
     - ``nslice = 5``
   * - :literal:`mapdef`
     - :const:`true`
     - :const:`true` = damap Jacobian (default); :const:`false` = finite-difference with 7 particles. See :doc:`DAmap <mad_mod_diffmap>`.
     - ``mapdef = false``

**Integration** (see :ref:`ch.phy.intrg`)

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`method`
     - :const:`nil`
     - Integration order 1–8, or named string (:literal:`'teapot'`, …). See :ref:`ch.phy.intrg`.
     - ``method = 'teapot'``
   * - :literal:`model`
     - :const:`nil`
     - Integration model: :literal:`'TKT'` or :literal:`'DKD'`. See :ref:`ch.phy.intrg`. [#f2]_
     - ``model = 'DKD'``
   * - :literal:`secnmul`
     - :const:`nil`
     - Curved-multipole expansion order for bends. See :ref:`ch.phy.intrg`.
     - ``secnmul = -1``
   * - :literal:`fringe`
     - :const:`nil`
     - Enable fringe fields (:const:`true` / bitmask).
     - ``fringe = false``
   * - :literal:`frngmax`
     - :const:`nil`
     - Maximum multipole order for fringe-field expansions.
     - ``frngmax = 4``
   * - :literal:`misalign`
     - :const:`nil`
     - Apply **error** misalignments from :literal:`seq:ealign`. Permanent :literal:`elm.misalign` is always applied.
     - ``misalign = true``
   * - :literal:`aperture`
     - :const:`nil`
     - Default aperture for elements without one.
     - ``aperture = {kind='circle', 0.05}``
   * - :literal:`radiate`
     - :const:`nil`
     - Radiation mode (collapsed to damping for Newton iterations). See :ref:`ch.phy.radia`.
     - ``radiate = true``
   * - :literal:`nocavity`
     - :const:`nil`
     - Disable RF cavities (5D tracking).
     - ``nocavity = true``
   * - :literal:`totalpath`
     - :const:`nil`
     - Use total path for :literal:`t`.
     - ``totalpath = true``
   * - :literal:`implicit`
     - :const:`nil`
     - Slice implicit elements.
     - ``implicit = true``
   * - :literal:`cmap`
     - :const:`nil`
     - Use C/C++ maps when available.
     - ``cmap = false``
   * - :literal:`ptcmodel`
     - :const:`nil`
     - Backend: :const:`nil` = MAD-NG, :const:`true` = PTC, :const:`false` = MAD-X. [#f3]_
     - ``ptcmodel = true``

**Closed orbit solver**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`coitr`
     - :const:`25`
     - Maximum Newton iterations. Objects not converged are tagged :literal:`"unstable"`.
     - ``coitr = 5``
   * - :literal:`cotol`
     - :const:`1e-8`
     - Convergence tolerance :math:`|\Delta X|`. Converged objects tagged :literal:`"stable"`.
     - ``cotol = 1e-6``
   * - :literal:`costp`
     - :const:`1e-8`
     - Finite-difference step scale when :literal:`mapdef=false`. Falls back to :literal:`max(costp,cotol)` for zero-norm objects.
     - ``costp = 1e-10``
   * - :literal:`O1`
     - :const:`0`
     - Coordinates :literal:`{x,px,y,py,t,pt}` subtracted from the final converged orbit.
     - ``O1 = {t=100, pt=10}``

**Output and saving** (see :ref:`ch.phy.intrg` for selector strings)

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`save`
     - :const:`false`
     - When to save rows: :const:`false` = none (default), :const:`true` = at exit, or selector string.
     - ``save = true``
   * - :literal:`aper`
     - :const:`nil`
     - When to check aperture, or selector string.
     - ``aper = 'atbody'``
   * - :literal:`observe`
     - :const:`nil`
     - Save only :meth:`:is_observed` elements every :math:`n` turns.
     - ``observe = 0``
   * - :literal:`savesel`
     - :const:`nil`
     - Predicate :literal:`(elm,mflw,lw,islc)` to filter saved elements.
     - ``savesel = \e -> mylist[e.name]``
   * - :literal:`savemap`
     - :const:`nil`
     - Save damap in column :literal:`__map`.
     - ``savemap = true``

**Action hooks** (see :ref:`ch.phy.intrg` for slice index convention)

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`atentry`
     - :const:`nil`
     - :literal:`(elm,mflw,0,-1)` — called at element entry (slice :const:`-1`).
     - ``atentry = myaction``
   * - :literal:`atslice`
     - :const:`nil`
     - :literal:`(elm,mflw,lw,islc)` — called at each body slice (slice :const:`0`…:math:`N`).
     - ``atslice = myaction``
   * - :literal:`atexit`
     - :const:`nil`
     - :literal:`(elm,mflw,0,-2)` — called at element exit (slice :const:`-2`).
     - ``atexit = myaction``
   * - :literal:`atsave`
     - :const:`nil`
     - :literal:`(elm,mflw,lw,islc)` — called when a row is saved.
     - ``atsave = myaction``
   * - :literal:`ataper`
     - :const:`nil`
     - :literal:`(elm,mflw,lw,islc)` — called at aperture check; sets :literal:`status="lost"` for lost objects.
     - ``ataper = myaction``
   * - :literal:`atdebug`
     - :const:`nil`
     - :literal:`(elm,mflw,lw,[msg],[...])` — called at map entry/exit. Defaults to :literal:`mdump` if :literal:`debug >= 4`.
     - ``atdebug = myaction``
   * - :literal:`apersel`
     - :const:`nil`
     - Predicate to suppress aperture check per element.
     - ``apersel = \e -> e.kind ~= 'marker'``

**Misc**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`info`
     - :const:`nil`
     - Verbosity level for console output.
     - ``info = 2``
   * - :literal:`debug`
     - :const:`nil`
     - Debug output level.
     - ``debug = 2``
   * - :literal:`usrdef`
     - :const:`nil`
     - User data attached to the mflow and passed to element maps.
     - ``usrdef = {myvar=val}``
   * - :literal:`mflow`
     - :const:`nil`
     - Existing mflow to continue (reuses setup; only :literal:`nstep`, :literal:`info`, :literal:`debug` are refreshed).
     - ``mflow = mflw0``

The :var:`cofind` command stops when all particles or damaps are tagged as :literal:`"stable"`, :literal:`"unstable"`, :literal:`"singular"`, or :literal:`"lost"`. It returns the following objects:

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Return
     - Description
   * - :literal:`mtbl`
     - An *mtable* from the underlying :var:`track` command where :literal:`status` may also be :literal:`"stable"`, :literal:`"unstable"`, or :literal:`"singular"`.
   * - :literal:`mflw`
     - An *mflow* from :var:`track`. Particles/damaps are tagged and ordered by :literal:`"stable"`, :literal:`"unstable"`, :literal:`"singular"`, :literal:`"lost"`, then :literal:`id`. Each result also carries solver metadata fields :literal:`id`, :literal:`status`, :literal:`rank`, and :literal:`coitr` alongside the coordinates :literal:`x`, :literal:`px`, :literal:`y`, :literal:`py`, :literal:`t`, :literal:`pt`.

The closed-orbit coordinates are converged against :literal:`cotol`. In other words, users should validate the returned orbit against :literal:`cotol` (or a tighter user-specified value), not against machine epsilon.

Cofind mtable
-------------
.. _sec.cofind.mtable:

The :var:`cofind` command returns the :var:`track` *mtable* unmodified except for the :literal:`status` column. The tracked objects id will appear once per iteration at the :literal:`\$end` marker, and other defined observation points if any, until they are removed from the list of tracked objects.

Examples
--------

The example below was working for MAD-NG version :literal:`1.1.13_P`.

Minimal closed-orbit search on the saved PSB sequence:

.. literalinclude:: ../../verified_examples/cofind_minimal.mad
   :language: mad

In the validated run, :literal:`mf[1].status` was :literal:`"stable"`. The
script keeps the returned closed-orbit vector in :literal:`xco` for reuse in
later tracking or matching steps, and it writes a compact
:literal:`cofind_minimal.tfs` file from the returned *mtable*.

The companion fields :literal:`coitr` and :literal:`rank` report the iteration
at which the orbit converged and the rank of the linear system solved by the
Newton step.

When :literal:`save=true`, the returned *mtable* records one row per saved
observation and iteration until each tracked object is classified. That makes
:var:`cofind` useful both as a solver and as a diagnostic trace of convergence
or failure.

.. [#f1] Initial coordinates :var:`X0` may override it by providing a beam per particle or damap.
.. [#f2] The :literal:`TKT` scheme (Yoshida) is automatically converted to the :literal:`MKM` scheme (Boole) when appropriate.
.. [#f3] In all cases, MAD-NG uses PTC setup :expr:`time=true, exact=true`.
