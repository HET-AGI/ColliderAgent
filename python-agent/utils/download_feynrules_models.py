"""
FeynRules Model Downloader

Downloads .fr model files from the official FeynRules model database.
Organizes files by category and generates metadata.

Usage:
    python download_feynrules_models.py [--output-dir DIR] [--categories CATS]
"""

import os
import json
import time
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FeynRules base URL
BASE_URL = "https://cp3.irmp.ucl.ac.be/projects/feynrules"

# Model categories
CATEGORIES = {
    "simple_extensions": "SimpleExtensions",
    "susy_models": "SusyModels",
    "extra_dim": "ExtraDimModels",
    "effective": "EffectiveModels",
    "standard_model": "StandardModel",
    "miscellaneous": "MiscellaneousModels",
    "nlo": "NLOModels"
}


class FeynRulesDownloader:
    """Downloads .fr model files from FeynRules database."""

    def __init__(self, output_dir: str = "database/reference_models", max_retries: int = 3):
        """
        Initialize downloader.

        Args:
            output_dir: Directory to save downloaded files (default: database/reference_models)
            max_retries: Maximum number of download retry attempts
        """
        self.output_dir = Path(output_dir)
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FeynRules-Model-Downloader/1.0'
        })
        self.metadata = {
            "download_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "base_url": BASE_URL,
            "categories": {},
            "total_models": 0,
            "successful_downloads": 0,
            "failed_downloads": 0
        }
        self.model_index = []  # For database/index.json

    def download_all_categories(self, categories: Optional[List[str]] = None):
        """
        Download models from all specified categories.

        Args:
            categories: List of category keys to download (None = all)
        """
        if categories is None:
            categories = list(CATEGORIES.keys())

        logger.info(f"Starting download from {len(categories)} categories")

        for category_key in categories:
            if category_key not in CATEGORIES:
                logger.warning(f"Unknown category: {category_key}, skipping")
                continue

            category_name = CATEGORIES[category_key]
            logger.info(f"Processing category: {category_name}")

            try:
                self._download_category(category_key, category_name)
            except Exception as e:
                logger.error(f"Error processing category {category_name}: {e}")

        # Save metadata
        self._save_metadata()
        logger.info(f"Download complete! {self.metadata['successful_downloads']}/{self.metadata['total_models']} models downloaded")

    def _download_category(self, category_key: str, category_name: str):
        """Download all models from a specific category."""
        # Create category directory
        category_dir = self.output_dir / category_key
        category_dir.mkdir(parents=True, exist_ok=True)

        # Get list of models in category
        category_url = f"{BASE_URL}/wiki/{category_name}"
        models = self._scrape_model_list(category_url)

        logger.info(f"Found {len(models)} models in {category_name}")
        self.metadata["categories"][category_key] = {
            "name": category_name,
            "url": category_url,
            "models": {}
        }

        # Download each model
        for model_name in tqdm(models, desc=f"{category_name}", unit="model"):
            try:
                model_info = self._download_model(model_name, category_dir)
                self.metadata["categories"][category_key]["models"][model_name] = model_info
                self.metadata["successful_downloads"] += 1
            except Exception as e:
                logger.error(f"Failed to download {model_name}: {e}")
                self.metadata["categories"][category_key]["models"][model_name] = {
                    "status": "failed",
                    "error": str(e)
                }
                self.metadata["failed_downloads"] += 1

            # Be polite - small delay between requests
            time.sleep(0.5)

    def _scrape_model_list(self, category_url: str) -> List[str]:
        """
        Scrape list of model names from a category page.

        Args:
            category_url: URL of the category page

        Returns:
            List of model names (wiki page identifiers)
        """
        try:
            response = self.session.get(category_url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch category page {category_url}: {e}")
            return []

        soup = BeautifulSoup(response.content, 'lxml')

        # Find all links that point to model pages
        # Pattern: /projects/feynrules/wiki/ModelName
        models = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/wiki/' in href and href.startswith('/projects/feynrules/wiki/'):
                # Extract model name from URL
                model_name = href.split('/wiki/')[-1]
                # Skip category pages and main pages
                if model_name and model_name not in CATEGORIES.values():
                    if model_name not in ['ModelDatabaseMainPage', 'WikiStart', 'FeynRulesManual']:
                        models.append(model_name)

        # Remove duplicates
        models = list(set(models))
        return models

    def _download_model(self, model_name: str, category_dir: Path) -> Dict:
        """
        Download .fr file(s) for a specific model.

        Args:
            model_name: Name of the model (wiki page identifier)
            category_dir: Directory to save the model file

        Returns:
            Dictionary with model download information
        """
        self.metadata["total_models"] += 1

        model_url = f"{BASE_URL}/wiki/{model_name}"

        # Get model page
        try:
            response = self.session.get(model_url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch model page: {e}")

        soup = BeautifulSoup(response.content, 'lxml')

        # Find .fr file download links
        fr_files = self._find_fr_files(soup, model_name)

        if not fr_files:
            raise RuntimeError("No .fr files found on model page")

        # Download first/primary .fr file
        primary_fr = fr_files[0]
        download_url = f"{BASE_URL}/raw-attachment/wiki/{model_name}/{primary_fr}"
        save_path = category_dir / primary_fr

        # Download with retries
        for attempt in range(self.max_retries):
            try:
                logger.debug(f"Downloading {primary_fr} (attempt {attempt + 1}/{self.max_retries})")
                file_response = self.session.get(download_url, timeout=30)
                file_response.raise_for_status()

                # Save file
                with open(save_path, 'wb') as f:
                    f.write(file_response.content)

                file_size = len(file_response.content)
                logger.info(f"Downloaded {primary_fr} ({file_size} bytes)")

                # Create metadata for the model
                model_metadata = self._create_model_metadata(model_name, primary_fr, save_path)

                # Add to model index for database/index.json
                self.model_index.append({
                    "name": model_name,
                    "path": str(save_path.relative_to(self.output_dir.parent)),
                    "keywords": model_metadata.get("keywords", []),
                    "particles": model_metadata.get("particles", []),
                    "sectors": model_metadata.get("sectors", []),
                    "operators": model_metadata.get("operators", [])
                })

                return {
                    "status": "success",
                    "model_url": model_url,
                    "fr_file": primary_fr,
                    "download_url": download_url,
                    "file_size": file_size,
                    "save_path": str(save_path),
                    "all_fr_files": fr_files,
                    "metadata": model_metadata
                }

            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(f"Download failed after {self.max_retries} attempts: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff

    def _find_fr_files(self, soup: BeautifulSoup, model_name: str) -> List[str]:
        """
        Find .fr file names in a model page.

        Args:
            soup: BeautifulSoup object of the model page
            model_name: Name of the model

        Returns:
            List of .fr filenames
        """
        fr_files = []

        # Look for attachment links
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Pattern: /attachment/wiki/ModelName/file.fr or /raw-attachment/...
            if '.fr' in href.lower() and model_name in href:
                # Extract filename
                filename = href.split('/')[-1]
                if filename.endswith('.fr'):
                    fr_files.append(filename)

        # Also check for direct text mentions of .fr files
        for text in soup.stripped_strings:
            if '.fr' in text.lower():
                # Simple pattern matching
                words = text.split()
                for word in words:
                    if word.endswith('.fr'):
                        fr_files.append(word)

        # Remove duplicates and sort
        fr_files = sorted(list(set(fr_files)))
        return fr_files

    def _save_metadata(self):
        """Save download metadata to JSON file."""
        metadata_path = self.output_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        logger.info(f"Metadata saved to {metadata_path}")

        # Also save model index for database/index.json
        self._save_model_index()

    def _save_model_index(self):
        """Save model index to database/index.json for semantic search."""
        index_path = self.output_dir.parent / "index.json"

        # Load existing index if it exists
        if index_path.exists():
            with open(index_path, 'r') as f:
                index_data = json.load(f)
        else:
            index_data = {
                "version": "1.0",
                "description": "Search index for FeynRules reference models",
                "models": []
            }

        # Add/update model entries
        index_data["models"] = self.model_index

        with open(index_path, 'w') as f:
            json.dump(index_data, f, indent=2)

        logger.info(f"Model index saved to {index_path}")

    def _create_model_metadata(self, model_name: str, fr_file: str, save_path: Path) -> Dict:
        """
        Create metadata JSON file for a model by analyzing the .fr file.

        Args:
            model_name: Name of the model
            fr_file: Name of the .fr file
            save_path: Path where .fr file was saved

        Returns:
            Metadata dictionary
        """
        metadata = {
            "model_name": model_name,
            "fr_file": fr_file,
            "keywords": [],
            "particles": [],
            "sectors": [],
            "operators": []
        }

        try:
            with open(save_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Extract particles (simplified pattern matching)
            if 'lepton' in content.lower() or 'l[' in content or 'vl[' in content:
                metadata["sectors"].append("lepton")
                metadata["particles"].extend(["l", "vl", "lbar"])

            if 'quark' in content.lower() or 'uq[' in content or 'dq[' in content:
                metadata["sectors"].append("quark")
                metadata["particles"].extend(["uq", "dq", "uqbar", "dqbar"])

            if 'gauge' in content.lower() or 'W[' in content or 'Z[' in content or 'G[' in content:
                metadata["sectors"].append("gauge")
                metadata["particles"].extend(["W", "Z", "A", "G"])

            if 'higgs' in content.lower() or 'H[' in content:
                metadata["sectors"].append("Higgs")
                metadata["particles"].append("H")

            # Extract keywords from model name
            name_lower = model_name.lower()
            if 'sm' in name_lower or 'standard' in name_lower:
                metadata["keywords"].append("standard model")
            if 'mssm' in name_lower or 'susy' in name_lower:
                metadata["keywords"].extend(["MSSM", "supersymmetry"])
            if '2hdm' in name_lower:
                metadata["keywords"].append("two Higgs doublet")
            if 'zprime' in name_lower or "z'" in name_lower:
                metadata["keywords"].append("Z'")

            # Extract common operators
            if 'ProjM' in content or 'ProjP' in content:
                metadata["operators"].extend(["ProjM", "ProjP"])
            if 'Ga[' in content:
                metadata["operators"].append("Ga")
            if 'DC[' in content:
                metadata["operators"].append("DC")

            # Remove duplicates
            metadata["sectors"] = list(set(metadata["sectors"]))
            metadata["particles"] = list(set(metadata["particles"]))
            metadata["operators"] = list(set(metadata["operators"]))
            metadata["keywords"] = list(set(metadata["keywords"]))

        except Exception as e:
            logger.warning(f"Failed to extract metadata from {fr_file}: {e}")

        # Save metadata JSON alongside .fr file
        metadata_path = save_path.with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        logger.debug(f"Created metadata file: {metadata_path}")

        return metadata

    def _categorize_model(self, category_key: str, model_name: str) -> str:
        """
        Determine which subdirectory to place the model in.

        Args:
            category_key: Original category key
            model_name: Name of the model

        Returns:
            Subdirectory name (standard_model, beyond_sm, or effective)
        """
        name_lower = model_name.lower()

        # Standard Model
        if 'sm' == name_lower or 'standardmodel' in name_lower.replace('_', ''):
            return "standard_model"

        # Effective field theory
        if 'eft' in name_lower or 'effective' in name_lower or category_key == "effective":
            return "effective"

        # Everything else is beyond SM
        return "beyond_sm"


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Download FeynRules model files from official database"
    )
    parser.add_argument(
        '--output-dir',
        default='database/reference_models',
        help='Output directory for downloaded files (default: database/reference_models)'
    )
    parser.add_argument(
        '--categories',
        nargs='+',
        choices=list(CATEGORIES.keys()) + ['all'],
        default=['all'],
        help='Categories to download (default: all)'
    )
    parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='Maximum download retry attempts (default: 3)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Determine which categories to download
    categories = None if 'all' in args.categories else args.categories

    # Create downloader and start
    downloader = FeynRulesDownloader(
        output_dir=args.output_dir,
        max_retries=args.max_retries
    )

    downloader.download_all_categories(categories)


if __name__ == "__main__":
    main()
