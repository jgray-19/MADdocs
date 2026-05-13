Survey
======
.. _ch.cmd.survey:

The :literal:`survey` command provides a simple interface to the *geometric* tracking code. [#f1]_ The geometric tracking can be used to place the elements of a sequence in the global reference system in :numref:`fig-phy-grs`.

.. code-block:: lua
    :caption: Synopsis of the :literal:`survey` command with default setup.
    :name: fig-surv-synop

    mtbl, mflw [, eidx] = survey {
        sequence=sequ,  -- sequence (required)
        range=nil,      -- range of tracking (or sequence.range)
        dir=1,          -- s-direction of tracking (1 or -1)
        s0=0,           -- initial s-position offset [m]
        X0=0,           -- initial coordinates x, y, z [m]
        A0=0,           -- initial angles theta, phi, psi [rad] or matrix W0
        nturn=1,        -- number of turns to track
        nstep=-1,       -- number of elements to track
        nslice=1,       -- number of slices (or weights) for each element
        implicit=false, -- slice implicit elements too (e.g. plots)
        misalign=false, -- consider misalignment
        save=true,      -- create mtable and save results
        title=nil,      -- title of mtable (default seq.name)
        observe=0,      -- save only in observed elements (every n turns)
        savesel=fnil,   -- save selector (predicate)
        savemap=false,  -- save the orientation matrix W in the column __map
        atentry=fnil,   -- action called when entering an element
        atslice=fnil,   -- action called after each element slices
        atexit=fnil,    -- action called when exiting an element
        atsave=fnil,    -- action called when saving in mtable
        atdebug=fnil,   -- action called when debugging the element maps
        info=nil,       -- information level (output on terminal)
        debug=nil,      -- debug information level (output on terminal)
        usrdef=nil,     -- user defined data attached to the mflow
        mflow=nil,      -- mflow, exclusive with other attributes except nstep
    }

.. _fig.survey.synop:

The :literal:`survey` command format is summarized in :numref:`fig-surv-synop`, including the default setup of the attributes.

**Sequence and geometry**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`sequence`
     - *required*
     - Sequence to survey.
     - ``sequence = lhcb1``
   * - :literal:`range`
     - :const:`nil`
     - Sub-range of the sequence (or :literal:`seq.range`).
     - ``range = "IP1/IP5"``
   * - :literal:`dir`
     - :const:`1`
     - Survey direction: :const:`1` forward, :const:`-1` backward.
     - ``dir = -1``
   * - :literal:`s0`
     - :const:`0`
     - Initial :math:`s`-position offset [m].
     - ``s0 = 5000``
   * - :literal:`X0`
     - :const:`0`
     - Initial position :math:`(x, y, z)` [m].
     - ``X0 = {x=100, y=-50}``
   * - :literal:`A0`
     - :const:`0`
     - Initial angles :math:`(\theta, \phi, \psi)` [rad] or orientation matrix :math:`W_0`. [#f2]_
     - ``A0 = {theta=deg2rad(30)}``
   * - :literal:`nturn`
     - :const:`1`
     - Number of turns.
     - ``nturn = 2``
   * - :literal:`nstep`
     - :const:`-1`
     - Number of elements (:const:`-1` = all).
     - ``nstep = 10``
   * - :literal:`nslice`
     - :const:`1`
     - Slices per element: number, list, or callable :literal:`(elm,mflw,lw)`. See :ref:`ch.phy.intrg`.
     - ``nslice = 5``
   * - :literal:`implicit`
     - :const:`false`
     - Slice implicit elements (e.g. drifts) for smooth plotting.
     - ``implicit = true``
   * - :literal:`misalign`
     - :const:`false`
     - Apply **error** misalignments from :literal:`seq:ealign`. Permanent :literal:`elm.misalign` is always applied.
     - ``misalign = true``

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
     - When to save rows: :const:`true` = at exit, :const:`false` = none, or selector string.
     - ``save = 'atbody'``
   * - :literal:`observe`
     - :const:`0`
     - Save all elements (:const:`0`) or only :meth:`:is_observed` every :math:`n` turns.
     - ``observe = 1``
   * - :literal:`title`
     - :const:`nil`
     - Title of the output mtable (default: :literal:`seq.name`).
     - ``title = "LHC survey"``
   * - :literal:`savesel`
     - :literal:`fnil`
     - Predicate :literal:`(elm,mflw,lw,islc)` to filter saved elements.
     - ``savesel = \e -> mylist[e.name]``
   * - :literal:`savemap`
     - :const:`false`
     - Save orientation matrix :math:`W` in column :literal:`__map`.
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
     - :literal:`(elm,mflw,lw,islc)` — called at each geometric slice (slice :const:`0`…:math:`N`).
     - ``atslice = myaction``
   * - :literal:`atexit`
     - :literal:`fnil`
     - :literal:`(elm,mflw,0,-2)` — called at element exit (slice :const:`-2`).
     - ``atexit = myaction``
   * - :literal:`atsave`
     - :literal:`fnil`
     - :literal:`(elm,mflw,lw,islc)` — called when a row is saved.
     - ``atsave = myaction``
   * - :literal:`atdebug`
     - :literal:`fnil`
     - :literal:`(elm,mflw,lw,[msg],[...])` — called at map entry/exit. Defaults to :literal:`mdump` if :literal:`debug >= 4`.
     - ``atdebug = myaction``

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


The :literal:`survey` command returns the following objects:

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Return
     - Description
   * - :literal:`mtbl`
     - An *mtable* corresponding to the TFS table of the :literal:`survey` command.
   * - :literal:`mflw`
     - An *mflow* corresponding to the map flow of the :literal:`survey` command.
   * - :literal:`eidx`
     - An optional *number* corresponding to the last surveyed element index when :literal:`nstep` stopped the command before the end of the :literal:`range`.


Survey mtable
-------------
.. _sec.survey.mtable:

The :literal:`survey` command returns a *mtable* where the information described hereafter is the default list of fields written to the TFS files. [#f3]_

The header of the *mtable* contains the fields in the default order:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Field
     - Description
   * - :literal:`name`
     - Name of the command, e.g. :literal:`"survey"`.
   * - :literal:`type`
     - Type of the mtable, i.e. :literal:`"survey"`.
   * - :literal:`title`
     - Value of the command attribute :literal:`title`.
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
   * - :literal:`range`
     - Value of the command attribute :literal:`range`. [#f4]_
   * - :literal:`__seq`
     - The *sequence* from the command attribute :literal:`sequence`. [#f5]_

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
   * - :literal:`angle`
     - Bending angle from the start to the end of the element slice.
   * - :literal:`tilt`
     - Tilt of the element.
   * - :literal:`x`
     - Global coordinate :math:`x` at the :math:`s`-position.
   * - :literal:`y`
     - Global coordinate :math:`y` at the :math:`s`-position.
   * - :literal:`z`
     - Global coordinate :math:`z` at the :math:`s`-position.
   * - :literal:`theta`
     - Global angle :math:`\theta` at the :math:`s`-position.
   * - :literal:`phi`
     - Global angle :math:`\phi` at the :math:`s`-position.
   * - :literal:`psi`
     - Global angle :math:`\psi` at the :math:`s`-position.
   * - :literal:`slc`
     - Slice index ranging from :literal:`-2` to :literal:`nslice`. See :ref:`ch.phy.intrg`.
   * - :literal:`turn`
     - Turn number.
   * - :literal:`tdir`
     - :math:`t`-direction of the tracking in the element.
   * - :literal:`eidx`
     - Index of the element in the sequence.
   * - :literal:`__map`
     - Orientation matrix :math:`W` at the :math:`s`-position (only if :literal:`savemap=true`). [#f5]_


Geometrical tracking
--------------------

:numref:`fig.survey.trkslc` presents the scheme of the geometrical tracking through an element sliced with :literal:`nslice=3`. The actions :literal:`atentry` (index :literal:`-1`), :literal:`atslice` (indexes :literal:`0..3`), and :literal:`atexit` (index :literal:`-2`) are reversed between the forward tracking (:literal:`dir=1` with increasing :math:`s`-position) and the backward tracking (:literal:`dir=-1` with decreasing :math:`s`-position). By default, the action :literal:`atsave` is attached to the exit slice, and hence it is also reversed in the backward tracking.


.. _fig.survey.trkslc:
.. figure:: fig/dyna-trck-slice-crop.png

	Geometrical tracking with slices.

Slicing
"""""""

The slicing can take three different forms:

	*	 A *number* of the form :literal:`nslice=`:math:`N` that specifies the number of slices with indexes :literal:`0..N`. This defines a uniform slicing with slice length :math:`l_{\text{slice}} = l_{\text{elem}}/N`.

	*	 An *iterable* of the form :literal:`nslice={lw_1,lw_2,..,lw_N}` with :math:`\sum_i lw_i=1` that specifies the fraction of length of each slice with indexes :literal:`0..N` where :math:`N=`\ :literal:`#nslice`. This defines a non-uniform slicing with a slice length of :math:`l_i = lw_i\times l_{\text{elem}}`.

	*	 A *callable* :literal:`(elm, mflw, lw)` returning one of the two previous forms of slicing. The arguments are in order, the current element, the tracked map flow, and the length weight of the step, which should allow to return a user-defined element-specific slicing.


The surrounding :literal:`P` and :literal:`P`\ :math:`^{-1}` maps represent the patches applied around the body of the element to change the frames, after the :literal:`atentry` and before the :literal:`atexit` actions:

	*	 The misalignment of the element to move from the *global frame* to the *element frame* if the command attribute :literal:`misalign` is set to :const:`true`.

	*	 The tilt of the element to move from the element frame to the *titled frame* if the element attribute :literal:`tilt` is non-zero. The :literal:`atslice` actions take place in this frame.

These patches do not change the global frame per se, but they may affect the way that other components change the global frame, e.g. the tilt combined with the angle of a bending element.

Sub-elements
""""""""""""

The :literal:`survey` command takes sub-elements into account, mainly for compatibility with the :var:`track` command. In this case, the slicing specification is taken between sub-elements, e.g. 3 slices with 2 sub-elements gives a final count of 9 slices. It is possible to adjust the number of slices between sub-elements with the third form of slicing specifier, i.e. by using a callable where the length weight argument is between the current (or the end of the element) and the last sub-elements (or the start of the element).

Save Setup
----------

The :literal:`atentry`, :literal:`atslice`, and :literal:`atexit` hooks and the
:literal:`save` attribute work together to control which positions are recorded
in the output table.  The table below summarises the most common cases for
:literal:`nslice=1`; :literal:`E`, :literal:`S`, and :literal:`X` denote the
element entry, body slice, and exit positions respectively.

.. list-table::
   :header-rows: 1
   :widths: 10 20 20 20 30

   * - Case
     - atentry
     - atslice
     - atexit
     - Positions saved
   * - 0 (default)
     - nil
     - nil
     - nil
     - X only (exit)
   * - 1
     - nil
     - ftrue
     - nil
     - S and X
   * - 2
     - ftrue
     - ftrue
     - nil
     - E, S, and X
   * - 3
     - nil
     - ftrue
     - fnone
     - S only
   * - 4
     - ftrue
     - nil
     - nil
     - E and X
   * - 5
     - ftrue
     - ftrue
     - fnone
     - E and S
   * - 6
     - ftrue
     - nil
     - fnone
     - E only
   * - 7
     - nil
     - nil
     - fnone
     - nothing

The :literal:`save` string shortcuts provide the same control without
specifying hooks individually: :literal:`"atentry"`, :literal:`"atslice"`,
:literal:`"atexit"` (default), :literal:`"atbound"` (E + X),
:literal:`"atbody"` (S + X), and :literal:`"atall"` (E + S + X).

.. note::
   The :literal:`s` column in the survey mtable refers to the :math:`s`-position
   at the *end* of the element slice (consistent with :literal:`track` and
   :literal:`twiss`), not the centre.  To recover the MAD-X convention you can
   compute ``s_madx = srv.s[i] - srv.l[i]`` for each row.

Typical Workflows
-----------------

**Basic geometry survey**

Run survey on a loaded sequence to obtain element positions and orientations:

.. literalinclude:: ../../verified_examples/survey_minimal.mad
   :language: mad

**Survey with increased resolution**

Use :literal:`nslice` and :literal:`save="atbody"` to record intermediate
positions inside long elements:

.. code-block:: mad

   srv = survey {
     sequence = seq,
     nslice   = 10,
     save     = "atbody",
   }

**Backward survey**

Set :literal:`dir=-1` and provide a starting state :literal:`X0` / :literal:`A0`
to survey from the end of the sequence towards the start:

.. code-block:: mad

   srv = survey {
     sequence = seq,
     dir      = -1,
     X0       = { x=0, y=0, z=seq.l },
   }

Interpreting Outputs
--------------------

After a successful :literal:`survey` call the main output is:

**mtbl** (the TFS table)

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Column
     - Meaning
   * - :literal:`s`
     - Longitudinal path length at the end of the slice [m]
   * - :literal:`l`
     - Length contribution of this slice [m]
   * - :literal:`x`, :literal:`y`, :literal:`z`
     - Cartesian position of the local frame origin in the global frame [m]
   * - :literal:`theta`
     - Rotation angle about the global :math:`y`-axis (azimuth) [rad]
   * - :literal:`phi`
     - Rotation angle about the rotated :math:`x`-axis (elevation) [rad]
   * - :literal:`psi`
     - Rotation angle about the rotated :math:`z`-axis (roll) [rad]
   * - :literal:`angle`
     - Accumulated bending angle from the start of the element [rad]
   * - :literal:`tilt`
     - Element tilt [rad]
   * - :literal:`__map`
     - 3×3 orientation matrix :math:`W` (only when :literal:`savemap=true`)

The orientation matrix :math:`W` can also be reconstructed from the three
angles with :literal:`W = matrix(3):rotzxy(-phi, theta, psi)`.

Common Pitfalls
---------------

* **Survey does not close**: for a nominally closed ring, the survey should
  return close to its starting state after one full turn.  A significant
  mismatch signals a bending-angle or tilt error in the element definitions.
* **s convention differs from MAD-X**: see the note in the save-setup section
  above.
* **No beam required**: :literal:`survey` is purely geometric and does not
  require a beam to be attached.  However, attaching a beam before survey is
  harmless and is good practice before subsequent :literal:`twiss` or
  :literal:`track` calls.
* **Misalignment**: element misalignments are only applied when
  :literal:`misalign=true`; by default the ideal geometry is used.

Examples
--------

See :doc:`common_tasks` for additional workflow examples.


.. rubric:: Footnotes

.. [#f1] MAD-NG implements only two tracking codes denominated the *geometric* and *dynamic* tracking
.. [#f2] An orientation matrix can be obtained from the 3 angles with :literal:`W=matrix(3):rotzxy(- phi,theta,psi)`
.. [#f3] The output of mtable in TFS files can be fully customized by the user.
.. [#f4] This field is not saved in the TFS table by default.
.. [#f5] Fields and columns starting with two underscores are protected data and never saved to TFS files.
