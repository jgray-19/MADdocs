.. _ch.prg.mod:

Modules
=======

This page gives a first practical overview of how modules appear in current
MAD-NG code.

It is intentionally limited to patterns that are directly visible in the
current manual, embedded help, and shipped examples. It does not try to
describe undocumented internals of the module loader.

Two module patterns appear repeatedly in the code base:

* embedded modules exposed through the top-level :literal:`MAD` environment
* local helper modules loaded with :literal:`require`

Embedded Modules
----------------

Most day-to-day MAD-NG scripts use embedded modules through :literal:`MAD`.

Typical examples from the source tree and manual are:

.. code-block:: mad

   local beam, twiss, survey in MAD
   local quadrupole in MAD.element
   local printf in MAD.utility
   local real, imag in MAD.gmath

In other words, module access is usually done by retrieving selected names into
local scope, not by exporting everything into globals.

From the current code base, common embedded module namespaces include:

* :literal:`MAD.element`
* :literal:`MAD.utility`
* :literal:`MAD.gmath`
* :literal:`MAD.gfunc`
* :literal:`MAD.gphys`
* :literal:`MAD.typeid`
* :literal:`MADX`

The :doc:`mad_prg_mad` page documents the main environment itself. This page is
about how modules are then used from that environment.

Recommended access pattern
--------------------------

The most common and least ambiguous style in the current examples is:

.. code-block:: mad

   local beam, twiss in MAD
   local sequence, quadrupole in MAD.element
   local printf in MAD.utility

This keeps dependencies visible and avoids relying on names being present in
the global environment.

The alternative style also exists:

.. code-block:: mad

   local qf = MAD.element.quadrupole "qf" { l=1.0, k1=0.25 }
   local b1 = MAD.beam { particle="proton", energy=450 }

Both forms are visible in current material. The first is more common in longer
scripts.

Loading Local Helper Modules
----------------------------

The shipped examples also use :literal:`require` for helper modules that live
next to the main script.

For example, :literal:`MAD/examples/ex-fodo-trkopt/ex-fodo-trkopt.mad`
contains:

.. code-block:: mad

   local twiss_4plot, plot_twiss, plot_chrom, plot_wchrom, tw_cols =
     in require "toolbox"

This pattern is useful for:

* plot helpers
* reusable example-local utilities
* splitting a larger study into several files

Important practical point:

* such scripts may depend on their working directory
* a script using :literal:`require "toolbox"` is not automatically runnable
  from an arbitrary directory unless the required module is also on the MAD-NG
  package search path

That working-directory sensitivity is one reason the documentation in this repo
prefers small locally verified scripts for direct citation.

Advanced Environment Management
-------------------------------

The embedded help for :literal:`MAD`, :literal:`import`, and
:literal:`export` describes two environment-management helpers:

.. code-block:: mad

   local import, export in MAD

   import("module")
   import({name=myfun})

   export({"sin", "cos", "tan"}, {})

From the embedded help in :literal:`MAD/src/help/madh_main.mad`, the current
behavior is:

* :literal:`MAD.import(...)` imports module or table content into the
  :literal:`MAD` environment
* if the first argument is a string, it is treated as a module name and loaded
  through :literal:`require` before import processing continues
* raw tables are flattened into the :literal:`MAD` environment
* :literal:`MAD.export(...)` exports selected names from :literal:`MAD` into a
  destination context, or into :literal:`_G` if no destination is provided

These helpers are useful when building a custom working environment, but they
are not the recommended first style for ordinary user scripts. In this manual
they should be treated as expert tools:

* use them when you intentionally want to construct or reshape an environment
* avoid them when simple :literal:`local ... in MAD` bindings are clearer
* avoid broad exports to :literal:`_G` in documentation aimed at new users

When To Use Which Pattern
-------------------------

For practical documentation purposes, the current patterns can be summarized as
follows:

* use :literal:`local ... in MAD` for normal scripts
* use :literal:`MAD.<module>.<name>` when explicit qualification improves
  readability
* use :literal:`require "..."` for helper modules stored as separate files
* use :literal:`MAD.import` and :literal:`MAD.export` when intentionally
  constructing or reshaping an environment in expert-oriented code

Minimal Example
---------------

.. code-block:: mad

   local beam, twiss in MAD
   local quadrupole, sequence in MAD.element
   local printf in MAD.utility

   local qf = quadrupole "qf" { l=1.0, k1=0.25 }
   local seq = sequence "line" { qf { at=0 }, l=2.0 }
   seq.beam = beam { particle="proton", energy=450 }

   local tw = twiss { sequence=seq }
   printf("q1 = %.6f\n", tw.q1)

Open Points
-----------

This page is only a first useful version.

Topics that still need deeper documentation include:

* the exact search-path behavior for :literal:`require`
* how to package larger reusable MAD-NG libraries cleanly
* when :literal:`MAD.import` is genuinely preferable to explicit locals
* how module conventions differ between embedded MAD-NG modules and external
  Lua/MAD helper files

See Also
--------

* :doc:`mad_prg_mad`
* :doc:`mad_prg_debug`
* :doc:`mad_gen_script`
* :doc:`mad_gen_madx`
* :doc:`mad_mod_miscfuns`
