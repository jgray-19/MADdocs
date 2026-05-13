.. _ch.prg.madenv:

MAD environment
===============

This programming section exists primarily to document expert-facing mechanisms
that are part of MAD-NG itself: debugging, command/object internals, module
plumbing, and FFI boundaries.

For normal usage (loading sequences, running commands, and interpreting
outputs) prefer the Part I–IV pages. The single most important entry point on
the programming side is :literal:`MAD.dbg`, documented in :doc:`mad_prg_debug`.

Module-Level Environments
-------------------------

For programming purposes, treat :literal:`MAD` and :literal:`MADX` as the two
primary module environments:

* :literal:`MAD` is the top-level environment that exposes embedded modules,
  constructors, and utilities.
* :literal:`MADX` is the compatibility environment that stores imported MAD-X /
  MAD8 names and provides import helpers.

In scripts, prefer explicit local bindings so dependencies are visible:

.. code-block:: mad

   local beam, twiss, dbg in MAD
   local seq in MADX

   seq.beam = beam { particle="proton", energy=450 }
   dbg() -- interactive breakpoint if armed
   tw, mflw = twiss { sequence=seq }

This page intentionally avoids re-documenting normal workflows and syntax that
are covered elsewhere. The pages under Programming are meant to answer:

* how to debug MAD-NG execution (:doc:`mad_prg_debug`)
* how command objects are built and invoked (:doc:`mad_prg_commands`)
* how element objects and lookup behave internally (:doc:`mad_prg_elements`)
* how modules are imported/exported (:doc:`mad_prg_modules`)

See also
--------

* :doc:`mad_prg_debug`
* :doc:`mad_prg_modules`
* :doc:`mad_prg_commands`
