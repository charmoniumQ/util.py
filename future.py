class Lazy(Generic[T]):
    def __init__(
        self,
        value_fn: Optional[Callable[[], T]] = None,
    ) -> None:
        self.value_fn = value_fn
        self.computed = False
        if self.is_fulfilled and self.value_fn:
            raise ValueError("Cannot supply a value and a value_fn")

    def unwrap(self) -> T:
        """Returns the value, and ValueErrors if it is not yet fulfilled."""
        if self.computed:
            return self.value
        else:
            self.computed = True
            self._value = self._value_fn()
            return self._value

    def __getattr__(self, attr: str) -> Any:
        return getattr(self.unwrap(), attr)

    @classmethod
    def create(
            cls: type[Future[T]],
            value_fn: Optional[Callable[[], T]] = None,
    ) -> T:
        return cast(T, Future(value_fn))

class Future(Generic[T]):
    def __init__(self) -> None:
        self.computed = False

    def unwrap(self) -> T:
        if self.computed:
            raise ValueError("Future is not yet fulfilled.")
        else:
            return self.computed

    def __getattr__(self, attr: str) -> Any:
        return getattr(self.unwrap(), attr)

    def fulfill(self, value: T) -> None:
        if self.computed:
            raise ValueError("Future is already fulfilled.")
        self.value = value
