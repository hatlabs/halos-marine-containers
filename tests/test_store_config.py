"""Tests for marine store configuration."""

from pathlib import Path

import pytest
import yaml


def test_marine_yaml_is_valid():
    """Test that marine.yaml is syntactically valid YAML."""
    store_file = Path(__file__).parent.parent / "store" / "marine.yaml"

    with open(store_file) as f:
        data = yaml.safe_load(f)

    assert data is not None
    assert isinstance(data, dict)


def test_marine_yaml_has_required_fields():
    """Test that marine.yaml has all required fields."""
    store_file = Path(__file__).parent.parent / "store" / "marine.yaml"

    with open(store_file) as f:
        data = yaml.safe_load(f)

    # Required fields per cockpit-apt StoreConfig schema
    assert "id" in data
    assert "name" in data
    assert "description" in data
    assert "filters" in data

    # Validate ID
    assert data["id"] == "marine"

    # Validate filters structure
    assert isinstance(data["filters"], dict)

    # At least one filter type must be specified
    filters = data["filters"]
    has_filter = (
        (filters.get("include_tags") and len(filters["include_tags"]) > 0) or
        (filters.get("include_origins") and len(filters["include_origins"]) > 0) or
        (filters.get("include_sections") and len(filters["include_sections"]) > 0) or
        (filters.get("include_packages") and len(filters["include_packages"]) > 0)
    )
    assert has_filter, "At least one filter type must be specified"


def test_category_metadata_structure():
    """Test that category_metadata follows the correct structure."""
    store_file = Path(__file__).parent.parent / "store" / "marine.yaml"

    with open(store_file) as f:
        data = yaml.safe_load(f)

    # category_metadata is optional
    if "category_metadata" not in data:
        return

    metadata = data["category_metadata"]
    assert isinstance(metadata, list), "category_metadata must be a list"

    # Each entry must have id and label (required), icon and description (optional)
    for entry in metadata:
        assert "id" in entry, "Each category must have an 'id'"
        assert "label" in entry, "Each category must have a 'label'"

        # id and label must be non-empty strings
        assert isinstance(entry["id"], str) and len(entry["id"]) > 0
        assert isinstance(entry["label"], str) and len(entry["label"]) > 0

        # icon and description are optional, but if present must be strings
        if "icon" in entry and entry["icon"] is not None:
            assert isinstance(entry["icon"], str)

        if "description" in entry and entry["description"] is not None:
            assert isinstance(entry["description"], str)


def test_category_metadata_matches_app_tags():
    """Test that category metadata IDs match actual category tags used by apps."""
    store_file = Path(__file__).parent.parent / "store" / "marine.yaml"

    with open(store_file) as f:
        data = yaml.safe_load(f)

    if "category_metadata" not in data:
        pytest.skip("No category_metadata defined")

    # Get all category IDs from metadata
    metadata_ids = {entry["id"] for entry in data["category_metadata"]}

    # Expected categories based on tags added to marine apps
    # These should match the category:: tags in apps/*/metadata.yaml
    expected_categories = {
        "navigation",
        "chartplotters",
        "monitoring",
        "communication",
        "visualization",
    }

    # All expected categories should have metadata
    assert expected_categories == metadata_ids, \
        f"Category metadata IDs don't match expected categories.\n" \
        f"Expected: {expected_categories}\n" \
        f"Got: {metadata_ids}\n" \
        f"Missing: {expected_categories - metadata_ids}\n" \
        f"Extra: {metadata_ids - expected_categories}"


def test_no_section_metadata():
    """Test that old section_metadata field is not present."""
    store_file = Path(__file__).parent.parent / "store" / "marine.yaml"

    with open(store_file) as f:
        data = yaml.safe_load(f)

    assert "section_metadata" not in data, \
        "section_metadata is deprecated, use category_metadata instead"


def test_no_custom_sections():
    """Test that old custom_sections field is not present."""
    store_file = Path(__file__).parent.parent / "store" / "marine.yaml"

    with open(store_file) as f:
        data = yaml.safe_load(f)

    assert "custom_sections" not in data, \
        "custom_sections is deprecated, use category_metadata instead"
