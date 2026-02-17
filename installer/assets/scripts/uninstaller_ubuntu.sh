echo "Uninstalling Template Toolkit......."
sleep 3

rm -rf ${HOME}/.local/share/applications/ansys_pyetk.desktop
rm -rf ${HOME}/.local/usr/share/doc/ansys_pyetk

rm -rf ${HOME}/.local/opt/ansys_pyetk

sed -i '/# Add alias for Electronic Transformer toolKit/d' ~/.bashrc
sed -i  '/alias  ansys_pyetk/d' ~/.bashrc