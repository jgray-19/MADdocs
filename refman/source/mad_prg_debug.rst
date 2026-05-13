.. _ch.prg.debug:

Debugging
=========

This page is intentionally expert-facing. It documents the embedded debugger
exposed as :literal:`MAD.dbg`, based on the current implementation in
:literal:`MAD/src/madl_dbg.lua`.

For ordinary scripts, the usual :literal:`info`, :literal:`debug`, and
:literal:`atdebug` options on commands such as :doc:`mad_cmd_track`,
:doc:`mad_cmd_survey`, :doc:`mad_cmd_cofind`, and :doc:`mad_cmd_twiss` are
often enough. :literal:`MAD.dbg()` is for interactive inspection of Lua/MAD-NG
execution itself.

What `MAD.dbg` Is
-----------------

From the current source:

* :literal:`madl_dbg.lua` returns :literal:`{ dbg = dbg }`, so the debugger is
  exposed in the :literal:`MAD` environment as :literal:`MAD.dbg`
* the debugger object is callable, so :literal:`dbg(...)` is the normal entry
  point
* interactive input is read through :literal:`dbg.read(prompt)` and output is
  written through :literal:`dbg.write(str)`
* the implementation uses Lua's :literal:`debug` library and line/call/return
  hooks to stop at source lines

In scripts, access it as either:

.. code-block:: mad

   local dbg in MAD

or:

.. code-block:: mad

   MAD.dbg(...)

Entering the Debugger
---------------------

The callable form behaves as a conditional breakpoint:

.. code-block:: mad

   local dbg in MAD

   local function probe(x)
     dbg(x > 0)
     return x
   end

If the first argument is true, the call returns immediately. If it is false or
omitted, the debugger arms a hook and stops at the next source line in Lua/MAD
code.

The implementation also accepts optional stack/source arguments internally, but
the current manual only recommends the simple conditional-breakpoint form above
for user code.

Interactive Commands
--------------------

The built-in command list in :literal:`madl_dbg.lua` currently defines:

* :literal:`c` to continue execution
* :literal:`s` to step into the next line
* :literal:`n` to step to the next line while skipping over called functions
* :literal:`f` to continue until the current function returns
* :literal:`u` and :literal:`d` to move up or down the stack
* :literal:`i [index]` to inspect a specific stack frame
* :literal:`w [line count]` to print source lines around the current line
* :literal:`e [statement]` to execute a statement in the current frame
* :literal:`p [expression]` to evaluate and print an expression
* :literal:`t` to print the stack trace
* :literal:`l` to print locals, arguments, and upvalues
* :literal:`h` to print the debugger help
* :literal:`q` to exit immediately through :literal:`dbg.exit(0)`

The implementation also repeats the previous command when you press return on
an empty prompt.

Useful Helpers
--------------

The same source file exposes a few helper entry points that are safer to use in
scripts than manually wiring hooks:

* :literal:`dbg.error(err, level)` prints the error, enters the debugger, then
  raises the Lua error
* :literal:`dbg.assert(condition, message, ...)` behaves like
  :literal:`assert`, but enters the debugger before failing
* :literal:`dbg.call(f, ...)` behaves like :literal:`xpcall` with a debugger
  stop on error
* :literal:`dbg.msgh(...)` is an error-message handler intended for protected
  calls
* :literal:`dbg.pretty(value[, depth])` and :literal:`dbg.pp(value[, depth])`
  format values for inspection

The following knobs are also present in the current implementation:

* :literal:`dbg.pretty_depth` controls the default recursion depth for pretty
  printing
* :literal:`dbg.auto_where` prints surrounding source lines automatically when
  set to a number
* :literal:`dbg.auto_eval` lets unrecognized input fall through to
  :literal:`cmd_eval`
* :literal:`dbg.use_color(boolean)` toggles ANSI coloring

Practical Limits
----------------

The debugger skips frames without source-line information. In practice that
means C frames, bytecode-only frames, and some generated chunks are not good
interactive debugging targets.

Source Availability
-------------------

Some debugger features require access to the MAD-NG Lua source tree. The
distributed binary includes compiled chunks, so operations that need to show
source lines (such as :literal:`w` or stepping with context) depend on the
original files being available.

For full interactive debugging, keep the MAD-NG source checkout nearby (the
scripts live under :literal:`MAD/src`).

The source also exposes :literal:`dbg.dbgfun` and :literal:`dbg.dbghook`, but
this page does not document them further yet because their intended workflow is
not clearly explained in the embedded help.

Example
-------

The example below was working for MAD-NG version :literal:`1.1.13_P`.

It replaces :literal:`dbg.read` temporarily so the debugger can be exercised in
an automated documentation script instead of waiting for a human at the
terminal.

.. literalinclude:: ../../verified_examples/dbg_minimal.mad
   :language: mad
   :caption: verified_examples/dbg_minimal.mad

See also
--------

* :doc:`mad_prg_mad`
* :doc:`mad_prg_modules`
* :doc:`mad_cmd_track`
* :doc:`mad_cmd_twiss`
