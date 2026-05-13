##########
Quickstart
##########

This page gives a short route through the manual for a first useful MAD-NG
session. It assumes that you already have a MAD-NG binary available locally.

0. Locate the MAD-NG Binary
---------------------------

Make sure the MAD-NG executable is available. In this repository, the binary
is typically called :literal:`mad` and lives at the repository root. If you
installed from a release, use the path to the downloaded binary instead.

Official binaries are published at:

* https://madx.web.cern.ch/releases/madng/1.1/

1. Start MAD-NG
---------------

Launch MAD-NG in interactive mode:

.. code-block:: console

   $ rlwrap ./mad

You should see the MAD-NG banner and a prompt. For the full startup options and
interactive behaviour, see :doc:`mad_gen_intro`.

2. Load a Sequence
------------------

In practical workflows, the most common path is to load a saved sequence or a
MAD-X lattice description into the :literal:`MADX` compatibility environment:

.. code-block:: mad

   MADX:load("fodo.seq", "fodo.mad")
   local seq in MADX

This gives you a MAD-NG sequence object that can be used directly by
:literal:`survey`, :literal:`twiss`, and :literal:`track`.

For more detail, see :doc:`mad_gen_madx`.

If you want a concrete starting point from this repo, look in :file:`doc_sequences/`
for saved sequences and translated inputs (for example :file:`sps.seq` /
:file:`sps.mad`).

If you are reading the published docs and do not have the repository checked
out locally, fetch these files by cloning the documentation repository:

.. code-block:: console

   $ git clone https://github.com/jgray-19/MADdocs.git
   $ cd MADdocs

3. Attach a Beam
----------------

After loading a sequence, attach a beam explicitly:

.. code-block:: mad

   seq.beam = beam { particle="proton", energy=450 }

The exact beam attributes depend on your machine and workflow. See
:doc:`mad_gen_beam`.

4. Run Survey
-------------

Use :literal:`survey` when you need element placement and reference-frame
information:

.. code-block:: mad

   srv, sflow = survey { sequence=seq }

The returned table can be written to file or inspected in memory. See
:doc:`mad_cmd_survey`.

5. Run Twiss
------------

For optics calculations, :literal:`twiss` is usually the next command:

.. code-block:: mad

   tws, tflow = twiss { sequence=seq }

This produces an :literal:`mtable` with optics quantities such as the position,
beta functions, phase advances, and dispersion. See :doc:`mad_cmd_twiss`.

6. Run Track
------------

For particle transport or turn-by-turn studies:

.. code-block:: mad

   trk, flow = track {
       sequence=seq,
       X0={x=1e-3, px=0, y=0, py=0},
       nturn=1,
   }

For realistic workflows, :literal:`track` is also used with explicit
:literal:`range`, :literal:`dir`, observed BPMs, and multiple particles. See
:doc:`mad_cmd_track`.

7. Inspect Results
------------------

The command outputs are usually returned as an :literal:`mtable` plus a map
flow object. The table is the main user-facing result:

.. code-block:: mad

   tws:write("twiss.tfs")
   trk:write("track.tfs")

You can then check that the files were created:

.. code-block:: console

   $ ls twiss.tfs track.tfs
   twiss.tfs  track.tfs

For the data model behind those outputs, see :doc:`mad_gen_mtable`.

Next Steps
==========

After this page, the most useful follow-up pages are:

* :doc:`common_tasks`
* :doc:`parametric_optics_and_rdts`
* :doc:`mad_gen_madx`
* :doc:`mad_cmd_survey`
* :doc:`mad_cmd_twiss`
* :doc:`mad_cmd_track`
