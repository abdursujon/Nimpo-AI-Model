from local_service.analysis_client import ingest_csv, get_analysis
import json

def test_full_pipeline():
    csv = "x,y\n1,2\n2,3"
    res = ingest_csv(csv)
    analysis = get_analysis(res["id"])

    print(json.dumps(analysis, indent=2))

    assert analysis["numberOfRows"] == 2
