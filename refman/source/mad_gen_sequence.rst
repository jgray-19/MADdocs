#########
Sequences
#########

.. toctree::
   :numbered:

The MAD Sequences are objects convenient to describe accelerators lattices built from a *list* of elements with increasing :data:`s`-positions. The sequences are also containers that provide fast access to their elements by referring to their indexes, :data:`s`-positions, or (mangled) names, or by running iterators constrained with ranges and predicates.

The :var:`sequence` object is the *root object* of sequences that store information relative to lattices.

The :var:`sequence` module extends the :doc:`typeid <mad_mod_types>` module with the :func:`is_sequence` function, which returns :const:`true` if its argument is a :var:`sequence` object, :const:`false` otherwise.

Synopsis
========

.. code-block:: mad
   :caption: Sequence constructor.

   local sequence in MAD.element

   seq = sequence 'name' {
     -- attributes (commonly used)
     dir     = 1,
     refer   = "centre",
     minlen  = 1e-6,
     l       = nil,         -- nil => computed from installed elements
     beam    = nil,
     aperture= nil,

     -- element list (examples)
     -- drift 'd1' { l=1 },
     -- quadrupole 'qf' { l=1, k1=0.3 },
     -- marker 'mk' {},
   }

Attributes
==========

The :var:`sequence` object provides the following attributes:

.. list-table::
   :widths: 16 64 20
   :header-rows: 1

   * - Attribute
     - Description
     - Default
   * - :literal:`l`
     - Length of the sequence [m]. :const:`nil` is replaced by the computed lattice length. Values :math:`\\geq` computed length place the :literal:`$end` marker; other values raise an error.
     - :const:`nil`
   * - :literal:`dir`
     - Sequence direction: :const:`1` forward or :const:`-1` backward. [#f1]_
     - :const:`1`
   * - :literal:`refer`
     - Default element reference position: :literal:`"entry"`, :literal:`"centre"`, or :literal:`"exit"`. Elements can override via :literal:`refpos`. See `element positions`_.
     - :literal:`"centre"`

.. **owner**
..     A *logical* specifying if an *empty* sequence is a view with no data (:expr:`owner~=true`), or a sequence holding data (:expr:`owner==true`). (default: :const:`nil`)

   * - :literal:`minlen`
     - Minimal length [m] when checking negative drifts or generating *implicit* drifts in :math:`s`-iterators (:literal:`:siter`). Automatically set to :math:`10^{-6}` m for sequences created within :literal:`MADX`.
     - :math:`10^{-6}`
   * - :literal:`aperture`
     - Default aperture used when missing at element level (for example in implicit drifts). See :doc:`track <mad_cmd_track>` for aperture semantics.
     - :expr:`{kind='circle', 1}`
   * - :literal:`beam`
     - Attached :doc:`beam <mad_gen_beam>`.
     - :const:`nil`
   * - :literal:`__dat`
     - Private data table (read-only; do not use).
     - internal
   * - :literal:`__cycle`
     - Reference to the marker registered by :literal:`:cycle` (read-only; do not use).
     - :const:`nil`

.. important::
   The private attributes :literal:`__dat` and :literal:`__cycle` are present in all
   sequences and should never be set or modified; doing so leads to undefined behavior.


Methods
=======

The :var:`sequence` object provides the following methods:

.. list-table::
   :widths: 16 22 62
   :header-rows: 1

   * - Method
     - Signature
     - Description
   * - :literal:`elem`
     - :literal:`(idx)`
     - Return element at positive index :literal:`idx`, or :const:`nil`.
   * - :literal:`spos`
     - :literal:`(idx)`
     - Return :math:`s`-position at element entry for index :literal:`idx`, or :const:`nil`.
   * - :literal:`upos`
     - :literal:`(idx)`
     - Return :math:`s`-position at the user reference offset (:literal:`refpos`) for index :literal:`idx`, or :const:`nil`.
   * - :literal:`ds`
     - :literal:`(idx)`
     - Return element length at index :literal:`idx`, or :const:`nil`.
   * - :literal:`align`
     - :literal:`(idx)`
     - Return a set describing element misalignment at index :literal:`idx`, or :const:`nil`.
   * - :literal:`index`
     - :literal:`(idx)`
     - Normalize an index. Negative indexes are reflected versus the sequence size (for example :const:`-1` becomes :literal:`#self`).
   * - :literal:`name_of`
     - :literal:`(idx, [ref])`
     - Return the (mangled) element name at index :literal:`idx`. Duplicate names are mangled by absolute or reference-relative counts (for example :literal:`mq[3]`, :literal:`mq{-2}`).
   * - :literal:`index_of`
     - :literal:`(a, [ref], [dir])`
     - Resolve :literal:`a` to an element index. :literal:`a` may be an :math:`s`-position, a (mangled) name, or an element reference. :literal:`dir` may be :const:`1`, :const:`-1`, or :const:`0` (may return half-integers for implicit drifts).
   * - :literal:`range_of`
     - :literal:`([rng], [ref], [dir])`
     - Return (*start*, *end*, *dir*) for a range (or :const:`nil` for empty). Accepts numeric, name, ``"A/B"`` and list forms; supports :literal:`ref='idx'` to treat numbers as indexes.
   * - :literal:`length_of`
     - :literal:`([rng], [ntrn], [dir])`
     - Return the range length (optionally plus :literal:`ntrn` turns), based on :literal:`:range_of`.
   * - :literal:`iter`
     - :literal:`([rng], [ntrn], [dir])`
     - Iterator over elements in a range (and turns), yielding index, element, running :math:`s`, and signed length.
   * - :literal:`siter`
     - :literal:`([rng], [ntrn], [dir])`
     - :math:`s`-iterator yielding implicit drifts as needed (half-integer indexes).
   * - :literal:`foreach`
     - :literal:`(act, [rng], [sel], [not])`
     - Apply :literal:`act(elm, idx, [midx])` to selected elements over a range iterator. Selection rules are described in `element selections`_. [#f2]_
   * - :literal:`select`
     - :literal:`([flg], [rng], [sel], [not])`
     - Select elements using :literal:`:foreach` and set flag :literal:`flg` (default selection marks only :literal:`$end` as observed).
   * - :literal:`deselect`
     - :literal:`([flg], [rng], [sel], [not])`
     - Deselect elements using :literal:`:foreach` and clear flag :literal:`flg`.
   * - :literal:`filter`
     - :literal:`([rng], [sel], [not])`
     - Return a list of selected element indexes (may include non-integers for sub-elements encoded as :literal:`midx.sat`) and its size.
   * - :literal:`install`
     - :literal:`(elm, [rng], [sel], [cmp])`
     - Install elements at their `element positions`_. Supports :literal:`from=\"selected\"` for multiple installations relative to selected elements.
   * - :literal:`replace`
     - :literal:`(elm, [rng], [sel])`
     - Replace selected elements (and optionally sub-elements) with items from list :literal:`elm`, returning replaced elements and indexes.
   * - :literal:`remove`
     - :literal:`([rng], [sel])`
     - Remove selected elements, returning removed elements and their indexes.
   * - :literal:`move`
     - :literal:`([rng], [sel])`
     - Update `element positions`_ for selected elements without reordering them. [#f3]_
   * - :literal:`update`
     - :literal:`()`
     - Recompute positions of all elements.
   * - :literal:`misalign`
     - :literal:`(algn, [rng], [sel])`
     - Set element misalignments on filtered elements using a mappable, iterable, or callable :literal:`(idx)`.
   * - :literal:`reflect`
     - :literal:`([name])`
     - Return a new sequence that is the reversed sequence (default name :literal:`self.name..'_rev'`).
   * - :literal:`cycle`
     - :literal:`(a)`
     - Register marker :literal:`a` as the cycle reference, stored in :literal:`__cycle` and cleared by editing operations.
   * - :literal:`share`
     - :literal:`(seq2)`
     - Share elements between sequences by name when unique in both sequences.
   * - :literal:`unique`
     - :literal:`([fmt])`
     - Replace non-unique elements with unique instances, using optional name-formatting callable or format string.
   * - :literal:`publish`
     - :literal:`(env, [keep])`
     - Publish elements into environment :literal:`env` (preserving existing elements if :literal:`keep=true`).
   * - :literal:`copy`
     - :literal:`([name])`
     - Copy sequence (views remain views) and optionally set name.
   * - :literal:`set_readonly`
     - :literal:`()`
     - Set the sequence as read-only, including its columns.
   * - :literal:`save_flags`
     - :literal:`([flgs])`
     - Save all element flags into :literal:`flgs` (default :literal:`{}`) and return it.
   * - :literal:`restore_flags`
     - :literal:`(flgs)`
     - Restore all element flags from :literal:`flgs`.
   * - :literal:`dumpseq`
     - :literal:`([fil], [info])`
     - Dump element position/length information to :literal:`fil` (default :literal:`io.stdout`); :literal:`info` enables extra details.
   * - :literal:`check_sequ`
     - :literal:`()`
     - Integrity check of the sequence and dictionary (debug only).


Metamethods
===========

The :var:`sequence` object provides the following metamethods:

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Metamethod
     - Signature
     - Description
   * - :literal:`__len`
     - :literal:`()`
     - Length operator :literal:`#`: number of stored elements including :literal:`"$start"` and :literal:`"$end"`.
   * - :literal:`__index`
     - :literal:`(key)`
     - Indexing operator :literal:`[key]`: if *key* is a number, treat as element index; otherwise treat as object attribute; if attribute value is :const:`nil`, treat *key* as element name and return the element or an iterable. [#f4]_
   * - :literal:`__newindex`
     - :literal:`(key, val)`
     - Assignment operator :literal:`[key]=val`: creates new attributes. Writing to numeric indexes or existing element names raises :literal:`"invalid sequence write access (use replace method)"`.
   * - :literal:`__init`
     - :literal:`()`
     - Constructor hook: compute element positions. [#f5]_
   * - :literal:`__copy`
     - :literal:`()`
     - Copy hook similar to :meth:`:copy`.
   * - :literal:`__sequ`
     - internal
     - Unique private reference that characterizes sequences.

Sequences creation
==================

During its creation as an *object*, a sequence can defined its attributes as any object, and the *list* of its elements that must form a
*sequence* of increasing :math:`s`-positions. When subsequences are part of this *list*, they are replaced by their respective elements as a
sequence *element* cannot be present inside other sequences. If the length of the sequence is not provided, it will be computed and set automatically.
During their creation, sequences compute the :math:`s`-positions of their elements as described in the section `element positions`_, and check for overlapping
elements that would raise a "negative drift" runtime error.

The following example shows how to create a sequence form a *list* of elements and subsequences:

::

   local sequence, drift, marker in MAD.element
   local df, mk = drift 'df' {l=1}, marker 'mk' {}
   local seq = sequence 'seq' {
   df 'df1' {}, mk 'mk1' {},
   sequence {
      sequence { mk 'mk0' {} },
      df 'df.s' {}, mk 'mk.s' {}
   },
   df 'df2' {}, mk 'mk2' {},
   } :dumpseq()

Displays:

.. code-block:: text

   sequence: seq, l=3
   idx  kind     name         l          dl       spos       upos    uds
   001  marker   start        0.000       0       0.000      0.000   0.000
   002  drift    df1          1.000       0       0.000      0.500   0.500
   003  marker   mk1          0.000       0       1.000      1.000   0.000
   004  marker   mk0          0.000       0       1.000      1.000   0.000
   005  drift    df.s         1.000       0       1.000      1.500   0.500
   006  marker   mk.s         0.000       0       2.000      2.000   0.000
   007  drift    df2          1.000       0       2.000      2.500   0.500
   008  marker   mk2          0.000       0       3.000      3.000   0.000
   009  marker   end          0.000       0       3.000      3.000   0.000

.. _elpos:

Element positions
=================

A sequence looks at the following attributes of an element, including sub-sequences, when installing it, *and only at that time*, to determine its position:

.. list-table::
   :widths: 16 64 20
   :header-rows: 1

   * - Attribute
     - Description
     - Default
   * - :literal:`at`
     - Position [m] of the element relative to the reference specified by :literal:`from`.
     - required
   * - :literal:`from`
     - Reference used for :literal:`at`: one of :literal:`"start"`, :literal:`"prev"`, :literal:`"next"`, :literal:`"end"`, :literal:`"selected"`, an element name, or a number [m] from sequence start.
     - depends on :literal:`at`
   * - :literal:`refpos`
     - Element reference point: one of :literal:`"entry"`, :literal:`"centre"`, :literal:`"exit"`, a sub-element name, or a position [m] from the element start; converted to an offset subtracted from :literal:`at` to compute element entry :math:`s`.
     - :literal:`self.refer`
   * - :literal:`shared`
     - Whether the element is used at multiple positions in the same sequence definition (implemented via temporary instances at install time).
     - :const:`false`

**Warning:** The :literal:`at` and :literal:`from` attributes are not considered as intrinsic properties of the elements and are used only once during installation.
Any reuse of these attributes is the responsibility of the user, including the consistency between :literal:`at` and :literal:`from` after updates.


Element selections
==================

The element selection in sequence use predicates in combination with iterators. The sequence iterator manages the range of elements where to apply the selection,
while the predicate says if an element in this range is illegible for the selection. In order to ease the use of methods based on the :literal:`:foreach` method,
the selector predicate :literal:`sel` can be built from different types of information provided in a *set* with the following attributes:


**flag**
   A *number* interpreted as a flags mask to pass to the element method :literal:`:is_selected`. It should not be confused with the flags passed as argument to methods
   :literal:`:select` and :literal:`:deselect`, as both flags can be used together but with different meanings!

**pattern**
   A *string* interpreted as a pattern to match the element name using :literal:`string.match` from the standard library, see
   `Lua 5.2 <http://github.com/MethodicalAcceleratorDesign/MADdocs/blob/master/lua52-refman-madng.pdf>`_ §6.4 for details.

**class**
   An *element* interpreted as a *class* to pass to the element method :literal:`:is_instansceOf`.

**list**
   An *iterable* interpreted as a *list* used to build a *set* and select the elements by their name, i.e. the built predicate will use :literal:`tbl[elm.name]`
   as a *logical*. If the *iterable* is a single item, e.g. a *string*, it will be converted first to a *list*.

**table**
   A *mappable* interpreted as a *set* used to select the elements by their name, i.e. the built predicate will use :literal:`tbl[elm.name]` as a *logical*.
   If the *mappable* contains a *list* or is a single item, it will be converted first to a *list* and its *set* part will be discarded.

**select**
   A *callable* interpreted as the selector itself, which allows to build any kind of predicate or to complete the restrictions already built above.

**subelem**
   A *boolean* indicating to include or not the sub-elements in the scanning loop. The predicate and the action receive the sub-element and its sub-index as
   first and second argument, and the main element index as third argument.

All these attributes are used in the aforementioned order to incrementally build predicates that are combined with logical conjunctions, i.e. :literal:`and`'ed,
to give the final predicate used by the :literal:`:foreach` method. If only one of these attributes is needed, it is possible to pass it directly in :literal:`sel`,
not as an attribute in a *set*, and its type will be used to determine the kind of predicate to build. For example, :literal:`self:foreach(act, monitor)` is equivalent
to :literal:`self:foreach\{action=act, class=monitor}`.

Indexes, names and counts
=========================

Indexing a sequence triggers a complex look up mechanism where the arguments will be interpreted in various ways as described in the :literal:`:__index` metamethod.
A *number* will be interpreted as a relative slot index in the list of elements, and a negative index will be considered as relative to the end of the sequence,
i.e. :const:`-1` is the :literal:`$end` marker. Non-\ *number* will be interpreted first as an object key (can be anything), looking for sequence methods or attributes;
then as an element name if nothing was found.

If an element exists but its name is not unique in the sequence, an *iterable* is returned. An *iterable* supports the length :literal:`#` operator to retrieve the
number of elements with the same name, the indexing operator :literal:`[]` waiting for a count :math:`n` to retrieve the :math:`n`-th element from the start with that name,
and the iterator :literal:`ipairs` to use with generic :literal:`for` loops.

The returned *iterable* is in practice a proxy, i.e. a fake intermediate object that emulates the expected behavior, and any attempt to access the proxy in
another manner should raise a runtime error.

**Warning:** The indexing operator :literal:`[]` interprets a *number* as a (relative) element index as the method :literal:`:index`, while the method :literal:`:index_of` interprets a
*number* as a (relative) element :math:`s`-position [m].

The following example shows how to access to the elements through indexing and the *iterable*:::

   local sequence, drift, marker in MAD.element
   local seq = sequence {
   drift 'df' { id=1 }, marker 'mk' { id=2 },
   drift 'df' { id=3 }, marker 'mk' { id=4 },
   drift 'df' { id=5 }, marker 'mk' { id=6 },
   }
   print(seq[ 1].name) -- display: $start (start marker)
   print(seq[-1].name) -- display: $end   (end   marker)

   print(#seq.df, seq.df[3].id)                        -- display: 3   5
   for _,e in ipairs(seq.df) do io.write(e.id," ") end -- display: 1 3 5
   for _,e in ipairs(seq.mk) do io.write(e.id," ") end -- display: 2 4 6

   -- print name of drift with id=3 in absolute and relative to id=6.
   print(seq:name_of(4))       -- display: df[2]  (2nd df from start)
   print(seq:name_of(2, -2))   -- display: df{-3} (3rd df before last mk)


The last two lines of code display the name of the same element but mangled with absolute and relative counts.

Iterators and ranges
====================

Ranging a sequence triggers a complex look up mechanism where the arguments will be interpreted in various ways as described in the :literal:`:range_of` method,
itself based on the methods :literal:`:index_of` and :literal:`:index`. The number of elements selected by a sequence range can be computed by the :literal:`:length_of` method,
which accepts an extra *number* of turns to consider in the calculation.

The sequence iterators are created by the methods :literal:`:iter` and :literal:`:siter`, and both are based on the :literal:`:range_of` method as mentioned in their descriptions
and includes an extra *number* of turns as for the method :literal:`:length_of`, and a direction :const:`1` (forward) or :const:`-1` (backward) for the iteration.
The :literal:`:siter` differs from the :literal:`:iter` by its loop, which returns not only the sequence elements but also *implicit* drifts built on-the-fly when a gap
:math:`>10^{-10}` m is detected between two sequence elements. Such implicit drift have half-integer indexes and make the iterator "continuous" in :math:`s`-positions.

The method :literal:`:foreach` uses the iterator returned by :literal:`:iter` with a range as its sole argument to loop over the elements where to apply the predicate before
executing the action. The methods :literal:`:select`, :literal:`:deselect`, :literal:`:filter`, :literal:`:install`, :literal:`:replace`, :literal:`:remove`, :literal:`:move`, and :literal:`:misalign` are all based
directly or indirectly on the :literal:`:foreach` method. Hence, to iterate backward over a sequence range, these methods have to use either its *list* form or a numerical range.
For example the invocation :literal:`seq:foreach(\\e -> print(e.name), {2, 2, 'idx', -1)` will iterate backward over the entire sequence :literal:`seq` excluding the :literal:`$start`
and :literal:`$end` markers, while the invocation :literal:`seq:foreach(\\e -> print(e.name), 5..2..-1)` will iterate backward over the elements with :math:`s`-positions sitting in the
interval :math:`[2,5]` m.

The tracking commands :literal:`survey` and :var:`track` use the iterator returned by :literal:`:siter` for their main loop, with their :literal:`range`, :literal:`nturn` and :literal:`dir` attributes as arguments. These commands also save the iterator states in their :literal:`mflw` to allow the users to run them :literal:`nstep` by :literal:`nstep`, see commands :doc:`survey <mad_cmd_survey>` and :doc:`track <mad_cmd_track>` for details.

The following example shows how to access to the elements with the :literal:`:foreach` method:::

   local sequence, drift, marker in MAD.element
   local observed in MAD.element.flags
   local seq = sequence {
   drift 'df' { id=1 }, marker 'mk' { id=2 },
   drift 'df' { id=3 }, marker 'mk' { id=4 },
   drift 'df' { id=5 }, marker 'mk' { id=6 },
   }

   local act = \e -> print(e.name,e.id)
   seq:foreach(act, "df[2]/mk[3]")
   -- display:
   --          df   3
   --          mk   4
   --          df   5
   --          mk   6

   seq:foreach{action=act, range="df[2]/mk[3]", class=marker}
   -- display: markers at ids 4 and 6
   seq:foreach{action=act, pattern="^[^$]"}
   -- display: all elements except $start and $end markers
   seq:foreach{action=\e -> e:select(observed), pattern="mk"}
   -- same as: seq:select(observed, {pattern="mk"})

   local act = \e -> print(e.name, e.id, e:is_observed())
   seq:foreach{action=act, range="#s/#e"}
   -- display:
   --          $start   nil  false
   --          df       1    false
   --          mk       2    true
   --          df       3    false
   --          mk       4    true
   --          df       5    false
   --          mk       6    true
   --          $end     nil  true

Examples
========

FODO cell
---------

The following example shows how to build a very simple FODO cell and an arc made of 10 FODO cells.

.. code-block::

   local sequence, sbend, quadrupole, sextupole, hkicker, vkicker, marker in MAD.element
   local mkf = marker 'mkf' {}
   local ang=2*math.pi/80
   local fodo = sequence 'fodo' { refer='entry',
   mkf             { at=0, shared=true      }, -- mark the start of the fodo
   quadrupole 'qf' { at=0, l=1  , k1=0.3    },
   sextupole  'sf' {       l=0.3, k2=0      },
   hkicker    'hk' {       l=0.2, kick=0    },
   sbend      'mb' { at=2, l=2  , angle=ang },

   quadrupole 'qd' { at=5, l=1  , k1=-0.3   },
   sextupole  'sd' {       l=0.3, k2=0      },
   vkicker    'vk' {       l=0.2, kick=0    },
   sbend      'mb' { at=7, l=2  , angle=ang },
   }
   local arc = sequence 'arc' { refer='entry', 10*fodo }
   fodo:dumpseq() ; print(fodo.mkf, mkf)


Display:

.. code-block:: text

   sequence: fodo, l=9
   idx  kind          name          l          dl       spos       upos    uds
   001  marker        $start  0.000       0       0.000      0.000   0.000
   002  marker        mkf     0.000       0       0.000      0.000   0.000
   003  quadrupole    qf      1.000       0       0.000      0.000   0.000
   004  sextupole     sf      0.300       0       1.000      1.000   0.000
   005  hkicker       hk      0.200       0       1.300      1.300   0.000
   006  sbend         mb      2.000       0       2.000      2.000   0.000
   007  quadrupole    qd      1.000       0       5.000      5.000   0.000
   008  sextupole     sd      0.300       0       6.000      6.000   0.000
   009  vkicker       vk      0.200       0       6.300      6.300   0.000
   010  sbend         mb      2.000       0       7.000      7.000   0.000
   011  marker        $end    0.000       0       9.000      9.000   0.000
   marker : 'mkf' 0x01015310e8	marker: 'mkf' 0x01015310e8 -- same marker


SPS compact description
-----------------------

The following dummy example shows a compact definition of the SPS mixing elements, beam lines and sequence definitions.
The elements are zero-length, so the lattice is too. ::

   local drift, sbend, quadrupole, bline, sequence in MAD.element

   -- elements (empty!)
   local ds = drift      'ds' {}
   local dl = drift      'dl' {}
   local dm = drift      'dm' {}
   local b1 = sbend      'b1' {}
   local b2 = sbend      'b2' {}
   local qf = quadrupole 'qf' {}
   local qd = quadrupole 'qd' {}

   -- subsequences
   local pf  = bline 'pf'  {qf,2*b1,2*b2,ds}           -- #: 6
   local pd  = bline 'pd'  {qd,2*b2,2*b1,ds}           -- #: 6
   local p24 = bline 'p24' {qf,dm,2*b2,ds,pd}          -- #: 11 (5+6)
   local p42 = bline 'p42' {pf,qd,2*b2,dm,ds}          -- #: 11 (6+5)
   local p00 = bline 'p00' {qf,dl,qd,dl}               -- #: 4
   local p44 = bline 'p44' {pf,pd}                     -- #: 12 (6+6)
   local insert = bline 'insert' {p24,2*p00,p42}       -- #: 30 (11+2*4+11)
   local super  = bline 'super'  {7*p44,insert,7*p44}  -- #: 198 (7*12+30+7*12)

   -- final sequence
   local SPS = sequence 'SPS' {6*super}                -- # = 1188 (6*198)

   -- check number of elements and length
   print(#SPS, SPS.l)  -- display: 1190  0 (no element length provided)


Installing elements I
---------------------

The following example shows how to install elements and subsequences in an empty initial sequence::

   local sequence, drift in MAD.element
   local seq   = sequence "seq" { l=16, refer="entry", owner=true }
   local sseq1 = sequence "sseq1" {
   at=5, l=6 , refpos="centre", refer="entry",
   drift "df1'" {l=1, at=-4, from="end"},
   drift "df2'" {l=1, at=-2, from="end"},
   drift "df3'" {     at= 5            },
   }
   local sseq2 = sequence "sseq2" {
   at=14, l=6, refpos="exit", refer="entry",
   drift "df1''" { l=1, at=-4, from="end"},
   drift "df2''" { l=1, at=-2, from="end"},
   drift "df3''" {      at= 5            },
   }
   seq:install {
   drift "df1" {l=1, at=1},
   sseq1, sseq2,
   drift "df2" {l=1, at=15},
   } :dumpseq()

Display:

.. code-block:: text

   sequence: seq, l=16
   idx  kind          name       l          dl       spos       upos    uds
   001  marker        $start*    0.000       0       0.000      0.000   0.000
   002  drift         df1        1.000       0       1.000      1.000   0.000
   003  drift         df1'       1.000       0       4.000      4.000   0.000
   004  drift         df2'       1.000       0       6.000      6.000   0.000
   005  drift         df3'       0.000       0       7.000      7.000   0.000
   006  drift         df1''      1.000       0      10.000     10.000   0.000
   007  drift         df2''      1.000       0      12.000     12.000   0.000
   008  drift         df3''      0.000       0      13.000     13.000   0.000
   009  drift         df2        1.000       0      15.000     15.000   0.000
   010  marker        $end       0.000       0      16.000     16.000   0.000

Installing elements II
----------------------

The following more complex example shows how to install elements and subsequences in a sequence using a selection and the packed form for arguments::

   local mk   = marker   "mk"  { }
   local seq  = sequence "seq" { l = 10, refer="entry",
   mk "mk1" { at = 2 },
   mk "mk2" { at = 4 },
   mk "mk3" { at = 8 },
   }
   local sseq = sequence "sseq" { l = 3 , at = 5, refer="entry",
   drift "df1'" { l = 1, at = 0 },
   drift "df2'" { l = 1, at = 1 },
   drift "df3'" { l = 1, at = 2 },
   }
   seq:install {
   class    = mk,
   elements = {
      drift "df1" { l = 0.1, at = 0.1, from="selected" },
      drift "df2" { l = 0.1, at = 0.2, from="selected" },
      drift "df3" { l = 0.1, at = 0.3, from="selected" },
      sseq,
      drift "df4" { l = 1, at = 9 },
   }
   }

   seq:dumpseq()

Display:

.. code-block:: text

   sequence: seq, l=10
   idx  kind          name      l          dl       spos       upos    uds
   001  marker        $start    0.000       0       0.000      0.000   0.000
   002  marker        mk1       0.000       0       2.000      2.000   0.000
   003  drift         df1       0.100       0       2.100      2.100   0.000
   004  drift         df2       0.100       0       2.200      2.200   0.000
   005  drift         df3       0.100       0       2.300      2.300   0.000
   006  marker        mk2       0.000       0       4.000      4.000   0.000
   007  drift         df1       0.100       0       4.100      4.100   0.000
   008  drift         df2       0.100       0       4.200      4.200   0.000
   009  drift         df3       0.100       0       4.300      4.300   0.000
   010  drift         df1'      1.000       0       5.000      5.000   0.000
   011  drift         df2'      1.000       0       6.000      6.000   0.000
   012  drift         df3'      1.000       0       7.000      7.000   0.000
   013  marker        mk3       0.000       0       8.000      8.000   0.000
   014  drift         df1       0.100       0       8.100      8.100   0.000
   015  drift         df2       0.100       0       8.200      8.200   0.000
   016  drift         df3       0.100       0       8.300      8.300   0.000
   017  drift         df4       1.000       0       9.000      9.000   0.000
   018  marker        $end      0.000       0      10.000     10.000   0.000


.. rubric:: Footnotes

.. [#f1] This is equivalent to the MAD-X :literal:`bv` flag.
.. [#f2] For example, the :literal:`:remove` method needs :literal:`not=true` to *not* remove all elements if no selector is provided.
.. [#f3] Updating directly the positions attributes of an element has no effect.
.. [#f4] An *iterable* supports the length operator :literal:`#`, the indexing operator :literal:`[]` and generic :literal:`for` loops with :literal:`ipairs`.
.. [#f5] MAD-NG does not have a MAD-X like :literal:`"USE"` command to finalize this computation.
