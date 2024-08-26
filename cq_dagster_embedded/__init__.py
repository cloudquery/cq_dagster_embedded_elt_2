from dagster import (
  Definitions, load_assets_from_modules, define_asset_job, AssetSelection,
  FilesystemIOManager
)

from dagster_duckdb import DuckDBResource

from .cloudquery.resource import CloudqueryResource

from . import assets
from .constants import DUCKDB_CONNECTION_STRING

all_assets = load_assets_from_modules([assets])

hackernews_job = define_asset_job(
  "hackernews_job",
  selection=AssetSelection.all())

io_manager = FilesystemIOManager(
    base_dir="data",  # Path is built relative to where `dagster dev` is run
)

resources = {
  "duckdb": DuckDBResource(
      database=DUCKDB_CONNECTION_STRING,
  ),
  "cloudquery": CloudqueryResource(),
}

defs = Definitions(
    assets=all_assets,
    jobs=[hackernews_job],  # Addition: add the job to Definitions object (see below)
    resources=resources,
)
