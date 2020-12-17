from abc import ABC, abstractmethod
import json
import os


__all__ = ['ClamsApp']

from typing import Union

from mmif import Mmif


class ClamsApp(ABC):
    def __init__(self):
        # TODO (krim @ 10/9/20): eventually we might end up with a python class
        # for this metadata (with a JSON schema)
        self.metadata: dict = self.setupmetadata()
        super().__init__()

    def appmetadata(self):
        # TODO (krim @ 10/9/20): when self.metadata is no longer a `dict`
        # this method might needs to be changed to properly serialize input
        return json.dumps(self.metadata)

    @abstractmethod
    def setupmetadata(self) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def sniff(self, mmif) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def annotate(self, mmif) -> str:
        raise NotImplementedError()

    @staticmethod
    def validate_document_files(mmif: Union[str, Mmif]) -> None:
        if isinstance(mmif, str):
            mmif = Mmif(mmif)
        for document in mmif.documents:
            loc = document.location
            if loc is not None and len(loc) > 0:
                # TODO (krim @ 12/15/20): when `location` implements full URI values
                #  (https://github.com/clamsproject/mmif/issues/151) , check for protocol first and use proper check
                #  methods based on the protocol (e.g. file:// --> os.path.exists())
                if os.path.exists(loc):
                    raise FileNotFoundError(f'{document.id}: {loc}')
                # TODO (krim @ 12/15/20): with implementation of file checksum
                #  (https://github.com/clamsproject/mmif/issues/150) , here is a good place for additional check for
                #  file integrity