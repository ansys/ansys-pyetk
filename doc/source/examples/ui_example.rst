============================================
Create Transformer using the User Interface
============================================

This example demonstrates how to use the PyETK's User Interface (UI) to create an electronic transformer.
It provides a step-by-step guide on how to navigate through the UI, specify settings,
and design a transformer using the available fields and tools.

The design is that of a planar transformer, which is commonly used in power electronics applications.

    .. image:: ../_static/planar-transformer.png
         :align: center
         :width: 400
         :alt: Planar transformer

For simplicity the example focuses on one sub-menu at a time, starting with the core model, dimensions and materials,
then moving to the bobbin, winding and excitation information, and finally the Maxwell settings.

#. First, launch the PyETK, and connect to AEDT by clicking the **Connect to AEDT** button under the settings tab.
   For installation instructions, see :ref:`installation`.


    .. image:: ../_static/pyetk-toolkit-settings.png
        :width: 800
        :alt: Transformer Builder tab

#. Next, navigate to the **Transformer Builder** tab. This tab contains all the fields and tools to design and model electronic transformers.
   Modify the core information in the **Core** section by selecting the core type, core dimensions, and core material.

    .. image:: ../_static/menu-core.png
        :width: 600
        :alt: Transformer Builder tab

    .. note::
         The **Custom Core** checkbox enables the user to use a standard core shape with custom dimensions.

#. Then, modify the board information in the **Bobbin and Margin** section by selecting the bobbin type and bobbin dimensions.

    .. image:: ../_static/menu-bobbin-margin.png
        :width: 400
        :alt: Bobbin Margin Menu

    .. note::
         In PyETK the names bobbin and board are interchangeable. **Bobbin** is used to refer to *Wound* build types, while **Board** is used to refer to *Planar* build types. The fields in the UI are the same for both build types.
