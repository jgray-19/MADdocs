.. _ch.prg.cmd:

Commands
========

This page gives a conservative programming view of MAD-NG command objects,
based on the current implementation in :literal:`MAD/src/madl_command.mad`
and the concrete command modules in :literal:`madl_track.mad`,
:literal:`madl_survey.mad`, :literal:`madl_cofind.mad`, and
:literal:`madl_twiss.mad`.

What a Command Is
-----------------

The root command object is created in :literal:`madl_command.mad` as:

.. code-block:: mad

   local command = object 'command' {}

The same file then gives it command identity and execution behavior through
metamethods:

* a private :literal:`__cmd` marker is used for :literal:`is_command`
* :literal:`__init` calls an internal :literal:`exec` helper
* if :literal:`exec=false`, the configured object is left unevaluated
* if :literal:`exec` is callable, it is promoted into the metatable as
  :literal:`__exec`
* otherwise, an already-installed :literal:`__exec` is run

In practical terms, a command object is a configured object that normally
executes when constructed, unless the caller explicitly disables execution.

How Concrete Commands Are Declared
----------------------------------

The major physics commands follow the same pattern.

For example:

* :literal:`madl_track.mad` defines :literal:`local track = command 'track' { ... }`
* :literal:`madl_survey.mad` defines :literal:`local survey = command 'survey' { ... }`
* :literal:`madl_cofind.mad` defines :literal:`local cofind = command 'cofind' { ... }`
* :literal:`madl_twiss.mad` defines :literal:`local twiss = command 'twiss' { ... }`

Each of these objects has:

* a block of user-facing attributes with defaults
* an :literal:`exec=exec` field that points at the module-local execution
  function
* an :literal:`__attr` table listing setup attributes and, where needed,
  :literal:`noeval` fields
* a final :literal:`:set_readonly()` so the reference command object itself is
  treated as immutable

Each module then returns the command by name, for example
:literal:`return { track = track }`, which is how the embedded module exposes
it through :literal:`MAD`.

Construction and Invocation
---------------------------

The normal user-facing form is:

.. code-block:: mad

   local track in MAD
   local mtbl, mflw = track { sequence=seq, beam=seq.beam }

That construction both creates the configured command object and executes it.

The source also relies on a non-executing form for command composition:

.. code-block:: mad

   local _, mflw = track  { exec=false } :copy_variables(self)
   local _, mflw = cofind { exec=false } :copy_variables(self)

Current examples in the source use this pattern to reuse attribute sets while
building higher-level commands:

* :doc:`mad_cmd_cofind` builds on :doc:`mad_cmd_track`
* :doc:`mad_cmd_twiss` reuses both :doc:`mad_cmd_cofind` and
  :doc:`mad_cmd_track`

What Lives Where
----------------

For the commands inspected in this pass, the implementation split is:

* :literal:`madl_command.mad` provides the generic command object
* :literal:`madl_track.mad` defines the tracking command and its mflow/mtable
  setup
* :literal:`madl_survey.mad` defines the survey command and its geometry flow
* :literal:`madl_cofind.mad` defines closed-orbit search on top of track-style
  setup
* :literal:`madl_twiss.mad` defines optics analysis on top of track and
  cofind-derived setup

This means the programming-level command abstraction is thin: the generic
module provides the lifecycle hook, while the real semantics live in each
command module.

Minimal Example
---------------

.. code-block:: mad

   local survey in MAD

   local mtbl, mflw = survey {
     sequence = seq,
     save     = true,
     exec     = true,
   }

The corresponding programming detail is that :literal:`survey` is already a
readonly reference command object, and the construction above creates and runs
a configured child object.

Open Points
-----------

This page stays intentionally conservative. The following areas still need
deeper work before they should be documented in more detail:

* how much attribute evaluation happens before :literal:`exec`
* the full semantics of :literal:`noeval`
* contributor guidance for defining entirely new commands

See Also
--------

* :doc:`mad_prg_mad`
* :doc:`mad_prg_elements`
* :doc:`mad_cmd_track`
* :doc:`mad_cmd_survey`
* :doc:`mad_cmd_cofind`
* :doc:`mad_cmd_twiss`
