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

.. _product:


================
Product Commands
================

Create
======

.. code-block:: bash

   fakturo product-create [positional arg] [opts]

List
====

Example

.. code-block:: bash

   fakturo product-list 4028868b3c4c43ed013c4c4551600000

Result

.. code-block:: text

   +----------------------------------------------+--------------------------+-------+--------+---------+------------+----------------------------------+-----------------------------------------+
   | merchant                                     | name                     | title | source | measure | type       | id                               | description                             |
   +----------------------------------------------+--------------------------+-------+--------+---------+------------+----------------------------------+-----------------------------------------+
   | {u'id': u'4028868b3c4c43ed013c4c4551600000'} | instance                 |       |        | unit    | gauge      | 4028868b3c4c43ed013c4c4553320002 | Duration of instance                    |
   | {u'id': u'4028868b3c4c43ed013c4c4551600000'} | memory                   |       |        | mb      | gauge      | 4028868b3c4c43ed013c4c4553760003 | Volume of RAM in MB                     |
   | {u'id': u'4028868b3c4c43ed013c4c4551600000'} | vcpus                    |       |        | vcpu    | gauge      | 4028868b3c4c43ed013c4c4553940004 | Number of VCPUs                         |
   +----------------------------------------------+--------------------------+-------+--------+---------+------------+----------------------------------+-----------------------------------------+

Get
===

Example

.. code-block:: bash

   fakturo product-get 4028868b3c4c43ed013c4c4551600000 4028868b3c4c43ed013c4c4553320002

Result

.. code-block:: text

   +-------------+----------------------------------------------+
   | Field       | Value                                        |
   +-------------+----------------------------------------------+
   | merchant    | {u'id': u'4028868b3c4c43ed013c4c4551600000'} |
   | name        | instance                                     |
   | title       | None                                         |
   | source      | None                                         |
   | measure     | unit                                         |
   | type        | gauge                                        |
   | id          | 4028868b3c4c43ed013c4c4553320002             |
   | description | Duration of instance                         |
   +-------------+----------------------------------------------+

Update
======

.. code-block:: bash

   fakturo product-update [positional arg] [opts]

Delete
======

.. code-block:: bash

   fakturo product-delete 4028868b3c4c43ed013c4c4551600000 4028868b3c4c43ed013c4c4553320000
