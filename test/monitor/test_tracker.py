import pytest
from WeTest.tool import tracker
from WeTest.util import provider


data = provider.read_excel_to_dict("data/monitor/tracker.xlsx", 0)


@pytest.mark.parametrize("data", data, ids=lambda data: "{}-{}".format(data["tc_id"], data["tc_desc"]))
def test_tracker(data):
    
    macro = [("{{domain}}", "www.baidu.com")]

    tracker.send(macro, None, **data)
