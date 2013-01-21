..
    Copyright 2012 Endre Karlson for Bouvet ASA

    Licensed under the Apache License, Version 2.0 (the "License"); you may
    not use this file except in compliance with the License. You may obtain
    a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
    License for the specific language governing permissions and limitations
    under the License.

.. _customer:

=================
Customer Commands
=================

Create
======

.. code-block:: bash

   fakturo customer-create [positional arg] [opts]

List
====

Example

.. code-block:: bash

   fakturo customer-list 4028868b3c4c43ed013c4c4551600000

Results

.. code-block:: text

   +----------+----------------------------------+----------+--------+
   | currency | id                               | language | name   |
   +----------+----------------------------------+----------+--------+
   | NOK      | 4028868b3c4c43ed013c4c4622130016 | NO       | Test   |
   +----------+----------------------------------+----------+--------+

Get
===

Example

.. code-block:: bash

   fakturo customer-get [positional arg] [opts]

Result

.. code-block:: text

   +----------+----------------------------------+
   | Field    | Value                            |
   +----------+----------------------------------+
   | currency | NOK                              |
   | id       | 4028868b3c4c43ed013c4c4622130016 |
   | language | no                               |
   | name     | Test                             |
   +----------+----------------------------------+

Update
======

.. code-block:: bash

   fakturo customer-update [positional arg] [opts]

Delete
======

Example

.. code-block:: bash

   fakturo customer-delete 4028868b3c4c43ed013c4c455160000 4028868b3c4c43ed013c4c4622130016

