.. _ch.prg.elems:

Elements
========

This page is about the programmer workflow for defining a new element kind:

* declaring a new element class in :literal:`MAD.element` (defaults, flags, and
  basic structure)
* attaching tracking and/or survey behavior so :doc:`mad_cmd_track` and
  :doc:`mad_cmd_survey` can execute it

For the user-facing element catalog and attribute semantics, see
:doc:`mad_gen_elements`.

Where To Add Things In Source
-----------------------------

The implementation is split across three source modules:

* :literal:`MAD/src/madl_element.mad` declares the element taxonomy (classes)
  and shared defaults, and installs default :literal:`track` / :literal:`survey`
  methods that raise errors for unsupported kinds.
* :literal:`MAD/src/madl_etrck.mad` defines per-kind tracking functions and
  then attaches them via :literal:`E.<kind>:set_methods { track = ... }`.
* :literal:`MAD/src/madl_esurv.mad` does the same for survey/geometry via
  :literal:`E.<kind>:set_methods { survey = ... }`.

The key consequence is: adding a new element kind is a two-step change.
Declaring the class alone is not enough; you must also attach behavior.

Step 1: Declare A New Element Kind
----------------------------------

New element kinds are declared by deriving from one of the intermediate classes
in :literal:`madl_element.mad` (for example :literal:`thin_element`,
:literal:`thick_element`, :literal:`drift_element`, :literal:`patch_element`).

The pattern in the source is:

.. code-block:: mad

   local E = MAD.element

   E.myelm = E.thick_element 'myelm' {
     l = 1.0,
     -- add kind-specific defaults here
     k1 = 0,
     -- optional: disable automatic updates for map-carrying elements
     -- update = false,
   }

Notes from the existing taxonomy:

* thick kinds typically define strength-like fields and may enable fringe flags
* thick and drift kinds also support sub-elements via the :literal:`sat` helpers
  installed in :literal:`madl_element.mad`

Step 2: Attach `track` Behavior
-------------------------------

Tracking behavior is attached in :literal:`madl_etrck.mad` by:

1. defining a function :literal:`track_myelm(elm, mflw)`
2. wiring it onto the element class with :literal:`:set_methods { track = ... }`

You can see the wiring table near the end of :literal:`madl_etrck.mad`, for
example:

* :literal:`E.quadrupole :set_methods {track = track_quadrupole}`
* :literal:`E.multipole  :set_methods {track = track_multipole}`
* :literal:`E.genmap     :set_methods {track = track_genmap}`

Your new kind should follow the same pattern:

.. code-block:: mad

   local element in MAD
   local E = element

   local function track_myelm(elm, m)
     -- populate the flow fields your map needs, then delegate to a dynmap
     -- implementation (or use the existing integration helpers).
     -- See existing implementations in madl_etrck.mad for templates.
   end

   E.myelm:set_methods { track = track_myelm }

Step 3 (Optional): Attach `survey` Behavior
-------------------------------------------

Survey/geometry behavior is wired similarly in :literal:`madl_esurv.mad` with:

.. code-block:: mad

   local element in MAD
   local E = element

   local function survey_myelm(elm, m)
     -- delegate to geomap primitives or treat as thin/thick as appropriate
   end

   E.myelm:set_methods { survey = survey_myelm }

If you do not attach :literal:`survey`, the :doc:`mad_cmd_survey` command will
fail on your element kind (because :literal:`madl_element.mad` installs an
invalid default).

Common Gotchas
--------------

* **Declared but not wired**: declaring :literal:`E.myelm = ...` without adding
  :literal:`track` / :literal:`survey` wiring will fail at runtime when a
  command hits the element.
* **Length semantics**: choose the base class (thin vs thick vs drift) to match
  your physics. The tracking loaders treat them differently.
* **Sub-elements**: if your kind supports sub-elements, it must be compatible
  with the :literal:`sat` mechanism used by sequences and by the tracking
  helpers in :literal:`madl_etrck.mad`.

See Also
--------

* :doc:`mad_gen_elements`
* :doc:`mad_cmd_track`
* :doc:`mad_cmd_survey`
