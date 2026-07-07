import os
import tempfile
import unittest
from unittest.mock import patch

import sync_from_confluence as sync_mod


class SyncFromConfluenceTests(unittest.TestCase):
    def test_sync_includes_parent_page_when_parent_has_no_descendants(self):
        root_page = {
            "id": "4575395844",
            "title": "DPA end-to-end 測試方法",
            "version": {"number": 5},
            "ancestors": [
                {"id": "1", "title": "Home"},
                {"id": "2", "title": "Commerce-AD"},
            ],
            "body": {"view": {"value": "<h1>DPA Spec</h1><p>content</p>"}},
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = os.path.join(tmpdir, "source_files")
            state_file = os.path.join(tmpdir, "confluence_state.json")

            with patch.object(sync_mod, "CONFLUENCE_URL", "https://example.atlassian.net/wiki"):
                with patch.object(sync_mod, "CONFLUENCE_EMAIL", "user@example.com"):
                    with patch.object(sync_mod, "CONFLUENCE_API_TOKEN", "token"):
                        with patch.object(sync_mod, "CONFLUENCE_PARENT_ID", "4575395844"):
                            with patch.object(sync_mod, "SOURCE_FILES_DIR", source_dir):
                                with patch.object(sync_mod, "STATE_FILE", state_file):
                                    with patch.object(sync_mod, "search_all_descendants", return_value=[]):
                                        with patch.object(sync_mod, "get_page_by_id", return_value=root_page, create=True):
                                            with patch.object(sync_mod, "get_attachments", return_value=[]):
                                                sync_mod.sync()

            expected_html = os.path.join(
                source_dir,
                "DPA end-to-end 測試方法",
                "DPA end-to-end 測試方法.html",
            )
            self.assertTrue(os.path.exists(expected_html))


if __name__ == "__main__":
    unittest.main()
