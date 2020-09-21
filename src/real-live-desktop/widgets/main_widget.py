# -*- coding: utf-8 -*-
"""
@Author    : parzulpan

@Email     : parzulpan@gmail.com

@Summary   : 软件主页面，使用单例模式

@Attention :
"""

import sys
import os

from PyQt5.QtWidgets import QMainWindow, QApplication, QMenuBar, QMenu, QAction, QDesktopWidget, qApp, \
    QToolBar, QActionGroup, QFontDialog, QSlider, QLabel, QFileDialog
from PyQt5.QtGui import QKeySequence, QIcon, QDesktopServices, QFont
from PyQt5.QtCore import Qt, QSize, QUrl

from utils.common import *
from utils.path_helper import PathHelper
from widgets.radio_station_widget import RadioStationWidget
from widgets.search_widget import SearchWidget
from widgets.tv_widget import TvWidget
from widgets.live_widget import LiveWidget
from widgets.about_widget import AboutWidget
from widgets.preferences_widget import PreferencesWidget


class MainWindow(QMainWindow):
    """

    """
    def __init__(self):
        super(MainWindow, self).__init__()

        self.menu_bar = QMenuBar()

        self.media_menu = QMenu("媒体(&M)", self.menu_bar)
        self.local_action = QAction("本地文件(L)", self.media_menu)
        self.local_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_M))
        self.local_action.triggered.connect(self.show_local_widget)
        self.live_search_action = QAction("直播搜索(F)", self.media_menu)
        self.live_search_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_F))
        self.live_search_action.triggered.connect(self.show_search_widget)
        self.tv_live_search_action = QAction("高清电视(F)", self.media_menu)
        self.tv_live_search_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_F))
        self.tv_live_search_action.triggered.connect(self.show_tv_widget)
        self.radio_station_search_action = QAction("广播电台(F)", self.media_menu)
        self.radio_station_search_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_F))
        self.radio_station_search_action.triggered.connect(self.show_radio_station_widget)
        self.close_action = QAction("关闭(C)", self.media_menu)
        self.close_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_C))
        self.close_action.triggered.connect(self.answer_close_action_triggered)
        self.quit_action = QAction("退出(Q)", self.media_menu)
        self.quit_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q))
        self.quit_action.triggered.connect(lambda: sys.exit())

        self.tool_menu = QMenu("增强(&E)", self.menu_bar)
        self.screenshot_action = QAction("截图(J)", self.tool_menu)
        self.screenshot_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_J))
        self.screenshot_action.triggered.connect(self.answer_screenshot_action_triggered)
        self.gif_action = QAction("动图(G)", self.tool_menu)
        self.gif_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_G))
        self.gif_action.triggered.connect(self.answer_gif_action_triggered)
        self.screen_record_action = QAction("录屏(L)", self.tool_menu)
        self.screen_record_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_L))
        self.screen_record_action.triggered.connect(self.answer_screen_record_action_triggered)
        self.preferences_action = QAction("偏好设置(L)", self.tool_menu)
        self.preferences_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_L))
        self.preferences_action.triggered.connect(self.answer_screen_record_action_triggered)
        self.hide_action = QAction("隐藏工具栏(V)", self.tool_menu)
        self.hide_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_V))
        self.hide_action.setCheckable(True)
        self.hide_action.triggered.connect(self.answer_hide_action_triggered)

        self.help_menu = QMenu("帮助(&H)", self.menu_bar)
        self.help_action = QAction("帮助文档(H)", self.help_menu)
        self.help_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_H))
        self.help_action.triggered.connect(self.answer_help_action_triggered)
        self.change_log_action = QAction("更新日志(U)", self.help_menu)
        self.change_log_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_U))
        self.change_log_action.triggered.connect(self.answer_change_log_action_triggered)
        self.check_version_action = QAction("检查版本(C)", self.help_menu)
        self.check_version_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_C))
        self.check_version_action.triggered.connect(self.answer_check_version_action_triggered)
        self.about_action = QAction("关于软件(A)", self.help_menu)
        self.about_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_A))
        self.about_action.triggered.connect(self.answer_about_action_triggered)

        self.tool_bar = QToolBar()
        self.tool_bar.setFloatable(False)
        self.tool_bar.setMovable(True)
        self.tool_bar.setIconSize(QSize(35, 35))
        # self.tool_bar.setStyleSheet("QToolBar{border: 1px solid #313335; spacing:5px; }")
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar)
        self.live_tool_action = QAction("", self.tool_bar)
        self.live_tool_action.setToolTip("直播搜索")
        self.live_tool_action.setIcon(QIcon(PathHelper.get_img_path("search@128x128.png")))
        self.search_widget = SearchWidget()
        self.live_tool_action.triggered.connect(self.show_search_widget)
        self.search_widget.watch_live_signal.connect(self.answer_watch_live_signal)

        self.tv_live_tool_action = QAction("", self.tool_bar)
        self.tv_live_tool_action.setToolTip("高清电视")
        self.tv_live_tool_action.setIcon(QIcon(PathHelper.get_img_path("tv@128x128.png")))
        self.tv_widget = TvWidget()
        self.tv_live_tool_action.triggered.connect(self.show_tv_widget)
        self.tv_widget.watch_live_signal.connect(self.answer_watch_live_signal)

        self.radio_station_tool_action = QAction("", self.tool_bar)
        self.radio_station_tool_action.setToolTip("广播电台")
        self.radio_station_tool_action.setIcon(QIcon(PathHelper.get_img_path("radio_station@128x128.png")))
        self.radio_station_widget = RadioStationWidget()
        self.radio_station_tool_action.triggered.connect(self.show_radio_station_widget)
        self.radio_station_widget.listen_radio_station_signal.connect(self.answer_listen_radio_station_signal)

        self.hot_live_tool_action = QAction("", self.tool_bar)
        self.hot_live_tool_action.setToolTip("热门直播")
        self.hot_live_tool_action.setIcon(QIcon(PathHelper.get_img_path("hot@128x128.png")))

        self.attention_tool_action = QAction("", self.tool_bar)
        self.attention_tool_action.setToolTip("我的关注")
        self.attention_tool_action.setIcon(QIcon(PathHelper.get_img_path("attention@128x128.png")))
        # self.attention_tool_action.triggered.connect(self.show_search_widget)

        self.preferences_tool_action = QAction("", self.tool_bar)
        self.preferences_tool_action.setToolTip("偏好设置")
        self.preferences_tool_action.setIcon(QIcon(PathHelper.get_img_path("preferences@128x128.png")))
        self.preferences_tool_action.triggered.connect(self.show_preferences_widget)

        self.nlp_tool_action = QAction("", self.tool_bar)
        self.nlp_tool_action.setToolTip("智能字幕")
        self.nlp_tool_action.setIcon(QIcon(PathHelper.get_img_path("nlp@128x128.png")))
        # self.nlp_tool_action.triggered.connect(self.show_search_widget)

        self.note_tool_action = QAction("", self.tool_bar)
        self.note_tool_action.setToolTip("边看边记")
        self.note_tool_action.setIcon(QIcon(PathHelper.get_img_path("note@128x128.png")))
        # self.note_tool_action.triggered.connect(self.show_search_widget)

        self.play_pause_btn = ControlBtn("pause@128x128.png", "play@128x128.png")
        self.play_pause_btn.setToolTip("播放/暂停")
        self.play_pause_btn.setShortcut(Qt.Key_Space)
        self.play_pause_btn.clicked.connect(self.answer_play_pause_btn_clicked)

        self.refresh_btn = ControlBtn("refresh@128x128.png", "refresh@128x128.png")
        self.refresh_btn.setToolTip("刷新")
        self.refresh_btn.clicked.connect(self.answer_refresh_btn_clicked)

        self.rewind_btn = ControlBtn("rewind@128x128.png", "rewind@128x128.png")
        self.rewind_btn.setToolTip("后退10秒")
        self.rewind_btn.clicked.connect(self.answer_rewind_btn_clicked)

        self.stop_btn = ControlBtn("stop@128x128.png", "stop@128x128.png")
        self.stop_btn.setToolTip("停止")
        self.stop_btn.clicked.connect(self.answer_stop_btn_clicked)

        self.fast_forward_btn = ControlBtn("fast_forward@128x128.png", "fast_forward@128x128.png")
        self.fast_forward_btn.setToolTip("前进10秒")
        self.fast_forward_btn.clicked.connect(self.answer_fast_forward_btn_clicked)

        self.fullscreen_narrow_btn = ControlBtn("fullscreen@128x128.png", "narrow@128x128.png")
        self.fullscreen_narrow_btn.setToolTip("最大化/最小化")
        self.fullscreen_narrow_btn.setShortcut(Qt.Key_Escape)
        self.fullscreen_narrow_btn.clicked.connect(self.answer_fullscreen_narrow_btn_clicked)

        self.volume_btn = ControlBtn("volume@128x128.png", "mute@128x128.png")
        self.volume_btn.setToolTip("音量")
        self.volume_btn.clicked.connect(self.answer_volume_btn_clicked)

        self.volume_slider = QSlider(Qt.Vertical)
        self.volume_slider.setFixedHeight(35)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setSingleStep(1)
        self.volume_slider.setTickInterval(1)
        self.volume_slider.setTickPosition(QSlider.TicksAbove)
        self.volume_slider.valueChanged.connect(self.answer_volume_slider_value_changed)

        self.current_volume = None
        self.current_slider_value = None
        self.volume_slider_value_label = QLabel("")
        self.current_url = None

        self.live_widget = LiveWidget()

        self._init_ui()
        self._init_cfg()

    def _init_ui(self):
        """

        :return:
        """
        # 菜单栏
        self.media_menu.addAction(self.local_action)
        self.media_menu.addAction(self.live_search_action)
        self.media_menu.addAction(self.tv_live_search_action)
        self.media_menu.addAction(self.radio_station_search_action)
        self.media_menu.addSeparator()
        self.media_menu.addAction(self.close_action)
        self.media_menu.addAction(self.quit_action)

        self.tool_menu.addAction(self.screenshot_action)
        self.tool_menu.addAction(self.gif_action)
        self.tool_menu.addAction(self.screen_record_action)
        self.tool_menu.addSeparator()
        self.tool_menu.addAction(self.preferences_action)
        self.tool_menu.addSeparator()
        self.tool_menu.addAction(self.hide_action)

        self.help_menu.addAction(self.help_action)
        self.help_menu.addAction(self.change_log_action)
        self.help_menu.addAction(self.check_version_action)
        self.help_menu.addSeparator()
        self.help_menu.addAction(self.about_action)

        self.menu_bar.addMenu(self.media_menu)
        self.menu_bar.addMenu(self.tool_menu)
        self.menu_bar.addMenu(self.help_menu)

        self.setMenuBar(self.menu_bar)

        # 工具栏
        self.tool_bar.addAction(self.live_tool_action)
        self.tool_bar.addAction(self.tv_live_tool_action)
        self.tool_bar.addAction(self.radio_station_tool_action)
        self.tool_bar.addAction(self.hot_live_tool_action)
        self.tool_bar.addAction(self.attention_tool_action)
        self.tool_bar.addSeparator()
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.nlp_tool_action)
        self.tool_bar.addAction(self.note_tool_action)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.preferences_tool_action)
        # 工具栏播放控制
        self.tool_bar.addSeparator()
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.play_pause_btn)
        self.tool_bar.addWidget(self.refresh_btn)
        self.tool_bar.addWidget(self.rewind_btn)
        self.tool_bar.addWidget(self.stop_btn)
        self.tool_bar.addWidget(self.fast_forward_btn)
        self.tool_bar.addWidget(self.fullscreen_narrow_btn)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.volume_btn)
        self.tool_bar.addWidget(self.volume_slider_value_label)
        self.tool_bar.addWidget(self.volume_slider)

        # 显示区域
        self.setCentralWidget(self.live_widget)

        self.set_window_info()

    def _init_cfg(self):
        """

        :return:
        """

        # 工具栏可见性
        visible = get_tool_bar_visible()
        if visible:
            self.hide_action.setChecked(False)
            self.hide_action.triggered.emit(False)
        else:
            self.hide_action.setChecked(True)
            self.hide_action.triggered.emit(True)

        # 皮肤设置
        skin = get_skin()
        set_skin(skin)

        # 语言设置
        language = get_language()
        set_language(language)

        # 字体设置
        font_dict = get_font()
        font = QFont()
        font.setFamily(font_dict["font_family"])
        font.setStyleName(font_dict["font_style"])
        font.setPointSize(font_dict["font_size"])
        qApp.setFont(font)
        qApp.processEvents()

    def set_window_info(self):
        """

        :return:
        """
        desktop_widget = QDesktopWidget()
        screen_rect = desktop_widget.screenGeometry()
        self.setGeometry(screen_rect)
        _app_info = get_app_info()
        title = _app_info["name"] + " " + _app_info["version"]
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(PathHelper.get_img_path("logo@48x48.png")))
        self.showMaximized()

    def show_local_widget(self):
        """

        :return:
        """
        file_name, file_type = QFileDialog.getOpenFileName(self, "选择音视频文件", ".", "All Files (*)")
        if file_name:
            _type = os.path.splitext(file_name)[-1][1:]
            _type_list = ["3g2", "3gp", "3gp2", "3gpp", "amv", "asf", "avi", "bik", "bin", "divx", "drc", "dv", "f4v",
                          "flv", "gvi", "gxf", "iso", "m1v", "m2v", "m2t", "m2ts", "m4v", "mkv", "mov", "mp2", "mp4",
                          "mp4v", "mpe", "mpeg", "mpeg1", "mpeg2", "mpeg4", "mpg", "mpv2", "mts", "mxf", "mxg", "nsv",
                          "nuv", "ogg", "ogm", "ogv", "ps", "rec", "rm", "rmvb", "rpl", "thp", "tod", "ts", "tts",
                          "txd", "vob", "vro", "webm", "wm", "wmv", "wtv", "xesc",
                          "3ga", "669", "a52", "acc", "ac3", "adt", "adts", "aif", "aiff", "amr", "aob", "ape", "awb",
                          "caf", "dts", "flac", "it",
                          "kar", "m4a", "m4b", "m4p", "m5p", "mid", "mka", "mlp", "mod", "mpa", "mp1", "mp2", "mp3",
                          "mpc", "mpga", "mus", "oga",
                          "ogg", "oma", "opus", "qcp", "ra", "rmi", "s3m", "sid", "spx", "thd", "tta", "voc", "vqf",
                          "w64", "wav", "wma", "wv", "xa", "xm"]
            if _type in _type_list:
                self.answer_watch_live_signal(file_name)
            else:
                _box = PromptBox(2, "音视频文件错误!", 1)
                width, height = get_window_center_point(_box)
                _box.move(width, height)
                _box.exec_()

    def show_search_widget(self):
        """

        :return:
        """
        width, height = get_window_center_point(self.search_widget)
        self.search_widget.move(width, height)
        self.search_widget.exec_()

    def show_tv_widget(self):
        """

        :return:
        """
        width, height = get_window_center_point(self.tv_widget)
        self.tv_widget.move(width, height)
        self.tv_widget.exec_()

    def show_radio_station_widget(self):
        """

        :return:
        """
        width, height = get_window_center_point(self.radio_station_widget)
        self.radio_station_widget.move(width, height)
        self.radio_station_widget.exec_()

    @staticmethod
    def show_preferences_widget():
        """

        :return:
        """
        preferences_widget = PreferencesWidget()
        width, height = get_window_center_point(preferences_widget)
        preferences_widget.move(width, height)
        preferences_widget.exec_()

    @staticmethod
    def answer_help_action_triggered():
        """

        :return:
        """
        desktop_services = QDesktopServices()
        _app_info = get_app_info()
        desktop_services.openUrl(QUrl(_app_info["help_url"]))

    @staticmethod
    def answer_change_log_action_triggered():
        """

        :return:
        """
        desktop_services = QDesktopServices()
        _app_info = get_app_info()
        desktop_services.openUrl(QUrl(_app_info["change_log_url"]))

    @staticmethod
    def answer_check_version_action_triggered():
        """

        :return:
        """
        # TODO: 获取 GitHub API 进行检查并弹窗
        desktop_services = QDesktopServices()
        _app_info = get_app_info()
        desktop_services.openUrl(QUrl(_app_info["update"]))

    @staticmethod
    def answer_about_action_triggered():
        """

        :return:
        """
        about_widget = AboutWidget()
        width, height = get_window_center_point(about_widget)
        about_widget.move(width, height)
        about_widget.exec_()

    def answer_watch_live_signal(self, url):
        """

        :param url:
        :return:
        """
        self.live_widget.vlc_widget.play_url(url)
        self.live_widget.set_player_widget(True)

    def answer_listen_radio_station_signal(self, url):
        """

        :param url:
        :return:
        """
        self.live_widget.vlc_widget.play_url(url)
        self.live_widget.set_player_widget(True)

    def answer_close_action_triggered(self):
        """

        :return:
        """
        self.live_widget.set_player_widget(False)
        self.live_widget.vlc_widget.stop()

    def answer_hide_action_triggered(self, checked):
        """

        :param checked:
        :return:
        """
        if checked:
            self.tool_bar.hide()
            set_tool_bar_visible(0)
        else:
            self.tool_bar.show()
            set_tool_bar_visible(1)

    @staticmethod
    def answer_screenshot_action_triggered():
        """

        :return:
        """
        pass

    def answer_gif_action_triggered(self):
        """

        :return:
        """
        pass

    def answer_screen_record_action_triggered(self):
        """

        :return:
        """
        pass

    def closeEvent(self, event) -> None:
        """

        :param event:
        :return:
        """
        pass

    def answer_play_pause_btn_clicked(self):
        """

        :return:
        """
        if self.play_pause_btn.isChecked():
            self.pause()
        else:
            self.resume()

    def answer_refresh_btn_clicked(self):
        """

        :return:
        """
        self.play_url(self.current_url)

    def answer_rewind_btn_clicked(self):
        """

        :return:
        """
        pass

    def answer_stop_btn_clicked(self):
        """

        :return:
        """
        self.stop()

    def answer_fast_forward_btn_clicked(self):
        """

        :return:
        """
        pass

    def answer_fullscreen_narrow_btn_clicked(self):
        """

        :return:
        """
        pass

    def answer_volume_btn_clicked(self):
        """

        :return:
        """
        if self.volume_btn.isChecked():
            self.current_volume = self.get_volume()
            self.current_slider_value = self.volume_slider.value()
            self.set_volume(0)
            self.volume_slider.setValue(0)
        else:
            self.set_volume(self.current_volume)
            self.volume_slider.setValue(self.current_slider_value)

    def answer_volume_slider_value_changed(self):
        """

        :return:
        """
        # volume_value = self.volume_slider.value()
        # if 0 == volume_value:
        #     self.volume_btn.setChecked(True)
        # else:
        #     self.volume_btn.setChecked(False)
        # self.volume_slider_value_label.setText("{0}%".format(volume_value))
        # self.set_volume(volume_value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
