#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clean, 3-view PySide6 GUI for browsing, inspecting, and syncing Skill-Agents."""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

from PySide6.QtCore import QObject, QSize, QThread, QUrl, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QDesktopServices, QFont, QGuiApplication
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextBrowser,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

try:
    import sync_skills as core
except ImportError:
    _SCRIPTS_DIR = str(Path(__file__).resolve().parent)
    if _SCRIPTS_DIR not in sys.path:
        sys.path.insert(0, _SCRIPTS_DIR)
    import sync_skills as core


LIGHT_TOKENS = {
    "bg": "#F8FAFC",
    "surface": "#FFFFFF",
    "surface_alt": "#F1F5F9",
    "text": "#0F172A",
    "muted": "#475569",
    "border": "#CBD5E1",
    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",
    "primary_text": "#FFFFFF",
    "badge_found_bg": "#DBEAFE",
    "badge_found_fg": "#1E40AF",
    "badge_new_bg": "#E2E8F0",
    "badge_new_fg": "#475569",
    "success_bg": "#DCFCE7",
    "success_fg": "#166534",
    "warn_bg": "#FEF3C7",
    "warn_fg": "#92400E",
    "error_bg": "#FEE2E2",
    "error_fg": "#991B1B",
    "code_bg": "#F1F5F9",
    "focus": "#2563EB",
}

DARK_TOKENS = {
    "bg": "#0F172A",
    "surface": "#1E293B",
    "surface_alt": "#263348",
    "text": "#F8FAFC",
    "muted": "#CBD5E1",
    "border": "#334155",
    "primary": "#2563EB",
    "primary_hover": "#3B82F6",
    "primary_text": "#FFFFFF",
    "badge_found_bg": "#1E3A8A",
    "badge_found_fg": "#DBEAFE",
    "badge_new_bg": "#334155",
    "badge_new_fg": "#CBD5E1",
    "success_bg": "#14532D",
    "success_fg": "#DCFCE7",
    "warn_bg": "#78350F",
    "warn_fg": "#FEF3C7",
    "error_bg": "#7F1D1D",
    "error_fg": "#FEE2E2",
    "code_bg": "#0F172A",
    "focus": "#60A5FA",
}

TEXT_PREVIEW_EXTS = {
    ".md", ".txt", ".py", ".ps1", ".sh", ".bat", ".json", ".yaml", ".yml", ".toml", ".csv",
}


def build_stylesheet(tokens: dict[str, str]) -> str:
    return f"""
    QMainWindow, QWidget#RootWidget {{
        background-color: {tokens["bg"]};
        color: {tokens["text"]};
        font-family: "Segoe UI", "Noto Sans Thai", sans-serif;
        font-size: 13px;
    }}
    QFrame#Panel {{
        background-color: {tokens["surface"]};
        border: 1px solid {tokens["border"]};
        border-radius: 10px;
    }}
    QFrame#NavStrip {{
        background-color: {tokens["surface_alt"]};
        border: 1px solid {tokens["border"]};
        border-radius: 9px;
        padding: 2px;
    }}
    QLabel#TitleLabel {{
        font-size: 18px;
        font-weight: 700;
        color: {tokens["text"]};
    }}
    QLabel#SectionTitle {{
        font-size: 14px;
        font-weight: 700;
        color: {tokens["text"]};
    }}
    QLabel#DetailTitle {{
        font-size: 17px;
        font-weight: 700;
        color: {tokens["text"]};
    }}
    QLabel#MutedLabel {{
        font-size: 12px;
        color: {tokens["muted"]};
    }}
    QLabel#MonoHint {{
        font-family: "Consolas", "Cascadia Mono", monospace;
        font-size: 11px;
        color: {tokens["muted"]};
    }}
    QLabel#BadgeFound, QLabel#BadgeSuccess, QLabel#BadgeNew, QLabel#BadgeWarn {{
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 11px;
        font-weight: 600;
    }}
    QLabel#BadgeFound {{
        background-color: {tokens["badge_found_bg"]};
        color: {tokens["badge_found_fg"]};
    }}
    QLabel#BadgeSuccess {{
        background-color: {tokens["success_bg"]};
        color: {tokens["success_fg"]};
    }}
    QLabel#BadgeWarn {{
        background-color: {tokens["warn_bg"]};
        color: {tokens["warn_fg"]};
    }}
    QLabel#BadgeNew {{
        background-color: {tokens["badge_new_bg"]};
        color: {tokens["badge_new_fg"]};
    }}
    QFrame#BannerSuccess {{
        background-color: {tokens["success_bg"]};
        border: 1px solid {tokens["success_fg"]};
        border-radius: 8px;
    }}
    QFrame#BannerError {{
        background-color: {tokens["error_bg"]};
        border: 1px solid {tokens["error_fg"]};
        border-radius: 8px;
    }}
    QLabel#BannerSuccessText {{
        color: {tokens["success_fg"]};
        font-weight: 600;
    }}
    QLabel#BannerErrorText {{
        color: {tokens["error_fg"]};
        font-weight: 600;
    }}
    QLineEdit, QComboBox, QPlainTextEdit, QTextBrowser {{
        background-color: {tokens["surface"]};
        color: {tokens["text"]};
        border: 1px solid {tokens["border"]};
        border-radius: 7px;
        padding: 6px 10px;
    }}
    QLineEdit:focus, QComboBox:focus, QPlainTextEdit:focus,
    QListWidget:focus, QTreeWidget:focus, QTableWidget:focus {{
        border: 2px solid {tokens["focus"]};
    }}
    QListWidget, QTreeWidget, QTableWidget {{
        background-color: {tokens["surface"]};
        color: {tokens["text"]};
        border: 1px solid {tokens["border"]};
        border-radius: 8px;
        outline: none;
        gridline-color: {tokens["border"]};
    }}
    QListWidget::item {{
        border-bottom: 1px solid {tokens["surface_alt"]};
    }}
    QTreeWidget::item {{
        padding: 6px 4px;
        border-radius: 5px;
    }}
    QTreeWidget::item:selected, QTableWidget::item:selected {{
        background-color: {tokens["badge_found_bg"]};
        color: {tokens["badge_found_fg"]};
    }}
    QHeaderView::section {{
        background-color: {tokens["surface_alt"]};
        color: {tokens["text"]};
        border: none;
        border-bottom: 1px solid {tokens["border"]};
        border-right: 1px solid {tokens["border"]};
        padding: 6px 8px;
        font-weight: 700;
        font-size: 12px;
    }}
    QTabWidget::pane {{
        border: 1px solid {tokens["border"]};
        border-radius: 8px;
        background-color: {tokens["surface"]};
    }}
    QTabBar::tab {{
        background-color: {tokens["surface_alt"]};
        color: {tokens["muted"]};
        border: 1px solid {tokens["border"]};
        border-bottom: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 6px 14px;
        margin-right: 4px;
        font-weight: 600;
    }}
    QTabBar::tab:selected {{
        background-color: {tokens["surface"]};
        color: {tokens["text"]};
    }}
    QPushButton {{
        background-color: {tokens["surface"]};
        color: {tokens["text"]};
        border: 1px solid {tokens["border"]};
        border-radius: 7px;
        padding: 6px 12px;
        min-height: 22px;
        font-weight: 600;
    }}
    QPushButton:hover {{
        background-color: {tokens["surface_alt"]};
    }}
    QPushButton:focus {{
        border: 2px solid {tokens["focus"]};
    }}
    QPushButton:disabled {{
        opacity: 0.55;
    }}
    QPushButton#NavTab {{
        background-color: transparent;
        border: none;
        border-radius: 7px;
        padding: 7px 14px;
        color: {tokens["muted"]};
        font-weight: 600;
    }}
    QPushButton#NavTab:hover {{
        color: {tokens["text"]};
        background-color: {tokens["surface"]};
    }}
    QPushButton#NavTab:checked {{
        background-color: {tokens["surface"]};
        color: {tokens["primary"]};
        border: 1px solid {tokens["border"]};
        font-weight: 700;
    }}
    QPushButton#LinkBtn {{
        background-color: transparent;
        border: 1px solid {tokens["border"]};
        padding: 3px 9px;
        min-height: 18px;
        font-size: 11px;
        color: {tokens["primary"]};
    }}
    QPushButton#LinkBtn:hover {{
        background-color: {tokens["badge_found_bg"]};
    }}
    QPushButton#PrimaryBtn {{
        background-color: {tokens["primary"]};
        color: {tokens["primary_text"]};
        border: none;
        padding: 9px 18px;
        min-height: 24px;
        font-size: 13px;
        font-weight: 700;
    }}
    QPushButton#PrimaryBtn:hover {{
        background-color: {tokens["primary_hover"]};
    }}
    QPushButton#PrimaryBtn:disabled {{
        background-color: {tokens["border"]};
        color: {tokens["muted"]};
    }}
    QCheckBox, QRadioButton {{
        spacing: 8px;
        color: {tokens["text"]};
    }}
    QScrollArea, QWidget#TransparentBox {{
        border: none;
        background: transparent;
    }}
    QProgressBar {{
        border: 1px solid {tokens["border"]};
        border-radius: 5px;
        background-color: {tokens["surface_alt"]};
        height: 8px;
    }}
    QProgressBar::chunk {{
        background-color: {tokens["primary"]};
        border-radius: 4px;
    }}
    """


def build_markdown_css(tokens: dict[str, str]) -> str:
    return f"""
    body {{
        font-family: "Segoe UI", "Noto Sans Thai", sans-serif;
        font-size: 13px;
        line-height: 1.55;
        color: {tokens["text"]};
    }}
    h1 {{ font-size: 18px; font-weight: 700; margin: 4px 0 10px 0; color: {tokens["text"]}; }}
    h2 {{ font-size: 15px; font-weight: 700; margin: 14px 0 6px 0; color: {tokens["text"]}; }}
    h3 {{ font-size: 13px; font-weight: 700; margin: 10px 0 4px 0; color: {tokens["muted"]}; }}
    p {{ margin: 4px 0 8px 0; }}
    code {{
        font-family: "Consolas", "Cascadia Mono", monospace;
        background-color: {tokens["code_bg"]};
        padding: 1px 4px;
        border-radius: 4px;
        font-size: 12px;
    }}
    pre {{
        font-family: "Consolas", "Cascadia Mono", monospace;
        background-color: {tokens["code_bg"]};
        border: 1px solid {tokens["border"]};
        padding: 10px;
        border-radius: 6px;
        font-size: 12px;
    }}
    table {{ border-collapse: collapse; margin: 8px 0; }}
    th, td {{ border: 1px solid {tokens["border"]}; padding: 5px 8px; }}
    th {{ background-color: {tokens["surface_alt"]}; font-weight: 700; }}
    blockquote {{
        border-left: 3px solid {tokens["primary"]};
        margin: 8px 0;
        padding-left: 10px;
        color: {tokens["muted"]};
    }}
    a {{ color: {tokens["primary"]}; }}
    """


def _elide_text(text: str, max_chars: int = 86) -> str:
    clean = " ".join(text.split())
    if len(clean) <= max_chars:
        return clean
    return clean[: max_chars - 1].rstrip() + "…"


class FetchWorker(QObject):
    finished = Signal(object, str)
    log_line = Signal(str)

    def __init__(self, temp_dir: Path) -> None:
        super().__init__()
        self._temp_dir = temp_dir

    def run(self) -> None:
        try:
            root = core.fetch_repo_from_github(dest_dir=self._temp_dir, log_cb=self.log_line.emit)
            self.finished.emit(root, "")
        except Exception as exc:
            self.finished.emit(None, str(exc))


class SyncWorker(QObject):
    finished = Signal(object)
    log_line = Signal(str)

    def __init__(
        self,
        source_root: Path,
        skill_names: list[str],
        provider_keys: list[str],
        mode: str,
        dry_run: bool,
    ) -> None:
        super().__init__()
        self._source_root = source_root
        self._skill_names = skill_names
        self._provider_keys = provider_keys
        self._mode = mode
        self._dry_run = dry_run

    def run(self) -> None:
        res = core.run_sync_pipeline(
            self._source_root,
            self._skill_names,
            self._provider_keys,
            mode=self._mode,
            dry_run=self._dry_run,
            log_cb=self.log_line.emit,
        )
        self.finished.emit(res)


class SkillCardRow(QWidget):
    """Compact 2-line skill row showing selection, sub-skill count, install status, and quick inspect."""

    toggled = Signal(str, bool)
    inspect_requested = Signal(str)

    def __init__(
        self,
        info: core.SkillInfo,
        checked: bool,
        status_text: str,
        status_obj_name: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._skill_name = info.name

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        top = QHBoxLayout()
        top.setSpacing(8)

        self.checkbox = QCheckBox(info.name)
        font = self.checkbox.font()
        font.setBold(True)
        self.checkbox.setFont(font)
        self.checkbox.setChecked(checked)
        self.checkbox.toggled.connect(lambda state: self.toggled.emit(self._skill_name, state))
        top.addWidget(self.checkbox)

        if info.subskills:
            sub_chip = QLabel(f"{len(info.subskills)} sub-skills")
            sub_chip.setObjectName("BadgeNew")
            top.addWidget(sub_chip)

        top.addStretch()

        status_pill = QLabel(status_text)
        status_pill.setObjectName(status_obj_name)
        top.addWidget(status_pill)

        read_btn = QPushButton("อ่านคู่มือ")
        read_btn.setObjectName("LinkBtn")
        read_btn.setToolTip(f"เปิดดูรายละเอียดของ {info.name} ในแท็บ คลัง Skills")
        read_btn.clicked.connect(lambda: self.inspect_requested.emit(self._skill_name))
        top.addWidget(read_btn)

        desc = QLabel(_elide_text(info.description))
        desc.setObjectName("MutedLabel")
        desc.setToolTip(info.description)
        desc.setContentsMargins(24, 0, 0, 0)

        layout.addLayout(top)
        layout.addWidget(desc)


class SkillSyncWindow(QMainWindow):
    """3-view Skill-Agents desktop installer, documentation explorer, and status matrix."""

    def __init__(self, force_github: bool = False) -> None:
        super().__init__()
        self.setWindowTitle("Skill-Agents Sync")
        self.resize(1080, 740)
        self.setMinimumSize(900, 640)

        self._local_repo = core.find_local_repo_root()
        self._source_root: Path | None = None
        self._skills: list[core.SkillInfo] = []
        self._skills_by_name: dict[str, core.SkillInfo] = {}
        self._checked_skills: set[str] = set()
        self._installed_matrix: dict[str, dict[str, bool]] = {}
        self._last_records: list[core.SyncRecord] = []
        self._temp_dir: Path | None = None
        self._active_thread: QThread | None = None
        self._active_worker: QObject | None = None
        self._last_touched_dir: Path | None = None
        self._current_detail_folder: Path | None = None
        self._busy = False

        scheme = QGuiApplication.styleHints().colorScheme()
        self._dark_mode = scheme == Qt.ColorScheme.Dark

        self._provider_checks: dict[str, QCheckBox] = {}
        self._provider_count_labels: dict[str, QLabel] = {}
        self._provider_badges: dict[str, QLabel] = {}

        self._build_ui(force_github=force_github)
        self._apply_theme()
        self._load_initial_source(force_github=force_github)

    # ------------------------------------------------------------------ UI setup
    def _build_ui(self, force_github: bool) -> None:
        root = QWidget(self)
        root.setObjectName("RootWidget")
        self.setCentralWidget(root)

        outer = QVBoxLayout(root)
        outer.setContentsMargins(16, 12, 16, 12)
        outer.setSpacing(10)

        # Top header
        header = QHBoxLayout()
        header.setSpacing(12)

        title_lbl = QLabel("Skill-Agents Sync")
        title_lbl.setObjectName("TitleLabel")
        header.addWidget(title_lbl)

        # Segmented navigation
        nav_frame = QFrame()
        nav_frame.setObjectName("NavStrip")
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setContentsMargins(3, 3, 3, 3)
        nav_layout.setSpacing(4)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        self.nav_sync_btn = QPushButton("1. ติดตั้ง && ซิงค์")
        self.nav_explore_btn = QPushButton("2. คลัง Skills && คู่มือ")
        self.nav_status_btn = QPushButton("3. สถานะ && ผลลัพธ์")
        for idx, btn in enumerate((self.nav_sync_btn, self.nav_explore_btn, self.nav_status_btn)):
            btn.setObjectName("NavTab")
            btn.setCheckable(True)
            self.nav_group.addButton(btn, idx)
            nav_layout.addWidget(btn)
        self.nav_sync_btn.setChecked(True)
        self.nav_group.idClicked.connect(self._switch_page)
        header.addWidget(nav_frame)

        header.addStretch()

        src_lbl = QLabel("แหล่งข้อมูล:")
        src_lbl.setObjectName("MutedLabel")
        header.addWidget(src_lbl)

        self.source_combo = QComboBox()
        if self._local_repo is not None:
            self.source_combo.addItem("โฟลเดอร์ในเครื่อง (Local)", "local")
        self.source_combo.addItem(f"GitHub ล่าสุด ({core.DEFAULT_GITHUB_REPO})", "github")
        if force_github or self._local_repo is None:
            idx = self.source_combo.findData("github")
            if idx >= 0:
                self.source_combo.setCurrentIndex(idx)
        self.source_combo.currentIndexChanged.connect(self._on_source_changed)
        header.addWidget(self.source_combo)

        self.refresh_btn = QPushButton("รีเฟรช")
        self.refresh_btn.clicked.connect(self._reload_current_source)
        header.addWidget(self.refresh_btn)

        self.theme_btn = QPushButton("สลับธีม")
        self.theme_btn.clicked.connect(self._toggle_theme)
        header.addWidget(self.theme_btn)

        outer.addLayout(header)

        # Stacked main views
        self.pages = QStackedWidget()
        self.pages.addWidget(self._build_sync_view())
        self.pages.addWidget(self._build_explorer_view())
        self.pages.addWidget(self._build_status_view())
        outer.addWidget(self.pages, 1)

        # Banner
        self.banner_frame = QFrame()
        self.banner_frame.setObjectName("BannerSuccess")
        banner_layout = QHBoxLayout(self.banner_frame)
        banner_layout.setContentsMargins(12, 7, 12, 7)
        banner_layout.setSpacing(10)

        self.banner_text = QLabel("")
        self.banner_text.setObjectName("BannerSuccessText")
        banner_layout.addWidget(self.banner_text, 1)

        self.banner_results_btn = QPushButton("ดูตารางผลลัพธ์")
        self.banner_results_btn.clicked.connect(lambda: self._switch_page(2))
        self.banner_results_btn.hide()
        banner_layout.addWidget(self.banner_results_btn)

        self.banner_frame.hide()
        outer.addWidget(self.banner_frame)

        # Persistent bottom action bar
        footer = QHBoxLayout()
        footer.setSpacing(10)

        status_col = QVBoxLayout()
        status_col.setSpacing(4)
        self.status_lbl = QLabel("พร้อมใช้งาน")
        self.status_lbl.setObjectName("MutedLabel")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFixedWidth(220)
        self.progress_bar.hide()
        status_col.addWidget(self.status_lbl)
        status_col.addWidget(self.progress_bar)
        footer.addLayout(status_col, 1)

        self.open_folder_btn = QPushButton("เปิดโฟลเดอร์ปลายทาง")
        self.open_folder_btn.clicked.connect(self._open_last_folder)
        self.open_folder_btn.hide()
        footer.addWidget(self.open_folder_btn)

        self.dry_run_btn = QPushButton("จำลองผล (Dry Run)")
        self.dry_run_btn.clicked.connect(lambda: self._start_sync(dry_run=True))
        footer.addWidget(self.dry_run_btn)

        self.sync_btn = QPushButton("ติดตั้ง")
        self.sync_btn.setObjectName("PrimaryBtn")
        self.sync_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.sync_btn.clicked.connect(lambda: self._start_sync(dry_run=False))
        footer.addWidget(self.sync_btn)

        outer.addLayout(footer)
        self._update_summary()

    def _build_sync_view(self) -> QWidget:
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # Left: Skills cards
        left_panel = QFrame()
        left_panel.setObjectName("Panel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(14, 14, 14, 14)
        left_layout.setSpacing(10)

        skills_hdr = QHBoxLayout()
        skills_title = QLabel("1. เลือก Skills ที่ต้องการติดตั้ง")
        skills_title.setObjectName("SectionTitle")
        self.skill_count_lbl = QLabel("เลือกอยู่ 0 รายการ")
        self.skill_count_lbl.setObjectName("MutedLabel")
        skills_hdr.addWidget(skills_title)
        skills_hdr.addStretch()
        skills_hdr.addWidget(self.skill_count_lbl)
        left_layout.addLayout(skills_hdr)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ค้นหาชื่อ skill, คำอธิบาย หรือ sub-skill...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self._render_skill_list)
        left_layout.addWidget(self.search_input)

        tools = QHBoxLayout()
        tools.setSpacing(8)
        self.select_all_skills_btn = QPushButton("เลือกทั้งหมด")
        self.select_all_skills_btn.clicked.connect(self._select_all_skills)
        self.clear_skills_btn = QPushButton("ล้างทั้งหมด")
        self.clear_skills_btn.clicked.connect(self._clear_all_skills)
        tools.addWidget(self.select_all_skills_btn)
        tools.addWidget(self.clear_skills_btn)
        tools.addStretch()
        left_layout.addLayout(tools)

        self.skill_list = QListWidget()
        self.skill_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.skill_list.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        left_layout.addWidget(self.skill_list, 1)

        self.empty_search_lbl = QLabel("ไม่พบ Skill ที่ตรงกับคำค้นหา")
        self.empty_search_lbl.setObjectName("MutedLabel")
        self.empty_search_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_search_lbl.hide()
        left_layout.addWidget(self.empty_search_lbl)

        # Right: Providers & Mode
        right_panel = QFrame()
        right_panel.setObjectName("Panel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(14, 14, 14, 14)
        right_layout.setSpacing(10)

        prov_hdr = QHBoxLayout()
        prov_title = QLabel("2. เลือกแอป AI ปลายทาง")
        prov_title.setObjectName("SectionTitle")
        self.prov_count_lbl = QLabel("เลือกอยู่ 0 แอป")
        self.prov_count_lbl.setObjectName("MutedLabel")
        prov_hdr.addWidget(prov_title)
        prov_hdr.addStretch()
        prov_hdr.addWidget(self.prov_count_lbl)
        right_layout.addLayout(prov_hdr)

        prov_tools = QHBoxLayout()
        prov_tools.setSpacing(8)
        self.select_detected_btn = QPushButton("เฉพาะแอปที่มีในเครื่อง")
        self.select_detected_btn.clicked.connect(self._select_detected_providers)
        self.select_all_prov_btn = QPushButton("เลือกทุกแอป")
        self.select_all_prov_btn.clicked.connect(self._select_all_providers)
        self.clear_prov_btn = QPushButton("ล้าง")
        self.clear_prov_btn.clicked.connect(self._clear_all_providers)
        prov_tools.addWidget(self.select_detected_btn)
        prov_tools.addWidget(self.select_all_prov_btn)
        prov_tools.addWidget(self.clear_prov_btn)
        prov_tools.addStretch()
        right_layout.addLayout(prov_tools)

        prov_scroll = QScrollArea()
        prov_scroll.setWidgetResizable(True)
        prov_scroll.viewport().setObjectName("TransparentBox")
        prov_container = QWidget()
        prov_container.setObjectName("TransparentBox")
        prov_list_layout = QVBoxLayout(prov_container)
        prov_list_layout.setContentsMargins(0, 2, 0, 2)
        prov_list_layout.setSpacing(8)

        detected = core.detect_providers()
        any_detected = any(detected.values())
        for spec in core.PROVIDERS:
            row_box = QWidget()
            row_v = QVBoxLayout(row_box)
            row_v.setContentsMargins(4, 4, 4, 4)
            row_v.setSpacing(2)

            top_r = QHBoxLayout()
            top_r.setSpacing(8)

            cb = QCheckBox(spec.name)
            cb_font = cb.font()
            cb_font.setBold(True)
            cb.setFont(cb_font)
            is_found = detected.get(spec.key, False)
            if is_found or (not any_detected and spec.key == "1"):
                cb.setChecked(True)
            cb.stateChanged.connect(self._on_provider_selection_changed)

            count_lbl = QLabel("มีแล้ว 0")
            count_lbl.setObjectName("BadgeNew")

            badge = QLabel("พบบนเครื่อง" if is_found else "จะสร้างใหม่")
            badge.setObjectName("BadgeFound" if is_found else "BadgeNew")

            top_r.addWidget(cb)
            top_r.addStretch()
            top_r.addWidget(count_lbl)
            top_r.addWidget(badge)

            path_hint = QLabel("/".join(["~", *spec.skills_rel]))
            path_hint.setObjectName("MonoHint")
            path_hint.setContentsMargins(24, 0, 0, 0)

            row_v.addLayout(top_r)
            row_v.addWidget(path_hint)

            self._provider_checks[spec.key] = cb
            self._provider_count_labels[spec.key] = count_lbl
            self._provider_badges[spec.key] = badge
            prov_list_layout.addWidget(row_box)

        prov_list_layout.addStretch()
        prov_scroll.setWidget(prov_container)
        right_layout.addWidget(prov_scroll, 1)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        right_layout.addWidget(divider)

        mode_title = QLabel("รูปแบบการติดตั้ง")
        mode_title.setObjectName("SectionTitle")
        right_layout.addWidget(mode_title)

        self.mode_group = QButtonGroup(self)
        self.mode_skills_radio = QRadioButton("เฉพาะ Skills (แนะนำ — ปลอดภัย ไม่ทับ Rules/Agents เดิม)")
        self.mode_skills_radio.setChecked(True)
        self.mode_full_radio = QRadioButton("Full Setup (รวม Antigravity Agents, Global Rules และ dist)")
        self.mode_group.addButton(self.mode_skills_radio)
        self.mode_group.addButton(self.mode_full_radio)
        right_layout.addWidget(self.mode_skills_radio)
        right_layout.addWidget(self.mode_full_radio)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([560, 480])
        return splitter

    def _build_explorer_view(self) -> QWidget:
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # Left tree
        tree_panel = QFrame()
        tree_panel.setObjectName("Panel")
        tree_layout = QVBoxLayout(tree_panel)
        tree_layout.setContentsMargins(12, 12, 12, 12)
        tree_layout.setSpacing(8)

        tree_title = QLabel("โครงสร้าง Skills & Sub-skills")
        tree_title.setObjectName("SectionTitle")
        tree_layout.addWidget(tree_title)

        self.explorer_search = QLineEdit()
        self.explorer_search.setPlaceholderText("กรองชื่อ skill หรือ sub-skill...")
        self.explorer_search.setClearButtonEnabled(True)
        self.explorer_search.textChanged.connect(self._render_explorer_tree)
        tree_layout.addWidget(self.explorer_search)

        self.explorer_tree = QTreeWidget()
        self.explorer_tree.setHeaderHidden(True)
        self.explorer_tree.setAnimated(True)
        self.explorer_tree.currentItemChanged.connect(self._on_explorer_item_selected)
        tree_layout.addWidget(self.explorer_tree, 1)

        # Right reader
        detail_panel = QFrame()
        detail_panel.setObjectName("Panel")
        detail_layout = QVBoxLayout(detail_panel)
        detail_layout.setContentsMargins(16, 14, 16, 14)
        detail_layout.setSpacing(10)

        hdr_row = QHBoxLayout()
        hdr_row.setSpacing(10)
        self.detail_title_lbl = QLabel("เลือก Skill ทางซ้ายเพื่ออ่านรายละเอียด")
        self.detail_title_lbl.setObjectName("DetailTitle")
        hdr_row.addWidget(self.detail_title_lbl, 1)

        self.detail_toggle_sync_btn = QPushButton("เลือกสำหรับซิงค์")
        self.detail_toggle_sync_btn.clicked.connect(self._toggle_current_detail_sync)
        self.detail_toggle_sync_btn.hide()
        hdr_row.addWidget(self.detail_toggle_sync_btn)
        detail_layout.addLayout(hdr_row)

        self.detail_desc_lbl = QLabel("")
        self.detail_desc_lbl.setObjectName("MutedLabel")
        self.detail_desc_lbl.setWordWrap(True)
        detail_layout.addWidget(self.detail_desc_lbl)

        self.detail_chips_layout = QHBoxLayout()
        self.detail_chips_layout.setSpacing(6)
        self.detail_chips_layout.addStretch()
        detail_layout.addLayout(self.detail_chips_layout)

        self.detail_tabs = QTabWidget()

        # Tab 1: Formatted Markdown
        self.markdown_browser = QTextBrowser()
        self.markdown_browser.setOpenExternalLinks(True)
        self.markdown_browser.document().setDocumentMargin(14)
        self.detail_tabs.addTab(self.markdown_browser, "คู่มือ (SKILL.md)")

        # Tab 2: Supporting files
        files_tab = QSplitter(Qt.Orientation.Horizontal)
        files_tab.setChildrenCollapsible(False)
        self.files_list = QListWidget()
        self.files_list.currentItemChanged.connect(self._on_file_selected)
        self.file_preview = QPlainTextEdit()
        self.file_preview.setReadOnly(True)
        mono = QFont("Consolas", 10)
        mono.setStyleHint(QFont.StyleHint.Monospace)
        self.file_preview.setFont(mono)
        self.file_preview.setPlaceholderText("คลิกเลือกไฟล์ทางซ้ายเพื่อดูเนื้อหา")
        files_tab.addWidget(self.files_list)
        files_tab.addWidget(self.file_preview)
        files_tab.setSizes([240, 420])
        self.detail_tabs.addTab(files_tab, "ไฟล์ประกอบ")

        detail_layout.addWidget(self.detail_tabs, 1)

        splitter.addWidget(tree_panel)
        splitter.addWidget(detail_panel)
        splitter.setSizes([310, 730])
        return splitter

    def _build_status_view(self) -> QWidget:
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setChildrenCollapsible(False)

        # Top: Installed Matrix
        matrix_panel = QFrame()
        matrix_panel.setObjectName("Panel")
        matrix_layout = QVBoxLayout(matrix_panel)
        matrix_layout.setContentsMargins(14, 12, 14, 12)
        matrix_layout.setSpacing(8)

        mat_hdr = QHBoxLayout()
        mat_title = QLabel("สถานะการติดตั้งในเครื่อง (Installed Matrix)")
        mat_title.setObjectName("SectionTitle")
        mat_hint = QLabel("ดับเบิลคลิกช่องที่ 'ติดตั้งแล้ว' เพื่อเปิดโฟลเดอร์")
        mat_hint.setObjectName("MutedLabel")
        self.refresh_matrix_btn = QPushButton("รีเฟรชสถานะ")
        self.refresh_matrix_btn.clicked.connect(self._refresh_installed_state)
        mat_hdr.addWidget(mat_title)
        mat_hdr.addSpacing(8)
        mat_hdr.addWidget(mat_hint)
        mat_hdr.addStretch()
        mat_hdr.addWidget(self.refresh_matrix_btn)
        matrix_layout.addLayout(mat_hdr)

        self.matrix_table = QTableWidget()
        self.matrix_table.setColumnCount(1 + len(core.PROVIDERS))
        self.matrix_table.setHorizontalHeaderLabels(
            ["Skill", *(p.short_name for p in core.PROVIDERS)]
        )
        self.matrix_table.verticalHeader().setVisible(False)
        self.matrix_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.matrix_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.matrix_table.setAlternatingRowColors(True)
        self.matrix_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in range(1, 1 + len(core.PROVIDERS)):
            self.matrix_table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        self.matrix_table.cellDoubleClicked.connect(self._on_matrix_double_clicked)
        matrix_layout.addWidget(self.matrix_table, 1)

        # Bottom: Structured Sync / Dry Run Results + collapsible Raw Log
        results_panel = QFrame()
        results_panel.setObjectName("Panel")
        results_layout = QVBoxLayout(results_panel)
        results_layout.setContentsMargins(14, 12, 14, 12)
        results_layout.setSpacing(8)

        res_hdr = QHBoxLayout()
        self.results_title_lbl = QLabel("ผลลัพธ์ Sync / Dry Run ล่าสุด (ยังไม่มีการรัน)")
        self.results_title_lbl.setObjectName("SectionTitle")
        self.raw_log_toggle = QPushButton("▸ ดู Raw Log")
        self.raw_log_toggle.setCheckable(True)
        self.raw_log_toggle.toggled.connect(self._toggle_raw_log)
        res_hdr.addWidget(self.results_title_lbl)
        res_hdr.addStretch()
        res_hdr.addWidget(self.raw_log_toggle)
        results_layout.addLayout(res_hdr)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["รายการ", "แอป AI", "สถานะ", "ปลายทาง / หมายเหตุ"])
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.results_table.setAlternatingRowColors(True)
        hdr = self.results_table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        results_layout.addWidget(self.results_table, 1)

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMaximumHeight(130)
        mono = QFont("Consolas", 10)
        mono.setStyleHint(QFont.StyleHint.Monospace)
        self.log_box.setFont(mono)
        self.log_box.hide()
        results_layout.addWidget(self.log_box)

        splitter.addWidget(matrix_panel)
        splitter.addWidget(results_panel)
        splitter.setSizes([330, 290])
        return splitter

    # ------------------------------------------------------------------ Theme & Navigation
    def _tokens(self) -> dict[str, str]:
        return DARK_TOKENS if self._dark_mode else LIGHT_TOKENS

    def _apply_theme(self) -> None:
        tokens = self._tokens()
        self.setStyleSheet(build_stylesheet(tokens))
        self.theme_btn.setText("ธีม: มืด" if self._dark_mode else "ธีม: สว่าง")
        self.markdown_browser.document().setDefaultStyleSheet(build_markdown_css(tokens))
        self._render_matrix_table()
        self._render_results_table()

    def _toggle_theme(self) -> None:
        self._dark_mode = not self._dark_mode
        self._apply_theme()

    def _switch_page(self, index: int) -> None:
        self.pages.setCurrentIndex(index)
        btn = self.nav_group.button(index)
        if btn is not None:
            btn.setChecked(True)

    def _toggle_raw_log(self, checked: bool) -> None:
        self.raw_log_toggle.setText("▾ ซ่อน Raw Log" if checked else "▸ ดู Raw Log")
        self.log_box.setVisible(checked)

    # ------------------------------------------------------------------ Source loading
    def _load_initial_source(self, force_github: bool) -> None:
        if not force_github and self._local_repo is not None:
            self._apply_loaded_source(self._local_repo)
        else:
            self._fetch_from_github()

    def _on_source_changed(self) -> None:
        self._reload_current_source()

    def _reload_current_source(self) -> None:
        if self._busy:
            return
        mode = self.source_combo.currentData()
        if mode == "local" and self._local_repo is not None:
            self._apply_loaded_source(self._local_repo)
        else:
            self._fetch_from_github()

    def _set_busy(self, busy: bool, status_text: str) -> None:
        self._busy = busy
        self.status_lbl.setText(status_text)
        self.progress_bar.setVisible(busy)
        self.source_combo.setEnabled(not busy)
        self.refresh_btn.setEnabled(not busy)
        self._update_summary()

    def _fetch_from_github(self) -> None:
        self._cleanup_temp()
        self._temp_dir = Path(tempfile.mkdtemp(prefix="skill-agents-gui-"))
        self._set_busy(True, "กำลังโหลด Skills ล่าสุดจาก GitHub...")
        self.banner_frame.hide()

        thread = QThread(self)
        worker = FetchWorker(self._temp_dir)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.log_line.connect(self._append_log)
        worker.finished.connect(self._on_fetch_finished)
        worker.finished.connect(thread.quit)
        thread.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        self._active_thread = thread
        self._active_worker = worker
        thread.start()

    def _on_fetch_finished(self, root: object, err: str) -> None:
        self._active_thread = None
        self._active_worker = None
        if err or not isinstance(root, Path):
            self._set_busy(False, "โหลดจาก GitHub ไม่สำเร็จ")
            self._show_banner(
                f"{err} (ตรวจสอบอินเทอร์เน็ต หรือสลับไปใช้ไฟล์ในเครื่อง)",
                is_error=True,
                show_results_btn=False,
            )
            self.raw_log_toggle.setChecked(True)
            return
        self._apply_loaded_source(root)

    def _apply_loaded_source(self, source_root: Path) -> None:
        self._source_root = source_root
        self._skills = core.discover_skills(source_root)
        self._skills_by_name = {s.name: s for s in self._skills}
        self._checked_skills = {s.name for s in self._skills}
        self._refresh_installed_state()
        self._render_explorer_tree()
        if self.explorer_tree.topLevelItemCount() > 0:
            self.explorer_tree.setCurrentItem(self.explorer_tree.topLevelItem(0))
        self._set_busy(False, f"พร้อมใช้งาน (โหลดแล้ว {len(self._skills)} Skills)")

    def _refresh_installed_state(self) -> None:
        names = [s.name for s in self._skills]
        self._installed_matrix = core.inspect_installed_skills(names)
        detected = core.detect_providers()
        for spec in core.PROVIDERS:
            is_found = detected.get(spec.key, False)
            badge = self._provider_badges[spec.key]
            badge.setText("พบบนเครื่อง" if is_found else "จะสร้างใหม่")
            badge.setObjectName("BadgeFound" if is_found else "BadgeNew")
            badge.style().unpolish(badge)
            badge.style().polish(badge)

            installed_count = sum(
                1 for skill_name in names if self._installed_matrix.get(skill_name, {}).get(spec.key)
            )
            self._provider_count_labels[spec.key].setText(f"มีแล้ว {installed_count}/{len(names)}")

        self._render_skill_list()
        self._render_matrix_table()
        # Refresh current explorer chips if open
        cur = self.explorer_tree.currentItem()
        if cur is not None:
            self._on_explorer_item_selected(cur, None)

    # ------------------------------------------------------------------ View 1: Sync Cards
    def _skill_install_status(self, skill_name: str, selected_providers: list[str]) -> tuple[str, str]:
        row_map = self._installed_matrix.get(skill_name, {})
        targets = selected_providers or [p.key for p in core.PROVIDERS]
        installed_n = sum(1 for k in targets if row_map.get(k, False))
        if installed_n == 0:
            return "ใหม่", "BadgeNew"
        if installed_n == len(targets):
            return "ครบแล้ว", "BadgeSuccess"
        return f"มีแล้ว {installed_n}/{len(targets)}", "BadgeWarn"

    def _render_skill_list(self) -> None:
        query = self.search_input.text().strip().lower()
        selected_provs = self._selected_provider_keys()
        self.skill_list.clear()

        matched = 0
        for info in self._skills:
            haystack = f"{info.name} {info.description} {' '.join(info.subskills)}".lower()
            if query and query not in haystack:
                continue
            matched += 1
            status_text, status_obj = self._skill_install_status(info.name, selected_provs)
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, info.name)
            item.setSizeHint(QSize(0, 64))

            widget = SkillCardRow(
                info=info,
                checked=(info.name in self._checked_skills),
                status_text=status_text,
                status_obj_name=status_obj,
            )
            widget.toggled.connect(self._on_skill_card_toggled)
            widget.inspect_requested.connect(self._jump_to_explorer)

            self.skill_list.addItem(item)
            self.skill_list.setItemWidget(item, widget)

        self.skill_list.setVisible(matched > 0)
        self.empty_search_lbl.setVisible(matched == 0 and len(self._skills) > 0)
        self._update_summary()

    def _on_skill_card_toggled(self, skill_name: str, checked: bool) -> None:
        if checked:
            self._checked_skills.add(skill_name)
        else:
            self._checked_skills.discard(skill_name)
        self._update_summary()

    def _on_provider_selection_changed(self) -> None:
        self._render_skill_list()

    def _select_all_skills(self) -> None:
        for i in range(self.skill_list.count()):
            name = self.skill_list.item(i).data(Qt.ItemDataRole.UserRole)
            if name:
                self._checked_skills.add(name)
        self._render_skill_list()

    def _clear_all_skills(self) -> None:
        for i in range(self.skill_list.count()):
            name = self.skill_list.item(i).data(Qt.ItemDataRole.UserRole)
            if name:
                self._checked_skills.discard(name)
        self._render_skill_list()

    def _select_detected_providers(self) -> None:
        detected = core.detect_providers()
        any_found = any(detected.values())
        for key, cb in self._provider_checks.items():
            cb.blockSignals(True)
            cb.setChecked(detected.get(key, False) or (not any_found and key == "1"))
            cb.blockSignals(False)
        self._render_skill_list()

    def _select_all_providers(self) -> None:
        for cb in self._provider_checks.values():
            cb.blockSignals(True)
            cb.setChecked(True)
            cb.blockSignals(False)
        self._render_skill_list()

    def _clear_all_providers(self) -> None:
        for cb in self._provider_checks.values():
            cb.blockSignals(True)
            cb.setChecked(False)
            cb.blockSignals(False)
        self._render_skill_list()

    def _selected_provider_keys(self) -> list[str]:
        return [key for key, cb in self._provider_checks.items() if cb.isChecked()]

    def _update_summary(self) -> None:
        n_skills = len(self._checked_skills)
        total_skills = len(self._skills)
        n_provs = len(self._selected_provider_keys())

        self.skill_count_lbl.setText(f"เลือกอยู่ {n_skills} / {total_skills} รายการ")
        self.prov_count_lbl.setText(f"เลือกอยู่ {n_provs} แอป")

        can_run = (not self._busy) and self._source_root is not None and n_skills > 0 and n_provs > 0
        self.sync_btn.setEnabled(can_run)
        self.dry_run_btn.setEnabled(can_run)
        self.sync_btn.setText(f"ติดตั้ง {n_skills} Skills ไปยัง {n_provs} แอป")

    # ------------------------------------------------------------------ View 2: Explorer
    def _jump_to_explorer(self, skill_name: str) -> None:
        self._switch_page(1)
        for i in range(self.explorer_tree.topLevelItemCount()):
            top = self.explorer_tree.topLevelItem(i)
            if top.data(0, Qt.ItemDataRole.UserRole) == (skill_name, None):
                self.explorer_tree.setCurrentItem(top)
                top.setExpanded(True)
                break

    def _render_explorer_tree(self) -> None:
        query = self.explorer_search.text().strip().lower()
        self.explorer_tree.clear()

        for info in self._skills:
            matching_subs = [
                sub
                for sub in info.subskill_details
                if not query or query in f"{sub.name} {sub.description}".lower()
            ]
            top_matches = not query or query in f"{info.name} {info.description}".lower()
            if not top_matches and not matching_subs:
                continue

            label = f"{info.name} ({len(info.subskill_details)})" if info.subskill_details else info.name
            top_item = QTreeWidgetItem([label])
            top_item.setData(0, Qt.ItemDataRole.UserRole, (info.name, None))
            top_font = top_item.font(0)
            top_font.setBold(True)
            top_item.setFont(0, top_font)

            subs_to_add = info.subskill_details if top_matches else matching_subs
            for sub in subs_to_add:
                child = QTreeWidgetItem([sub.name])
                child.setData(0, Qt.ItemDataRole.UserRole, (info.name, sub.name))
                top_item.addChild(child)

            self.explorer_tree.addTopLevelItem(top_item)
            if query and matching_subs:
                top_item.setExpanded(True)

    def _clear_detail_chips(self) -> None:
        while self.detail_chips_layout.count() > 1:
            item = self.detail_chips_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _add_detail_chip(self, text: str, obj_name: str) -> None:
        lbl = QLabel(text)
        lbl.setObjectName(obj_name)
        self.detail_chips_layout.insertWidget(self.detail_chips_layout.count() - 1, lbl)

    def _on_explorer_item_selected(
        self, current: QTreeWidgetItem | None, _prev: QTreeWidgetItem | None
    ) -> None:
        if current is None:
            return
        payload = current.data(0, Qt.ItemDataRole.UserRole)
        if not payload:
            return
        skill_name, sub_name = payload
        info = self._skills_by_name.get(skill_name)
        if info is None:
            return

        self._clear_detail_chips()
        if sub_name is None:
            self.detail_title_lbl.setText(info.name)
            self.detail_desc_lbl.setText(info.description)
            self._current_detail_folder = info.path
            files = info.files
            md_body = info.markdown_body
            if info.subskills:
                self._add_detail_chip(f"{len(info.subskills)} sub-skills", "BadgeFound")
            self._add_detail_chip(f"{len(files)} ไฟล์", "BadgeNew")
            installed_apps = [
                core.PROVIDERS_BY_KEY[k].short_name
                for k, ok in self._installed_matrix.get(info.name, {}).items()
                if ok
            ]
            if installed_apps:
                self._add_detail_chip(f"ติดตั้งใน: {', '.join(installed_apps)}", "BadgeSuccess")
            else:
                self._add_detail_chip("ยังไม่ติดตั้งในเครื่อง", "BadgeNew")
            self.detail_toggle_sync_btn.show()
            self._sync_detail_toggle_label(info.name)
        else:
            sub_info = next((s for s in info.subskill_details if s.name == sub_name), None)
            if sub_info is None:
                return
            self.detail_title_lbl.setText(f"{info.name} / {sub_info.name}")
            self.detail_desc_lbl.setText(sub_info.description)
            self._current_detail_folder = sub_info.path
            files = sub_info.files
            md_body = sub_info.markdown_body
            self._add_detail_chip(f"หมวดหมู่: {info.name}", "BadgeFound")
            self._add_detail_chip(f"{len(files)} ไฟล์", "BadgeNew")
            self.detail_toggle_sync_btn.hide()

        self.markdown_browser.document().setMarkdown(md_body)
        self.files_list.clear()
        for rel in files:
            self.files_list.addItem(rel)
        self.detail_tabs.setTabText(1, f"ไฟล์ประกอบ ({len(files)} ไฟล์)")
        self.file_preview.clear()
        if self.files_list.count() > 0:
            self.files_list.setCurrentRow(0)

    def _sync_detail_toggle_label(self, skill_name: str) -> None:
        if skill_name in self._checked_skills:
            self.detail_toggle_sync_btn.setText("เลือกไว้แล้ว (คลิกเพื่อเอาออก)")
        else:
            self.detail_toggle_sync_btn.setText("เลือกสำหรับซิงค์")

    def _toggle_current_detail_sync(self) -> None:
        cur = self.explorer_tree.currentItem()
        if cur is None:
            return
        payload = cur.data(0, Qt.ItemDataRole.UserRole)
        if not payload or payload[1] is not None:
            return
        skill_name = payload[0]
        if skill_name in self._checked_skills:
            self._checked_skills.discard(skill_name)
        else:
            self._checked_skills.add(skill_name)
        self._sync_detail_toggle_label(skill_name)
        self._render_skill_list()

    def _on_file_selected(self, current: QListWidgetItem | None, _prev: QListWidgetItem | None) -> None:
        if current is None or self._current_detail_folder is None:
            return
        target = self._current_detail_folder / current.text()
        if not target.is_file():
            self.file_preview.setPlainText("(ไม่พบไฟล์)")
            return
        if target.suffix.lower() not in TEXT_PREVIEW_EXTS:
            self.file_preview.setPlainText(f"(ไฟล์ไบนารี: {target.name})")
            return
        text = target.read_text(encoding="utf-8", errors="replace")
        if len(text) > 65536:
            text = text[:65536] + "\n\n... (ตัดทอนเนื่องจากไฟล์มีขนาดใหญ่)"
        self.file_preview.setPlainText(text)

    # ------------------------------------------------------------------ View 3: Matrix & Results
    def _render_matrix_table(self) -> None:
        tokens = self._tokens()
        skills = self._skills
        self.matrix_table.setRowCount(len(skills))

        ok_bg = QBrush(QColor(tokens["success_bg"]))
        ok_fg = QBrush(QColor(tokens["success_fg"]))
        muted_fg = QBrush(QColor(tokens["muted"]))

        for r, info in enumerate(skills):
            name_item = QTableWidgetItem(info.name)
            f = name_item.font()
            f.setBold(True)
            name_item.setFont(f)
            self.matrix_table.setItem(r, 0, name_item)

            row_map = self._installed_matrix.get(info.name, {})
            for c, spec in enumerate(core.PROVIDERS, start=1):
                installed = row_map.get(spec.key, False)
                cell = QTableWidgetItem("ติดตั้งแล้ว" if installed else "—")
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if installed:
                    cell.setBackground(ok_bg)
                    cell.setForeground(ok_fg)
                    cell.setData(
                        Qt.ItemDataRole.UserRole,
                        str(spec.skills_dir() / info.name),
                    )
                    cell.setToolTip(f"ดับเบิลคลิกเพื่อเปิด {spec.skills_dir() / info.name}")
                else:
                    cell.setForeground(muted_fg)
                self.matrix_table.setItem(r, c, cell)

    def _on_matrix_double_clicked(self, row: int, col: int) -> None:
        if col <= 0:
            return
        item = self.matrix_table.item(row, col)
        if item is None:
            return
        path_str = item.data(Qt.ItemDataRole.UserRole)
        if path_str and Path(path_str).exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(path_str))

    def _render_results_table(self) -> None:
        tokens = self._tokens()
        records = self._last_records
        self.results_table.setRowCount(len(records))

        action_styles = {
            "installed": ("ติดตั้งใหม่", tokens["success_bg"], tokens["success_fg"]),
            "updated": ("อัปเดตแล้ว", tokens["badge_found_bg"], tokens["badge_found_fg"]),
            "dry-run": ("จำลองผล", tokens["warn_bg"], tokens["warn_fg"]),
            "skipped": ("ข้าม", tokens["badge_new_bg"], tokens["badge_new_fg"]),
            "failed": ("ล้มเหลว", tokens["error_bg"], tokens["error_fg"]),
        }

        for r, rec in enumerate(records):
            self.results_table.setItem(r, 0, QTableWidgetItem(rec.item))
            self.results_table.setItem(r, 1, QTableWidgetItem(rec.provider))

            label_text, bg_hex, fg_hex = action_styles.get(
                rec.action, (rec.action, tokens["badge_new_bg"], tokens["badge_new_fg"])
            )
            action_item = QTableWidgetItem(label_text)
            action_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            action_item.setBackground(QBrush(QColor(bg_hex)))
            action_item.setForeground(QBrush(QColor(fg_hex)))
            self.results_table.setItem(r, 2, action_item)

            detail = rec.dest_path if not rec.message else f"{rec.dest_path}  ({rec.message})"
            self.results_table.setItem(r, 3, QTableWidgetItem(detail))

    # ------------------------------------------------------------------ Sync Execution
    def _append_log(self, line: str) -> None:
        self.log_box.appendPlainText(line)

    def _show_banner(self, text: str, *, is_error: bool, show_results_btn: bool) -> None:
        self.banner_text.setText(text)
        self.banner_frame.setObjectName("BannerError" if is_error else "BannerSuccess")
        self.banner_text.setObjectName("BannerErrorText" if is_error else "BannerSuccessText")
        for w in (self.banner_frame, self.banner_text):
            w.style().unpolish(w)
            w.style().polish(w)
        self.banner_results_btn.setVisible(show_results_btn)
        self.banner_frame.show()

    def _start_sync(self, *, dry_run: bool) -> None:
        if self._busy or self._source_root is None:
            return
        selected_skills = [s.name for s in self._skills if s.name in self._checked_skills]
        selected_providers = self._selected_provider_keys()
        if not selected_skills or not selected_providers:
            return

        mode = "full" if self.mode_full_radio.isChecked() else "skills"
        if mode == "full" and not dry_run:
            reply = QMessageBox.question(
                self,
                "ยืนยันการติดตั้งแบบ Full Setup",
                "โหมด Full Setup จะเขียนทับไฟล์ Custom Agents และ Global Rules เดิมใน ~/.gemini/config/\n"
                "ต้องการดำเนินการต่อหรือไม่?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        self.log_box.clear()
        self.banner_frame.hide()
        self.open_folder_btn.hide()
        self._set_busy(True, "กำลังจำลองผลลัพธ์..." if dry_run else "กำลังติดตั้ง Skills...")

        thread = QThread(self)
        worker = SyncWorker(self._source_root, selected_skills, selected_providers, mode, dry_run)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.log_line.connect(self._append_log)
        worker.finished.connect(lambda res: self._on_sync_finished(res, dry_run))
        worker.finished.connect(thread.quit)
        thread.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        self._active_thread = thread
        self._active_worker = worker
        thread.start()

    def _on_sync_finished(self, res: object, dry_run: bool) -> None:
        self._active_thread = None
        self._active_worker = None
        if not isinstance(res, core.SyncResult):
            self._set_busy(False, "เกิดข้อผิดพลาดระหว่างการทำงาน")
            return

        self._last_records = list(res.records)
        self._render_results_table()
        kind = "จำลองผล (Dry Run)" if dry_run else "ติดตั้ง"
        self.results_title_lbl.setText(f"ผลลัพธ์ {kind} ล่าสุด ({len(res.records)} รายการ)")

        if not dry_run:
            self._refresh_installed_state()

        if res.failed:
            self._set_busy(False, f"เสร็จสิ้นแบบมีข้อผิดพลาด ({len(res.failed)} รายการ)")
            self._show_banner(
                f"สำเร็จ {len(res.synced)} รายการ แต่ล้มเหลว {len(res.failed)} รายการ",
                is_error=True,
                show_results_btn=True,
            )
            self.raw_log_toggle.setChecked(True)
            self._switch_page(2)
        else:
            prefix = "จำลองผลสำเร็จ" if dry_run else "ติดตั้งเรียบร้อย"
            self._set_busy(False, f"{prefix} ({len(res.synced)} รายการ)")
            self._show_banner(
                f"{prefix}: ดำเนินการทั้งหมด {len(res.synced)} รายการเรียบร้อยแล้ว",
                is_error=False,
                show_results_btn=(not dry_run),
            )
            if dry_run:
                self._switch_page(2)

        if not dry_run and res.touched_dirs:
            self._last_touched_dir = res.touched_dirs[0]
            self.open_folder_btn.show()

    def _open_last_folder(self) -> None:
        if self._last_touched_dir and self._last_touched_dir.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self._last_touched_dir)))

    def _cleanup_temp(self) -> None:
        if self._temp_dir and self._temp_dir.exists():
            shutil.rmtree(self._temp_dir, ignore_errors=True)
        self._temp_dir = None

    def closeEvent(self, event) -> None:  # type: ignore[override]
        if self._active_thread and self._active_thread.isRunning():
            self._active_thread.quit()
            self._active_thread.wait(2000)
        self._cleanup_temp()
        super().closeEvent(event)


def run_gui(force_github: bool = False) -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    window = SkillSyncWindow(force_github=force_github)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run_gui("--from-github" in sys.argv))
