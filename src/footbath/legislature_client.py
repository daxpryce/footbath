import asyncio

import polars as pl
from zeep import AsyncClient, Settings
from zeep.cache import SqliteCache
from zeep.transports import AsyncTransport

from footbath.models import Amendment


class LegislatureClient:
    amendments: AsyncClient
    committee: AsyncClient
    committee_actions: AsyncClient
    legislative_documents: AsyncClient
    legislation: AsyncClient
    rcw_cite_affected: AsyncClient
    session_law: AsyncClient
    sponsor_services: AsyncClient

    def __init__(self):
        settings = Settings(strict=True, force_https=True)  # ty:ignore[unknown-argument]
        self._transport = AsyncTransport(cache=SqliteCache())
        self.amendments = AsyncClient(
            "https://wslwebservices.leg.wa.gov/AmendmentService.asmx?WSDL",
            transport=self._transport,
            settings=settings,
        )
        self.committee = AsyncClient(
            "https://wslwebservices.leg.wa.gov/CommitteeService.asmx?WSDL",
            transport=self._transport,
            settings=settings,
        )
        self.committee_actions = AsyncClient(
            "https://wslwebservices.leg.wa.gov/CommitteeActionService.asmx?WSDL",
            transport=self._transport,
            settings=settings,
        )
        self.committee_meetings = AsyncClient(
            "https://wslwebservices.leg.wa.gov/CommitteeMeetingService.asmx?WSDL",
            transport=self._transport,
            settings=settings,
        )
        self.legislative_documents = AsyncClient(
            "https://wslwebservices.leg.wa.gov/LegislativeDocumentService.asmx?WSDL",
            transport=self._transport,
            settings=settings,
        )
        self.legislation = AsyncClient(
            "https://wslwebservices.leg.wa.gov/LegislationService.asmx?WSDL",
            transport=self._transport,
            settings=settings,
        )
        self.rcw_cite_affected = AsyncClient(
            "https://wslwebservices.leg.wa.gov/RcwCiteAffectedService.asmx?WSDL",
            transport=self._transport,
            settings=settings,
        )
        self.session_law = AsyncClient(
            "https://wslwebservices.leg.wa.gov/SessionLawService.asmx?WSDL",
            transport=self._transport,
            settings=settings,
        )
        self.sponsor_services = AsyncClient(
            "https://wslwebservices.leg.wa.gov/SponsorService.asmx?WSDL",
            transport=self._transport,
            settings=settings,
        )

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._transport.aclose()

    async def amendments_for(self, *years: int) -> pl.DataFrame:
        """
        Note that the resulting DataFrame has discontiguous chunks and if used for direct analytics, should be .rechunk()'d first
        :param years: 1..n discrete years that we will query the Washington State Legislature web services for amendments for
        :return: A dataframe including all the years queried.
        """

        # todo: swap to asyncio.gather -- you know, the whole point of insisting upon async
        async def _amendments_for_year(client: AsyncClient, year: int) -> pl.DataFrame:
            results = await client.service.GetAmendments(year=year)
            return pl.DataFrame(
                data=[
                    Amendment.from_zeep(zeep_model.__values__) for zeep_model in results
                ]
            )

        frames: list[pl.DataFrame] = list(
            await asyncio.gather(
                *(_amendments_for_year(self.amendments, year) for year in years)
            )
        )
        return pl.concat(frames)
