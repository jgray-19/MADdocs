Comparing MAD-NG to MAD-X
=========================

Creating the equivalent of MAD-X macros is also very different in MAD-NG. In MAD-X, macros can be defined in a different file and then called in the main file. The closest equivalent in MAD-NG is to create a function in a seperate file. There are two ways of then calling this function from the main file. The first is to use the ``require`` function, which the following example shows.

A function is defined in a file called ``myfunc.mad`` like so.

.. code-block:: mad
    
    local myfunc = function()
        print("Hello World!")
    end

    return { myfunc=myfunc }

Then in the main file, we can call the function.

.. code-block:: mad
    
    local myfunc in require "myfunc"
    myfunc() --prints "Hello World!"

This scenario requires the ``myfunc.mad`` file to be in the same directory as the main file. 

The second way is to use the ``loadfile`` function. This is useful if you want to call the function without having to assign it to a variable. The following example shows how to do this.

A function is defined in a file called ``myfunc.mad`` like so.

.. code-block:: mad
    
    local myfunc = function()
        print("Hello World!")
    end

    return myfunc

Then in the main file, we can call the function.

.. code-block:: mad
    
    assert(loadfile("myfunc.mad"))()() --prints "Hello World!"

    --Or alternatively:
    local myfunc = assert(loadfile("myfunc.mad"))()
    myfunc() --prints "Hello World!"

The ``assert`` function is used to check if the file was loaded correctly, ff it was not, then the program will exit with an error message. The ``loadfile`` function returns a function, so the ``()`` at the end of the ``loadfile`` function call is to run the file. The ``()`` at the end of the ``myfunc()`` call then simply calls the function ``myfunc``.

In general, the ``require`` function is preferred as it is more explicit and easier to read. 

Loading sequence files, originating from MAD-X, on the other hand cannot use this method. This is because, we need to parse the sequence file and then create the sequence object. This is done using the special ``MADX`` object. The following example shows how to load a sequence file called ``fodo.seq``.

.. code-block:: mad
    
    local MADX in MAD
    MADX:load("fodo.seq") --Loads the sequence file fodo.seq
    local seq in MADX     --Grabs the sequence name seq from the MAD-X environment

In MAD-NG, scoping is very important, like python, but very different from the global scope of MAD-X. Furthermore, using the global scope is not recommended as this slows down the code. Therefore, a lot of functions and objects have been placed into modules and need to be "imported" before they can be used. The following example shows how to import the ``math`` module and use the ``sin`` function.

.. code-block:: mad
    
    local sin in math
    print(sin(0.5))
    
    --Eqivalent to:
    print(math.sin(0.5))

The use of scoping also leads to situations which are not necessary in MAD-X. For example, a sequence requires a beam object to be attached to it or placed in the function call. This is because in MAD-X, it has access to the global scope and therefore can use the global beam object.

.. code-block:: mad
    
    local beam, sequence, twiss in MAD
    MADX:load("fodo.seq")               ! Load a sequence from a MAD-X .seq file
    local seq in MADX                   ! Grab the sequence name seq from the MAD-X environment
    seq.beam = beam                     ! Attach a default beam object to the sequence
    local mtbl = twiss { sequence=seq } ! Run twiss on the sequence

    --Equivalent to:
    local beam, sequence, twiss in MAD
    MADX:load("fodo.seq")                               ! Load a sequence from a MAD-X .seq file
    local mtbl = twiss { sequence=MADX.seq, beam=beam } ! Run twiss on the sequence

MAD-NG also has inheritance of elements, however the syntax is slightly different from MAD-X. In MAD-X, we would do ``name: element, attrs``. In MAD-NG, we do ``local name = element "name" { attrs }``. The following example shows how to create a new element called ``myquad`` which is a quadrupole with a length of 1.0 and a strength of 1.0. A more detailed introduction into objects and inheritance can be found in the :doc:`objects` section.

.. code-block:: mad
    
    local quadrupole in MAD.element
    local myquad = quadrupole "myquad" { l=1.0, k1=1.0 }

Another common command that is used in MAD-X is the ``SAVEBETA`` command. This command is used to save a ``BETA0`` block at a location in the sequence. This function can be *almost* replicated in MAD-NG, however, MAD-NG is far more flexible with how and what you can grab mid-twiss. The attribute that is most useful here is ``atsave``, but you could also use ``atentry``, ``atslice`` or ``atexit`` (although these will also be called during the cofind). The following example shows how to grab the MAD-NG ``beta0`` block at the exit of the 3rd element.

.. code-block:: mad

    local beam, sequence, twiss, beta0 in MAD
    local map2bet                      in MAD.gphys
    MADX:load("fodo.seq")                           ! Load a sequence from a MAD-X .seq file
    local seq in MADX                               ! Grab the sequence name seq from the MAD-X environment
    seq.beam = beam                                 ! Attach a default beam object to the sequence
    local saved_beta                                ! Create a local variable to store the beta0 block
    local function save_beta(elm, mflw)             ! Define a function to save the beta0 block
        if mflw.eidx == 3 then                      ! Only save the beta0 block if the element index is 3
            saved_beta = map2bet(mflw[1])           ! Convert the damap to a beta0 block and save it
        end
    end
    local mtbl = twiss { sequence=seq, atsave=save_beta }
