Twiss
=====
.. _ch.cmd.twiss:

The :var:`twiss` command provides a simple interface to compute the optical functions around an orbit on top of the :var:`track` command, and the :var:`cofind` command if the search for closed orbits is requested.

In practical advanced workflows, :var:`twiss` is also used as the main entry
point for derivative-driven optics and resonance-driving-term calculations
through :literal:`X0`, :literal:`trkopt`, and :literal:`trkrdt`. See
:doc:`parametric_optics_and_rdts`.


The :var:`twiss` command format is summarized in :numref:`fig-twiss-synop`, including the default setup of the attributes. Most of these attributes are set to :const:`nil` by default, meaning that :var:`twiss` relies on the :var:`track` and the :var:`cofind` commands defaults.

.. code-block:: lua
	:name: fig-twiss-synop
	:caption: Synopsis of the :var:`twiss` command with default setup.


	mtbl, mflw [, eidx] = twiss {
		sequence=sequ,  -- sequence (required)
		beam=nil, 	-- beam (or sequence.beam, required)
		range=nil,  	-- range of tracking (or sequence.range)
		dir=nil,  	-- s-direction of tracking (1 or -1)
		s0=nil,  	-- initial s-position offset [m]
		X0=nil,  	-- initial coordinates (or damap(s), or beta block(s))
		O0=nil,  	-- initial coordinates of reference orbit
		deltap=nil,  	-- initial deltap(s)
		chrom=false,  	-- compute chromatic functions by finite difference
		coupling=false, -- compute optical functions for non-diagonal modes
		trkopt=false,  	-- compute selected parametric optical functions
		trkrdt=false,  	-- compute selected resonance driving terms
		nturn=nil,  	-- number of turns to track
		nstep=nil,  	-- number of elements to track
		nslice=nil,  	-- number of slices (or weights) for each element
		method=nil,  	-- method or order for integration (1 to 8)
		model=nil,  	-- model for integration ('DKD' or 'TKT')
		mapdef=2,  	-- setup for damap (or list of, true => {xy=1})
		secnmul=nil,  	-- curved-multipole expansion for bends
		implicit=nil,  	-- slice implicit elements too (e.g. plots)
		misalign=nil,  	-- consider misalignment
		aperture=nil,  	-- default aperture
		fringe=nil,  	-- enable fringe fields (see element.flags.fringe)
		frngmax=nil,  	-- maximum multipole fringe field order
		radiate=nil,  	-- radiate at slices
		nocavity=nil,  	-- disable rfcavities
		totalpath=nil,  -- variable 't' is the totalpath
		cmap=nil,  	-- use C/C++ maps when available
		ptcmodel=nil,  	-- nil=MADNG, true=PTC, false=MADX
		save=true,  	-- create mtable and save results
		aper=nil,  	-- check for aperture
		observe=0,  	-- save only in observed elements (every n turns)
		savesel=nil,  	-- save selector (predicate)
		savemap=nil,  	-- save damap in the column __map
		saveanf=nil,  	-- save analysed normal form in the column __nf
		atentry=nil,  	-- action called when entering an element
		atslice=nil,  	-- action called after each element slices
		atexit=nil,  	-- action called when exiting an element
		ataper=nil,  	-- action called when checking for aperture
		atsave=nil,  	-- action called when saving in mtable
		atdebug=nil,  	-- action called when debugging the element maps
		apersel=nil,  	-- aperture selector (predicate)
		costp=nil,  	-- finite-difference scale for Jacobian
		coitr=nil,  	-- maximum number of iterations
		cotol=nil,  	-- closed orbit tolerance (i.e.|dX|)
		O1=nil,  	-- optional final coordinates translation
		info=nil,  	-- information level (output on terminal)
		debug=nil, 	-- debug information level (output on terminal)
		usrdef=nil,  	-- user defined data attached to the mflow
		mflow=nil,  	-- mflow, exclusive with other attributes
	}

The :var:`twiss` command supports the following attributes:

.. _twiss.attr:

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
     - Sequence to analyse.
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
     - Initial coordinates :literal:`{x,px,y,py,t,pt}`, damap(s), or beta0 block(s). A :var:`beam` override and :literal:`nosave=true` per object are supported.
     - ``X0 = {x=1e-3}``
   * - :literal:`O0`
     - :const:`nil`
     - Reference orbit. Set :literal:`cofind=true` on the table to search.
     - ``O0 = {x=1e-4}``
   * - :literal:`deltap`
     - :const:`nil`
     - Initial :math:`\delta_p` offset(s) added to :literal:`pt`.
     - ``deltap = 1e-3``
   * - :literal:`nturn`
     - :const:`nil`
     - Number of turns (default 1 via :var:`track`).
     - ``nturn = 2``
   * - :literal:`nstep`
     - :const:`nil`
     - Number of elements (:const:`-1` = all).
     - ``nstep = 10``

**Optics**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`chrom`
     - :const:`false`
     - Compute chromatic functions by finite difference (:math:`\delta_p = 10^{-6}`).
     - ``chrom = true``
   * - :literal:`coupling`
     - :const:`false`
     - Compute coupling optical functions in normalised forms.
     - ``coupling = true``
   * - :literal:`trkopt`
     - :const:`false`
     - List of parametric optical-function names to track. See :doc:`parametric_optics_and_rdts`.
     - ``trkopt = {'beta11_01'}``
   * - :literal:`trkrdt`
     - :const:`false`
     - List of resonance driving term names (must start with :literal:`'f'`). See :doc:`parametric_optics_and_rdts`.
     - ``trkrdt = {'f3000'}``
   * - :literal:`mapdef`
     - :const:`2`
     - DA map order: :const:`2` forces second-order for normal-form analysis, :const:`true` ⇒ :literal:`{xy=1}`. See :doc:`DAmap <mad_mod_diffmap>`.
     - ``mapdef = {xy=2, pt=5}``

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
     - Integration model: :literal:`'TKT'` or :literal:`'DKD'`. See :ref:`ch.phy.intrg`. [#f7]_
     - ``model = 'DKD'``
   * - :literal:`nslice`
     - :const:`nil`
     - Slices per element: number, list, or callable :literal:`(elm,mflw,lw)`.
     - ``nslice = 5``
   * - :literal:`secnmul`
     - :const:`nil`
     - Curved-multipole expansion order. See :ref:`ch.phy.intrg`.
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
     - Radiation mode (collapsed to damping for closed-orbit/OTM stages). See :ref:`ch.phy.radia`.
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
     - Slice implicit elements for smooth plotting.
     - ``implicit = true``
   * - :literal:`cmap`
     - :const:`nil`
     - Use C/C++ maps when available.
     - ``cmap = false``
   * - :literal:`ptcmodel`
     - :const:`nil`
     - Backend: :const:`nil` = MAD-NG, :const:`true` = PTC, :const:`false` = MAD-X. [#f8]_
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
     - When to save rows: :const:`true` = at exit, :const:`false` = none, or selector string. See :ref:`ch.phy.intrg`.
     - ``save = false``
   * - :literal:`aper`
     - :const:`nil`
     - When to check aperture, or selector string.
     - ``aper = 'atbody'``
   * - :literal:`observe`
     - :const:`0`
     - Save all elements (:const:`0`) or only :meth:`:is_observed` every :math:`n` turns.
     - ``observe = 1``
   * - :literal:`savesel`
     - :const:`nil`
     - Predicate :literal:`(elm,mflw,lw,islc)` to filter saved elements.
     - ``savesel = \e -> mylist[e.name]``
   * - :literal:`savemap`
     - :const:`nil`
     - Save damap in column :literal:`__map`.
     - ``savemap = true``
   * - :literal:`saveanf`
     - :const:`nil`
     - Save analysed normal form in column :literal:`__nf`.
     - ``saveanf = true``

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
     - :literal:`(elm,mflw,lw,islc)` — called at aperture check.
     - ``ataper = myaction``
   * - :literal:`atdebug`
     - :const:`nil`
     - :literal:`(elm,mflw,lw,[msg],[...])` — called at map entry/exit. Defaults to :literal:`mdump` if :literal:`debug >= 4`.
     - ``atdebug = myaction``
   * - :literal:`apersel`
     - :const:`nil`
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
   * - :literal:`costp`
     - :const:`nil`
     - Finite-difference scale for orbit Jacobian (inherited from :var:`cofind` if nil).
     - ``costp = 1e-8``
   * - :literal:`coitr`
     - :const:`nil`
     - Maximum closed-orbit Newton iterations (inherited if nil).
     - ``coitr = 25``
   * - :literal:`cotol`
     - :const:`nil`
     - Closed-orbit convergence tolerance (inherited if nil).
     - ``cotol = 1e-6``
   * - :literal:`O1`
     - :const:`nil`
     - Orbit translation subtracted from the final closed orbit.
     - ``O1 = {t=100, pt=10}``
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


The :var:`twiss` command returns the following objects:

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Return
     - Description
   * - :literal:`mtbl`
     - An *mtable* corresponding to the augmented TFS table of the :var:`track` command with the :var:`twiss` command columns.
   * - :literal:`mflw`
     - An *mflow* corresponding to the augmented map flow of the :var:`track` command with the :var:`twiss` command data.
   * - :literal:`eidx`
     - An optional *number* corresponding to the last tracked element index in the sequence when :literal:`nstep` stopped the command before the end of the :literal:`range`.


Twiss mtable
------------
.. _sec.twiss.mtable:

The :var:`twiss` command returns a *mtable* where the information described hereafter is the default list of fields written to the TFS files. [#f2]_

The header of the *mtable* contains the fields in the default order: [#f3]_

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Field
     - Description
   * - :literal:`name`
     - Name of the command, e.g. :literal:`"twiss"`.
   * - :literal:`type`
     - Type of the mtable, i.e. :literal:`"twiss"`.
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
   * - :literal:`chrom`
     - Value of the command attribute :literal:`chrom`.
   * - :literal:`coupling`
     - Value of the command attribute :literal:`coupling`.
   * - :literal:`trkopt`
     - Value of the command attribute :literal:`trkopt`.
   * - :literal:`trkrdt`
     - Value of the command attribute :literal:`trkrdt`.
   * - :literal:`length`
     - :math:`s`-length of the tracked design orbit.
   * - :literal:`q1`
     - Tunes of mode 1.
   * - :literal:`q2`
     - Tunes of mode 2.
   * - :literal:`q3`
     - Tunes of mode 3.
   * - :literal:`alfap`
     - Momentum compaction factor :math:`\alpha_p`.
   * - :literal:`etap`
     - Phase slip factor :math:`\eta_p`.
   * - :literal:`gammatr`
     - Energy gamma transition :math:`\gamma_{\text{tr}}`.
   * - :literal:`synch_1`
     - First synchrotron radiation integral.
   * - :literal:`synch_2`
     - Second synchrotron radiation integral.
   * - :literal:`synch_3`
     - Third synchrotron radiation integral.
   * - :literal:`synch_4`
     - Fourth synchrotron radiation integral.
   * - :literal:`synch_5`
     - Fifth synchrotron radiation integral.
   * - :literal:`synch_6`
     - Sixth synchrotron radiation integral.
   * - :literal:`synch_8`
     - Eighth synchrotron radiation integral.

The core of the *mtable* contains the columns in the default order: [#f6]_

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
   * - :literal:`alfa11`
     - Optical function :math:`\alpha` of mode 1 at the :math:`s`-position.
   * - :literal:`beta11`
     - Optical function :math:`\beta` of mode 1 at the :math:`s`-position.
   * - :literal:`gama11`
     - Optical function :math:`\gamma` of mode 1 at the :math:`s`-position.
   * - :literal:`mu1`
     - Phase advance :math:`\mu` of mode 1 at the :math:`s`-position.
   * - :literal:`dx`
     - Dispersion function of :math:`x` at the :math:`s`-position.
   * - :literal:`dpx`
     - Dispersion function of :math:`p_x` at the :math:`s`-position.
   * - :literal:`alfa22`
     - Optical function :math:`\alpha` of mode 2 at the :math:`s`-position.
   * - :literal:`beta22`
     - Optical function :math:`\beta` of mode 2 at the :math:`s`-position.
   * - :literal:`gama22`
     - Optical function :math:`\gamma` of mode 2 at the :math:`s`-position.
   * - :literal:`mu2`
     - Phase advance :math:`\mu` of mode 2 at the :math:`s`-position.
   * - :literal:`dy`
     - Dispersion function of :math:`y` at the :math:`s`-position.
   * - :literal:`dpy`
     - Dispersion function of :math:`p_y` at the :math:`s`-position.
   * - :literal:`alfa33`
     - Optical function :math:`\alpha` of mode 3 at the :math:`s`-position.
   * - :literal:`beta33`
     - Optical function :math:`\beta` of mode 3 at the :math:`s`-position.
   * - :literal:`gama33`
     - Optical function :math:`\gamma` of mode 3 at the :math:`s`-position.
   * - :literal:`mu3`
     - Phase advance :math:`\mu` of mode 3 at the :math:`s`-position.
   * - :literal:`__map`
     - Damap at the :math:`s`-position (only if :literal:`savemap=true`). [#f5]_

If :literal:`saveanf == true`, the protected column :literal:`__nf` is also added and stores the analysed normal form at each saved row.

The mtable also carries the in-memory attributes :literal:`taper`, :literal:`range` and the protected sequence handle :literal:`__seq`, but they are not part of the default header list written to TFS files.

When :literal:`chrom=true`, the following header fields are added:

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Field
     - Description
   * - :literal:`dq1`
     - Chromatic derivative of tunes of mode 1 (chromaticity).
   * - :literal:`dq2`
     - Chromatic derivative of tunes of mode 2 (chromaticity).
   * - :literal:`dq3`
     - Chromatic derivative of tunes of mode 3 (chromaticity).

When :literal:`chrom=true`, the following columns are added:

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Column
     - Description
   * - :literal:`dmu1`
     - Chromatic derivative of the phase advance of mode 1 at the :math:`s`-position.
   * - :literal:`ddx`
     - Chromatic derivative of the dispersion function of :math:`x` at the :math:`s`-position.
   * - :literal:`ddpx`
     - Chromatic derivative of the dispersion function of :math:`p_x` at the :math:`s`-position.
   * - :literal:`wx`
     - Chromatic amplitude function of mode 1 at the :math:`s`-position.
   * - :literal:`phix`
     - Chromatic phase function of mode 1 at the :math:`s`-position.
   * - :literal:`dmu2`
     - Chromatic derivative of the phase advance of mode 2 at the :math:`s`-position.
   * - :literal:`ddy`
     - Chromatic derivative of the dispersion function of :math:`y` at the :math:`s`-position.
   * - :literal:`ddpy`
     - Chromatic derivative of the dispersion function of :math:`p_y` at the :math:`s`-position.
   * - :literal:`wy`
     - Chromatic amplitude function of mode 2 at the :math:`s`-position.
   * - :literal:`phiy`
     - Chromatic phase function of mode 2 at the :math:`s`-position.

When :literal:`coupling=true`, the following columns are added:

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Column
     - Description
   * - :literal:`alfa12`
     - Optical function :math:`\alpha` of coupling mode 1-2 at the :math:`s`-position.
   * - :literal:`beta12`
     - Optical function :math:`\beta` of coupling mode 1-2 at the :math:`s`-position.
   * - :literal:`gama12`
     - Optical function :math:`\gamma` of coupling mode 1-2 at the :math:`s`-position.
   * - :literal:`alfa13`
     - Optical function :math:`\alpha` of coupling mode 1-3 at the :math:`s`-position.
   * - :literal:`beta13`
     - Optical function :math:`\beta` of coupling mode 1-3 at the :math:`s`-position.
   * - :literal:`gama13`
     - Optical function :math:`\gamma` of coupling mode 1-3 at the :math:`s`-position.
   * - :literal:`alfa21`
     - Optical function :math:`\alpha` of coupling mode 2-1 at the :math:`s`-position.
   * - :literal:`beta21`
     - Optical function :math:`\beta` of coupling mode 2-1 at the :math:`s`-position.
   * - :literal:`gama21`
     - Optical function :math:`\gamma` of coupling mode 2-1 at the :math:`s`-position.
   * - :literal:`alfa23`
     - Optical function :math:`\alpha` of coupling mode 2-3 at the :math:`s`-position.
   * - :literal:`beta23`
     - Optical function :math:`\beta` of coupling mode 2-3 at the :math:`s`-position.
   * - :literal:`gama23`
     - Optical function :math:`\gamma` of coupling mode 2-3 at the :math:`s`-position.
   * - :literal:`alfa31`
     - Optical function :math:`\alpha` of coupling mode 3-1 at the :math:`s`-position.
   * - :literal:`beta31`
     - Optical function :math:`\beta` of coupling mode 3-1 at the :math:`s`-position.
   * - :literal:`gama31`
     - Optical function :math:`\gamma` of coupling mode 3-1 at the :math:`s`-position.
   * - :literal:`alfa32`
     - Optical function :math:`\alpha` of coupling mode 3-2 at the :math:`s`-position.
   * - :literal:`beta32`
     - Optical function :math:`\beta` of coupling mode 3-2 at the :math:`s`-position.
   * - :literal:`gama32`
     - Optical function :math:`\gamma` of coupling mode 3-2 at the :math:`s`-position.


Tracking linear normal form
---------------------------

Internally, :var:`twiss` computes optics by converting each surviving one-turn
map into a normalizing map and then tracking that linear normal form through
the requested range. The relevant status transitions in the implementation are:

* coordinate or damap input from :literal:`X0` enters as :literal:`"Xset"` or
  :literal:`"Mset"`
* if closed-orbit search is needed, :var:`cofind` promotes eligible inputs to
  :literal:`"stable"` or rejects them as :literal:`"unstable"`,
  :literal:`"singular"`, or :literal:`"lost"`
* stable inputs are converted into one-turn maps
* one-turn maps are converted in-place into normalizing maps and tagged
  :literal:`"Aset"`
* the final :var:`track` pass propagates those normalizing maps while
  :var:`twiss` extracts optics, optional parametric optics, and optional RDTs

This matters for advanced use because :literal:`trkopt`, :literal:`trkrdt`,
and :literal:`saveanf` all depend on that analysed normal-form stage:

* :literal:`trkopt` requests extra optics-like columns computed from the
  tracked normalizing map at each saved row
* :literal:`trkrdt` requests explicit resonance-driving-term columns and
  therefore requires analysed normal forms
* :literal:`saveanf=true` stores the analysed normal form in the protected
  column :literal:`__nf`

If :var:`twiss` receives an :literal:`"Aset"` damap directly, it can reuse it
for optics propagation. However, RDT tracking still requires an analysed normal
form; providing an :literal:`"Aset"` damap without :literal:`__nf` is therefore
insufficient for :literal:`trkrdt` or :literal:`saveanf`.

Typical Workflows
-----------------

**Standard optics table**

The simplest use: run twiss on a sequence with an attached beam and inspect
the tunes and beta functions.

.. literalinclude:: ../../verified_examples/twiss_minimal.mad
   :language: mad

**Chromatic functions**

Add :literal:`chrom=true` to request chromaticities and the chromatic amplitude
and phase functions in a single pass using finite differences:

.. code-block:: mad

   tw = twiss { sequence=seq, chrom=true }
   print("dq1=", tw.dq1, " dq2=", tw.dq2)

**Ranged twiss**

Supply a :literal:`range` to compute optics over a sub-section only.  The
initial conditions can be a beta0 block or a damap:

.. code-block:: mad

   tw = twiss { sequence=seq, range="BPM1/BPM2" }

Interpreting Outputs
--------------------

After a successful :literal:`twiss` call the two returned objects are:

**mtbl** (the TFS table)

Scalar summary quantities in the table header:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Field
     - Meaning
   * - :literal:`q1`, :literal:`q2`
     - Tunes of mode 1 and 2
   * - :literal:`dq1`, :literal:`dq2`
     - Chromaticities (requires :literal:`chrom=true`)
   * - :literal:`alfap`
     - Momentum compaction factor :math:`\alpha_p`
   * - :literal:`etap`
     - Phase slip factor :math:`\eta_p`
   * - :literal:`gammatr`
     - Transition energy :math:`\gamma_{\text{tr}}`
   * - :literal:`length`
     - Total tracked length [m]
   * - :literal:`synch_1` … :literal:`synch_8`
     - Synchrotron radiation integrals

Column arrays at each saved element:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Column
     - Meaning
   * - :literal:`beta11`, :literal:`beta22`
     - Beta functions of mode 1 (:math:`x`) and mode 2 (:math:`y`)
   * - :literal:`alfa11`, :literal:`alfa22`
     - Alpha functions
   * - :literal:`mu1`, :literal:`mu2`
     - Phase advances [rad/2π]
   * - :literal:`dx`, :literal:`dy`
     - Dispersion functions [m]
   * - :literal:`x`, :literal:`px`, :literal:`y`, :literal:`py`
     - Closed-orbit coordinates at each element
   * - :literal:`status`
     - :literal:`"stable"` if the one-turn map is on the unit circle
   * - :literal:`slc`
     - Slice index: :const:`-2` at exit (default), :const:`-1` at entry,
       :const:`0` … :const:`N` for body slices (see :literal:`save`).

**mflw** (the map flow)

Carries the one-turn map, the normalising map, and any saved normal forms.
Advanced users can pass it back via :literal:`mflow=mflw` for a follow-up
ranged twiss without repeating the closed-orbit and normal-form preparation.

Common Pitfalls
---------------

* **Lost particle at turn 0**: the closed-orbit search failed.  The lattice is
  either unstable at the given energy or the initial guess is far from the orbit.
  Try :literal:`info=2` to see the iteration log.
* **Missing beta columns**: twiss only saves at the exit of each element by
  default (:literal:`observe=0`).  The number of rows equals the number of
  elements; column values at intermediate slices are not stored unless
  :literal:`save="atbody"` or similar is set.
* **Column names vs MAD-X**: MAD-NG uses :literal:`beta11` / :literal:`beta22`
  (double-index, mode-based) instead of MAD-X's :literal:`betx` / :literal:`bety`.
* **trkopt requires a damap X0**: parametric columns are only available when
  :literal:`X0` is a damap with named parameters.  Passing plain coordinates
  silently produces no parametric columns.
* **chrom vs trkopt**: :literal:`chrom=true` uses a finite-difference
  approximation.  Use :literal:`trkopt` with a :literal:`pt`-dependent damap for
  exact chromatic derivatives.

Examples
--------

The examples below were working for MAD-NG version :literal:`1.1.13_P`.

Minimal derivative-aware optics request with :literal:`trkopt`:

.. literalinclude:: ../../verified_examples/trkopt_minimal.mad
   :language: mad

This setup requests only the named extra columns; the base optics columns are
still present in the returned *mtable*.

Minimal RDT request with :literal:`trkrdt` and :literal:`saveanf`:

.. literalinclude:: ../../verified_examples/trkrdt_minimal.mad
   :language: mad

In this case the returned *mtable* includes the requested RDT columns and the
protected column :literal:`__nf`.

For a workflow-oriented overview of these derivative and RDT patterns, see
:doc:`parametric_optics_and_rdts`.


.. rubric:: Footnotes

.. [#f1] Initial coordinates :var:`X0` may override it by providing a beam per particle or damap.
.. [#f7] The :literal:`TKT` scheme (Yoshida) is automatically converted to the :literal:`MKM` scheme (Boole) when appropriate.
.. [#f8] In all cases, MAD-NG uses PTC setup :literal:`time=true, exact=true`.
.. [#f2] The output of mtable in TFS files can be fully customized by the user.
.. [#f3] The fields from :literal:`name` to :literal:`lost` are set by the :var:`track` command
.. [#f5] Fields and columns starting with two underscores are protected data and never saved to TFS files.
.. [#f6] The column from :literal:`name` to :literal:`status` are set by the :var:`track` command.
