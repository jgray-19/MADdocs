Beams
=====
.. _ch.gen.beam:

The :var:`beam` object is the *root object* of beams that store information relative to particles and particle beams. It also provides a simple interface to the particles and nuclei database.

The :var:`beam` module extends the :doc:`typeid <mad_mod_types>` module with the :func:`is_beam` *function*, which returns :const:`true` if its argument is a :var:`beam` object, :const:`false` otherwise.

Synopsis
--------

.. code-block:: mad
   :caption: Beam constructor with default setup.

   local beam in MAD

   b = beam {
     particle = "positron",
     -- identity (readonly; set via particle database or by defining a new particle)
     energy  = 1,
     -- derived views (setting these updates energy)
     -- pc, beta, gamma, betgam, brho, pc2, beta2, betgam2
     -- emittances
     ex      = 1,
     ey      = 1,
     et      = 1e-3,
     -- bunch parameters
     nbunch  = 0,
     npart   = 0,
     sigt    = 1,
     sige    = 1e-3,
   }

Attributes
----------

The :var:`beam` *object* provides the following attributes:

.. list-table::
   :widths: 16 64 20
   :header-rows: 1

   * - Attribute
     - Description
     - Default
   * - :literal:`particle`
     - Particle name.
     - :literal:`"positron"`
   * - :literal:`mass`
     - Particle energy-mass [GeV].
     - :literal:`emass`
   * - :literal:`charge`
     - Particle charge in [q] unit of :literal:`qelect`. [#f1]_
     - :const:`1`
   * - :literal:`spin`
     - Particle spin.
     - :const:`0`
   * - :literal:`emrad`
     - Electromagnetic radius [m],

       :math:`\mathrm{emrad} = \mathrm{krad_GeV}\times\mathrm{charge}^2/\mathrm{mass}` where :math:`\mathrm{krad_GeV} = 10^{-9} (4 \pi\varepsilon_0)^{-1} q`.
     - computed
   * - :literal:`aphot`
     - Average number of photons emitted per bending unit,

       :math:`\mathrm{aphot} = \mathrm{kpht_GeV}\times\mathrm{charge}^2\times\mathrm{betgam}` where :math:`\mathrm{kpht_GeV}` :math:`= \frac{5}{2\sqrt{3}}` :math:`\mathrm{krad_GeV}` :math:`(\hbar c)^{-1}`.
     - computed
   * - :literal:`energy`
     - Particle energy [GeV].
     - :const:`1`
   * - :literal:`pc`
     - Momentum times the speed of light [GeV],

       :math:`\mathrm{pc} = (\mathrm{energy}^2 - \mathrm{mass}^2)^{\frac{1}{2}}`.
     - computed
   * - :literal:`beta`
     - Relativistic :math:`\beta=\frac{v}{c}`,

       :math:`\mathrm{beta} = (1 - (\mathrm{mass}/\mathrm{energy})^2)^{\frac{1}{2}}`.
     - computed
   * - :literal:`gamma`
     - Lorentz factor :math:`\gamma=(1-\beta^2)^{-\frac{1}{2}}`,

       :math:`\mathrm{gamma} = \mathrm{energy}/\mathrm{mass}`.
     - computed
   * - :literal:`betgam`
     - Product :math:`\beta\gamma`,

       :math:`\mathrm{betgam} = (\mathrm{gamma}^2 - 1)^\frac{1}{2}`.
     - computed
   * - :literal:`pc2`
     - :math:`\mathrm{pc}^2`, avoiding the square root.
     - computed
   * - :literal:`beta2`
     - :math:`\mathrm{beta}^2`, avoiding the square root.
     - computed
   * - :literal:`betgam2`
     - :math:`\mathrm{betgam}^2`, avoiding the square root.
     - computed
   * - :literal:`brho`
     - Magnetic rigidity [T.m],

       :literal:`brho = GeV_c * pc/|charge|` where :literal:`GeV_c` = :math:`10^{9}/c`
     - computed
   * - :literal:`ex`
     - Horizontal emittance :math:`\epsilon_x` [m].
     - :const:`1`
   * - :literal:`ey`
     - Vertical emittance :math:`\epsilon_y` [m].
     - :const:`1`
   * - :literal:`et`
     - Longitudinal emittance :math:`\epsilon_t` [m].
     - :const:`1e-3`
   * - :literal:`exn`
     - Normalized horizontal emittance [m], :expr:`exn = ex * betgam`.
     - computed/update
   * - :literal:`eyn`
     - Normalized vertical emittance [m], :expr:`eyn = ey * betgam`.
     - computed/update
   * - :literal:`etn`
     - Normalized longitudinal emittance [m], :expr:`etn = et * betgam`.
     - computed/update
   * - :literal:`nbunch`
     - Number of particle bunches in the machine.
     - :const:`0`
   * - :literal:`npart`
     - Number of particles per bunch.
     - :const:`0`
   * - :literal:`sigt`
     - Bunch length in :math:`c \sigma_t`.
     - :const:`1`
   * - :literal:`sige`
     - Relative energy spread in :math:`\sigma_E/E` [GeV].
     - :const:`1e-3`

The :var:`beam` *object* also implements a special protect-and-update mechanism for its attributes to ensure consistency and precedence between the physical quantities stored internally:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Category
     - Attributes / behavior
   * - Read-only
     - Writing triggers an error: :literal:`mass`, :literal:`charge`, :literal:`spin`, :literal:`emrad`, :literal:`aphot`.
   * - Read-write
     - Stored values (with ranges): :literal:`particle`, :literal:`energy` :math:`>` :var:`mass`; :literal:`ex` :math:`>0`, :literal:`ey` :math:`>0`, :literal:`et` :math:`>0`; :literal:`nbunch` :math:`>0`, :literal:`npart` :math:`>0`, :literal:`sigt` :math:`>0`, :literal:`sige` :math:`>0`.
   * - Read-update (energy)
     - Setting updates :literal:`energy`: :literal:`pc` :math:`>0`, :math:`0.9>` :literal:`beta` :math:`>0`, :literal:`gamma` :math:`>1`, :literal:`betgam` :math:`>0.1`, :literal:`brho` :math:`>0`, plus :literal:`pc2`, :literal:`beta2`, :literal:`betgam2`.
   * - Read-update (emittances)
     - Setting updates :literal:`ex`, :literal:`ey`, :literal:`et`: :literal:`exn` :math:`>0`, :literal:`eyn` :math:`>0`, :literal:`etn` :math:`>0`.


Methods
-------

The :var:`beam` object provides the following methods:

.. list-table::
   :widths: 20 30 50
   :header-rows: 1

   * - Method
     - Signature
     - Description
   * - :literal:`new_particle`
     - :literal:`(particle, mass, charge, [spin])`
     - Create new particles or nuclei in the shared database. Arguments may also be passed as a single table.
   * - :literal:`set_variables`
     - :literal:`(set)`
     - Set attributes from (*key*, *value*) pairs, applying the protect/update mechanism (update order undefined). Shortcut :literal:`setvar`.
   * - :literal:`showdb`
     - :literal:`([file])`
     - Display the particles database to :literal:`file` (default: :literal:`io.stdout`).


Metamethods
-----------

The :var:`beam` object provides the following metamethods:

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Metamethod
     - Signature
     - Description
   * - :literal:`__init`
     - :literal:`()`
     - Process initialization using the protect/update mechanism (update order undefined). Creates a new particle on-the-fly if :literal:`mass` and :literal:`charge` are defined.
   * - :literal:`__newindex`
     - :literal:`(key, val)`
     - Handle assignments by creating attributes or updating the underlying physical quantity consistently.
   * - :literal:`__beam`
     - internal
     - Unique private reference that characterizes beams.


Particles database
------------------

The :var:`beam` *object* manages the particles database, which is shared by all :var:`beam` instances. The default set of supported particles is:

		electron, positron, proton, antiproton, neutron, antineutron, ion, muon,
		antimuon, deuteron, antideuteron, negmuon (=muon), posmuon (=antimuon).

New particles can be added to the database, either explicitly using the :literal:`new_particle` method, or by creating or updating a beam *object* and specifying all the attributes of a particle, i.e. :literal:`particle`'s name, :var:`charge`, :var:`mass`, and (optional) :var:`spin`:

.. code-block:: lua

	local beam in MAD
	local nmass, pmass, mumass in MAD.constant

	-- create a new particle
	beam:new_particle{ particle='mymuon', mass=mumass, charge=-1, spin=1/2 }

	-- create a new beam and a new nucleus
	local pbbeam = beam { particle='pb208', mass=82*pmass+126*nmass, charge=82 }

The particles database can be displayed with the :func:`showdb` method at any time from any beam:

.. code-block:: lua

	beam:showdb()  -- check that both, mymuon and pb208 are in the database.


Particle charges
----------------

The physics of MAD-NG is aware of particle charges. To enable the compatibility with codes like MAD-X that ignores the particle charges, the global option :var:`nocharge` can be used to control the behavior of created beams as shown by the following example:

.. code-block:: lua

	local beam, option in MAD
	local beam1 = beam { particle="electron" } -- beam with negative charge
	print(beam1.charge, option.nocharge)       -- display: -1  false

	option.nocharge = true                     -- disable particle charges
	local beam2 = beam { particle="electron" } -- beam with negative charge
	print(beam2.charge, option.nocharge)       -- display:  1  true

	-- beam1 was created before nocharge activation...
	print(beam1.charge, option.nocharge)       -- display: -1  true

This approach ensures consistency of beams behavior during their entire lifetime. [#f2]_

Examples
--------

The following code snippet creates the LHC lead beams made of bare nuclei :math:`^{208}\mathrm{Pb}^{82+}`

.. code-block:: lua

	local beam in MAD
	local lhcb1, lhcb2 in MADX
	local nmass, pmass, amass in MAD.constant
	local pbmass = 82*pmass+126*nmass

	-- attach a new beam with a new particle to lhcb1 and lhcb2.
	lhc1.beam = beam 'Pb208' { particle='pb208', mass=pbmass, charge=82 }
	lhc2.beam = lhc1.beam -- let sequences share the same beam...

	-- print Pb208 nuclei energy-mass in GeV and unified atomic mass.
	print(lhcb1.beam.mass, lhcb1.beam.mass/amass)


.. rubric:: Footnotes

.. [#f1] The :var:`qelect` value is defined in the :doc:`mad_mod_const` module.
.. [#f2] The option :var:`rbarc` in MAD-X is too volatile and does not ensure such consistency...
