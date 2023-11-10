"""
Copyright 2023 binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from abc import ABC, abstractmethod

from common.models import ImportSourceResult

from .base_converter import BaseConverter


class CsvConverter(BaseConverter, ABC):
    @abstractmethod
    def handle_csv(self, data: list[list]) -> ImportSourceResult:
        pass
