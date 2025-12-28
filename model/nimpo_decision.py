def nimpo_decision(meta):
    quality = meta.get("qualityScore")
    issues = meta.get("issues", [])
    drift = meta.get("driftDetected", False)

    if quality is None:
        usable = False
        risk = "HIGH"
    else:
        usable = quality >= 7 and not drift
        risk = "HIGH" if quality < 5 or drift else "MEDIUM" if quality < 7 else "LOW"

    actions = []
    if issues:
        actions.append("REVIEW_DATASET")
    if drift:
        actions.append("CHECK_DATA_DRIFT")

    return {
        "qualityScore": quality,
        "usable": usable,
        "riskLevel": risk,
        "issues": issues,
        "recommendedActions": actions,
        "confidenceScore": quality
    }
