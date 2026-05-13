Correct
=======
.. _ch.cmd.correct:

The :var:`correct` command (i.e. orbit correction) provides a simple interface to compute the orbit steering correction and setup the kickers of the sequences from the analysis of their :var:`track` and :var:`twiss` mtables.

.. code-block:: lua
    :caption: Synopsis of the :var:`correct` command with default setup.
    :name: fig-correct-synop

    mlst = correct {
        sequence=nil,   -- sequence(s) (required)
        range=nil,      -- sequence(s) range(s) (or sequence.range)
        title=nil,      -- title of mtable (default seq.name)
        model=nil,      -- mtable(s) with twiss functions (required)
        orbit=nil,      -- mtable(s) with measured orbit(s), or use model
        target=nil,     -- mtable(s) with target orbit(s), or zero orbit
        kind='ring',    -- 'line' or 'ring'
        plane='xy',     -- 'x', 'y' or 'xy'
        method='micado',-- 'LSQ', 'SVD' or 'MICADO'
        ncor=0,         -- number of correctors to consider by method, 0=all
        tol=1e-5,       -- rms tolerance on the orbit
        units=1,        -- units in [m] of the orbit
        corcnd=false,   -- precond of correctors using 'svdcnd' or 'pcacnd'
        corcut=0,       -- value to threshold singular values in precond
        cortol=0,       -- value to threshold correctors in svdcnd
        corset=true,    -- update correctors correction strengths
        monon=false,    -- fraction (0<?<=1) of randomly available monitors
        moncut=false,   -- cut monitors above moncut sigmas
        monerr=false,   -- 1:use mrex/mrey alignment errors of monitors
                        -- 2:use msex/msey scaling errors of monitors
        info=nil,       -- information level (output on terminal)
        debug=nil,      -- debug information level (output on terminal)
    }

.. _sec.correct.synop:

Command synopsis
----------------

The :var:`correct` command format is summarized in :numref:`fig-correct-synop`, including the default setup of the attributes.

**Sequence and model**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`sequence`
     - *required*
     - Sequence (or list of sequences) to correct.
     - ``sequence = lhcb1``
   * - :literal:`range`
     - :const:`nil`
     - Range (or list of ranges) for the sequence (or :literal:`seq.range`).
     - ``range = "S.DS.L8.B1/E.DS.R8.B1"``
   * - :literal:`title`
     - :const:`nil`
     - Title of the output *mtable*; defaults to :literal:`seq.name`.
     - ``title = "IP5 correction"``
   * - :literal:`model`
     - *required*
     - *mtable* (or list) providing :var:`twiss`-like optics and orbit data.
     - ``model = twmtbl``
   * - :literal:`orbit`
     - :const:`nil`
     - *mtable* (or list) with measured orbits; defaults to model orbit.
     - ``orbit = tkmtbl``
   * - :literal:`target`
     - :const:`nil`
     - *mtable* (or list) with target orbits; defaults to design orbit.
     - ``target = tgmtbl``

**Correction settings**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`kind`
     - :literal:`'ring'`
     - Correction topology: :literal:`'line'` respects causality; :literal:`'ring'` treats the system as periodic.
     - ``kind = 'line'``
   * - :literal:`plane`
     - :literal:`'xy'`
     - Plane(s) to correct: :literal:`'x'`, :literal:`'y'`, or :literal:`'xy'`.
     - ``plane = 'x'``
   * - :literal:`method`
     - :literal:`'micado'`
     - Solver: :literal:`'LSQ'` (:literal:`solve`), :literal:`'SVD'` (:literal:`ssolve`), or :literal:`'MICADO'` (:literal:`nsolve`). See :doc:`mad_mod_linalg`.
     - ``method = 'svd'``
   * - :literal:`ncor`
     - :const:`0`
     - Number of correctors for :literal:`micado`; :const:`0` uses all available.
     - ``ncor = 4``
   * - :literal:`tol`
     - :const:`1e-5`
     - RMS tolerance on the residual orbit [m].
     - ``tol = 1e-6``
   * - :literal:`units`
     - :const:`1`
     - Unit of :literal:`orbit` and :literal:`target` coordinates [m].
     - ``units = 1e-3``

**Corrector settings**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`corcnd`
     - :const:`false`
     - Preconditioning method for the corrector system: :literal:`'svdcnd'` or :literal:`'pcacnd'`. See :doc:`mad_mod_linalg`.
     - ``corcnd = 'pcacnd'``
   * - :literal:`corcut`
     - :const:`0`
     - Singular-value threshold passed to :literal:`svdcnd` / :literal:`pcacnd`.
     - ``corcut = 1e-6``
   * - :literal:`cortol`
     - :const:`0`
     - Corrector threshold passed to :literal:`svdcnd`.
     - ``cortol = 1e-8``
   * - :literal:`corset`
     - :const:`true`
     - Apply computed corrections to corrector strengths in the sequence.
     - ``corset = false``

**Monitor settings**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`monon`
     - :const:`false`
     - Fraction :math:`(0,1]` of monitors randomly kept (uniform RNG).
     - ``monon = 0.8``
   * - :literal:`moncut`
     - :const:`false`
     - Cut monitors whose reading exceeds :literal:`moncut` sigma.
     - ``moncut = 2``
   * - :literal:`monerr`
     - :const:`false`
     - Monitor error type: :const:`1` = alignment (:literal:`mrex`/:literal:`mrey`/:literal:`dpsi`); :const:`2` = scaling (:literal:`msex`/:literal:`msey`); :const:`3` = both.
     - ``monerr = 3``

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

The :var:`correct` command returns the following object:

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Return
     - Description
   * - :literal:`mlst`
     - An *mtable* (or list of *mtable*) from the correction. A list is returned when multiple sequences are corrected together.


Correct mtable
--------------
.. _sec.correct.mtable:

The :var:`correct` command returns a *mtable* where the information described hereafter is the default list of fields written to the TFS files. [#f1]_

The header of the *mtable* contains the fields in the default order:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Field
     - Description
   * - :literal:`name`
     - Name of the command that created the *mtable*, e.g. :literal:`"correct"`.
   * - :literal:`type`
     - Type of the *mtable*, i.e. :literal:`"correct"`.
   * - :literal:`title`
     - Value of the command attribute :literal:`title`.
   * - :literal:`origin`
     - Origin of the application, e.g. :literal:`"MAD 1.0.0 OSX 64"`.
   * - :literal:`date`
     - Date of creation, e.g. :literal:`"27/05/20"`.
   * - :literal:`time`
     - Time of creation, e.g. :literal:`"19:18:36"`.
   * - :literal:`refcol`
     - Reference column for the *mtable* dictionary, e.g. :literal:`"name"`.
   * - :literal:`range`
     - Value of the command attribute :literal:`range`. [#f2]_
   * - :literal:`__seq`
     - Sequence from the command attribute :var:`sequence`. [#f3]_

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
     - Length from the start of the element to the end of the element slice.
   * - :literal:`x_old`
     - Local coordinate :math:`x` before correction.
   * - :literal:`y_old`
     - Local coordinate :math:`y` before correction.
   * - :literal:`x`
     - Predicted local coordinate :math:`x` after correction.
   * - :literal:`y`
     - Predicted local coordinate :math:`y` after correction.
   * - :literal:`rx`
     - Predicted local residual :math:`r_x` after correction.
   * - :literal:`ry`
     - Predicted local residual :math:`r_y` after correction.
   * - :literal:`hkick_old`
     - Horizontal kick before correction.
   * - :literal:`vkick_old`
     - Vertical kick before correction.
   * - :literal:`hkick`
     - Predicted horizontal kick after correction.
   * - :literal:`vkick`
     - Predicted vertical kick after correction.
   * - :literal:`shared`
     - :const:`true` if the element is shared with another sequence.
   * - :literal:`eidx`
     - Index of the element in the sequence.

Note that :var:`correct` does not use particle or damap :literal:`id`\ s from an augmented :var:`track` *mtable*; the provided tables should contain single-particle or single-damap information.

Examples
--------



.. rubric:: Footnotes

.. [#f1] The output of mtable in TFS files can be fully customized by the user.
.. [#f2] This field is not saved in the TFS table by default.
.. [#f3] Fields and columns starting with two underscores are protected data and never saved to TFS files.
