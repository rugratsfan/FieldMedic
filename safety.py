def run_safety_checks(
    heart_rate,
    respiratory_rate,
    systolic_pressure,
    oxygen,
    altered_mental_status,
    uncontrolled_bleeding
):
    danger_signs = []
    force_immediate = False

    if uncontrolled_bleeding:
        danger_signs.append("Reported uncontrolled or severe bleeding")
        force_immediate = True

    if altered_mental_status:
        danger_signs.append(
            "Reported confusion, unresponsiveness, or altered mental status"
        )
        force_immediate = True

    if systolic_pressure is not None and systolic_pressure < 90:
        danger_signs.append(
            f"Low reported systolic blood pressure: {systolic_pressure} mmHg"
        )
        force_immediate = True

    if oxygen is not None and oxygen < 90:
        danger_signs.append(
            f"Low reported oxygen saturation: {oxygen}%"
        )
        force_immediate = True

    if heart_rate is not None and heart_rate > 130:
        danger_signs.append(
            f"Very high reported heart rate: {heart_rate} bpm"
        )

    if heart_rate is not None and 0 < heart_rate < 40:
        danger_signs.append(
            f"Very low reported heart rate: {heart_rate} bpm"
        )
        force_immediate = True

    if respiratory_rate is not None and respiratory_rate > 30:
        danger_signs.append(
            f"Very high reported respiratory rate: {respiratory_rate}"
        )

    if respiratory_rate is not None and 0 < respiratory_rate < 8:
        danger_signs.append(
            f"Very low reported respiratory rate: {respiratory_rate}"
        )
        force_immediate = True

    return {
        "danger_signs": danger_signs,
        "force_immediate": force_immediate
    }