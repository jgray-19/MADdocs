Comparing MAD-NG to MAD-X
=========================

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

