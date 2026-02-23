User Interface
==============

This section describes how to use the PyETK. It assumes that you have already launched the
toolkit. For toolkit installation, see :ref:`installation`

The first section focuses on the general tools available in the UI, coming from the common toolkit framework.
The second section focuses on the application specific fields and tools to design and model electronic transformers.

Toolkit common framework
=========================

This section describes the use of the common framework of the PyETK, which is shared across all toolkits.
Basic navigation through the UI starting from the starting page to the settings and log tabs is described below.

   .. image:: ../_static/pyetk-gui.png
      :width: 800
      :alt: UI start page tab


#. On the **Settings** tab, specify settings for either creating an AEDT session or
   connecting to an existing AEDT session.

   .. note::
      If the PyETK Wizard is launched from AEDT, the **Settings** tab does not appear
      because the toolkit is directly connected to the specific AEDT session.

   .. image:: ../_static/pyetk-toolkit-settings.png
      :width: 800
      :alt: Settings tab

#. A general log window is available by clicking on the **Log** tab on the left side.
   This log file provides information about the toolkit's operations, such as the status of the connection to AEDT,
   the creation of geometries, and any errors that may occur during the process.

    .. image:: ../_static/pyetk-toolkit-log.png
        :width: 800
        :alt: Log tab


#. The **Help** tab provides access to the PyETK documentation, and Github's tracked issues.

    .. image:: ../_static/pyetk-toolkit-help.png
        :width: 800
        :alt: Help tab

Transformer Builder
====================

The **Transformer Builder** expands the fields to design and model electronic transformers.
It provides fields to specify the core type, core dimensions, bobbin type, bobbin dimensions, winding information, and excitation information.
In addition there is a settings section to specify Maxwell analysis settings such as number of passes, percent error, maximum number of passes and frequency sweeps.

    .. image:: ../_static/pyetk-toolkit-builder.png
        :width: 800
        :alt: Transformer Builder tab