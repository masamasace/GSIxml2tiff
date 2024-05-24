from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProject
from qgis.gui import QgsMessageBar
import os.path

class MyPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = self.tr(u'&My Plugin')
        self.toolbar = self.iface.addToolBar(u'MyPlugin')
        self.toolbar.setObjectName(u'MyPlugin')

    def tr(self, message):
        return QCoreApplication.translate('MyPlugin', message)

    def initGui(self):
        icon_path = ':/plugins/MyPlugin/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Import DEM XML and convert to GeoTIFF'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def add_action(self, icon_path, text, callback, enabled_flag=True, add_to_menu=True, add_to_toolbar=True, status_tip=None, whats_this=None, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        if add_to_toolbar:
            self.toolbar.addAction(action)
        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)
        self.actions.append(action)
        return action

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&My Plugin'), action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        self.import_and_convert()

    def import_and_convert(self):
        # DEM XMLファイルの選択
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, "Select DEM XML file", "", "XML Files (*.xml)")

        if not file_path:
            return

        # GeoTIFFに変換
        import gdal
        dem_data = gdal.Open(file_path)
        output_path = os.path.splitext(file_path)[0] + ".tif"
        gdal.Translate(output_path, dem_data)
        self.iface.messageBar().pushMessage("Conversion complete", f"GeoTIFF saved to {output_path}", level=Qgis.Info, duration=5)
