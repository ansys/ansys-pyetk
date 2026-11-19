.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start

`0.5.0 <https://github.com/ansys/ansys-pyetk/releases/tag/v0.5.0>`_ - November 19, 2026
=======================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Log and Settings Open by Default
          - `#211 <https://github.com/ansys/ansys-pyetk/pull/211>`_

        * - Browse removal
          - `#221 <https://github.com/ansys/ansys-pyetk/pull/221>`_

        * - User can add own materials on top of shipped ones
          - `#429 <https://github.com/ansys/ansys-pyetk/pull/429>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Core and Conductor Faceting to use Segmentation Number not Mix of Angle and Number
          - `#201 <https://github.com/ansys/ansys-pyetk/pull/201>`_

        * - Correct Frequency Units in JSON Import Route
          - `#208 <https://github.com/ansys/ansys-pyetk/pull/208>`_

        * - Added region and winding support for half symmetry U and UI core models
          - `#209 <https://github.com/ansys/ansys-pyetk/pull/209>`_

        * - UI defaults
          - `#213 <https://github.com/ansys/ansys-pyetk/pull/213>`_

        * - Frontend - Validation Checks Added
          - `#239 <https://github.com/ansys/ansys-pyetk/pull/239>`_

        * - JSON load issue for Current excitation and Insulation Thickness
          - `#264 <https://github.com/ansys/ansys-pyetk/pull/264>`_

        * - JSON Insulation Import
          - `#302 <https://github.com/ansys/ansys-pyetk/pull/302>`_

        * - Export of None Connection Key to JSON
          - `#313 <https://github.com/ansys/ansys-pyetk/pull/313>`_

        * - Fix skin layers and improved material class
          - `#339 <https://github.com/ansys/ansys-pyetk/pull/339>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update individual contributors
          - `#196 <https://github.com/ansys/ansys-pyetk/pull/196>`_


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Bump actions/checkout from 6.0.2 to 6.0.3
          - `#230 <https://github.com/ansys/ansys-pyetk/pull/230>`_

        * - Bump astral-sh/setup-uv from 8.1.0 to 8.2.0
          - `#232 <https://github.com/ansys/ansys-pyetk/pull/232>`_

        * - Bump //github.com/python-jsonschema/check-jsonschema from 0.37.2 to 0.37.2
          - `#233 <https://github.com/ansys/ansys-pyetk/pull/233>`_

        * - Bump //github.com/astral-sh/ruff-pre-commit from v0.15.14 to 0.15.16
          - `#234 <https://github.com/ansys/ansys-pyetk/pull/234>`_

        * - Bump prek from 0.4.3 to 0.4.4
          - `#235 <https://github.com/ansys/ansys-pyetk/pull/235>`_

        * - Bump pyaedt from 1.0.1 to 1.1.0
          - `#236 <https://github.com/ansys/ansys-pyetk/pull/236>`_

        * - Bump tornado from 6.5.6 to 6.5.7
          - `#240 <https://github.com/ansys/ansys-pyetk/pull/240>`_

        * - Bump starlette from 1.2.1 to 1.3.1
          - `#241 <https://github.com/ansys/ansys-pyetk/pull/241>`_

        * - Bump jupyter-server from 2.19.0 to 2.20.0
          - `#242 <https://github.com/ansys/ansys-pyetk/pull/242>`_

        * - Bump https//github.com/astral-sh/ruff-pre-commit from v0.15.16 to 0.15.17
          - `#244 <https://github.com/ansys/ansys-pyetk/pull/244>`_

        * - Bump msgpack from 1.1.2 to 1.2.1
          - `#245 <https://github.com/ansys/ansys-pyetk/pull/245>`_

        * - Bump jupyterlab from 4.5.8 to 4.5.9
          - `#246 <https://github.com/ansys/ansys-pyetk/pull/246>`_

        * - Bump ansys/actions/release-github from 10.3.0 to 10.3.2
          - `#250 <https://github.com/ansys/ansys-pyetk/pull/250>`_

        * - Bump https//github.com/ansys/pre-commit-hooks from v0.7.2 to 0.8.0
          - `#251 <https://github.com/ansys/ansys-pyetk/pull/251>`_

        * - Bump https//github.com/astral-sh/ruff-pre-commit from v0.15.17 to 0.15.18
          - `#252 <https://github.com/ansys/ansys-pyetk/pull/252>`_

        * - Bump ansys/actions/doc-style from 10.3.0 to 10.3.2
          - `#253 <https://github.com/ansys/ansys-pyetk/pull/253>`_

        * - Bump softprops/action-gh-release from 2.6.2 to 3.0.1
          - `#254 <https://github.com/ansys/ansys-pyetk/pull/254>`_

        * - Bump ansys/actions/build-wheelhouse from 10.3.0 to 10.3.2
          - `#255 <https://github.com/ansys/ansys-pyetk/pull/255>`_

        * - Bump ansys/actions/doc-deploy-dev from 10.3.0 to 10.3.2
          - `#256 <https://github.com/ansys/ansys-pyetk/pull/256>`_

        * - Bump prek from 0.4.4 to 0.4.5
          - `#257 <https://github.com/ansys/ansys-pyetk/pull/257>`_

        * - Bump ansys-sphinx-theme from 1.8.2 to 1.9.0
          - `#258 <https://github.com/ansys/ansys-pyetk/pull/258>`_

        * - Bump pytest from 9.0.3 to 9.1.1
          - `#259 <https://github.com/ansys/ansys-pyetk/pull/259>`_

        * - Bump pyinstaller from 6.20.0 to 6.21.0
          - `#260 <https://github.com/ansys/ansys-pyetk/pull/260>`_

        * - Bump jupyterlab from 4.5.9 to 4.6.1
          - `#261 <https://github.com/ansys/ansys-pyetk/pull/261>`_

        * - Bump ansys/actions/doc-changelog from 10.3.0 to 10.3.2
          - `#265 <https://github.com/ansys/ansys-pyetk/pull/265>`_

        * - Bump actions/setup-python from 6.2.0 to 6.3.0
          - `#266 <https://github.com/ansys/ansys-pyetk/pull/266>`_

        * - Bump ansys/actions/check-actions-security from 10.3.0 to 10.3.2
          - `#268 <https://github.com/ansys/ansys-pyetk/pull/268>`_

        * - Bump ansys/actions/check-pr-title from 10.3.0 to 10.3.2
          - `#269 <https://github.com/ansys/ansys-pyetk/pull/269>`_

        * - Bump actions/checkout from 6.0.3 to 7.0.0
          - `#270 <https://github.com/ansys/ansys-pyetk/pull/270>`_

        * - Bump pyaedt from 1.1.0 to 1.2.0
          - `#271 <https://github.com/ansys/ansys-pyetk/pull/271>`_

        * - Bump mistune from 3.2.1 to 3.3.0
          - `#273 <https://github.com/ansys/ansys-pyetk/pull/273>`_

        * - Bump pillow from 12.2.0 to 12.3.0
          - `#277 <https://github.com/ansys/ansys-pyetk/pull/277>`_

        * - Bump setuptools from 82.0.1 to 83.0.0
          - `#278 <https://github.com/ansys/ansys-pyetk/pull/278>`_

        * - Bump jupyterlab from 4.5.9 to 4.5.10
          - `#279 <https://github.com/ansys/ansys-pyetk/pull/279>`_

        * - Bump https//github.com/codespell-project/codespell from v2.4.2 to 2.4.3
          - `#280 <https://github.com/ansys/ansys-pyetk/pull/280>`_

        * - Bump aiohttp from 3.14.1 to 3.14.3
          - `#284 <https://github.com/ansys/ansys-pyetk/pull/284>`_

        * - Bump https//github.com/python-jsonschema/check-jsonschema from 0.37.3 to 0.38.0
          - `#292 <https://github.com/ansys/ansys-pyetk/pull/292>`_

        * - Bump tornado from 6.5.7 to 6.5.8
          - `#299 <https://github.com/ansys/ansys-pyetk/pull/299>`_

        * - Bump mistune from 3.3.0 to 3.3.3
          - `#303 <https://github.com/ansys/ansys-pyetk/pull/303>`_

        * - Bump ansys/actions/doc-deploy-stable from 10.3.0 to 11.0.4
          - `#304 <https://github.com/ansys/ansys-pyetk/pull/304>`_

        * - Bump ansys/actions/doc-deploy-changelog from 10.3.0 to 11.0.4
          - `#305 <https://github.com/ansys/ansys-pyetk/pull/305>`_

        * - Bump ansys/actions/doc-deploy-dev from 10.3.2 to 11.0.6
          - `#306 <https://github.com/ansys/ansys-pyetk/pull/306>`_

        * - Bump actions/setup-python from 6.3.0 to 7.0.0
          - `#307 <https://github.com/ansys/ansys-pyetk/pull/307>`_

        * - Bump https//github.com/astral-sh/ruff-pre-commit from v0.15.18 to 0.16.5
          - `#308 <https://github.com/ansys/ansys-pyetk/pull/308>`_

        * - Bump astral-sh/setup-uv from 8.2.0 to 10.0.1
          - `#309 <https://github.com/ansys/ansys-pyetk/pull/309>`_

        * - Bump jupytext from 1.19.3 to 1.19.5
          - `#310 <https://github.com/ansys/ansys-pyetk/pull/310>`_

        * - Bump jupyterlab from 4.6.1 to 4.6.3
          - `#311 <https://github.com/ansys/ansys-pyetk/pull/311>`_

        * - Bump actions/labeler from 6.0.1 to 7.0.0
          - `#314 <https://github.com/ansys/ansys-pyetk/pull/314>`_

        * - Bump ansys/actions/release-github from 10.3.2 to 11.0.6
          - `#315 <https://github.com/ansys/ansys-pyetk/pull/315>`_

        * - Bump ansys/actions/doc-style from 10.3.2 to 11.0.8
          - `#316 <https://github.com/ansys/ansys-pyetk/pull/316>`_

        * - Bump ansys/actions/doc-build from 10.3.0 to 11.0.8
          - `#317 <https://github.com/ansys/ansys-pyetk/pull/317>`_

        * - Bump ansys/actions/build-wheelhouse from 10.3.2 to 11.0.8
          - `#318 <https://github.com/ansys/ansys-pyetk/pull/318>`_

        * - Bump https//github.com/astral-sh/ruff-pre-commit from v0.16.5 to 0.16.6
          - `#319 <https://github.com/ansys/ansys-pyetk/pull/319>`_

        * - Bump ipywidgets from 8.1.8 to 8.1.9
          - `#320 <https://github.com/ansys/ansys-pyetk/pull/320>`_

        * - Update flit-core requirement from <4,>=3.2 to >=3.2,<5
          - `#321 <https://github.com/ansys/ansys-pyetk/pull/321>`_

        * - Bump pyaedt from 1.2.0 to 1.6.0
          - `#322 <https://github.com/ansys/ansys-pyetk/pull/322>`_

        * - Bump prek from 0.4.5 to 0.5.2
          - `#323 <https://github.com/ansys/ansys-pyetk/pull/323>`_

        * - Bump soupsieve from 2.8.4 to 2.9
          - `#328 <https://github.com/ansys/ansys-pyetk/pull/328>`_

        * - Bump anyio from 4.13.0 to 4.14.2
          - `#329 <https://github.com/ansys/ansys-pyetk/pull/329>`_

        * - Bump ansys/actions/doc-deploy-changelog from 11.0.4 to 11.0.8
          - `#330 <https://github.com/ansys/ansys-pyetk/pull/330>`_

        * - Bump https//github.com/astral-sh/ruff-pre-commit from v0.16.6 to 0.16.7
          - `#331 <https://github.com/ansys/ansys-pyetk/pull/331>`_

        * - Bump astral-sh/setup-uv from 10.0.1 to 10.1.0
          - `#332 <https://github.com/ansys/ansys-pyetk/pull/332>`_

        * - Bump pypa/gh-action-pypi-publish from 1.14.0 to 1.14.2
          - `#333 <https://github.com/ansys/ansys-pyetk/pull/333>`_

        * - Bump ansys/actions/check-actions-security from 10.3.2 to 11.0.8
          - `#334 <https://github.com/ansys/ansys-pyetk/pull/334>`_

        * - Bump ansys/actions/doc-deploy-dev from 11.0.6 to 11.0.8
          - `#335 <https://github.com/ansys/ansys-pyetk/pull/335>`_

        * - Bump pyinstaller from 6.21.0 to 6.22.3
          - `#336 <https://github.com/ansys/ansys-pyetk/pull/336>`_

        * - Bump pyside6 from 6.11.1 to 6.11.2
          - `#337 <https://github.com/ansys/ansys-pyetk/pull/337>`_

        * - Bump ansys/actions/doc-changelog from 10.3.2 to 11.0.8
          - `#340 <https://github.com/ansys/ansys-pyetk/pull/340>`_

        * - Bump ansys/actions/build-library from 10.3.0 to 11.0.8
          - `#341 <https://github.com/ansys/ansys-pyetk/pull/341>`_

        * - Bump https//github.com/astral-sh/ruff-pre-commit from v0.16.7 to 0.16.8
          - `#342 <https://github.com/ansys/ansys-pyetk/pull/342>`_

        * - Bump actions/checkout from 7.0.0 to 7.0.1
          - `#343 <https://github.com/ansys/ansys-pyetk/pull/343>`_

        * - Bump ansys/actions/release-github from 11.0.6 to 11.0.8
          - `#344 <https://github.com/ansys/ansys-pyetk/pull/344>`_

        * - Bump softprops/action-gh-release from 3.0.1 to 3.0.3
          - `#345 <https://github.com/ansys/ansys-pyetk/pull/345>`_

        * - Bump prek from 0.5.2 to 0.5.3
          - `#346 <https://github.com/ansys/ansys-pyetk/pull/346>`_

        * - Bump pyaedt from 1.6.0 to 1.7.0
          - `#347 <https://github.com/ansys/ansys-pyetk/pull/347>`_

        * - Bump numpydoc from 1.10.0 to 1.11.0
          - `#348 <https://github.com/ansys/ansys-pyetk/pull/348>`_

        * - Bump ansys/actions/check-pr-title from 10.3.2 to 11.0.8
          - `#352 <https://github.com/ansys/ansys-pyetk/pull/352>`_

        * - Bump ansys/actions/doc-deploy-stable from 11.0.4 to 11.0.8
          - `#353 <https://github.com/ansys/ansys-pyetk/pull/353>`_

        * - Bump https//github.com/astral-sh/ruff-pre-commit from v0.16.8 to 0.16.9
          - `#354 <https://github.com/ansys/ansys-pyetk/pull/354>`_

        * - Bump https//github.com/python-jsonschema/check-jsonschema from 0.38.0 to 0.38.2
          - `#355 <https://github.com/ansys/ansys-pyetk/pull/355>`_

        * - Bump pyaedt from 1.7.0 to 1.8.0
          - `#356 <https://github.com/ansys/ansys-pyetk/pull/356>`_

        * - Bump astral-sh/setup-uv from 10.1.0 to 10.2.0
          - `#357 <https://github.com/ansys/ansys-pyetk/pull/357>`_

        * - Bump jupyterlab from 4.6.3 to 4.6.4
          - `#358 <https://github.com/ansys/ansys-pyetk/pull/358>`_

        * - Bump urllib3 from 2.7.0 to 2.8.0
          - `#359 <https://github.com/ansys/ansys-pyetk/pull/359>`_

        * - Bump tornado from 6.5.8 to 6.5.9
          - `#360 <https://github.com/ansys/ansys-pyetk/pull/360>`_

        * - Bump https//github.com/astral-sh/ruff-pre-commit from v0.16.9 to 0.16.10
          - `#362 <https://github.com/ansys/ansys-pyetk/pull/362>`_

        * - Bump prek from 0.5.3 to 0.5.4
          - `#363 <https://github.com/ansys/ansys-pyetk/pull/363>`_

        * - Bump werkzeug from 3.1.8 to 3.1.9
          - `#382 <https://github.com/ansys/ansys-pyetk/pull/382>`_

        * - Bump fsspec from 2026.4.0 to 2026.6.0
          - `#384 <https://github.com/ansys/ansys-pyetk/pull/384>`_

        * - Bump multidict from 6.7.1 to 6.9.1
          - `#385 <https://github.com/ansys/ansys-pyetk/pull/385>`_

        * - Bump actions/download-artifact from 7.0.0 to 8.0.2
          - `#386 <https://github.com/ansys/ansys-pyetk/pull/386>`_

        * - Bump actions/upload-artifact from 6.0.0 to 7.0.2
          - `#387 <https://github.com/ansys/ansys-pyetk/pull/387>`_

        * - Bump pypa/gh-action-pypi-publish from 1.14.2 to 1.14.3
          - `#406 <https://github.com/ansys/ansys-pyetk/pull/406>`_

        * - Bump the pre-commit group with 3 updates
          - `#425 <https://github.com/ansys/ansys-pyetk/pull/425>`_

        * - Bump the github-actions group with 13 updates
          - `#426 <https://github.com/ansys/ansys-pyetk/pull/426>`_

        * - Bump the python-dependencies group with 7 updates
          - `#427 <https://github.com/ansys/ansys-pyetk/pull/427>`_

        * - Bump the pre-commit group with 2 updates
          - `#430 <https://github.com/ansys/ansys-pyetk/pull/430>`_

        * - Bump the github-actions group with 12 updates
          - `#431 <https://github.com/ansys/ansys-pyetk/pull/431>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update CHANGELOG for v0.4.1
          - `#195 <https://github.com/ansys/ansys-pyetk/pull/195>`_

        * - Update main 0.5.dev0
          - `#197 <https://github.com/ansys/ansys-pyetk/pull/197>`_

        * - General updates related to configuration files and CI
          - `#226 <https://github.com/ansys/ansys-pyetk/pull/226>`_

        * - Use \`\`[dependency-groups]\`\` in \`\`pyproject.toml\`\` and introduce \`\`uv.lock\`\` file
          - `#227 <https://github.com/ansys/ansys-pyetk/pull/227>`_

        * - Update missing or outdated files
          - `#297 <https://github.com/ansys/ansys-pyetk/pull/297>`_

        * - Update ansys/actions to v11.1.3 and upgrade uv.lock file
          - `#401 <https://github.com/ansys/ansys-pyetk/pull/401>`_

        * - Add Groupings to Dependabot to reduce Volume of automatically Generated PRs
          - `#411 <https://github.com/ansys/ansys-pyetk/pull/411>`_


`0.4.1 <https://github.com/ansys/ansys-pyetk/releases/tag/v0.4.1>`_ - May 04, 2026
==================================================================================

.. tab-set::


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Fix turn spacing
          - `#190 <https://github.com/ansys/ansys-pyetk/pull/190>`_


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Bump ansys/actions from 10.2.9 to 10.3.0
          - `#193 <https://github.com/ansys/ansys-pyetk/pull/193>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update CHANGELOG for v0.4.0
          - `#192 <https://github.com/ansys/ansys-pyetk/pull/192>`_

        * - Update main branch v0.4.dev1
          - `#194 <https://github.com/ansys/ansys-pyetk/pull/194>`_


`0.4.0 <https://github.com/ansys/ansys-pyetk/releases/tag/v0.4.0>`_ - April 30, 2026
====================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Create multiple designs in same pyetk project
          - `#110 <https://github.com/ansys/ansys-pyetk/pull/110>`_

        * - Modify Navigation Buttons
          - `#134 <https://github.com/ansys/ansys-pyetk/pull/134>`_

        * - Core Dimension Check
          - `#164 <https://github.com/ansys/ansys-pyetk/pull/164>`_

        * - Add Current Version Number and Product Name to Splash Screen
          - `#165 <https://github.com/ansys/ansys-pyetk/pull/165>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Improve language regarding material database
          - `#152 <https://github.com/ansys/ansys-pyetk/pull/152>`_

        * - Update documentation images and use .svg instead of .png
          - `#161 <https://github.com/ansys/ansys-pyetk/pull/161>`_

        * - Upload .svg files to repo
          - `#163 <https://github.com/ansys/ansys-pyetk/pull/163>`_

        * - Remove expected behavior section in README
          - `#170 <https://github.com/ansys/ansys-pyetk/pull/170>`_

        * - Regenerate some of the documentation images to remove corporate logos
          - `#174 <https://github.com/ansys/ansys-pyetk/pull/174>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Removed mesh count limitation for core mesh refinement
          - `#146 <https://github.com/ansys/ansys-pyetk/pull/146>`_

        * - Fixed frequency sweep
          - `#150 <https://github.com/ansys/ansys-pyetk/pull/150>`_

        * - Add log scale plot to Ohmic_Loss plot
          - `#154 <https://github.com/ansys/ansys-pyetk/pull/154>`_

        * - Leakage inductance calculation
          - `#158 <https://github.com/ansys/ansys-pyetk/pull/158>`_

        * - Update UI message using .json version not just version
          - `#167 <https://github.com/ansys/ansys-pyetk/pull/167>`_

        * - Symmetry in U and UI cores
          - `#175 <https://github.com/ansys/ansys-pyetk/pull/175>`_

        * - Set core losses
          - `#176 <https://github.com/ansys/ansys-pyetk/pull/176>`_

        * - Create loss table
          - `#177 <https://github.com/ansys/ansys-pyetk/pull/177>`_

        * - Deleted folder old_json_files_delete
          - `#183 <https://github.com/ansys/ansys-pyetk/pull/183>`_

        * - Read ACT files
          - `#185 <https://github.com/ansys/ansys-pyetk/pull/185>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update CHANGELOG for v0.3.0
          - `#149 <https://github.com/ansys/ansys-pyetk/pull/149>`_

        * - Bump version 0.4.0dev
          - `#153 <https://github.com/ansys/ansys-pyetk/pull/153>`_

        * - Apply changes to ensure smooth deployment in PyPI
          - `#157 <https://github.com/ansys/ansys-pyetk/pull/157>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update AEDT version to 2026R1
          - `#180 <https://github.com/ansys/ansys-pyetk/pull/180>`_


`0.3.0 <https://github.com/ansys/ansys-pyetk/releases/tag/v0.3.0>`_ - April 17, 2026
====================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Included model validation
          - `#73 <https://github.com/ansys/ansys-pyetk/pull/73>`_

        * - General tidy up of UI inputs for QLineEdit and QTreeWidget.
          - `#130 <https://github.com/ansys/ansys-pyetk/pull/130>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Add example link in landing page
          - `#97 <https://github.com/ansys/ansys-pyetk/pull/97>`_

        * - Update main README.rst
          - `#102 <https://github.com/ansys/ansys-pyetk/pull/102>`_

        * - Add missing image of versioned json in documentation
          - `#104 <https://github.com/ansys/ansys-pyetk/pull/104>`_

        * - Overall review
          - `#106 <https://github.com/ansys/ansys-pyetk/pull/106>`_

        * - Use windows machine to build documentation
          - `#115 <https://github.com/ansys/ansys-pyetk/pull/115>`_

        * - Fix numbering in second example
          - `#118 <https://github.com/ansys/ansys-pyetk/pull/118>`_

        * - Add Ferroxcube material data link to help menu
          - `#136 <https://github.com/ansys/ansys-pyetk/pull/136>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Custom Core Dimensions
          - `#109 <https://github.com/ansys/ansys-pyetk/pull/109>`_

        * - Fix/logo
          - `#131 <https://github.com/ansys/ansys-pyetk/pull/131>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update CHANGELOG for v0.2.0
          - `#94 <https://github.com/ansys/ansys-pyetk/pull/94>`_

        * - Bump dev version into v0.3.dev0
          - `#95 <https://github.com/ansys/ansys-pyetk/pull/95>`_

        * - Update dependabot.yml configuration
          - `#98 <https://github.com/ansys/ansys-pyetk/pull/98>`_

        * - Run doc-build in self-hosted runner for examples
          - `#99 <https://github.com/ansys/ansys-pyetk/pull/99>`_

        * - Fix doc build for main and release workflows
          - `#101 <https://github.com/ansys/ansys-pyetk/pull/101>`_

        * - Add missing env variables to fix doc build
          - `#111 <https://github.com/ansys/ansys-pyetk/pull/111>`_

        * - Fix path to upload artifact
          - `#112 <https://github.com/ansys/ansys-pyetk/pull/112>`_

        * - Bump ansys actions to v10.2.9 to fix doc style
          - `#113 <https://github.com/ansys/ansys-pyetk/pull/113>`_

        * - Cleanup and use windows for doc-build jobs
          - `#116 <https://github.com/ansys/ansys-pyetk/pull/116>`_

        * - Fix generated artifacts in PR workflows
          - `#117 <https://github.com/ansys/ansys-pyetk/pull/117>`_

        * - Update PR workflow to rerun on title edit
          - `#120 <https://github.com/ansys/ansys-pyetk/pull/120>`_

        * - Add missing ansys license env var
          - `#128 <https://github.com/ansys/ansys-pyetk/pull/128>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Rename mu(freq) and eps_r to match backend data model
          - `#105 <https://github.com/ansys/ansys-pyetk/pull/105>`_


`0.2.0 <https://github.com/ansys/ansys-pyetk/releases/tag/v0.2.0>`_ - March 03, 2026
====================================================================================

.. tab-set::


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Bump actions/checkout from 6.0.1 to 6.0.2
          - `#51 <https://github.com/ansys/ansys-pyetk/pull/51>`_

        * - Bump actions/setup-python from 6.1.0 to 6.2.0
          - `#52 <https://github.com/ansys/ansys-pyetk/pull/52>`_

        * - Bump ansys/actions from 10.1.4 to 10.2.5
          - `#81 <https://github.com/ansys/ansys-pyetk/pull/81>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Website Documentation
          - `#82 <https://github.com/ansys/ansys-pyetk/pull/82>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Edited the splash screen
          - `#70 <https://github.com/ansys/ansys-pyetk/pull/70>`_

        * - Remove Deletion of Top Level Parent Connection
          - `#76 <https://github.com/ansys/ansys-pyetk/pull/76>`_

        * - Remove AEDT Design title in toolkit Help Menu
          - `#78 <https://github.com/ansys/ansys-pyetk/pull/78>`_

        * - Deprecated arguments in generate_unique_project_name
          - `#80 <https://github.com/ansys/ansys-pyetk/pull/80>`_

        * - Delete Button added to delete row types Layers and Sides
          - `#86 <https://github.com/ansys/ansys-pyetk/pull/86>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update CHANGELOG for v0.1.0
          - `#65 <https://github.com/ansys/ansys-pyetk/pull/65>`_

        * - Bump version 0.2.0dev and update to year 2026
          - `#66 <https://github.com/ansys/ansys-pyetk/pull/66>`_

        * - Add new review changes
          - `#71 <https://github.com/ansys/ansys-pyetk/pull/71>`_

        * - Review of the backend code base
          - `#85 <https://github.com/ansys/ansys-pyetk/pull/85>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Assign_matrix
          - `#84 <https://github.com/ansys/ansys-pyetk/pull/84>`_

        * - Changes related to UI / frontend logic
          - `#88 <https://github.com/ansys/ansys-pyetk/pull/88>`_

        * - Remove AEDT timeout
          - `#93 <https://github.com/ansys/ansys-pyetk/pull/93>`_


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

        * - Add missing job dependency in release job
          - `#64 <https://github.com/ansys/ansys-pyetk/pull/64>`_

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