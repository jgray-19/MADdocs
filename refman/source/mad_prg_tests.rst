.. _ch.prg.tests:

Tests
=====

This page gives a first practical overview of how testing appears in the
current MAD-NG tree and in this documentation repository.

It is not yet a full reference for the :literal:`utest` module. The embedded
help in :literal:`src/help/madh_utest.mad` is currently very small and points
readers to LuaUnit rather than documenting a large MAD-NG-specific test API.

Current Testing Layers
----------------------

From the current repository layout, three different testing styles are visible:

* source-level tests and test drivers inside :literal:`MAD/src`
* larger runnable examples in :literal:`MAD/examples`
* small locally verified scripts in this docs repo under
  :literal:`verified_examples/`

Those layers serve different purposes:

* :literal:`src` tests are closest to implementation checks
* :literal:`examples` demonstrate larger workflows and regressions
* :literal:`verified_examples` are deliberately small scripts used to support
  direct documentation claims

The `utest` Module
------------------

The embedded help describes :literal:`utest` as providing utilities for
writing unit tests and test suites, and refers readers to LuaUnit.

From that help text alone, the safe current statement is:

* :literal:`utest` exists as a testing-related module in the MAD-NG runtime
* it is intended for unit-test and test-suite support
* its documentation in this repo is not yet complete enough to serve as a full
  API reference

Until the module itself is documented in more detail, it is better to treat
:literal:`utest` as an internal or advanced testing aid rather than as the
main entry point for end-user documentation.

Observable Test Patterns
------------------------

Several concrete test patterns are already visible in the current tree.

Assertion-based script checks
"""""""""""""""""""""""""""""

Small scripts often use plain :literal:`assert(...)` checks for validation.

Current examples in this docs repo include:

* :literal:`verified_examples/cofind_minimal.mad`
* :literal:`verified_examples/trkopt_minimal.mad`
* :literal:`verified_examples/trkrdt_minimal.mad`

This style is useful when the goal is to prove one narrow claim, for example:

* a requested column exists
* a closed-orbit search converges
* a protected result such as :literal:`__nf` is present

Standalone runnable drivers
"""""""""""""""""""""""""""

The source tree also contains standalone runnable files such as:

* :literal:`MAD/src/test_track.mad`
* :literal:`MAD/src/test_track.madng`

These are valuable because they exercise real command workflows rather than
only isolated helper functions.

Example-based regression coverage
"""""""""""""""""""""""""""""""""

Many files in :literal:`MAD/examples` are effectively test cases for larger
workflows, even when they were not written as minimal unit tests.

In practice they help answer questions such as:

* does this workflow still execute with the current binary?
* does a saved-sequence import still work?
* do advanced :literal:`twiss` / :literal:`trkopt` setups still run?

Testing Guidance for Documentation Work
---------------------------------------

For this documentation repository, the most useful pattern is the small,
explicitly validated script.

Current working rules are:

1. Prefer one narrow workflow per script.
2. Use :literal:`assert(...)` for the specific behavior the docs rely on.
3. Run the script locally with :literal:`./mad`.
4. Cite the script from the manual with :literal:`literalinclude` when
   practical.
5. Do not cite a large upstream example directly unless it has first been
   checked for current executability.

This is why the docs repo now keeps:

* :literal:`VERIFIED_EXAMPLES_SHORTLIST.md`
* :literal:`verified_examples/*.mad`

Minimal Pattern
---------------

The current verified examples use a pattern like:

.. code-block:: mad

   local beam, twiss, damap in MAD

   MADX:load("doc_sequences/psb3_saved.seq",
             "doc_sequences/psb3_saved.mad")

   local psb3 in MADX
   psb3.beam = beam { particle="proton", energy=1.098 }

   local tw = twiss {
     sequence=psb3,
     X0=damap { nv=6, no={3,3,3,3,1,1} },
     trkrdt={"f3000", "f2100"},
     saveanf=true,
   }

   assert(tw["f3000"], "missing f3000")
   assert(tw["f2100"], "missing f2100")
   assert(tw["__nf"],  "missing __nf")

This style is simple, readable, and directly usable for documentation
verification.

Open Points
-----------

The following testing topics still need fuller documentation:

* the actual public API of :literal:`MAD.utest`
* whether there is a preferred test-suite runner inside the MAD-NG tree
* how source-level tests are expected to be executed by contributors
* how documentation validation should eventually be automated

See Also
--------

* :doc:`mad_prg_modules`
* :doc:`mad_prg_mad`
* :doc:`mad_cmd_track`
