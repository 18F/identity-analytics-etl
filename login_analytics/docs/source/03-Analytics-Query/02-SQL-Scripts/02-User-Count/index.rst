.. contents::

.. _aq_user_count:

User Count
==============================================================================

SQL in this folder answers this type of questions:

    What is the number of users that ...


User Signup / Signin Workflow Diagram
------------------------------------------------------------------------------

Based on the workflow, we mark user as ``Member`` if they finished these, even they have not used it for any service:

1. Enter their email.
2. Confirmed their email. Then an ``user_id`` been created
3. Complete MFA Registration.

We have a diagram posted on mural.ly boards: https://app.mural.co/t/gsa6/m/gsa6/1528299310047/b4895b6f43c99fc715ab26fcdbacf0562360574e. And also a draw.io diagram:

.. raw:: html

    <div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile userAgent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\&quot; version=\&quot;9.3.1\&quot; editor=\&quot;www.draw.io\&quot; type=\&quot;device\&quot;&gt;&lt;diagram id=\&quot;d8824795-f73c-d7ba-4886-b69b77114190\&quot; name=\&quot;Page-1\&quot;&gt;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&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
    <script type="text/javascript" src="https://www.draw.io/js/viewer.min.js"></script>


Enter Email
------------------------------------------------------------------------------

.. literalinclude:: ./user-count-who-entered-their-email.sql
    :language: sql


Confirmed Email
------------------------------------------------------------------------------

.. literalinclude:: ./user-count-who-confirmed-their-email.sql
    :language: sql


Setup MFA
------------------------------------------------------------------------------

Put some explanation here.


.. literalinclude:: ./user-count-who-setup-MFA.sql
    :language: sql


Reference
------------------------------------------------------------------------------

:ref:`prod.redshift.schema.column.events.name`
