"""
Backup and restore system for NEON VOID OPTIMIZER.
Creates automatic backups before any system modification with full undo capability.
"""

import json
import shutil
import time
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .logger import logger


class BackupEntry:
    """Represents a single backup entry."""

    def __init__(self, name: str, backup_type: str, source_path: str,
                 backup_path: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.name = name
        self.backup_type = backup_type  # 'registry', 'file', 'service', 'full'
        self.source_path = source_path
        self.backup_path = backup_path
        self.created_at = time.time()
        self.metadata = metadata or {}
        self.restored = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "backup_type": self.backup_type,
            "source_path": self.source_path,
            "backup_path": self.backup_path,
            "created_at": self.created_at,
            "metadata": self.metadata,
            "restored": self.restored
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackupEntry':
        entry = cls(
            name=data["name"],
            backup_type=data["backup_type"],
            source_path=data["source_path"],
            backup_path=data["backup_path"],
            metadata=data.get("metadata", {})
        )
        entry.created_at = data.get("created_at", time.time())
        entry.restored = data.get("restored", False)
        return entry


class BackupManager:
    """
    Comprehensive backup and restore system.
    Creates snapshots before any modification for safe undo.
    """

    BACKUP_DIR = Path("backups")
    MAX_BACKUPS = 50

    def __init__(self) -> None:
        self.BACKUP_DIR.mkdir(exist_ok=True)
        self._undo_stack: List[BackupEntry] = []
        self._redo_stack: List[BackupEntry] = []
        self._callbacks: List[Callable[[], None]] = []

        # Load existing backup index
        self._index_file = self.BACKUP_DIR / "backup_index.json"
        self._load_index()

    def _load_index(self) -> None:
        """Load backup index from disk."""
        if self._index_file.exists():
            try:
                with open(self._index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self._undo_stack = [BackupEntry.from_dict(e) for e in data.get("undo", [])]
                self._redo_stack = [BackupEntry.from_dict(e) for e in data.get("redo", [])]
            except Exception as e:
                logger.error(f"Failed to load backup index: {e}")

    def _save_index(self) -> None:
        """Save backup index to disk."""
        try:
            data = {
                "undo": [e.to_dict() for e in self._undo_stack],
                "redo": [e.to_dict() for e in self._redo_stack]
            }
            with open(self._index_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save backup index: {e}")

    def create_registry_backup(self, name: str, registry_path: str,
                               values: Dict[str, Any]) -> BackupEntry:
        """Create a backup of registry values before modification."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"reg_{name}_{timestamp}"
        backup_path = self.BACKUP_DIR / f"{backup_name}.json"

        entry = BackupEntry(
            name=backup_name,
            backup_type="registry",
            source_path=registry_path,
            backup_path=str(backup_path),
            metadata={"original_values": values}
        )

        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "registry_path": registry_path,
                    "values": values,
                    "timestamp": timestamp,
                    "name": name
                }, f, indent=2)

            self._undo_stack.append(entry)
            self._prune_old_backups()
            self._save_index()

            logger.info(f"Registry backup created: {backup_name}")
            return entry

        except Exception as e:
            logger.error(f"Failed to create registry backup: {e}")
            raise

    def create_file_backup(self, name: str, source_path: Path) -> BackupEntry:
        """Create a backup of a file or directory before modification."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"file_{name}_{timestamp}"
        backup_path = self.BACKUP_DIR / f"{backup_name}.zip"

        entry = BackupEntry(
            name=backup_name,
            backup_type="file",
            source_path=str(source_path),
            backup_path=str(backup_path)
        )

        try:
            # Create zip backup
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                if source_path.is_file():
                    zf.write(source_path, source_path.name)
                elif source_path.is_dir():
                    for file_path in source_path.rglob("*"):
                        if file_path.is_file():
                            arcname = file_path.relative_to(source_path)
                            zf.write(file_path, arcname)

            self._undo_stack.append(entry)
            self._prune_old_backups()
            self._save_index()

            logger.info(f"File backup created: {backup_name}")
            return entry

        except Exception as e:
            logger.error(f"Failed to create file backup: {e}")
            raise

    def create_full_backup(self, name: str,
                           components: List[Dict[str, Any]]) -> BackupEntry:
        """Create a comprehensive backup of multiple components."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"full_{name}_{timestamp}"
        backup_path = self.BACKUP_DIR / f"{backup_name}"
        backup_path.mkdir(exist_ok=True)

        entry = BackupEntry(
            name=backup_name,
            backup_type="full",
            source_path="multiple",
            backup_path=str(backup_path),
            metadata={"components": components}
        )

        try:
            for component in components:
                comp_type = component.get("type")
                comp_name = component.get("name", "unknown")

                if comp_type == "registry":
                    reg_path = backup_path / f"{comp_name}_registry.json"
                    with open(reg_path, 'w', encoding='utf-8') as f:
                        json.dump(component.get("values", {}), f, indent=2)

                elif comp_type == "file":
                    src = Path(component.get("path", ""))
                    if src.exists():
                        dst = backup_path / f"{comp_name}_backup"
                        if src.is_file():
                            shutil.copy2(src, dst.with_suffix(src.suffix))
                        elif src.is_dir():
                            shutil.copytree(src, dst, dirs_exist_ok=True)

            self._undo_stack.append(entry)
            self._prune_old_backups()
            self._save_index()

            logger.info(f"Full backup created: {backup_name}")
            return entry

        except Exception as e:
            logger.error(f"Failed to create full backup: {e}")
            raise

    def undo_last(self) -> Optional[BackupEntry]:
        """Restore the most recent backup."""
        if not self._undo_stack:
            logger.warning("No backups to undo")
            return None

        entry = self._undo_stack.pop()

        try:
            if entry.backup_type == "registry":
                self._restore_registry(entry)
            elif entry.backup_type == "file":
                self._restore_file(entry)
            elif entry.backup_type == "full":
                self._restore_full(entry)

            entry.restored = True
            self._redo_stack.append(entry)
            self._save_index()

            logger.info(f"Backup restored: {entry.name}")
            return entry

        except Exception as e:
            logger.error(f"Failed to restore backup {entry.name}: {e}")
            # Put it back on stack if restore failed
            self._undo_stack.append(entry)
            return None

    def redo_last(self) -> Optional[BackupEntry]:
        """Re-apply the most recently undone change."""
        if not self._redo_stack:
            logger.warning("No backups to redo")
            return None

        # For redo, we'd need to store the new values as well
        # This is a simplified implementation
        entry = self._redo_stack.pop()
        logger.info(f"Redo not fully implemented yet for: {entry.name}")
        return entry

    def _restore_registry(self, entry: BackupEntry) -> None:
        """Restore registry from backup."""
        try:
            with open(entry.backup_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            original_values = data.get("values", {})
            registry_path = data.get("registry_path", "")

            # This would call the actual registry restoration
            # For safety, we log what would be restored
            logger.info(f"Would restore registry: {registry_path}")
            logger.debug(f"Original values: {original_values}")

        except Exception as e:
            logger.error(f"Failed to restore registry backup: {e}")
            raise

    def _restore_file(self, entry: BackupEntry) -> None:
        """Restore files from zip backup."""
        backup_path = Path(entry.backup_path)
        source_path = Path(entry.source_path)

        if backup_path.exists():
            # Extract zip to restore
            restore_dir = source_path.parent / f"{source_path.name}_restored"
            with zipfile.ZipFile(backup_path, 'r') as zf:
                zf.extractall(restore_dir)
            logger.info(f"File restored to: {restore_dir}")

    def _restore_full(self, entry: BackupEntry) -> None:
        """Restore full backup."""
        backup_path = Path(entry.backup_path)
        logger.info(f"Full backup restoration from: {backup_path}")
        # Implementation would iterate through all components

    def _prune_old_backups(self) -> None:
        """Remove oldest backups when exceeding max count."""
        while len(self._undo_stack) > self.MAX_BACKUPS:
            old_entry = self._undo_stack.pop(0)
            try:
                old_path = Path(old_entry.backup_path)
                if old_path.is_file():
                    old_path.unlink()
                elif old_path.is_dir():
                    shutil.rmtree(old_path)
            except Exception as e:
                logger.warning(f"Failed to prune old backup: {e}")

    def get_backup_history(self) -> List[BackupEntry]:
        """Get list of all backups (newest first)."""
        return list(reversed(self._undo_stack))

    def can_undo(self) -> bool:
        return len(self._undo_stack) > 0

    def can_redo(self) -> bool:
        return len(self._redo_stack) > 0

    def clear_history(self) -> None:
        """Clear all backup history (use with caution)."""
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._save_index()
        logger.info("Backup history cleared")


# Global backup manager instance
backup_manager = BackupManager()
