Track
=====
.. _ch.cmd.track:

The :var:`track` command provides a simple interface to the *dynamic* tracking code. [#f1]_ The dynamic tracking can be used to track the particles in the :ref:`local reference system <sec.phy.lrs>` while running through the elements of a sequence. The particles coordinates can be expressed in the :ref:`global reference system <sec.phy.grs>` by changing from the local to the global frames using the information delivered by the :doc:`survey <mad_cmd_survey>` command.


.. code-block:: lua
    :caption: Synopsis of the :var:`track` command with default setup.
    :name: fig-track-synop

    mtbl, mflw [, eidx] = track {
        sequence=sequ,   -- sequence (required)
        beam=nil,        -- beam (or sequence.beam, required)
        range=nil,       -- range of tracking (or sequence.range)
        dir=1,           -- s-direction of tracking (1 or -1)
        s0=0,            -- initial s-position offset [m]
        X0=0,            -- initial coordinates (or damap(s), or beta block(s))
        O0=0,            -- initial coordinates of reference orbit
        deltap=0,        -- initial deltap(s)
        nturn=1,         -- number of turns to track
        nstep=-1,        -- number of elements to track
        nslice=1,        -- number of slices (or weights) for each element
        method=4,        -- method or order for integration (1 to 8)
        model='TKT',     -- model for integration ('DKD' or 'TKT')
        mapdef=false,    -- setup for damap (or list of, true => {})
        secnmul=false,   -- curved-multipole expansion for sbends
        implicit=false,  -- slice implicit elements too (e.g. plots)
        misalign=false,  -- consider misalignments
        aperture=false,  -- default aperture
        fringe=true,     -- enable fringe fields (see element.flags.fringe)
        frngmax=2,       -- maximum multipole fringe field order
        radiate=false,   -- radiate at slices
        taper=false,     -- tapering compensation
        nocavity=false,  -- disable rfcavities
        totalpath=false, -- variable 't' is the totalpath
        cmap=true,       -- use C/C++ maps when available
        ptcmodel=nil,    -- nil=MADNG, true=PTC, false=MADX
        save=true,       -- create mtable and save results
        aper=true,       -- check for aperture
        observe=1,       -- save only in observed elements (every n turns)
        reserve=0,       -- preallocate output rows (0 => guess)
        savesel=fnil,    -- save selector (predicate)
        savemap=false,   -- save damap in the column __map
        atentry=fnil,    -- action called when entering an element
        atslice=fnil,    -- action called after each element slices
        atexit=fnil,     -- action called when exiting an element
        atsave=fnil,     -- action called when saving in mtable
        ataper=fnil,     -- action called when checking for aperture
        atdebug=fnil,    -- action called when debugging the element maps
        apersel=fnil,    -- aperture selector (predicate)
        coitr=nil,       -- closed-orbit iteration limit
        cotol=nil,       -- closed-orbit tolerance
        costp=nil,       -- finite-difference scale for closed-orbit Jacobian
        O1=nil,          -- optional final closed-orbit translation
        info=nil,        -- information level (output on terminal)
        debug=nil,       -- debug information level (output on terminal)
        usrdef=nil,      -- user defined data attached to the mflow
        mflow=nil,       -- mflow, exclusive with other attributes except nstep
    }

The :var:`track` command format is summarized in :numref:`fig-track-synop`, including the default setup of the attributes.

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
     - Sequence to track.
     - ``sequence = lhcb1``
   * - :literal:`beam`
     - :const:`nil`
     - Reference beam (or :literal:`seq.beam`). [#f2]_
     - ``beam = mybeam``
   * - :literal:`range`
     - :const:`nil`
     - Sub-range of the sequence (or :literal:`seq.range`).
     - ``range = "IP1/IP5"``
   * - :literal:`dir`
     - :const:`1`
     - Tracking direction: :const:`1` forward, :const:`-1` backward.
     - ``dir = -1``
   * - :literal:`s0`
     - :const:`0`
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
     - :const:`0`
     - Initial coordinates :literal:`{x,px,y,py,t,pt}`, damap(s), or beta block(s). Each object may contain a :var:`beam` override or :literal:`nosave=true`.
     - ``X0 = {x=1e-3, px=-1e-5}``
   * - :literal:`O0`
     - :const:`0`
     - Reference orbit. Set :literal:`cofind=true` on the table to search for the closed orbit.
     - ``O0 = {x=1e-4, py=1e-5}``
   * - :literal:`deltap`
     - :const:`0`
     - Initial :math:`\delta_p` offset(s) added to :literal:`pt` via the beam.
     - ``deltap = 1e-3``
   * - :literal:`nturn`
     - :const:`1`
     - Number of turns to track.
     - ``nturn = 1024``
   * - :literal:`nstep`
     - :const:`-1`
     - Number of elements to track (:const:`-1` = all).
     - ``nstep = 10``

**Integration** (see :ref:`ch.phy.intrg`)

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`method`
     - :const:`4`
     - Integration order 1–8, or named string (:literal:`'simple'`, :literal:`'teapot'`, :literal:`'teapot2/3/4'`, …). See :ref:`ch.phy.intrg`. [#f3]_
     - ``method = 'teapot'``
   * - :literal:`model`
     - :literal:`'TKT'`
     - Integration model: :literal:`'TKT'` (Thick-Kick-Thick) or :literal:`'DKD'` (Drift-Kick-Drift). See :ref:`ch.phy.intrg`.
     - ``model = 'DKD'``
   * - :literal:`nslice`
     - :const:`1`
     - Slices per element: number, list of relative positions, or callable :literal:`(elm,mflw,lw)`. Overridable per-element.
     - ``nslice = 5``
   * - :literal:`mapdef`
     - :const:`false`
     - DA map setup: :const:`true` ⇒ :literal:`{}`, or a damap spec. See :doc:`DAmap <mad_mod_diffmap>`.
     - ``mapdef = {xy=2, pt=5}``
   * - :literal:`secnmul`
     - :const:`false`
     - Curved-multipole expansion order for bends. :const:`false`=off, :const:`-1`=auto, positive N=fixed. See :ref:`ch.phy.intrg`.
     - ``secnmul = -1``
   * - :literal:`fringe`
     - :const:`true`
     - Enable fringe fields (:const:`true` / bitmask).
     - ``fringe = false``
   * - :literal:`frngmax`
     - :const:`2`
     - Maximum multipole order for fringe-field expansions.
     - ``frngmax = 4``
   * - :literal:`misalign`
     - :const:`false`
     - Apply **error** misalignments from :literal:`seq:ealign`. Permanent :literal:`elm.misalign` is always applied.
     - ``misalign = true``
   * - :literal:`aperture`
     - :const:`false`
     - Default aperture for elements without one (falls back to :literal:`seq.aperture`).
     - ``aperture = {kind='circle', 0.05}``
   * - :literal:`radiate`
     - :const:`false`
     - Synchrotron radiation: :const:`true` = damping, or :literal:`'damping'`, :literal:`'quantum'`, :literal:`'photon'` (append :literal:`'+'` to keep bookkeeping). See :ref:`ch.phy.radia`.
     - ``radiate = 'quantum'``
   * - :literal:`taper`
     - :const:`false`
     - Tapering compensation: :const:`true` = 3 passes, or positive number.
     - ``taper = true``
   * - :literal:`nocavity`
     - :const:`false`
     - Disable RF cavities (enforces 5D tracking).
     - ``nocavity = true``
   * - :literal:`totalpath`
     - :const:`false`
     - Use total path for :literal:`t` instead of local path.
     - ``totalpath = true``
   * - :literal:`implicit`
     - :const:`false`
     - Slice implicit elements (e.g. drifts) for smooth plotting.
     - ``implicit = true``
   * - :literal:`cmap`
     - :const:`true`
     - Use C/C++ maps when available.
     - ``cmap = false``
   * - :literal:`ptcmodel`
     - :const:`nil`
     - Backend: :const:`nil` = MAD-NG, :const:`true` = PTC, :const:`false` = MAD-X. [#f7]_
     - ``ptcmodel = true``

**Output and saving** (see :ref:`ch.phy.intrg` for selector strings)

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`save`
     - :const:`true`
     - When to save rows: :const:`true` = at exit, :const:`false` = none, or a slice-selector string. See :ref:`ch.phy.intrg`.
     - ``save = 'atbody'``
   * - :literal:`aper`
     - :const:`true`
     - When to check aperture: :const:`true` = at last body slice, :const:`false` = off, or selector string.
     - ``aper = false``
   * - :literal:`observe`
     - :const:`1`
     - Save only :meth:`:is_observed` elements every :math:`n` turns. :const:`0` = save all elements.
     - ``observe = 0``
   * - :literal:`reserve`
     - :const:`0`
     - Pre-allocate output rows (:const:`0` = auto-guess).
     - ``reserve = 50000``
   * - :literal:`savesel`
     - :literal:`fnil`
     - Predicate :literal:`(elm,mflw,lw,islc)` to filter saved elements.
     - ``savesel = \e -> mylist[e.name]``
   * - :literal:`savemap`
     - :const:`false`
     - Save damap in column :literal:`__map` of the mtable.
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
     - :literal:`fnil`
     - :literal:`(elm,mflw,0,-1)` — called at element entry (slice :const:`-1`).
     - ``atentry = myaction``
   * - :literal:`atslice`
     - :literal:`fnil`
     - :literal:`(elm,mflw,lw,islc)` — called at each body slice (slice :const:`0`…:math:`N`).
     - ``atslice = myaction``
   * - :literal:`atexit`
     - :literal:`fnil`
     - :literal:`(elm,mflw,0,-2)` — called at element exit (slice :const:`-2`).
     - ``atexit = myaction``
   * - :literal:`atsave`
     - :literal:`fnil`
     - :literal:`(elm,mflw,lw,islc)` — called when a row is saved to the mtable.
     - ``atsave = myaction``
   * - :literal:`ataper`
     - :literal:`fnil`
     - :literal:`(elm,mflw,lw,islc)` — called at aperture check; sets :literal:`status="lost"` for lost particles.
     - ``ataper = myaction``
   * - :literal:`atdebug`
     - :literal:`fnil`
     - :literal:`(elm,mflw,lw,[msg],[...])` — called at map entry/exit during integration. Defaults to :literal:`mdump` if :literal:`debug >= 4`.
     - ``atdebug = myaction``
   * - :literal:`apersel`
     - :literal:`fnil`
     - Predicate to suppress aperture check per element.
     - ``apersel = \e -> e.kind ~= 'marker'``

**Closed orbit and misc**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`coitr`
     - :const:`nil`
     - Maximum closed-orbit Newton iterations (inherited from cofind helper if nil).
     - ``coitr = 25``
   * - :literal:`cotol`
     - :const:`nil`
     - Closed-orbit convergence tolerance (inherited if nil).
     - ``cotol = 1e-8``
   * - :literal:`costp`
     - :const:`nil`
     - Finite-difference scale for closed-orbit Jacobian (inherited if nil).
     - ``costp = 1e-8``
   * - :literal:`O1`
     - :const:`nil`
     - Orbit translation subtracted from the final closed-orbit.
     - ``O1 = {t=100, pt=10}``
   * - :literal:`info`
     - :const:`nil`
     - Verbosity level for console output.
     - ``info = 2``
   * - :literal:`debug`
     - :const:`nil`
     - Debug output level (≥4 enables :literal:`mdump` in :literal:`atdebug`).
     - ``debug = 2``
   * - :literal:`usrdef`
     - :const:`nil`
     - User data attached to the mflow and passed to element maps.
     - ``usrdef = {myvar=val}``
   * - :literal:`mflow`
     - :const:`nil`
     - Existing mflow to continue (reuses setup; only :literal:`nstep`, :literal:`info`, :literal:`debug` are refreshed).
     - ``mflow = mflw0``


The :var:`track` command returns the following objects:

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Return
     - Description
   * - :literal:`mtbl`
     - An *mtable* corresponding to the TFS table of the :var:`track` command.
   * - :literal:`mflw`
     - An *mflow* corresponding to the map flow of the :var:`track` command.
   * - :literal:`eidx`
     - An optional *number* corresponding to the last tracked element index in the sequence when :literal:`nstep` stopped the command before the end of the :literal:`range`.


Track mtable
------------
.. _sec.track.mtable:

The :var:`track` command returns a *mtable* where the information described hereafter is the default list of fields written to the TFS files. [#f4]_

The header of the *mtable* contains the fields in the default order:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Field
     - Description
   * - :literal:`name`
     - Name of the command, e.g. :literal:`"track"`.
   * - :literal:`type`
     - Type of the mtable, i.e. :literal:`"track"`.
   * - :literal:`origin`
     - Application origin, e.g. :literal:`"MAD 1.0.0 OSX 64"`.
   * - :literal:`date`
     - Creation date, e.g. :literal:`"27/05/20"`.
   * - :literal:`time`
     - Creation time, e.g. :literal:`"19:18:36"`.
   * - :literal:`refcol`
     - Reference column for the mtable dictionary, e.g. :literal:`"name"`.
   * - :literal:`direction`
     - Value of the command attribute :literal:`dir`.
   * - :literal:`observe`
     - Value of the command attribute :literal:`observe`.
   * - :literal:`implicit`
     - Value of the command attribute :literal:`implicit`.
   * - :literal:`misalign`
     - Value of the command attribute :literal:`misalign`.
   * - :literal:`radiate`
     - Value of the command attribute :literal:`radiate`.
   * - :literal:`particle`
     - Reference beam particle name.
   * - :literal:`energy`
     - Reference beam energy.
   * - :literal:`deltap`
     - Value of the command attribute :literal:`deltap`.
   * - :literal:`lost`
     - Number of lost particle(s) or damap(s).

The core of the *mtable* contains the columns in the default order:

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Column
     - Description
   * - :literal:`name`
     - Name of the element.
   * - :literal:`kind`
     - Kind of the element.
   * - :literal:`s`
     - :math:`s`-position at the end of the element slice.
   * - :literal:`l`
     - Length from the start of the element to the end of the slice.
   * - :literal:`id`
     - Index of the particle or damap as provided in :literal:`X0`.
   * - :literal:`x`
     - Local coordinate :math:`x` at the :math:`s`-position.
   * - :literal:`px`
     - Local coordinate :math:`p_x` at the :math:`s`-position.
   * - :literal:`y`
     - Local coordinate :math:`y` at the :math:`s`-position.
   * - :literal:`py`
     - Local coordinate :math:`p_y` at the :math:`s`-position.
   * - :literal:`t`
     - Local coordinate :math:`t` at the :math:`s`-position.
   * - :literal:`pt`
     - Local coordinate :math:`p_t` at the :math:`s`-position.
   * - :literal:`pc`
     - Reference beam :math:`P_0c` in which :math:`p_t` is expressed.
   * - :literal:`ktap`
     - Tapering compensation factor at the current tracking position.
   * - :literal:`slc`
     - Slice index ranging from :literal:`-2` to :literal:`nslice`. See :ref:`ch.phy.intrg`.
   * - :literal:`turn`
     - Turn number.
   * - :literal:`tdir`
     - :math:`t`-direction of the tracking in the element.
   * - :literal:`eidx`
     - Index of the element in the sequence.
   * - :literal:`status`
     - Status of the particle or damap.
   * - :literal:`__map`
     - Damap at the :math:`s`-position (only if :literal:`savemap=true`). [#f6]_

The mtable also carries the in-memory attributes :literal:`taper`, :literal:`range` and the protected sequence handle :literal:`__seq`, but they are not part of the default header list written to TFS files.


Dynamical tracking
------------------

:numref:`fig track trkslc` presents the scheme of the dynamical tracking through an element sliced with :literal:`nslice=3`. The actions :literal:`atentry` (index :literal:`-1`), :literal:`atslice` (indexes :literal:`0..3`), and :literal:`atexit` (index :literal:`-2`) are reversed between the forward tracking (:literal:`dir=1` with increasing :math:`s`-position) and the backward tracking (:literal:`dir=-1` with decreasing :math:`s`-position). By default, the action :literal:`atsave` is attached to the exit slice and the action :literal:`ataper` is attached to the last slice just before exit, i.e. to the last :literal:`atslice` action in the tilted frame, and hence they are also both reversed in the backward tracking.

.. _fig track trkslc:

.. figure:: fig/dyna-trck-slice-crop.png
    :align: center
    :figwidth: 98%

    Dynamical tracking with slices.

Slicing
"""""""

The slicing can take three different forms:

    *	 A *number* of the form :expr:`nslice=N` that specifies the number of slices with indexes :math:`0`..:math:`N`. This defines a uniform slicing with slice length :math:`l_{\text{slice}} = l_{\text{elem}}/N`.

    *	 An *iterable* of the form :literal:`nslice={lw_1,lw_2,..,lw_N}` with :math:`\sum_i lw_i=1` that specifies the fraction of length of each slice with indexes :math:`0` .. :math:`N` where :math:`N`\ =\ :literal:`#nslice`. This defines a non-uniform slicing with a slice length of :math:`l_i = lw_i\times l_{\text{elem}}`.

    *	 A *callable* :literal:`(elm, mflw, lw)` returning one of the two previous forms of slicing. The arguments are in order, the current element, the tracked map flow, and the length weight of the step, which should allow to return a user-defined element-specific slicing.


The surrounding :math:`P` and :math:`P^{-1}` maps represent the patches applied around the body of the element to change the frames, after the :literal:`atentry` and before the :literal:`atexit` actions:

    *	 The misalignment of the element to move from the *global frame* to the *element frame* if the command attribute :literal:`misalign` is set to :const:`true`.

    *	 The tilt of the element to move from the element frame to the *titled frame* if the element attribute :literal:`tilt` is non-zero. The :literal:`atslice` actions take place in this frame.

The *map frame* is specific to some maps while tracking through the body of the element. In principle, the map frame is not visible to the user, only to the integrator. For example, a quadrupole with both :literal:`k1` and :literal:`k1s` defined will have a *map frame* tilted by the angle :math:`\alpha=-\frac{1}{2}\tan^{-1}\frac{k1s}{k1}` attached to its thick map, i.e. the focusing matrix handling only :math:`\tilde{k}_1 = \sqrt{k1^2+k1s^2}`, but not to its thin map, i.e. the kick from all multipoles (minus :literal:`k1` and :literal:`k1s`) expressed in the *tilted frame*\ , during the integration steps.

Sub-elements
""""""""""""

The :var:`track` command takes sub-elements into account. In this case, the slicing specification is taken between sub-elements, e.g. 3 slices with 2 sub-elements gives a final count of 9 slices. It is possible to adjust the number of slices between sub-elements with the third form of slicing specifier, i.e. by using a callable where the length weight argument is between the current (or the end of the element) and the last sub-elements (or the start of the element).

Particles status
""""""""""""""""

The :var:`track` command initializes the map flow with particles or damaps or both, depending on the attributes :var:`X0` and :literal:`mapdef`. The :literal:`status` attribute of each particle or damap will be set to one of :literal:`"Xset"`, :literal:`"Mset"`, and :literal:`"Aset"` to track the origin of its initialization: coordinates, damap, or normalizing damap (normal form or beta block). After the tracking, some particles or damaps may have the status :literal:`"lost"` and their number being recorded in the counter :literal:`lost` from TFS table header. Other commands like :var:`cofind` or :var:`twiss` may add extra tags to the status value, like :literal:`"stable"`, :literal:`"unstable"` and :literal:`"singular"`.

Typical Workflows
-----------------

**Single-particle, one-turn tracking**

The most common first use: track one particle for one turn and inspect the
exit coordinates.

.. literalinclude:: ../../verified_examples/track_minimal.mad
   :language: mad

**Multi-particle tracking**

Pass a list of coordinate mappables to :literal:`X0` to track several particles
at once; each gets its own :literal:`id` in the output table.

.. code-block:: mad

   trk = track {
     sequence = seq,
     X0       = { {x=0}, {x=1e-3}, {x=2e-3} },
     nturn    = 1,
   }

**Selecting observation points**

Use :literal:`observe=0` to record at every element, or mark specific elements
with :literal:`:is_observed` and set :literal:`observe=1` to record only there:

.. code-block:: mad

   trk = track {
     sequence = seq,
     X0       = { x=1e-3 },
     nturn    = 10,
     observe  = 0,   -- record at every element, every turn
   }

**DA map tracking**

Set :literal:`mapdef=true` (or a damap specification) to track DA maps instead
of single particle coordinates.  The result columns contain GTPSA polynomials.

.. code-block:: mad

   trk = track {
     sequence = seq,
     X0       = damap {},
     nturn    = 1,
     mapdef   = true,
     savemap  = true,
   }

Interpreting Outputs
--------------------

After a successful :literal:`track` call the two returned objects are:

**mtbl** (the TFS table)

* Each row corresponds to one observation point visit (element × turn × particle).
* The :literal:`id` column identifies which entry in :literal:`X0` produced the row.
* The :literal:`turn` column counts turns (starting at 1).
* The :literal:`slc` column holds the slice index at which the row was saved.
  The default (:literal:`save=true`) fires at exit (:const:`-2`).  See
  :ref:`ch.phy.intrg` for the complete slice index table and all valid
  :literal:`save` selector strings (:literal:`"atentry"`, :literal:`"atslice"`,
  :literal:`"atbody"`, :literal:`"atbound"`, :literal:`"atall"`, …).
* The :literal:`status` column is :literal:`"Xset"` for coordinate-initialised
  particles and :literal:`"lost"` for particles that hit an aperture.
* The header field :literal:`lost` counts the total number of lost items.
* Access column arrays as :literal:`trk["x"]`, scalars as :literal:`trk.lost`.

**mflw** (the map flow)

The map flow carries internal state and can be passed back to a subsequent
:literal:`track` call via :literal:`mflow=mflw` to continue tracking without
re-reading the sequence.

Common Pitfalls
---------------

* **Empty table**: the default is :literal:`observe=1`, which saves only elements
  explicitly marked as observed (:meth:`:is_observed`).  If no elements carry
  that mark you get an empty table.  Set :literal:`observe=0` to save every
  element, or mark the elements you care about with :literal:`seq["name"]:observe(MAD.element.flags.observed)`.
* **Missing beam**: :literal:`track` requires a beam attached to the sequence or
  passed explicitly.  The error is raised immediately.
* **Lost particles at turn 1**: a particle outside the physical aperture is lost
  on the first element that has an aperture definition.  Reduce :literal:`X0`
  amplitudes or disable aperture checking with :literal:`aper=false`.
* **Coordinate convention**: MAD-NG uses :math:`(x, p_x, y, p_y, t, p_t)` in
  normalised momenta.  The fifth variable :literal:`t` is the local path
  deviation :math:`-c\,\Delta t` by default; set :literal:`totalpath=true` for
  the total path instead.
* **5D vs 6D**: RF cavities are active by default.  To enforce 5D (no energy
  change), set :literal:`nocavity=true`.

Examples
--------

See :doc:`common_tasks` for additional workflow examples.


.. rubric:: Footnotes

.. [#f1] MAD-NG implements only two tracking codes denominated the *geometric* and the *dynamic* tracking.
.. [#f2] Initial coordinates :var:`X0` may override it by providing per particle or damap beam.
.. [#f3] The :literal:`TKT` scheme (Yoshida) is automatically converted to the :literal:`MKM` scheme (Boole) when approriate.
.. [#f7] In all cases, MAD-NG uses PTC setup :literal:`time=true, exact=true`.
.. [#f4] The output of mtable in TFS files can be fully customized by the user.
.. [#f6] Fields and columns starting with two underscores are protected data and never saved to TFS files.
