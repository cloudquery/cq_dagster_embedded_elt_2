from dagster import asset, AssetExecutionContext, MaterializeResult
from dagster_duckdb import DuckDBResource

from .cloudquery.resource import CloudqueryResource
from .constants import CQ_MIGRATE_ONLY, CQ_HN_SPEC, DUCKDB_CONNECTION_STRING


@asset
def hacker_news_content(context: AssetExecutionContext, cloudquery: CloudqueryResource) -> None:
  if CQ_MIGRATE_ONLY == "true":
    cloudquery.migrate(context, spec_blob=CQ_HN_SPEC)
  else:
    cloudquery.sync(context, spec_blob=CQ_HN_SPEC)

@asset(deps=[hacker_news_content])
def top_stories(duckdb: DuckDBResource) -> MaterializeResult:
  with duckdb.get_connection() as conn:
    conn.execute("CREATE TABLE if not exists hn_stories AS SELECT * FROM hackernews_items")
