def calculate_bill(meter_reading):
    """
    Calculate electricity bill from meter reading.

    Example:
        03560.8 -> 3560.8 units
    """

    try:
        # Convert OCR result to number
        units = float(str(meter_reading).strip())

        # Leading zero does not affect the value
        # 03560.8 becomes 3560.8
        print("Meter reading:", meter_reading)
        print("Units:", units)

        if units < 0:
            return 0

        # --------------------------------------------------
        # Tamil Nadu domestic electricity slab calculation
        # --------------------------------------------------
        #
        # This is a simple slab calculator.
        #
        # 0 - 100       : Free
        # 101 - 200     : ₹2.35/unit
        # 201 - 400     : ₹4.70/unit
        # 401 - 500     : ₹6.30/unit
        # Above 500     : ₹8.40/unit
        #
        # --------------------------------------------------

        remaining = units
        bill = 0.0

        # First 100 units
        if remaining <= 100:
            bill = 0
            remaining = 0
        else:
            remaining -= 100

        # Next 100 units
        if remaining > 0:
            slab_units = min(remaining, 100)
            bill += slab_units * 2.35
            remaining -= slab_units

        # Next 200 units
        if remaining > 0:
            slab_units = min(remaining, 200)
            bill += slab_units * 4.70
            remaining -= slab_units

        # Next 100 units
        if remaining > 0:
            slab_units = min(remaining, 100)
            bill += slab_units * 6.30
            remaining -= slab_units

        # Above 500 units
        if remaining > 0:
            bill += remaining * 8.40

        bill = round(bill, 2)

        print("Calculated bill: ₹", bill)

        return bill

    except (ValueError, TypeError) as e:
        print("Bill calculation error:", e)
        return 0