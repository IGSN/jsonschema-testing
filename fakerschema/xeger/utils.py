from collections.abc import Iterable
import functools


def flatten(iterables):
    "Flatten an iterable of iterables"
    for elem in iterables:
        if isinstance(elem, Iterable) and not isinstance(elem, str):
            for subelem in flatten(elem):
                yield subelem
        else:
            yield elem


def join(*strings):
    "Join strings together"
    return "".join(s for s in flatten(strings))


def cached_property(inputs=None):
    """
    Returns a cached proeprty that is calculated once.

    If inputs are specified, then if those properties change the propery is 
    recalculated. 

    Usage is as follows; given a class, you can declare a cached property with 
    the `@cached_property` decorator:

    ```python
    class Swallow:

        def __init__(self, laden):
            self.mass = 5
            self.laden = laden

        @cached_property(['mass', 'laden'])
        def air_speed(self):
            mass = self.mass + 16 if laden else 0
            time.sleep(100)  # must sleep after flying
            return mass / 400
    ```
    
    you can do the following:

    ```
    s = Swallow(laden=False)
    s.air_speed     # will be slow first time
    s.air_speed     # returns instantly using cache
    s.laden = True  # invalidate cache
    s.air_speed     # will recalculate
    ```

    i,.e. the `air_speed` will be lazily recalculated if `self.mass`, or 
    `self.laden` change.

    Parameters:
        inputs - dependencies which should be checked for changes
            to determine whether to recalculate the property. If None then
            this property is only laxily calculated once.
    """
    # Handle defaults
    inputs = inputs or [] 

    # Wrap property method
    def smart_cached_property(func):
        @functools.wraps(func)
        def get(self):
            # Determine whether we can use the cached value
            input_values = dict((k, getattr(self, k)) for k in inputs)
            try:
                # Pull from cache if possible
                x = self._property_cache[func]
                if input_values == self.property_input_cache[func]:
                    return x
            except AttributeError:
                # We haven't created the property cache yet
                self._property_cache = {}
                self._property_input_cache = {}
            except KeyError:
                # Input cache has been invalidated
                pass

            # Recalculate value
            x = self._property_cache[func] = func(self)
            self._property_input_cache[func] = input_values
            return x
        return property(get)
    return smart_cached_property
        