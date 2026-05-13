Introduction
============
.. _ch.gen.intro:

Overview
--------

The Methodical Accelerator Design -- Next Generation application is an all-in-one standalone versatile tool for particle accelerator design, modeling, and optimization, and for beam dynamics and optics studies. Its general purpose scripting language is based on the simple yet powerful Lua programming language (with a few extensions) and embeds the state-of-art Just-In-Time compiler LuaJIT. Its physics is based on symplectic integration of differential maps made out of GTPSA (Generalized Truncated Power Series). The physics of the transport maps and the normal form analysis were both strongly inspired by the PTC/FPP library from E. Forest. MAD-NG development started in 2016 by the author as a side project of MAD-X, hence MAD-X users should quickly become familiar with its ecosystem, e.g. lattices definition.

MAD-NG is free open-source software, distributed under the GNU General Public License v3.\ [#f1]_ The source code, units tests\ [#f5]_, integration tests, and examples are all available on its Github `repository <https://github.com/MethodicalAcceleratorDesign/MAD>`_, including the `documentation <https://github.com/MethodicalAcceleratorDesign/MADdocs>`_ and its LaTeX source. Official binaries are published at `https://madx.web.cern.ch/ <https://madx.web.cern.ch/>`_. For convenience, binaries and a few examples are also made available from the `releases repository <http://cern.ch/mad/releases/madng/>`_ located on the AFS shared file system at CERN.

In typical use, a MAD-NG session looks like:

* load or define a sequence
* attach a beam
* run :doc:`survey <mad_cmd_survey>`, :doc:`track <mad_cmd_track>`, or :doc:`twiss <mad_cmd_twiss>`
* inspect returned :doc:`mtable <mad_gen_mtable>` and flow objects

This page focuses on installation, interactive use, and the shell model. For
the language and object model itself, continue with :doc:`mad_gen_script` and
:doc:`mad_gen_object`.

Installation
------------

Download the binary corresponding to your platform from the MAD-X download site
(`https://madx.web.cern.ch/releases/madng/1.1/ <https://madx.web.cern.ch/releases/madng/1.1/>`_) or the
`releases repository`_. Install it in a local directory. Update (or check) that
the :literal:`PATH` environment variable contains the path to your local
directory or prefix :literal:`mad` with this path to run it. Rename the
application from :literal:`mad-arch-v.m.n` to :literal:`mad` and make it
executable with the command ':literal:`chmod u+x mad`' on Unix systems or add
the :literal:`.exe` extension on Windows.

If you build MAD-NG from source, keep the resulting :literal:`mad` binary
alongside the repository or install it into a directory on your :literal:`PATH`.

Verify your installation by running:

.. code-block:: console

	$ ./mad -h
	usage: ./mad [options]... [script [args]...].
	Available options are:
		- e chunk  	Execute string 'chunk'.
		- l name   	Require library 'name'.
		- b ...    	Save or list bytecode.
		- j cmd    	Perform JIT control command.
		- O[opt]   	Control JIT optimizations.
		- i        	Enter interactive mode after executing 'script'.
		- q        	Do not show version information.
		- M        	Do not load MAD environment.
		- Mt[=num] 	Set initial MAD trace level to 'num'.
		- MT[=num] 	Set initial MAD trace level to 'num' and location.
		- E        	Ignore environment variables.
		--        	 Stop handling options.
		-         	 Execute stdin and stop handling options.

If the command fails, check the following:

* the binary is executable (run :literal:`chmod u+x mad` on Unix)
* the file name is :literal:`mad`
* the directory is on your :literal:`PATH` or you are using :literal:`./mad`

Releases version
""""""""""""""""

MAD-NG releases are tagged on the Github repository and use mangled binary names on the releases repository, i.e. :literal:`mad-arch-v.m.n` where:

:arch: is the platform architecture for binaries among :literal:`linux`, :literal:`macos` and :literal:`windows`.
:v: is the **v**\ ersion number, :const:`0` meaning beta-version under active development.
:m: is the **m**\ ajor release number corresponding to features completeness.
:n: is the mi\ **n**\ or release number corresponding to bug fixes.


Beam Setup and Particle Charge
------------------------------

.. important::
   **Particle Charge Compatibility:** MAD-X lattice files typically define k values assuming positive particle charges. If you select a negatively charged particle (e.g., electrons) in your beam definition, :doc:`track <mad_cmd_track>` and :doc:`twiss <mad_cmd_twiss>` calculations may fail due to incorrect sign conventions.

   To restore MAD-X-compatible behavior for negatively charged particles, set the following option before running calculations:

   .. code-block:: mad

       MAD.option.nocharge = true

   This disables charge-dependent corrections in the physics calculations, ensuring compatibility with MAD-X lattice definitions.

Interactive Mode
----------------

To run MAD-NG in interactive mode, use the `readline wrapper <http://github.com/hanslub42/rlwrap>`_ :literal:`rlwrap` so that command editing and history work properly:

.. code-block:: console

  $ rlwrap ./mad
     ____  __   ______    ______     |   Methodical Accelerator Design
      /  \/  \   /  _  \   /  _  \   |   release: 0.9.0 (OSX 64)
     /  __   /  /  /_/ /  /  /_/ /   |   support: http://cern.ch/mad
    /__/  /_/  /__/ /_/  /_____ /    |   licence: GPL3 (C) CERN 2016+
                                     |   started: 2020-08-01 20:13:51
  > print "hello world!"
  hello world!"

Here the application is assumed to be installed in the current directory '`.`'.

Prompt Levels
"""""""""""""

The character :literal:`>` is the prompt waiting for user input. If you write
an incomplete statement, MAD-NG switches to the continuation prompt
:literal:`>>` until the statement is complete:

.. code-block::

	> print                -- 1st level prompt, incomplete statement
	>> "hello world!"      -- 2nd level prompt, complete the statement
	hello world!           -- execute

Typing the character ':literal:`=`' right after the 1st level prompt is equivalent to call the :literal:`print` function:

.. code-block::

	> = "hello world!"     -- 1st level prompt followed by =
	hello world!           -- execute print "hello world!"
	> = MAD.option.numfmt
	% -.10g

Scope Across Chunks
"""""""""""""""""""

Each line is executed in its own *chunk*\ [#f3]_, so :literal:`local` variables
do not carry over between prompts. Use globals for quick experiments or wrap
multiple lines in a :literal:`do ... end` block to keep locals together:

.. code-block::

	> local a = "hello"
	> print(a)
	nil

	> do                   -- open a chunk
	>> local a = "hello"
	>> print(a .. " world!")
	>> end                 -- close and execute the chunk
	hello world!

Interrupting Execution
""""""""""""""""""""""

To quit the application typewrite :literal:`Crtl+D` to send :literal:`EOF`
(end-of-file) on the input, [#f2]_ or :literal:`Crtl+\\` to send the
:literal:`SIGQUIT` (quit) signal, or :literal:`Crtl+C` to send the stronger
:literal:`SIGINT` (interrupt) signal. If the application is stalled or looping
forever, typewriting :literal:`Crtl+C` twice reliably stops it:

.. code-block::

	> while true do end
	^C
	^C
	stdin:1: interrupted!
	stack traceback:
	        stdin:1: in main chunk
	        [C]: at 0x004725b0

Interactive Workflow Tips
"""""""""""""""""""""""""

* use :literal:`show` to inspect values and object members
* test expressions incrementally and rely on the :literal:`>>` prompt when needed
* use :literal:`local` bindings from :literal:`MAD` (for example, :literal:`local track, twiss in MAD`)

Batch Mode
----------

To run MAD-NG in batch mode, just run it in the shell with files as arguments on the command line:

.. code-block:: console

	$ ./mad [mad options] myscript1.mad myscript2.mad ...


where the scripts contains programs written in the MAD-NG programming language (see :doc:`Scripting <mad_gen_script>`).

Interactive Inspection
----------------------

The function :literal:`show` displays the type and value of variables, and if
they have attributes, the list of their names in the lexicographic order:

.. code-block:: console

	> show "hello world!"
	:string: hello world!
	> show(MAD.option)
	:table: MAD.option
	colwidth           :number: 18
	hdrwidth           :number: 18
	intfmt             :string: % -10d
	madxenv            :boolean: false
	nocharge           :boolean: false
	numfmt             :string: % -.10g
	ptcmodel           :boolean: false
	strfmt             :string: % -25s

Additional Resources
--------------------

For quick syntax references and comparisons with other languages, see the upstream cheat sheets:

* `MAD-NG Language Cheatsheet <https://methodicalacceleratordesign.github.io/MAD-NG/madng-cheatsheet.html>`_ - Compact reference for MAD-NG syntax, operators, data types, and common pitfalls.
* `MAD-NG vs MATLAB/Python/Julia Comparison <https://methodicalacceleratordesign.github.io/MAD-NG/madng-comparison-cheatsheet.html>`_ - Side-by-side syntax comparisons for vectors, matrices, operations, and programming constructs.

.. rubric:: Footnotes

.. [#f1] MAD-NG embeds the libraries `FFTW <http://github.com/FFTW>`_ `NFFT <http://github.com/NFFT>`_ and `NLopt <http://github.com/stevengj/nlopt>`_ released under GNU (L)GPL too.
.. [#f5] MAD-NG has few thousands unit tests that do few millions checks, and it is constantly growing.
.. [#f2] Note that sending :literal:`Crtl+D` twice from MAD-NG invite will quit both MAD-NG and its parent Shell...
.. [#f3] A chunk is the unit of execution in Lua (see `Lua 5.2 <http://github.com/MethodicalAcceleratorDesign/MADdocs/blob/master/lua52-refman-madng.pdf>`_ §3.3.2).
