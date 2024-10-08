"""
Original code and data by Thalheim, Tranquillo, Quint
"""
from typing import List

from util import *


class Oldenburg(ScraperBase):

    POOL = PoolInfo(
        id="oldenburg",
        name="Oldenburg",
        public_url="https://oldenburg-service.de/pls/",
        source_url="https://oldenburg-service.de/pls.php",
        timezone="Europe/Berlin",
        attribution_contributor="Stadt Oldenburg",
        attribution_license=None,
        attribution_url="https://www.oldenburg.de/metanavigation/impressum.html",
    )

    def get_lot_data(self) -> List[LotData]:
        timestamp = self.now()
        soup = self.request_soup(self.POOL.source_url)

        lots = []

        # last_updated is the date when the data on the page was last updated
        last_updated = str(soup.select("body"))
        start = last_updated.find("Letzte Aktualisierung:") + 23
        last_updated = self.to_utc_datetime(last_updated[start:start + 16])
        
        table = soup.find_all("table")
#       The site now uses 2 tables. Table 1 holds the last updated info, table 2 the actual data. Tables dont have any ID or Class so we use 0 and 1        
        for tr in table[1].find_all("tr"):
            if tr.td is None:
                continue

            td = tr.findAll('td')
            parking_name = td[0].string
            # work-around for the Umlaute-problem: ugly but working
            if 'Heiligengeist-' in parking_name:
                parking_name = 'Parkhaus Heiligengeist-Höfe'
            elif 'Schlossh' in parking_name:
                parking_name = 'Parkhaus Schlosshöfe'
            elif 'August Carr' == parking_name:
                parking_name = 'Parkhaus August Carrée'

            parking_free = None
            parking_state = LotData.Status.open
            if 'Geschlossen' in td[4].text:
                parking_state = LotData.Status.closed
            try:
                parking_free = int(td[2].text)
            except:
                parking_state = LotData.Status.nodata
            parking_capacity = int(td[1].text)
            lots.append(
                LotData(
                    timestamp=timestamp,
                    lot_timestamp=last_updated,
                    id=name_to_legacy_id("oldenburg", parking_name),
                    status=parking_state,
                    num_free=parking_free,
                    capacity=parking_capacity
                )
            )

        return lots

    def get_lot_infos(self) -> List[LotInfo]:
        return self.get_v1_lot_infos_from_geojson("Oldenburg")
