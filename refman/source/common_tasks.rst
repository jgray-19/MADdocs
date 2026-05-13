Common Tasks
============

This page is a collection of self-contained task guides for the most common
MAD-NG workflows.  Each section has a goal, prerequisites, a minimal runnable
example, notes on important inputs and outputs, and common pitfalls.

All examples run from the repository root and use the PSB sequence shipped with
this documentation:

* :file:`doc_sequences/psb3_saved.seq`

----

Load MAD-X Sequences and Optics
---------------------------------

**Goal:** convert a MAD-X sequence file and an optics (strengths) file into
MAD-NG objects.

.. literalinclude:: ../../verified_examples/load_madx_minimal.mad
   :language: mad

**Important inputs**

* :literal:`MADX:load(seq_file, opt_file)` — the first argument is the MAD-X
  sequence file; the second is the optics (strengths) file.
* :literal:`local seq in MADX` — retrieves the sequence by its MAD-X name from
  the :literal:`MADX` environment.
* :literal:`seq.beam = beam { ... }` — attaches a beam; required before any
  physics command.

**Common pitfalls**

* :literal:`MADX:load` must be called before any name is extracted from
  :literal:`MADX`.
* MAD-X names are case-insensitive in MAD-X but lowercased by :literal:`MADX:load`.
* If the sequence file uses :literal:`CALL` to include other files, those files
  must be present relative to the working directory.

See :doc:`mad_gen_madx` and :doc:`mad_gen_beam`.

----

Run a Survey Calculation
--------------------------

**Goal:** compute the 3-D geometry of a sequence — Cartesian positions and
orientation angles of every element in the global reference frame.

.. literalinclude:: ../../verified_examples/survey_minimal.mad
   :language: mad

**Important inputs**

* :literal:`sequence` — the lattice to survey.
* :literal:`X0` (optional) — initial survey state
  :literal:`{x, y, z, theta, phi, psi}`; defaults to the origin looking along
  :math:`z`.
* :literal:`dir` (optional, default :const:`1`) — use :const:`-1` to survey
  backwards.

**Important outputs**

* Columns :literal:`x`, :literal:`y`, :literal:`z` — Cartesian coordinates.
* Columns :literal:`theta`, :literal:`phi`, :literal:`psi` — Tait–Bryan rotation
  angles of the local frame.
* Column :literal:`angle` — accumulated bending angle.

**Common pitfalls**

* :literal:`survey` does not find a closed orbit; it propagates geometry only.
* For a nominally closed ring, the survey should return close to its starting
  point.  A large gap signals a bending-angle mismatch.

See :doc:`mad_cmd_survey`.

----

Run a Twiss Calculation
------------------------

**Goal:** compute linear optics functions (beta functions, phase advances,
dispersion, tunes).

.. literalinclude:: ../../verified_examples/twiss_minimal.mad
   :language: mad

**Important inputs**

* :literal:`sequence` — the lattice (must have a beam attached).
* :literal:`cofind` (default :const:`true`) — searches for the closed orbit
  automatically before propagating optics.

**Important outputs**

* Scalar summaries: :literal:`tw.q1`, :literal:`tw.q2`, :literal:`tw.dq1`,
  :literal:`tw.dq2`, :literal:`tw.alfa`, :literal:`tw.gammatr`.
* Column arrays: :literal:`tw["beta11"]`, :literal:`tw["beta22"]`,
  :literal:`tw["mu1"]`, :literal:`tw["mu2"]`, :literal:`tw["dx"]`, etc.
* :literal:`tw:write(filename, cols)` writes selected columns to a TFS file.

**Common pitfalls**

* A :literal:`"lost particle"` error means the lattice is unstable at the given
  energy; check element strengths and beam parameters.
* Column names use a double-index suffix: :literal:`beta11` is
  :math:`\beta_x`, :literal:`beta22` is :math:`\beta_y`.

See :doc:`mad_cmd_twiss`.

----

Track Particles Through a Sequence
------------------------------------

**Goal:** transport one or more particles through a sequence for one or more
turns and write the turn-by-turn coordinates to a TFS file.

.. literalinclude:: ../../verified_examples/track_minimal.mad
   :language: mad

**Important inputs**

* :literal:`sequence` — the lattice (must have a beam attached).
* :literal:`X0` — initial 6D coordinate table
  :literal:`{x, px, y, py, t, pt}`.
* :literal:`nturn` — number of turns through the sequence.
* :literal:`deltap` (optional) — relative momentum deviation; converted
  internally to :literal:`pt`.

**Important outputs**

* The returned :literal:`trk` is an :literal:`mtable` with one row per element
  visit per turn.
* :literal:`trk:write(filename, cols)` writes selected columns to a TFS file.

**Common pitfalls**

* If the table is empty, check that the sequence is non-empty and
  :literal:`nturn` is at least 1.
* If tracking fails with missing-beam errors, ensure a beam is attached.

See :doc:`mad_cmd_track`.

----

Search for a Closed Orbit
---------------------------

**Goal:** find the periodic closed orbit of a circular machine.

.. literalinclude:: ../../verified_examples/cofind_minimal.mad
   :language: mad

**Important inputs**

* :literal:`X0` — a list of initial guess vectors.  Each entry is a 6D table.
  Near zero is usually sufficient for an ideal lattice.
* :literal:`save=true` — saves element-by-element coordinates in the returned
  :literal:`mtable`.
* :literal:`coitr` — maximum Newton iterations.

**Important outputs**

* First return: an :literal:`mtable` with element-by-element closed-orbit
  coordinates.
* Second return: a map flow list.  Each entry :literal:`mf[i]` carries:
  :literal:`status` (:literal:`"stable"` on success), :literal:`coitr`,
  :literal:`rank`, and :literal:`mf[i]:get0()` for the 6D state vector at the
  start of the sequence.

**Common pitfalls**

* :literal:`"unstable"` status means the orbit exists but the one-turn map
  eigenvalues are off the unit circle; the machine is linearly unstable.
* If Newton iterations hit :literal:`coitr`, try a larger limit or a better
  initial guess.

See :doc:`mad_cmd_cofind`.

----

Match Optics
-------------

**Goal:** adjust quadrupole strengths to reach specified optics targets (here:
horizontal and vertical tunes).

.. literalinclude:: ../../verified_examples/match_optics_minimal.mad
   :language: mad

**Important inputs**

* :literal:`command` — a deferred call (using :literal:`:=`) to the physics
  command; :literal:`match` re-evaluates it at each iteration.
* :literal:`variables` — list of variables to vary.  Each entry specifies
  :literal:`var` as a dotted global path (e.g. :literal:`"MADX.kbrqf"`).
* :literal:`equalities` — list of constraints.  Each :literal:`expr` is a
  function of the command result that should be zero at the solution.
* :literal:`broyden=true` — enables rank-1 Jacobian updates to reduce the
  number of :literal:`twiss` evaluations.

**Important outputs**

* :literal:`status` — stopping reason.  :literal:`"FMIN"` is the normal success
  code for least-squares matching.
* :literal:`fmin` — achieved residual.
* :literal:`ncall` — number of objective evaluations.
* After the match, variables are left at their matched values in the global
  environment.

**Common pitfalls**

* Variable strings must be exact global paths; a typo creates a new global
  instead of modifying the intended strength.
* Use :literal:`info=1` or :literal:`info=2` to monitor convergence.

See :doc:`mad_cmd_match`.

----

Observe and Unobserve Elements
--------------------------------

**Goal:** control which elements appear in the output mtable of :var:`track`
and :var:`twiss`, by marking specific elements as *observed*.

.. literalinclude:: ../../verified_examples/observe_minimal.mad
   :language: mad

The observation flag is a per-element flag from :literal:`MAD.element.flags`.
Only elements with the flag set are saved when the command attribute
:literal:`observe >= 1`.  :literal:`observe = 0` bypasses the flag entirely
and saves every element.

**Observe elements by name or pattern**

.. code-block:: mad

   local observed in MAD.element.flags

   -- observe a single element by exact name
   seq:select(observed, {pattern = "^ip1$"})

   -- observe every element whose name starts with "bpm"
   seq:select(observed, {pattern = "^bpm"})

**Observe elements by kind**

.. code-block:: mad

   local observed in MAD.element.flags

   -- observe all quadrupoles
   seq:select(observed, {class = MAD.element.quadrupole})

**Observe or clear a single element**

.. code-block:: mad

   local observed in MAD.element.flags

   seq[seq:index_of('ip1')]:set_flags(observed)
   seq[seq:index_of('ip1')]:clear_flags(observed)

**Important notes**

* :literal:`seq:select(flag, selector)` calls :literal:`elm:set_flags(flag)`
  on every matching element.
* :literal:`seq:deselect(flag, selector)` calls :literal:`elm:clear_flags(flag)`
  on matched elements; with no selector it affects **all** elements.
* A selector can be :literal:`{class=...}`, :literal:`{pattern=...}`,
  :literal:`{range="a/b"}`, or a list of element names — see
  :doc:`mad_gen_sequence` for the full syntax.
* :literal:`observe = 0` in :var:`track` or :var:`twiss` saves every element
  unconditionally and ignores the flag.
* :literal:`observe = 1` (default for :var:`track`) saves only observed
  elements once per turn; larger values save every :math:`n` turns.

See :doc:`mad_cmd_track`, :doc:`mad_cmd_twiss`, and :doc:`mad_gen_sequence`.

----

Parametric Optics and RDTs
---------------------------

For derivative-aware optics and resonance driving terms, see
:doc:`parametric_optics_and_rdts`.

----

Save and Inspect ``mtable`` Results
-------------------------------------

**Goal:** access scalar summaries and column arrays from any :literal:`mtable`,
and write selected columns to a TFS file.

.. literalinclude:: ../../verified_examples/save_inspect_mtable_minimal.mad
   :language: mad

**Important inputs**

* :literal:`mt:write(filename, cols)` — writes to :file:`filename.tfs`.
  :literal:`cols` is an optional list of column names.

**Important outputs**

* Scalar summaries are fields: :literal:`tw.q1`, :literal:`tw.dq1`,
  :literal:`tw.alfa`.
* Column data: :literal:`tw["beta11"]` returns a column array; use
  :literal:`col[i]` and :literal:`#col` for element access.
* Individual rows: :literal:`tw[i]` is a table with all column values for row
  :literal:`i`.

**Common pitfalls**

* Column arrays are C-backed cdata, not plain Lua tables.  Functions like
  :literal:`table.unpack` do not work on them; use numeric indexing instead.
* Writing without specifying columns can produce very large files.
* :literal:`mt:print()` prints the full TFS-formatted table to stdout — useful
  for quick inspection without writing a file.
* :literal:`MAD.tostring(t)` converts plain Lua tables to a readable string.
  MAD objects (mtables, vectors, maps) use :literal:`:print()` instead.

See :doc:`mad_gen_mtable`.

----

Use Python Integration (pymadng)
----------------------------------

**Goal:** control MAD-NG from Python, run :literal:`twiss`, and retrieve the
result table.

.. literalinclude:: ../../verified_examples/pymadng_minimal.py
   :language: python

**How it works**

:literal:`pymadng` launches a MAD-NG subprocess and communicates over a binary
pipe.

* **String-based:** :literal:`mad.send(...)` sends MAD-NG code;
  :literal:`py:send(obj)` on the MAD side returns the object to Python via
  :literal:`mad.recv(name)`.
* **Pythonic:** :literal:`mad.MADX.load(...)`, :literal:`mad.seq.beam = ...`,
  :literal:`mad["tw"] = mad.twiss(...)` translate Python calls into MAD-NG
  automatically.

**Common pitfalls**

* String arguments in the Pythonic interface must be double-quoted inside the
  Python string so they arrive as MAD-NG string literals.
* The MAD-NG subprocess shares the Python working directory; relative paths in
  :literal:`MADX:load` are resolved from there.

See the `pymadng repository <https://github.com/MethodicalAcceleratorDesign/MAD-NG.py>`_.

----

Where To Go Next
-----------------

* :doc:`quickstart` — a short route through the manual
* :doc:`parametric_optics_and_rdts` — derivative-aware optics and RDTs
* :doc:`mad_gen_intro` — language and environment overview
* :doc:`mad_gen_madx` — MAD-X compatibility layer
* :doc:`mad_cmd_survey`, :doc:`mad_cmd_twiss`, :doc:`mad_cmd_track`,
  :doc:`mad_cmd_cofind`, :doc:`mad_cmd_match`
