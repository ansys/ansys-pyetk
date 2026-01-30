.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start

`0.1.0 <https://github.com/ansys/ansys-pyetk/releases/tag/v0.1.0>`_ - January 30, 2026
======================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - JSON Example Files Added
          - `#5 <https://github.com/ansys/ansys-pyetk/pull/5>`_

        * - Settings Group Added to LHS UI Column
          - `#186 <https://github.com/ansys/ansys-pyetk/pull/186>`_

        * - Add Support for Bespoke and Reference Core Dimensions
          - `#196 <https://github.com/ansys/ansys-pyetk/pull/196>`_

        * - update json format
          - `#210 <https://github.com/ansys/ansys-pyetk/pull/210>`_

        * - BE tests improvement
          - `#214 <https://github.com/ansys/ansys-pyetk/pull/214>`_

        * - UI Save Button
          - `#215 <https://github.com/ansys/ansys-pyetk/pull/215>`_

        * - Add Connections to Data Exchange
          - `#231 <https://github.com/ansys/ansys-pyetk/pull/231>`_

        * - Add FE Tests
          - `#232 <https://github.com/ansys/ansys-pyetk/pull/232>`_


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Bump actions/setup-python from 6.0.0 to 6.1.0
          - `#212 <https://github.com/ansys/ansys-pyetk/pull/212>`_

        * - Bump softprops/action-gh-release from 2.3.3 to 2.5.0
          - `#217 <https://github.com/ansys/ansys-pyetk/pull/217>`_

        * - Bump actions/checkout from 5.0.0 to 6.0.1
          - `#218 <https://github.com/ansys/ansys-pyetk/pull/218>`_

        * - Bump actions/download-artifact from 5.0.0 to 7.0.0
          - `#223 <https://github.com/ansys/ansys-pyetk/pull/223>`_

        * - Bump actions/upload-artifact from 4.6.2 to 6.0.0
          - `#224 <https://github.com/ansys/ansys-pyetk/pull/224>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Remove Fixed Issues from README.rst
          - `#11 <https://github.com/ansys/ansys-pyetk/pull/11>`_

        * - Correct README.rst syntax
          - `#13 <https://github.com/ansys/ansys-pyetk/pull/13>`_

        * - Fix Help Menu Title "PyETK Transformer Toolkit"
          - `#18 <https://github.com/ansys/ansys-pyetk/pull/18>`_

        * - Improved backend API documentation
          - `#33 <https://github.com/ansys/ansys-pyetk/pull/33>`_

        * - Update badge link in README.rst
          - `#44 <https://github.com/ansys/ansys-pyetk/pull/44>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Fixed pyaedt arguments
          - `#22 <https://github.com/ansys/ansys-pyetk/pull/22>`_

        * - Backend model json_version typo
          - `#49 <https://github.com/ansys/ansys-pyetk/pull/49>`_

        * - Update backend properties, one property at a time
          - `#54 <https://github.com/ansys/ansys-pyetk/pull/54>`_

        * - Fixed layer spacing
          - `#60 <https://github.com/ansys/ansys-pyetk/pull/60>`_

        * - Rename create_transformer to create_model
          - `#188 <https://github.com/ansys/ansys-pyetk/pull/188>`_

        * - Fix load in side 1
          - `#191 <https://github.com/ansys/ansys-pyetk/pull/191>`_

        * - Fixes BE issues
          - `#197 <https://github.com/ansys/ansys-pyetk/pull/197>`_

        * - Frequency unit conversion
          - `#205 <https://github.com/ansys/ansys-pyetk/pull/205>`_

        * - Read from and Write gui_properties
          - `#216 <https://github.com/ansys/ansys-pyetk/pull/216>`_

        * - import fe_properties as properties
          - `#229 <https://github.com/ansys/ansys-pyetk/pull/229>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update license to Apache-2.0
          - `#2 <https://github.com/ansys/ansys-pyetk/pull/2>`_

        * - Clean doc and tests jobs
          - `#8 <https://github.com/ansys/ansys-pyetk/pull/8>`_

        * - Refactor into multiple workflors
          - `#21 <https://github.com/ansys/ansys-pyetk/pull/21>`_

        * - Update project's root level files
          - `#24 <https://github.com/ansys/ansys-pyetk/pull/24>`_

        * - Add missing checkout and wheelhouse
          - `#56 <https://github.com/ansys/ansys-pyetk/pull/56>`_

        * - update CHANGELOG for v0.1.0a0
          - `#178 <https://github.com/ansys/ansys-pyetk/pull/178>`_

        * - bump 0.2.dev0
          - `#179 <https://github.com/ansys/ansys-pyetk/pull/179>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update Save As button text
          - `#45 <https://github.com/ansys/ansys-pyetk/pull/45>`_

        * - Update main_page.py
          - `#46 <https://github.com/ansys/ansys-pyetk/pull/46>`_

        * - PostProcessing and new HTTP request through /create_model
          - `#184 <https://github.com/ansys/ansys-pyetk/pull/184>`_

        * - remove/modify PyAEDT from toolkit naming convention
          - `#189 <https://github.com/ansys/ansys-pyetk/pull/189>`_

        * - Frontend Data and DataBase Manager
          - `#228 <https://github.com/ansys/ansys-pyetk/pull/228>`_

        * - Connections Definitions and Minor FE Fixes
          - `#230 <https://github.com/ansys/ansys-pyetk/pull/230>`_


  .. tab-item:: Test

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Add additional bobbin unit tests
          - `#6 <https://github.com/ansys/ansys-pyetk/pull/6>`_

        * - Add additional data_manager unit tests
          - `#7 <https://github.com/ansys/ansys-pyetk/pull/7>`_

        * - Add circuit test
          - `#9 <https://github.com/ansys/ansys-pyetk/pull/9>`_

        * - Improved core tests
          - `#14 <https://github.com/ansys/ansys-pyetk/pull/14>`_

        * - UI Core with and without Airgap
          - `#15 <https://github.com/ansys/ansys-pyetk/pull/15>`_

        * - Add tests to FE data manager
          - `#16 <https://github.com/ansys/ansys-pyetk/pull/16>`_


.. vale on