from urllib import request, parse
import json

def test_accuracy(user, test_data):
    """Submits a test data set to the pydata server, and returns accuracy"""
    try:
        test_data = {str(k).lower().replace(".txt", ""):str(v).lower().strip() for k,v in test_data.items()}
        data = parse.urlencode({"user":user, "submission": json.dumps(test_data)}).encode()
        req =  request.Request("http://goren4u.com/nlp_classification/", data=data)
        resp = request.urlopen(req)
        return float(resp.read().decode("utf8"))
    except Exception as e:
        print (str(e))
        return None

if __name__ == "__main__":
    assert test_accuracy("ug", {"34048": "rsu"}) > 0
