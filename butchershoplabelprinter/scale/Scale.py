from typing import Callable, List, Tuple

class Scale():

    id : Tuple[str,str] = (None, None)

    isReal: bool = False

    isTareable: bool = False

    def measure(self, callback: Callable[[float], None] ) -> None :
        """ Execute the measure action and invoke the callback with the resulting weight in gramms """
        pass

    @staticmethod
    def available_scales() -> List[str]:
        return [s.id[0] for s in Scale.__subclasses__()]
    
    def __repr__(self):
        return f"Scale {id[1]}"