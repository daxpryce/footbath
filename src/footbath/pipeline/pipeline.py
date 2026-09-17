import polars as pl
from zeep import AsyncClient, Settings
from zeep.cache import SqliteCache
from zeep.transports import AsyncTransport

from ..models import Amendment


class Pipeline:
    amendments: AsyncClient

    def __init__(self):
        # there will be config for this at some point, but not today
        settings = Settings(strict=True, force_https=True)  # ty:ignore[unknown-argument]
        transport = AsyncTransport(cache=SqliteCache())
        self.amendments = AsyncClient(
            "https://wslwebservices.leg.wa.gov/AmendmentService.asmx?WSDL",
            transport=transport,
            settings=settings
        )
        # committee = "https://wslwebservices.leg.wa.gov/CommitteeService.asmx?WSDL"
        # committee_actions = "https://wslwebservices.leg.wa.gov/CommitteeActionService.asmx?WSDL"
        # committee_meetings = "https://wslwebservices.leg.wa.gov/CommitteeMeetingService.asmx?WSDL"
        # legislative_documents = "https://wslwebservices.leg.wa.gov/LegislativeDocumentService.asmx?WSDL"
        # legislation = "https://wslwebservices.leg.wa.gov/LegislationService.asmx?WSDL"
        # rcw_cite_affected = "https://wslwebservices.leg.wa.gov/RcwCiteAffectedService.asmx?WSDL"
        # session_law = "https://wslwebservices.leg.wa.gov/SessionLawService.asmx?WSDL"
        # sponsor_services = "https://wslwebservices.leg.wa.gov/SponsorService.asmx?WSDL"

    async def amendments_for(self, *args: int) -> pl.DataFrame:
        df: pl.DataFrame | None = None
        for year in args:
            results = await self.amendments.service.GetAmendments(year=year)
            amendments = [
                Amendment.from_zeep(zeep_model.__values__)
                for zeep_model in results
            ]
            batch_df = pl.DataFrame(amendments)
            df = batch_df if df is None else df.vstack(batch_df)

        if df is None:
            raise RuntimeError("Invalid year range") # probably
            
        return df


