Basic Differentiable Orbit Response (PSB)
=========================================

This example shows a minimal, runnable orbit-response workflow using MAD-NG's
basic differentiable machinery. It uses a saved PSB sequence and computes the
response of BPM orbits to horizontal and vertical corrector kicks.

The goal is to demonstrate:

* how to build a DA map with named parameters
* how to promote corrector kicks into those parameters
* how to extract first-order derivatives from the saved maps

Prerequisites
-------------

This example assumes you run from the repository root and use the provided
sequence files:

* doc_sequences/psb3_saved.seq
* doc_sequences/psb3_saved.mad

If you run from another directory, update the paths accordingly.

Example
-------

.. code-block:: mad

   local beam, damap, track, matrix in MAD

   MADX:load("doc_sequences/psb3_saved.seq", "doc_sequences/psb3_saved.mad")

   local psb3 in MADX
   psb3.beam = beam { particle="proton", energy=1.098 } ! around 160 MeV kinetic energy (proton rest mass is about 938 MeV)

   local observed in MAD.element.flags
    psb3:select(observed, {pattern="BR3.BPM"})

   local horizontal_correctors = {}
   local vertical_correctors = {}

   psb3:foreach{
       action=\e -> table.insert(horizontal_correctors, e.name),
       pattern="BR3.DHZ",
   }

   psb3:foreach{
       action=\e -> table.insert(vertical_correctors, e.name),
       pattern="BR3.DVT",
   }

   local knob_names = {}
   for _, name in ipairs(horizontal_correctors) do
       table.insert(knob_names, "k_" .. name)
   end
   for _, name in ipairs(vertical_correctors) do
       table.insert(knob_names, "k_" .. name)
   end

   local x0 = damap {
       nv=6,
       no={1,1,1,1,1,1},
       np=#knob_names,
       po=1,
       pn=knob_names,
   }

   for i, name in ipairs(horizontal_correctors) do
       local knob = knob_names[i]
       psb3[name].kick = psb3[name].kick + x0[knob]
   end

   for i, name in ipairs(vertical_correctors) do
       local knob = knob_names[#horizontal_correctors + i]
       psb3[name].kick = psb3[name].kick + x0[knob]
   end

   local trk = track {
       sequence=psb3,
       X0=x0,
       nturn=1,
       observe=1,
       savemap=true,
   }

   assert(trk.lost == 0, "Tracking failed for initial conditions")

   local n_points = trk:nrow()
   local n_knobs = #knob_names

   local response_x = matrix(n_knobs, n_points)
   local response_y = matrix(n_knobs, n_points)

   local function knob_monomial(index)
       return string.rep("0", 6 + index - 1) .. "1"
   end

   for j = 1, n_points do
       local map = trk.__map[j]
       for i = 1, n_knobs do
           local monomial = knob_monomial(i)
           response_x:set(i, j, map.x:get(monomial))
           response_y:set(i, j, map.y:get(monomial))
       end
   end

   response_x:print("Orbit response: x vs correctors")
   response_y:print("Orbit response: y vs correctors")

What to expect
--------------

* Each row corresponds to one corrector knob, in the order defined above.
* Each column corresponds to a BPM (the observed elements).
* The printed matrices should show reasonable nonzero responses for both planes.

If you want to restrict the correctors or BPMs, change the pattern strings in
:literal:`psb3:foreach` and :literal:`psb3:select`.

See Also
--------

* :doc:`mad_cmd_track`
* :doc:`mad_gen_sequence`
* :doc:`parametric_optics_and_rdts`
