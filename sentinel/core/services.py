from google.cloud import bigquery
import os
from typing import List, Dict, Any, Optional
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
import logging

Base = declarative_base()

class CompanyEntity(Base):
    __tablename__ = 'companies'
    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    ticker = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sector = sqlalchemy.Column(sqlalchemy.String)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now())

class EventStore:
    def __init__(self, dataset_id: str = "sentinel_events"):
        try:
            self.client = bigquery.Client()
            self.dataset_id = dataset_id
            self._ensure_dataset()
            self.demo_mode = False
        except Exception as e:
            logging.warning(f"BigQuery initialization failed: {e}. Running in demo mode.")
            self.demo_mode = True

    def _ensure_dataset(self):
        if self.demo_mode: return
        dataset_ref = self.client.dataset(self.dataset_id)
        try:
            self.client.get_dataset(dataset_ref)
        except Exception:
            try:
                self.client.create_dataset(bigquery.Dataset(dataset_ref))
            except Exception as e:
                logging.error(f"Could not create dataset: {e}")
                self.demo_mode = True

    def write_signals(self, table_name: str, signals: List[Dict[str, Any]]):
        if self.demo_mode:
            logging.info(f"[DEMO] Would write {len(signals)} signals to {table_name}")
            return
        table_ref = self.client.dataset(self.dataset_id).table(table_name)
        errors = self.client.insert_rows_json(table_ref, signals)
        if errors:
            logging.error(f"Errors writing to BigQuery: {errors}")

class CompanyRegistry:
    def __init__(self, db_url: Optional[str] = None):
        self.db_url = db_url or os.getenv("DATABASE_URL", "sqlite:///./sentinel.db")
        try:
            self.engine = sqlalchemy.create_engine(self.db_url)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            self.demo_mode = False
        except Exception as e:
            logging.warning(f"DB initialization failed: {e}. Using in-memory sqlite.")
            self.engine = sqlalchemy.create_engine("sqlite:///:memory:")
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)


    def register_company(self, company_id: str, name: str, sector: str, ticker: Optional[str] = None):
        with self.Session() as session:
            company = CompanyEntity(id=company_id, name=name, sector=sector, ticker=ticker)
            session.merge(company)
            session.commit()

    def get_company(self, company_id: str) -> Optional[Dict[str, Any]]:
        with self.Session() as session:
            company = session.query(CompanyEntity).filter_by(id=company_id).first()
            if company:
                return {"id": company.id, "name": company.name, "sector": company.sector, "ticker": company.ticker}
            return None
