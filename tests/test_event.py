from parsely_raw_data.event import (Event, VisitorInfo, TimestampInfo, DisplayInfo,
                                    SessionInfo, SlotInfo, Metadata)


event = Event(
    'example.com',
    'http://localhost:8000/examples.build/analytics.amp.html',
    None,
    'pageview',
    None,
    VisitorInfo(
        None,
        'amp-kiZ6-WZla1kXFFWAw2oxfLyJVWB8ytaeJ7ghXsXe5',
        '198.200.78.40'),
    None,
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    DisplayInfo(1920, 1200, 1916, 1177, 24),
    TimestampInfo(1451685961000, 1455027478791, None),
    SessionInfo(
        12345,
        1457737463000,
        "http://test.com",
        "http://test2.com",
        1457737463000
    ),
    SlotInfo("/html", "http://test.com/nothing", 400, 400),
    Metadata(
        ["Walt Whitman"],
        "http://parsely.com/testpost",
        ["http://parsely.com/testpost"],
        "post",
        "abcdefg",
        1451685961000,
        None,
        "vertical",
        ["tag1", "tag2"],
        1451685961000,
        "http://parsely.com/thumburl",
        "This is the title of the thing",
        "http://parsely.com/imgurl",
        420,
        ["http://twitter.com/nothing"],
        69
    )
)


def test_dict():
    serded = Event.from_dict(event.to_dict())
    assert serded == event

if __name__ == "__main__":
    test_dict()
