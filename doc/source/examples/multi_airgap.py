from ansys.aedt.core import Maxwell3d

height = 0.61267603887905
radius = 6.4
a_dist = 2 * height


def create_three_airgaps():
    # connect to current AEDT instance
    aedtapp = Maxwell3d()

    # create three cylinders
    airgap1 = aedtapp.modeler.create_cylinder(
        orientation="Z",
        origin=[0, 0, -height / 2 - a_dist],
        radius=radius,
        height=height,
        name="Airgap1",
        material="vacuum",
    )

    airgap2 = aedtapp.modeler.create_cylinder(
        orientation="Z", origin=[0, 0, -height / 2], radius=radius, height=height, name="Airgap2", material="vacuum"
    )

    airgap3 = aedtapp.modeler.create_cylinder(
        orientation="Z",
        origin=[0, 0, -height / 2 + a_dist],
        radius=radius,
        height=height,
        name="Airgap3",
        material="vacuum",
    )

    # subtract the cylinders from the magnetic core
    aedtapp.modeler.subtract(
        blank_list=["RM_Core_Top", "RM_Core_Bottom"],
        tool_list=[airgap1.name, airgap2.name, airgap3.name],
        keep_originals=False,
    )

    # bring all items to fit screen and release AEDT
    aedtapp.modeler.fit_all()
    aedtapp.release_desktop(close_desktop=False, close_projects=False)
