.. MAD-NG documentation master file, created by
   sphinx-quickstart on Wed Aug 24 15:30:21 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Unofficial MAD-NG Reference Manual!
==================================================

This manual is an unofficial working reference for MAD-NG users and developers.
It is intended to make the existing reference material easier to navigate while
the documentation is being expanded.

It was initially created by Laurent Deniau and is unofficialy maintained by
Joshua Gray. AI was used in the editing process, and therefore some of the text
may be AI-generated or AI-edited, leading to potential inaccuracies or inconsistencies.
If you notice any issues, please report them by opening an issue in the MAD-NG.py
repository, or speaking to the unofficial maintainer directly.

What Is MAD-NG?
===============

MAD-NG is a standalone accelerator-physics environment for sequence handling,
optics, survey, tracking, matching, differential algebra, and model analysis.

.. important::
   **Particle Charge Compatibility:** MAD-X lattice files typically define k values assuming positive particle charges. If you select a negatively charged particle (e.g., electrons) in your beam, :doc:`track <mad_cmd_track>` and :doc:`twiss <mad_cmd_twiss>` calculations may fail. To restore MAD-X-compatible behavior, set ``MAD.option.nocharge = true`` before running calculations.

In practical workflows, users commonly:

* load saved sequences through :doc:`MADX interoperability <mad_gen_madx>`
* attach a :doc:`beam <mad_gen_beam>` to a sequence
* run :doc:`survey <mad_cmd_survey>`, :doc:`twiss <mad_cmd_twiss>`, and :doc:`track <mad_cmd_track>`
* export and post-process results through :doc:`mtable <mad_gen_mtable>`

Start Here
==========

If you are new to this manual, start with:

* :doc:`Quickstart <quickstart>`
* :doc:`Common Tasks <common_tasks>`
* :doc:`Parametric Optics and RDTs <parametric_optics_and_rdts>`
* :doc:`Introduction <mad_gen_intro>`

Common Tasks
============

The most common practical workflows are:

* load a MAD-X sequence and optics into :doc:`MADX <mad_gen_madx>`
* attach a :doc:`beam <mad_gen_beam>` and inspect the imported :doc:`sequence <mad_gen_sequence>`
* run :doc:`twiss <mad_cmd_twiss>` to compute optics tables
* use :doc:`parametric_optics_and_rdts` for derivatives, sensitivities, and resonance driving terms
* run :doc:`track <mad_cmd_track>` for turn-by-turn tracking
* run :doc:`survey <mad_cmd_survey>` for the global picture of the lattice
* export and post-process results through :doc:`mtable <mad_gen_mtable>`

Additional Resources
====================

For quick syntax references and comparisons with other languages:

* `MAD-NG Language Cheatsheet <https://methodicalacceleratordesign.github.io/MAD-NG/madng-cheatsheet.html>`_ - Compact reference for MAD-NG syntax, operators, data types, and common pitfalls.
* `MAD-NG vs MATLAB/Python/Julia Comparison <https://methodicalacceleratordesign.github.io/MAD-NG/madng-comparison-cheatsheet.html>`_ - Side-by-side syntax comparisons for vectors, matrices, operations, and programming constructs.

Repository Assets
=================

This repo also ships a few local assets that examples and docs may reference:

* :file:`doc_sequences/` - a small set of saved MAD-X sequences and translated :literal:`.mad` inputs (for example SPS and PSB3).
* :file:`verified_examples/` - minimal examples used by the manual via :literalinclude.
* :file:`refman/source/` - the Sphinx manual sources themselves.

Structure
=========

The rest of the manual is still organised primarily as a reference manual. The
five main parts are kept below.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   /quickstart.rst
   /common_tasks.rst
   /basic_differentiable_orbit_response.rst
   /parametric_optics_and_rdts.rst

.. toctree::
   :maxdepth: 3
   :caption: Part I: Language

   /mad_gen_index.rst

.. toctree::
   :maxdepth: 3
   :caption: Part II: Commands

   /mad_cmd_index.rst

.. toctree::
   :maxdepth: 3
   :caption: Part III: Physics

   /mad_phy_index.rst

.. toctree::
   :maxdepth: 3
   :caption: Part IV: Modules

   /mad_mod_index.rst

.. toctree::
   :maxdepth: 3
   :caption: Part V: Programming

   /mad_prg_index.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
