def to_next_offset(total_size: int, offset: int, limit: int) -> int:
    if offset is not None:
        if offset * limit < total_size:
            return offset + 1
    return 0
