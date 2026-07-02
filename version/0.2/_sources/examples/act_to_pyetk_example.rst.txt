From ACT to PyETK example
============================================

This example demonstrates how to migrate from the ACT (Ansys Customization Toolkit) to the PyETK.
It provides a step-by-step guide on how to transition your existing ACT .json files to PyETK.

#. First, ensure you have a working ACT .json file. This file contains the configuration and settings for your transformer.
   The ACT's ETK .json file has no version and its structure contains three main sections: ``core_dimensions``, ``winding_definitions`` and ``setup_definitions``.
   It looks similar to the following:

   .. image:: ../_static/act-toolkit-json.png
      :align: center
      :width: 400
      :alt: UI start page tab

#. Next, open the PyETK User Interface (UI) and navigate to the **Transformer Builder** tab. Click *Open* and select your ACT .json file to load it into the PyETK.
   The PyETK automatically parses the ACT .json file and populate the fields in the UI with the corresponding values from the ACT .json file.

#. After loading the ACT .json file, you can review the populated fields in the UI to ensure that all the information has been correctly transferred.
   If you're planning on reusing the configuration file, click *Save As*. This way the ACT .json file is saved in the latest working .json format.

   .. image:: ../_static/load-act-json.png
      :align: center
      :width: 800
      :alt: Builder Window

   .. note::
      The Log window provides information about the loading process, including any errors or warnings that may occur during the migration.

#. PyETK's versioned .json file looks similar to the original ACT .json configuration file, however the differences enable better organization that allows for better readability and easier access to the different sections of the transformer configuration. The PyETK .json file contains a version number, which helps to track changes and updates to the file format over time. The PyETK .json file also has a more structured format, with clear sections for core dimensions, winding definitions, and setup definitions. This structure allows for easier navigation and understanding of the different components of the transformer configuration.
   Furthermore, it's versioned which implies that it can be updated and improved over time -- including further feature development -- without breaking compatibility with existing files.
   The versioned .json file looks like the following:

   .. image:: ../_static/pyetk-toolkit-json.png
      :align: center
      :width: 250
      :alt: Versioned .json file