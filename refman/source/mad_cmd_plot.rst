Plot
====
.. _ch.cmd.plot:

The :var:`plot` command provides a high-level interface to the `Gnuplot <http://www.gnuplot.info>`_ application. Gnuplot 5.2 or higher must be installed and visible in :envvar:`PATH`.

The command has two independent roles that can be used together or separately:

* **Data plotting** — dump columns from an :doc:`mtable <mad_gen_mtable>` or a plain Lua table to Gnuplot to produce curves.
* **Sequence layout** — draw a lattice diagram above, below, or overlaid on the data plot, using element shapes colour-coded by kind.

Command synopsis
----------------
.. _sec.plot.synop:

.. code-block:: lua
    :name: fig-plot-synop
    :caption: Synopsis of the :var:`plot` command with default setup.

    cmd = plot {
        -- stream
        sid         = 1,           -- Gnuplot instance id (1..25)

        -- window
        term        = "qt",        -- Gnuplot terminal
        wsizex      = 800,         -- window width  [px]
        wsizey      = 500,         -- window height [px]
        closewin    = true,        -- close windows on MAD exit

        -- output
        output      = nil,         -- "file.pdf" | "file.png" | window-id
        scrdump     = nil,         -- save Gnuplot script to "filename"

        -- data source
        data        = nil,         -- { col=vec, ... }  (overrides table columns)
        table       = nil,         -- mtable
        tablerange  = nil,         -- row range for table

        -- sequence layout source
        sequence    = nil,         -- seq | { seq1, seq2, ... } | "keep"
        range       = nil,         -- sequence range
        nturn       = 1,           -- turns for layout iteration
        s0          = nil,         -- initial s-offset
        X0          = {0,0,0},     -- initial survey position {x,y,z}
        A0          = nil,         -- initial survey angles   {theta,phi,psi}
        W0          = nil,         -- initial survey rotation matrix
        misalign    = nil,         -- pass misalign flag to survey

        -- layout style
        laypos      = "top",       -- "top"|"bottom"|"middle"|"middle0"|"in"|0..1
        laysize     = nil,         -- fraction of plot height (screen coords)
        layonly     = nil,         -- true = suppress data axes/tics
        laydistx    = 0,           -- horizontal offset between sequences [m]
        laydisty    = 0,           -- vertical   offset between sequences [m]
        layshift    = 0,           -- global horizontal shift of layout   [m]
        layproj     = nil,         -- projection for laypos="in": "XZ"|"ZX"|matrix
        layangle    = true,        -- follow element angles in layout
        elemsel     = ftrue,       -- predicate to filter elements in layout
        elemname    = true,        -- show element name/kind tooltip (interactive)
        elemwidth   = nil,         -- base element width before elemscale
        elemscale   = 1,           -- scale factor applied to elemwidth
        elemshift   = true,        -- shift elements vertically by strength sign
        kindcolor   = true,        -- true=default colours | false=none | table

        -- axis column selection
        x1y1        = nil,         -- bottom/left  axes
        x1y2        = nil,         -- bottom/right axes
        x2y1        = nil,         -- top/left     axes
        x2y2        = nil,         -- top/right    axes

        -- labels
        title       = "${name} MAD ${version} ${date} ${time}",
        legend      = nil,         -- { col = "label" } | false
        xlabel      = nil,
        x2label     = nil,
        ylabel      = nil,
        y2label     = nil,

        -- axis ranges
        xrange      = nil,         -- { min, max }
        x2range     = nil,
        yrange      = nil,
        y2range     = nil,

        -- customisation hooks
        prolog      = nil,         -- Gnuplot script prepended before layout
        epilog      = nil,         -- Gnuplot script appended after plot
        plotcfg     = nil,         -- Gnuplot script inserted before plot command
        plotcmd     = nil,         -- replace default Gnuplot plot command(s)
        plotvar     = nil,         -- table of variables for plotcmd interpolation

        -- plot position/size (screen coordinates)
        originx     = nil,
        originy     = nil,
        psizex      = nil,
        psizey      = nil,

        -- per-column data style
        styles      = nil,         -- { col = "lines" }
        colors      = nil,         -- { col = "red"   }
        dashtypes   = nil,         -- { col = "..-- " }
        linewidths  = nil,         -- { col = 2.3     }
        pointtypes  = nil,         -- { col = 2       }
        pointsizes  = nil,         -- { col = 1.5     }
        datastyles  = {},          -- { col = { style=, color=, ... } }

        -- decoration
        font        = nil,
        fontsize    = nil,
        titlefont   = nil,
        titlesize   = nil,
        legendfont  = nil,
        legendsize  = nil,
        legendpos   = "left top",
        grid        = nil,
        border      = nil,

        -- internal
        objshft     = 1000000,     -- starting index for Gnuplot objects

        -- deferred execution
        name        = nil,
        date        = nil,
        time        = nil,
        info        = nil,
        debug       = nil,
    }

Attributes
----------

**Stream and window**

.. list-table::
   :widths: 14 14 42 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`sid`
     - :const:`1`
     - Gnuplot instance id in :math:`[1,25]`. Use separate sids for independent interactive windows or simultaneous PDF outputs.
     - ``sid = 2``
   * - :literal:`term`
     - :literal:`"qt"`
     - Gnuplot window terminal (:literal:`"qt"`, :literal:`"wxt"`, :literal:`"x11"`, …). Ignored when :literal:`output` is a filename.
     - ``term = "wxt"``
   * - :literal:`wsizex`
     - :const:`800`
     - Window width in pixels.
     - ``wsizex = 1200``
   * - :literal:`wsizey`
     - :const:`500`
     - Window height in pixels.
     - ``wsizey = 800``
   * - :literal:`closewin`
     - :const:`true`
     - Close all interactive windows when MAD exits.
     - ``closewin = false``

**Output**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`output`
     - :const:`nil`
     - Output destination. A *string* ending in :literal:`".pdf"` or :literal:`".png"` writes a file. A *number* opens a window with that id. :const:`nil` opens a new auto-numbered window.
     - ``output = "optics.pdf"``
   * - :literal:`scrdump`
     - :const:`nil`
     - Save the generated Gnuplot script to this filename for inspection or replay.
     - ``scrdump = "plot.gp"``

**Data input**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`table`
     - :const:`nil`
     - An *mtable* (e.g. from :var:`twiss` or :var:`track`) whose columns are available for axis selection.
     - ``table = tw``
   * - :literal:`data`
     - :const:`nil`
     - Plain Lua table of named arrays or vectors: :literal:`{col=vec, ...}`. Takes precedence over columns of the same name in :literal:`table`.
     - ``data = {x=srv.x, z=srv.z}``
   * - :literal:`tablerange`
     - :const:`nil`
     - Row range :literal:`{first, last}` restricting which rows of :literal:`table` are used.
     - ``tablerange = {10, 110}``

**Sequence layout input**

.. list-table::
   :widths: 14 14 42 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`sequence`
     - :const:`nil`
     - Sequence (or list of sequences) to draw as a lattice layout. :literal:`"keep"` reuses the layout from the previous :var:`plot` call on the same :literal:`sid`.
     - ``sequence = psb3``
   * - :literal:`range`
     - :const:`nil`
     - Sequence range (or list of ranges) restricting which elements are drawn.
     - ``range = "IP1/IP5"``
   * - :literal:`nturn`
     - :const:`1`
     - Number of turns for the layout iterator.
     - ``nturn = 2``
   * - :literal:`s0`
     - :const:`nil`
     - Initial :math:`s`-offset for the layout.
     - ``s0 = 100``
   * - :literal:`X0`
     - :literal:`{0,0,0}`
     - Initial survey position :literal:`{x,y,z}` for :literal:`laypos="in"`.
     - ``X0 = {-1231, 0, 2970}``
   * - :literal:`A0`
     - :const:`nil`
     - Initial survey angles :literal:`{theta,phi,psi}` for :literal:`laypos="in"`.
     - ``A0 = {-pi/4, 0, 0}``
   * - :literal:`W0`
     - :const:`nil`
     - Initial survey rotation matrix for :literal:`laypos="in"`.
     - ``W0 = mymatrix``
   * - :literal:`misalign`
     - :const:`nil`
     - Pass misalignment flag to the internal :var:`survey` run.
     - ``misalign = true``

**Layout style**

.. list-table::
   :widths: 14 14 42 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`laypos`
     - :literal:`"top"`
     - Position of the layout strip. :literal:`"top"` / :literal:`"bottom"` places it above/below the data plot. :literal:`"middle"` places it at the screen midpoint. :literal:`"middle0"` places it at the data origin. :literal:`"in"` draws elements in the survey plane inside the data axes. A number :math:`(0,1)` is used as a screen-coordinate :math:`y` position.
     - ``laypos = "bottom"``
   * - :literal:`laysize`
     - :const:`nil`
     - Fraction of screen height allocated to the layout strip. Default auto-sized.
     - ``laysize = 0.15``
   * - :literal:`layonly`
     - :const:`nil`
     - :const:`true` suppresses data axes and tics, showing only the layout.
     - ``layonly = true``
   * - :literal:`laydistx`
     - :const:`0`
     - Horizontal offset between sequences [m] when plotting multiple sequences.
     - ``laydistx = 500``
   * - :literal:`laydisty`
     - :const:`0`
     - Vertical offset between sequences when plotting multiple sequences.
     - ``laydisty = mech_sep``
   * - :literal:`layshift`
     - :const:`0`
     - Global horizontal shift of the layout origin [m] (like :literal:`s0` for survey).
     - ``layshift = sstart``
   * - :literal:`layproj`
     - :const:`nil`
     - Projection plane for :literal:`laypos="in"`: :literal:`"XZ"` (default), :literal:`"ZX"`, :literal:`"-XZ"`, :literal:`"Z-X"`, or a custom 2×3 :var:`matrix`.
     - ``layproj = "ZX"``
   * - :literal:`layangle`
     - :const:`true`
     - Follow the bend angle of elements with the :literal:`layangle` flag set, deflecting the layout beam line.
     - ``layangle = false``
   * - :literal:`elemsel`
     - :literal:`ftrue`
     - Predicate :literal:`(elm) -> bool` selecting which elements are drawn.
     - ``elemsel = \e -> e.l > 1``
   * - :literal:`elemname`
     - :const:`true`
     - Show element name and kind as a tooltip when hovering over elements in interactive terminals.
     - ``elemname = false``
   * - :literal:`elemwidth`
     - :const:`nil`
     - Base element width before :literal:`elemscale` is applied. Default auto-computed.
     - ``elemwidth = 0.07``
   * - :literal:`elemscale`
     - :const:`1`
     - Multiplier applied to :literal:`elemwidth`.
     - ``elemscale = 1.5``
   * - :literal:`elemshift`
     - :const:`true`
     - Shift elements vertically based on their strength sign (e.g. focusing vs defocusing quadrupoles).
     - ``elemshift = false``
   * - :literal:`kindcolor`
     - :const:`true`
     - Element fill colours. :const:`true` = default per-kind palette. :const:`false` = all white. A table maps kind names to colour strings or style tables.
     - ``kindcolor = {sbend="red"}``

**Axis selection**

The four axis attributes select which data columns to plot and on which axes.
Each Gnuplot plot has two :math:`x` axes (bottom :literal:`x1`, top :literal:`x2`) and two :math:`y` axes (left :literal:`y1`, right :literal:`y2`).

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`x1y1`
     - :const:`nil`
     - Columns plotted on bottom-:math:`x` / left-:math:`y` axes.
     - ``x1y1 = {s="beta11"}``
   * - :literal:`x1y2`
     - :const:`nil`
     - Columns plotted on bottom-:math:`x` / right-:math:`y` axes.
     - ``x1y2 = {s="dx"}``
   * - :literal:`x2y1`
     - :const:`nil`
     - Columns plotted on top-:math:`x` / left-:math:`y` axes.
     - ``x2y1 = "mu1"``
   * - :literal:`x2y2`
     - :const:`nil`
     - Columns plotted on top-:math:`x` / right-:math:`y` axes.
     - ``x2y2 = {s2="px"}``

The axis value may be a *string* (single :math:`y` column, row index as :math:`x`), a *list* (multiple :math:`y` columns, row index as :math:`x`), or a *table* mapping :math:`x`-column names to :math:`y`-column names or lists:

.. code-block:: lua

    x1y1 = "beta11"                             -- y=beta11, x=row index
    x1y1 = {"beta11", "beta22"}                 -- y=beta11,beta22, x=row index
    x1y1 = { s = "beta11" }                     -- y=beta11, x=s
    x1y1 = { s = {"beta11", "beta22"} }         -- y=beta11,beta22, x=s
    x1y1 = { s = "beta11", s2 = "beta22" }      -- two x-columns, one y each

**Labels**

.. list-table::
   :widths: 14 24 32 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`title`
     - :literal:`"${name} MAD ${version} ${date} ${time}"`
     - Plot title string. Supports :literal:`${name}`, :literal:`${version}`, :literal:`${date}`, :literal:`${time}` interpolation.
     - ``title = "PSB optics"``
   * - :literal:`legend`
     - :const:`nil`
     - Map column names to legend labels. :const:`false` hides all legends; :literal:`{col=false}` hides one.
     - ``legend = {beta11="β_x"}``
   * - :literal:`xlabel`
     - :const:`nil`
     - Bottom :math:`x`-axis label.
     - ``xlabel = "s [m]"``
   * - :literal:`x2label`
     - :const:`nil`
     - Top :math:`x`-axis label.
     - ``x2label = "turn"``
   * - :literal:`ylabel`
     - :const:`nil`
     - Left :math:`y`-axis label.
     - ``ylabel = "β [m]"``
   * - :literal:`y2label`
     - :const:`nil`
     - Right :math:`y`-axis label.
     - ``y2label = "D [m]"``

**Axis ranges**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`xrange`
     - :const:`nil`
     - Bottom :math:`x`-axis range :literal:`{min, max}`. Reversed if :literal:`min > max`.
     - ``xrange = {0, 100}``
   * - :literal:`x2range`
     - :const:`nil`
     - Top :math:`x`-axis range.
     - ``x2range = {0, 10}``
   * - :literal:`yrange`
     - :const:`nil`
     - Left :math:`y`-axis range.
     - ``yrange = {0, 50}``
   * - :literal:`y2range`
     - :const:`nil`
     - Right :math:`y`-axis range.
     - ``y2range = {-2, 2}``

**Data style**

All style attributes accept either a scalar (applies to all curves) or a table keyed by column name.

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`styles`
     - :const:`nil`
     - Gnuplot :literal:`with` style: :literal:`"lines"`, :literal:`"points"`, :literal:`"linespoints"`, etc.
     - ``styles = "lines"``
   * - :literal:`colors`
     - :const:`nil`
     - Gnuplot colour string per column.
     - ``colors = {beta11="blue"}``
   * - :literal:`dashtypes`
     - :const:`nil`
     - Gnuplot dashtype string (pattern characters) per column.
     - ``dashtypes = {dx="..-- "}``
   * - :literal:`linewidths`
     - :const:`nil`
     - Line width per column.
     - ``linewidths = 2``
   * - :literal:`pointtypes`
     - :const:`nil`
     - Gnuplot point type integer per column.
     - ``pointtypes = {px=2}``
   * - :literal:`pointsizes`
     - :const:`nil`
     - Point size per column.
     - ``pointsizes = 1.5``
   * - :literal:`datastyles`
     - :literal:`{}`
     - Per-column grouped style table. Each entry may contain :literal:`style`, :literal:`color`, :literal:`dashtype`, :literal:`linewidth`, :literal:`pointtype`, :literal:`pointsize`.
     - ``datastyles = {beta11={style="lines",color="blue"}}``

**Customisation hooks**

The structure of the Gnuplot script sent by :var:`plot` is:

.. code-block:: text

    [prolog]
    setup (terminal, labels, ranges, grid, …)
    layout objects
    data block
    [plotcfg]
    plot command(s) [% plotvar]
    [epilog]

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`prolog`
     - :const:`nil`
     - Raw Gnuplot script inserted at the very beginning of the script.
     - ``prolog = "set multiplot"``
   * - :literal:`epilog`
     - :const:`nil`
     - Raw Gnuplot script appended at the very end.
     - ``epilog = "unset multiplot"``
   * - :literal:`plotcfg`
     - :const:`nil`
     - Raw Gnuplot script inserted just before the :literal:`plot` command (after data).
     - ``plotcfg = "set pm3d map"``
   * - :literal:`plotcmd`
     - :const:`nil`
     - Replacement string for the generated :literal:`plot` command(s). Supports :literal:`${cmd#}`, :literal:`${data#}`, :literal:`${using#}` etc. interpolation variables (see :ref:`sec.plot.interp`).
     - ``plotcmd = "splot ${data1} matrix"``
   * - :literal:`plotvar`
     - :const:`nil`
     - Table of extra variables for :literal:`plotcmd` interpolation.
     - ``plotvar = {color3="linecolor 'pink'"}``

**Decoration**

.. list-table::
   :widths: 14 14 42 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`font`
     - :const:`nil`
     - Default font name for all text.
     - ``font = "Arial"``
   * - :literal:`fontsize`
     - :const:`nil`
     - Default font size in points.
     - ``fontsize = 12``
   * - :literal:`titlefont`
     - :const:`nil`
     - Font name for the plot title.
     - ``titlefont = "Arial Black"``
   * - :literal:`titlesize`
     - :const:`nil`
     - Font size for the plot title.
     - ``titlesize = 18``
   * - :literal:`legendfont`
     - :const:`nil`
     - Font name for the legend.
     - ``legendfont = "Helvetica"``
   * - :literal:`legendsize`
     - :const:`nil`
     - Font size for the legend.
     - ``legendsize = 10``
   * - :literal:`legendpos`
     - :literal:`"left top"`
     - Gnuplot key position string.
     - ``legendpos = "bottom right"``
   * - :literal:`grid`
     - :const:`nil`
     - Background grid string passed to Gnuplot :literal:`set grid`. :const:`false` disables.
     - ``grid = "ytics"``
   * - :literal:`border`
     - :const:`nil`
     - Border bitmask (sum of sides: bottom=1, left=2, top=4, right=8). Default 15 (all sides).
     - ``border = 3``

**Plot position and size** (screen coordinates in :math:`[0,1]`)

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`originx`
     - :const:`nil`
     - :math:`x`-position of the plot origin in screen coordinates.
     - ``originx = 0.5``
   * - :literal:`originy`
     - :const:`nil`
     - :math:`y`-position of the plot origin in screen coordinates.
     - ``originy = 0.5``
   * - :literal:`psizex`
     - :const:`nil`
     - Plot width as a fraction of the screen.
     - ``psizex = 0.5``
   * - :literal:`psizey`
     - :const:`nil`
     - Plot height as a fraction of the screen.
     - ``psizey = 0.5``

**Misc**

.. list-table::
   :widths: 14 10 46 30
   :header-rows: 1

   * - Attribute
     - Default
     - Description
     - Example
   * - :literal:`name`
     - :const:`nil`
     - Override :literal:`${name}` in the title template (defaults to :literal:`table.name`).
     - ``name = "PSB"``
   * - :literal:`objshft`
     - :const:`1000000`
     - Starting index for Gnuplot :literal:`object` commands used by the layout. Increase if you draw more than a million objects yourself via :literal:`prolog` / :literal:`plotcfg`.
     - ``objshft = 2000000``
   * - :literal:`info`
     - :const:`nil`
     - Verbosity level for console output.
     - ``info = 2``
   * - :literal:`debug`
     - :const:`nil`
     - Debug output level.
     - ``debug = 2``

The :var:`plot` command returns itself (the command object).

.. _sec.plot.interp:

Plot command interpolation
--------------------------

When :var:`plot` generates the Gnuplot :literal:`plot` command it builds one command fragment per column using a template with numbered variables:

.. code-block:: text

    ${cmd#}${data#}${index#}${using#}with ${style#}${lines#}${points#}${color#}${title#}${axes#}${smooth#}

The :literal:`#` is replaced by the 1-based column index.  The generated variables for column :literal:`#` are:

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Variable
     - Content
   * - :literal:`cmd#`
     - :literal:`"plot "` for the first column, :literal:`"     "` for subsequent ones (continuation).
   * - :literal:`data#`
     - :literal:`"'$MAD_DATA' "` (first column) or :literal:`"'' "` (same datablock, continuation).
   * - :literal:`index#`
     - :literal:`"index N "` — the datablock index for this :math:`(x,y)` pair.
   * - :literal:`using#`
     - :literal:`"using 1:C "` where :literal:`C` is the column number in the datablock.
   * - :literal:`style#`
     - Gnuplot :literal:`with` keyword and style name.
   * - :literal:`lines#`
     - :literal:`dashtype` and :literal:`linewidth` sub-options.
   * - :literal:`points#`
     - :literal:`pointsize` and :literal:`pointtype` sub-options.
   * - :literal:`color#`
     - :literal:`linecolor '…'` sub-option.
   * - :literal:`title#`
     - :literal:`title '…'` sub-option.
   * - :literal:`axes#`
     - :literal:`axes xNyM` sub-option (e.g. :literal:`axes x1y1`).
   * - :literal:`smooth#`
     - :literal:`smooth …` sub-option (if :literal:`smooths` is set).

Supply :literal:`plotcmd` to replace the entire command; supply :literal:`plotvar` to override individual variables by number.

Examples
--------

**Optics functions with sequence layout**

Plot :math:`\beta_x` on the left axis and dispersion :math:`D_x` on the right axis, with the sequence layout on top:

.. code-block:: lua

    local beam, twiss, plot in MAD

    MADX:load("lattice.seq", "lattice.mad")
    local seq in MADX
    seq.beam = beam { particle="proton", energy=1.098 }

    local tw = twiss { sequence=seq, cofind=true }

    plot {
      sequence = seq,
      table    = tw,
      x1y1     = { s = "beta11" },
      x1y2     = { s = "dx"     },
      xlabel   = "s [m]",
      ylabel   = "β_x [m]",
      y2label  = "D_x [m]",
      title    = "PSB optics",
      legend   = { beta11 = "β_x", dx = "D_x" },
      styles   = "lines",
      output   = "optics.pdf",
    }

**Layout-only plot**

Draw just the lattice diagram without any data curves:

.. code-block:: lua

    plot {
      sequence = seq,
      layonly  = true,
      output   = "layout.pdf",
    }

**Layout inside the plot (survey plane)**

Overlay element shapes in the survey plane for a ring section:

.. code-block:: lua

    plot {
      sequence = lhcb1,
      laypos   = "in",
      range    = { "IP2", "IP4" },
      X0       = { -1231.18, 0, 2970.46 },
      A0       = { -pi/4,    0, 0        },
      data     = { bx = bet1.x, bz = bet1.z },
      x1y1     = { bx = "bz" },
      prolog   = "set size ratio -1\nset size square\n",
      epilog   = "set size noratio\nset size nosquare\n",
      xlabel   = "x [m]",
      ylabel   = "z [m]",
      styles   = "lines",
    }

**Multiple sequences in one layout**

Show two LHC beams around IP5 with the mechanical separation between them:

.. code-block:: lua

    local sstart = lhcb1:spos(lhcb1:index_of("E.DS.L5.B1"))
    plot {
      sequence = { lhcb1, lhcb2 },
      range    = { {"E.DS.L5.B1", "S.DS.R5.B1"},
                   {"E.DS.L5.B2", "S.DS.R5.B2"} },
      laydisty = lhcb2["E.DS.L5.B2"].mech_sep,
      layshift = sstart,
      layonly  = true,
    }

**Per-column data style**

Set independent styles for two curves:

.. code-block:: lua

    plot {
      table    = tw,
      x1y1     = { s = {"beta11", "beta22"} },
      styles   = { beta11 = "lines",      beta22 = "linespoints" },
      colors   = { beta11 = "dark-blue",  beta22 = "dark-red"    },
      linewidths = 2,
      legend   = { beta11 = "β_x", beta22 = "β_y" },
    }

**Save to PDF and dump the Gnuplot script**

.. code-block:: lua

    plot {
      sequence = seq,
      table    = tw,
      x1y1     = { s = "beta11" },
      output   = "beta.pdf",
      scrdump  = "beta.gp",
    }

**Custom Gnuplot commands via prolog/epilog**

.. code-block:: lua

    plot {
      table   = tw,
      x1y1    = { s = "beta11" },
      prolog  = "set multiplot layout 1,2",
      epilog  = "unset multiplot",
    }

**Reuse a layout across multiple plot calls (``"keep"``)**

The first call draws the layout; subsequent calls on the same :literal:`sid` reuse it without recomputing:

.. code-block:: lua

    plot { sequence = seq, table = tw1, x1y1 = { s = "beta11" } }
    plot { sequence = "keep", table = tw2, x1y1 = { s = "beta22" } }

**Element colour customisation**

.. code-block:: lua

    plot {
      sequence  = seq,
      kindcolor = {
        quadrupole = "blue",
        sbend      = { fillcolor = "red", fillstyle = "solid",
                       linecolor = "black" },
      },
      layonly   = true,
    }

**Deferred execution**

Set :literal:`exec=false` to build a template that can be specialised without re-specifying all attributes:

.. code-block:: lua

    local base = plot {
      exec     = false,
      styles   = "lines",
      linewidths = 2,
      fontsize = 12,
      output   = "optics.pdf",
    }

    -- specialise for beta functions
    base { sequence = seq, table = tw, x1y1 = { s = "beta11" } }

See also: :doc:`mad_cmd_twiss`, :doc:`mad_cmd_track`, :doc:`mad_cmd_survey`,
:doc:`mad_gen_mtable`.
