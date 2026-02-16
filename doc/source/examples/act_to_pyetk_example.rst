============================================
From ACT to PyETK Example
============================================

This example demonstrates how to migrate from the ACT (Ansys Customization Toolkit) to the PyETK.
It provides a step-by-step guide on how to transition your existing ACT json files to PyETK.

#. First, ensure you have a working ACT json file. This file contains the configuration and settings for your transformer.
   The ACT's ETK json file has no version and its structure contains three main sections: core_dimensions, winding_definitions and setup_definitions.
   It looks similar to the following:

   .. image:: ../_static/act-toolkit-json.png
      :width: 400
      :alt: UI start page tab

#. Next, open the PyETK User Interface (UI) and navigate to the **Transformer Builder** tab. Click *Open* and select your ACT json file to load it into the PyETK.
   The PyETK will automatically parse the ACT json file and populate the fields in the UI with the corresponding values from the ACT json file.

#. After loading the ACT json file, you can review the populated fields in the UI to ensure that all the information has been correctly transferred.
   If you're planning on reusing the configuration file, click on *Save As...*. This way the ACT json file is saved in the latest working json format.

   .. image:: ../_static/load-act-json.png
      :width: 800
      :alt: Builder Window

   .. note::
      The Log window will provide information about the loading process, including any errors or warnings that may occur during the migration.
